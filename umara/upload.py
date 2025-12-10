"""
File Upload handling for Umara.

Provides UploadedFile class with Streamlit-compatible API and
file upload processing utilities.
"""

from __future__ import annotations

import base64
import io
import mimetypes
from dataclasses import dataclass, field
from typing import Any, BinaryIO


@dataclass
class UploadedFile:
    """
    Represents an uploaded file with Streamlit-compatible API.

    This class wraps uploaded file data and provides convenient methods
    for accessing file content, similar to Streamlit's UploadedFile.

    Example:
        uploaded = um.file_uploader("Upload a file")
        if uploaded:
            content = uploaded.read()
            um.write(f"Uploaded: {uploaded.name} ({uploaded.size} bytes)")
    """

    name: str
    type: str  # MIME type
    size: int
    _data: bytes = field(repr=False)
    file_id: str = ""

    def __post_init__(self):
        """Initialize the BytesIO buffer."""
        self._buffer: io.BytesIO | None = None

    @classmethod
    def from_base64(
        cls,
        name: str,
        data_uri: str,
        file_id: str = "",
    ) -> "UploadedFile":
        """
        Create an UploadedFile from a base64 data URI.

        Args:
            name: Original filename
            data_uri: Base64 data URI (e.g., "data:image/png;base64,...")
            file_id: Unique file identifier

        Returns:
            UploadedFile instance
        """
        # Parse data URI
        if data_uri.startswith("data:"):
            # Format: data:[<mediatype>][;base64],<data>
            header, encoded = data_uri.split(",", 1)
            mime_type = header.split(":")[1].split(";")[0] if ":" in header else ""
        else:
            # Assume raw base64
            encoded = data_uri
            mime_type = mimetypes.guess_type(name)[0] or "application/octet-stream"

        # Decode the data
        data = base64.b64decode(encoded)

        return cls(
            name=name,
            type=mime_type,
            size=len(data),
            _data=data,
            file_id=file_id,
        )

    @classmethod
    def from_bytes(
        cls,
        name: str,
        data: bytes,
        mime_type: str | None = None,
        file_id: str = "",
    ) -> "UploadedFile":
        """
        Create an UploadedFile from raw bytes.

        Args:
            name: Original filename
            data: File content as bytes
            mime_type: MIME type (auto-detected if not provided)
            file_id: Unique file identifier

        Returns:
            UploadedFile instance
        """
        if mime_type is None:
            mime_type = mimetypes.guess_type(name)[0] or "application/octet-stream"

        return cls(
            name=name,
            type=mime_type,
            size=len(data),
            _data=data,
            file_id=file_id,
        )

    def read(self, size: int = -1) -> bytes:
        """
        Read file content.

        Args:
            size: Number of bytes to read (-1 for all)

        Returns:
            File content as bytes
        """
        if self._buffer is None:
            self._buffer = io.BytesIO(self._data)
        return self._buffer.read(size)

    def getvalue(self) -> bytes:
        """
        Get the entire file content as bytes.

        Returns:
            Complete file content
        """
        return self._data

    def getbuffer(self) -> memoryview:
        """
        Get a buffer view of the file content.

        Returns:
            Memory view of file data
        """
        return memoryview(self._data)

    def seek(self, pos: int, whence: int = 0) -> int:
        """
        Seek to a position in the file.

        Args:
            pos: Position to seek to
            whence: Reference point (0=start, 1=current, 2=end)

        Returns:
            New absolute position
        """
        if self._buffer is None:
            self._buffer = io.BytesIO(self._data)
        return self._buffer.seek(pos, whence)

    def tell(self) -> int:
        """
        Get current position in the file.

        Returns:
            Current position
        """
        if self._buffer is None:
            self._buffer = io.BytesIO(self._data)
        return self._buffer.tell()

    def readline(self, size: int = -1) -> bytes:
        """
        Read a line from the file.

        Args:
            size: Maximum bytes to read (-1 for no limit)

        Returns:
            Line content as bytes
        """
        if self._buffer is None:
            self._buffer = io.BytesIO(self._data)
        return self._buffer.readline(size)

    def readlines(self, hint: int = -1) -> list[bytes]:
        """
        Read all lines from the file.

        Args:
            hint: Maximum bytes to read (-1 for no limit)

        Returns:
            List of lines as bytes
        """
        if self._buffer is None:
            self._buffer = io.BytesIO(self._data)
        return self._buffer.readlines(hint)

    def __iter__(self):
        """Iterate over lines in the file."""
        if self._buffer is None:
            self._buffer = io.BytesIO(self._data)
        return iter(self._buffer)

    def __enter__(self) -> "UploadedFile":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Context manager exit."""
        return False

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary for serialization.

        Returns:
            Dictionary with file metadata (not content)
        """
        return {
            "name": self.name,
            "type": self.type,
            "size": self.size,
            "file_id": self.file_id,
        }

    @property
    def readable(self) -> bool:
        """Check if file is readable."""
        return True

    @property
    def writable(self) -> bool:
        """Check if file is writable."""
        return False

    @property
    def seekable(self) -> bool:
        """Check if file is seekable."""
        return True


def parse_uploaded_files(
    file_data: list[dict[str, Any]] | dict[str, Any] | None,
) -> list[UploadedFile] | UploadedFile | None:
    """
    Parse uploaded file data from frontend.

    Args:
        file_data: File data from frontend (single file or list)

    Returns:
        UploadedFile instance(s) or None
    """
    if file_data is None:
        return None

    if isinstance(file_data, list):
        if not file_data:
            return None
        return [
            UploadedFile.from_base64(
                name=f.get("name", "unknown"),
                data_uri=f.get("data", ""),
                file_id=f.get("id", ""),
            )
            for f in file_data
        ]
    else:
        return UploadedFile.from_base64(
            name=file_data.get("name", "unknown"),
            data_uri=file_data.get("data", ""),
            file_id=file_data.get("id", ""),
        )


def format_file_size(size: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}" if size != int(size) else f"{int(size)} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def validate_file_type(
    file: UploadedFile,
    accepted_types: list[str] | None,
) -> bool:
    """
    Validate that a file matches accepted types.

    Args:
        file: Uploaded file to validate
        accepted_types: List of accepted MIME types or extensions

    Returns:
        True if file type is accepted
    """
    if not accepted_types:
        return True

    for accepted in accepted_types:
        # Check MIME type
        if "/" in accepted:
            if accepted.endswith("/*"):
                # Wildcard (e.g., "image/*")
                category = accepted.split("/")[0]
                if file.type.startswith(category + "/"):
                    return True
            elif file.type == accepted:
                return True
        else:
            # Check extension
            ext = accepted.lower().lstrip(".")
            if file.name.lower().endswith("." + ext):
                return True

    return False


def validate_file_size(
    file: UploadedFile,
    max_size: int | None,
) -> bool:
    """
    Validate that a file is within size limits.

    Args:
        file: Uploaded file to validate
        max_size: Maximum allowed size in bytes

    Returns:
        True if file size is within limits
    """
    if max_size is None:
        return True
    return file.size <= max_size
