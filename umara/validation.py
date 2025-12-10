"""
Form Validation Helpers for Umara.

Provides declarative validation for form inputs with built-in validators
and support for custom validation rules. This is a feature that gives
Umara an advantage over Streamlit.

Example:
    import umara as um
    from umara.validation import validate, required, email, min_length

    with um.form("signup"):
        email_input = um.input("Email")
        password = um.input("Password", type="password")

        # Validate on submit
        if um.form_submit_button("Sign Up"):
            errors = validate({
                "email": (email_input, [required(), email()]),
                "password": (password, [required(), min_length(8)]),
            })

            if errors:
                for field, messages in errors.items():
                    um.error(f"{field}: {messages[0]}")
            else:
                um.success("Account created!")
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar

T = TypeVar("T")


@dataclass
class ValidationResult:
    """Result of a validation check."""

    is_valid: bool
    message: str | None = None
    field: str | None = None

    def __bool__(self) -> bool:
        return self.is_valid


@dataclass
class ValidationError:
    """A validation error with field and message."""

    field: str
    message: str
    code: str = "invalid"


# Type alias for validator functions
Validator = Callable[[Any], ValidationResult]


# =============================================================================
# Core Validators
# =============================================================================


def required(message: str = "This field is required") -> Validator:
    """
    Validate that a value is not empty.

    Args:
        message: Custom error message

    Example:
        errors = validate({
            "name": (name_input, [required()]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        if value is None:
            return ValidationResult(False, message)
        if isinstance(value, str) and not value.strip():
            return ValidationResult(False, message)
        if isinstance(value, (list, dict)) and len(value) == 0:
            return ValidationResult(False, message)
        return ValidationResult(True)

    return validator


def min_length(length: int, message: str | None = None) -> Validator:
    """
    Validate minimum length of a string or list.

    Args:
        length: Minimum required length
        message: Custom error message

    Example:
        errors = validate({
            "password": (password, [min_length(8)]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        msg = message or f"Must be at least {length} characters"
        if value is None:
            return ValidationResult(False, msg)
        if len(value) < length:
            return ValidationResult(False, msg)
        return ValidationResult(True)

    return validator


def max_length(length: int, message: str | None = None) -> Validator:
    """
    Validate maximum length of a string or list.

    Args:
        length: Maximum allowed length
        message: Custom error message

    Example:
        errors = validate({
            "bio": (bio, [max_length(500)]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        msg = message or f"Must be at most {length} characters"
        if value is None:
            return ValidationResult(True)
        if len(value) > length:
            return ValidationResult(False, msg)
        return ValidationResult(True)

    return validator


def email(message: str = "Invalid email address") -> Validator:
    """
    Validate email format.

    Args:
        message: Custom error message

    Example:
        errors = validate({
            "email": (email_input, [email()]),
        })
    """
    # RFC 5322 compliant email regex (simplified)
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def validator(value: Any) -> ValidationResult:
        if value is None or value == "":
            return ValidationResult(True)  # Use required() for empty check
        if not isinstance(value, str):
            return ValidationResult(False, message)
        if not re.match(pattern, value):
            return ValidationResult(False, message)
        return ValidationResult(True)

    return validator


def url(message: str = "Invalid URL") -> Validator:
    """
    Validate URL format.

    Args:
        message: Custom error message

    Example:
        errors = validate({
            "website": (website_input, [url()]),
        })
    """
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"

    def validator(value: Any) -> ValidationResult:
        if value is None or value == "":
            return ValidationResult(True)
        if not isinstance(value, str):
            return ValidationResult(False, message)
        if not re.match(pattern, value, re.IGNORECASE):
            return ValidationResult(False, message)
        return ValidationResult(True)

    return validator


def pattern(regex: str, message: str = "Invalid format") -> Validator:
    """
    Validate against a regex pattern.

    Args:
        regex: Regular expression pattern
        message: Custom error message

    Example:
        errors = validate({
            "phone": (phone, [pattern(r"^\d{3}-\d{3}-\d{4}$", "Invalid phone format")]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        if value is None or value == "":
            return ValidationResult(True)
        if not isinstance(value, str):
            return ValidationResult(False, message)
        if not re.match(regex, value):
            return ValidationResult(False, message)
        return ValidationResult(True)

    return validator


def min_value(minimum: int | float, message: str | None = None) -> Validator:
    """
    Validate minimum numeric value.

    Args:
        minimum: Minimum allowed value
        message: Custom error message

    Example:
        errors = validate({
            "age": (age, [min_value(18, "Must be 18 or older")]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        msg = message or f"Must be at least {minimum}"
        if value is None:
            return ValidationResult(True)
        try:
            if float(value) < minimum:
                return ValidationResult(False, msg)
            return ValidationResult(True)
        except (TypeError, ValueError):
            return ValidationResult(False, msg)

    return validator


def max_value(maximum: int | float, message: str | None = None) -> Validator:
    """
    Validate maximum numeric value.

    Args:
        maximum: Maximum allowed value
        message: Custom error message

    Example:
        errors = validate({
            "quantity": (qty, [max_value(100)]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        msg = message or f"Must be at most {maximum}"
        if value is None:
            return ValidationResult(True)
        try:
            if float(value) > maximum:
                return ValidationResult(False, msg)
            return ValidationResult(True)
        except (TypeError, ValueError):
            return ValidationResult(False, msg)

    return validator


def in_range(
    minimum: int | float,
    maximum: int | float,
    message: str | None = None,
) -> Validator:
    """
    Validate that a numeric value is within a range.

    Args:
        minimum: Minimum allowed value
        maximum: Maximum allowed value
        message: Custom error message

    Example:
        errors = validate({
            "rating": (rating, [in_range(1, 5)]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        msg = message or f"Must be between {minimum} and {maximum}"
        if value is None:
            return ValidationResult(True)
        try:
            num = float(value)
            if num < minimum or num > maximum:
                return ValidationResult(False, msg)
            return ValidationResult(True)
        except (TypeError, ValueError):
            return ValidationResult(False, msg)

    return validator


def one_of(options: list[Any], message: str | None = None) -> Validator:
    """
    Validate that value is one of the allowed options.

    Args:
        options: List of allowed values
        message: Custom error message

    Example:
        errors = validate({
            "status": (status, [one_of(["active", "inactive", "pending"])]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        msg = message or f"Must be one of: {', '.join(str(o) for o in options)}"
        if value is None:
            return ValidationResult(True)
        if value not in options:
            return ValidationResult(False, msg)
        return ValidationResult(True)

    return validator


def matches(
    other_value: Any,
    other_name: str = "other field",
    message: str | None = None,
) -> Validator:
    """
    Validate that value matches another value (e.g., password confirmation).

    Args:
        other_value: The value to match against
        other_name: Name of the other field for error message
        message: Custom error message

    Example:
        password = um.input("Password", type="password")
        confirm = um.input("Confirm Password", type="password")

        errors = validate({
            "confirm_password": (confirm, [matches(password, "password")]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        msg = message or f"Must match {other_name}"
        if value != other_value:
            return ValidationResult(False, msg)
        return ValidationResult(True)

    return validator


def numeric(message: str = "Must be a number") -> Validator:
    """
    Validate that value is numeric.

    Args:
        message: Custom error message

    Example:
        errors = validate({
            "price": (price, [numeric()]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        if value is None or value == "":
            return ValidationResult(True)
        try:
            float(value)
            return ValidationResult(True)
        except (TypeError, ValueError):
            return ValidationResult(False, message)

    return validator


def integer(message: str = "Must be a whole number") -> Validator:
    """
    Validate that value is an integer.

    Args:
        message: Custom error message

    Example:
        errors = validate({
            "quantity": (qty, [integer()]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        if value is None or value == "":
            return ValidationResult(True)
        try:
            int_val = int(value)
            float_val = float(value)
            if int_val != float_val:
                return ValidationResult(False, message)
            return ValidationResult(True)
        except (TypeError, ValueError):
            return ValidationResult(False, message)

    return validator


def alpha(message: str = "Must contain only letters") -> Validator:
    """
    Validate that value contains only letters.

    Args:
        message: Custom error message

    Example:
        errors = validate({
            "first_name": (name, [alpha()]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        if value is None or value == "":
            return ValidationResult(True)
        if not isinstance(value, str) or not value.isalpha():
            return ValidationResult(False, message)
        return ValidationResult(True)

    return validator


def alphanumeric(message: str = "Must contain only letters and numbers") -> Validator:
    """
    Validate that value contains only letters and numbers.

    Args:
        message: Custom error message

    Example:
        errors = validate({
            "username": (username, [alphanumeric()]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        if value is None or value == "":
            return ValidationResult(True)
        if not isinstance(value, str) or not value.isalnum():
            return ValidationResult(False, message)
        return ValidationResult(True)

    return validator


def no_whitespace(message: str = "Must not contain whitespace") -> Validator:
    """
    Validate that value contains no whitespace.

    Args:
        message: Custom error message

    Example:
        errors = validate({
            "username": (username, [no_whitespace()]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        if value is None or value == "":
            return ValidationResult(True)
        if not isinstance(value, str):
            return ValidationResult(True)
        if " " in value or "\t" in value or "\n" in value:
            return ValidationResult(False, message)
        return ValidationResult(True)

    return validator


def custom(
    check: Callable[[Any], bool],
    message: str = "Validation failed",
) -> Validator:
    """
    Create a custom validator from a function.

    Args:
        check: Function that returns True if valid
        message: Error message if invalid

    Example:
        def is_even(n):
            return n % 2 == 0

        errors = validate({
            "number": (num, [custom(is_even, "Must be even")]),
        })
    """

    def validator(value: Any) -> ValidationResult:
        try:
            if check(value):
                return ValidationResult(True)
            return ValidationResult(False, message)
        except Exception:
            return ValidationResult(False, message)

    return validator


# =============================================================================
# Main Validation Function
# =============================================================================


def validate(
    fields: dict[str, tuple[Any, list[Validator]]],
) -> dict[str, list[str]]:
    """
    Validate multiple fields with their validators.

    Args:
        fields: Dictionary mapping field names to (value, validators) tuples

    Returns:
        Dictionary of field names to list of error messages.
        Empty dict if all validations pass.

    Example:
        errors = validate({
            "email": (email_input, [required(), email()]),
            "password": (password, [required(), min_length(8)]),
            "age": (age, [required(), min_value(18)]),
        })

        if errors:
            for field, messages in errors.items():
                um.error(f"{field}: {messages[0]}")
        else:
            # All valid, proceed
            process_form()
    """
    errors: dict[str, list[str]] = {}

    for field_name, (value, validators) in fields.items():
        field_errors = []
        for validator in validators:
            result = validator(value)
            if not result.is_valid and result.message:
                field_errors.append(result.message)
        if field_errors:
            errors[field_name] = field_errors

    return errors


def validate_field(value: Any, validators: list[Validator]) -> list[str]:
    """
    Validate a single field with multiple validators.

    Args:
        value: The value to validate
        validators: List of validator functions

    Returns:
        List of error messages (empty if valid)

    Example:
        errors = validate_field(email_input, [required(), email()])
        if errors:
            um.error(errors[0])
    """
    errors = []
    for validator in validators:
        result = validator(value)
        if not result.is_valid and result.message:
            errors.append(result.message)
    return errors


def is_valid(value: Any, validators: list[Validator]) -> bool:
    """
    Check if a value passes all validators.

    Args:
        value: The value to validate
        validators: List of validator functions

    Returns:
        True if all validations pass

    Example:
        if is_valid(email_input, [required(), email()]):
            um.success("Valid email!")
    """
    for validator in validators:
        if not validator(value).is_valid:
            return False
    return True


# =============================================================================
# Form Integration Helpers
# =============================================================================


@dataclass
class FormValidator:
    """
    Form validation helper that collects validation rules and errors.

    Example:
        validator = FormValidator()

        name = um.input("Name")
        validator.add("name", name, [required()])

        email = um.input("Email")
        validator.add("email", email, [required(), email()])

        if um.form_submit_button("Submit"):
            if validator.is_valid():
                um.success("Form submitted!")
            else:
                validator.show_errors()
    """

    _fields: dict[str, tuple[Any, list[Validator]]] = field(default_factory=dict)
    _errors: dict[str, list[str]] | None = field(default=None)

    def add(
        self,
        name: str,
        value: Any,
        validators: list[Validator],
    ) -> "FormValidator":
        """
        Add a field with its validators.

        Args:
            name: Field name for error messages
            value: Current field value
            validators: List of validators to apply

        Returns:
            self for chaining
        """
        self._fields[name] = (value, validators)
        return self

    def validate(self) -> dict[str, list[str]]:
        """
        Run validation on all fields.

        Returns:
            Dictionary of errors (empty if valid)
        """
        self._errors = validate(self._fields)
        return self._errors

    def is_valid(self) -> bool:
        """
        Check if all fields are valid.

        Returns:
            True if no validation errors
        """
        if self._errors is None:
            self.validate()
        return len(self._errors or {}) == 0

    def get_errors(self, field_name: str | None = None) -> list[str]:
        """
        Get errors for a specific field or all errors.

        Args:
            field_name: Specific field to get errors for (None for all)

        Returns:
            List of error messages
        """
        if self._errors is None:
            self.validate()

        if field_name is not None:
            return (self._errors or {}).get(field_name, [])

        all_errors = []
        for errors in (self._errors or {}).values():
            all_errors.extend(errors)
        return all_errors

    def show_errors(self) -> None:
        """
        Display validation errors using um.error().

        Requires umara to be imported.
        """
        from umara.components import error as um_error

        if self._errors is None:
            self.validate()

        for field_name, messages in (self._errors or {}).items():
            for message in messages:
                um_error(f"{field_name}: {message}")

    def clear(self) -> None:
        """Clear all fields and errors."""
        self._fields.clear()
        self._errors = None
