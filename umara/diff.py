"""
Component Tree Diffing for Umara.

Provides efficient diffing of component trees to send only changes
instead of the entire tree on each update.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PatchOp(str, Enum):
    """Patch operation types."""
    ADD = "add"
    REMOVE = "remove"
    UPDATE = "update"
    REPLACE = "replace"
    MOVE = "move"


@dataclass
class Patch:
    """A single patch operation."""
    op: PatchOp
    path: str  # Component ID or path
    value: dict[str, Any] | None = None
    old_value: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "op": self.op.value,
            "path": self.path,
        }
        if self.value is not None:
            result["value"] = self.value
        return result


@dataclass
class DiffResult:
    """Result of diffing two component trees."""
    patches: list[Patch] = field(default_factory=list)
    has_changes: bool = False

    # Statistics for debugging/monitoring
    components_added: int = 0
    components_removed: int = 0
    components_updated: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "patches": [p.to_dict() for p in self.patches],
            "hasChanges": self.has_changes,
            "stats": {
                "added": self.components_added,
                "removed": self.components_removed,
                "updated": self.components_updated,
            }
        }


def diff_props(
    old_props: dict[str, Any],
    new_props: dict[str, Any],
) -> dict[str, Any] | None:
    """
    Diff two props dictionaries.

    Returns the changed props or None if no changes.
    """
    changes = {}

    # Check for added/changed props
    for key, new_val in new_props.items():
        old_val = old_props.get(key)
        if old_val != new_val:
            changes[key] = new_val

    # Check for removed props
    for key in old_props:
        if key not in new_props:
            changes[key] = None  # Signal removal

    return changes if changes else None


def diff_component(
    old: dict[str, Any] | None,
    new: dict[str, Any] | None,
    path: str = "root",
) -> list[Patch]:
    """
    Diff two component dictionaries.

    Returns a list of patches to transform old into new.
    """
    patches = []

    # Handle None cases
    if old is None and new is None:
        return patches

    if old is None:
        # Component was added
        patches.append(Patch(
            op=PatchOp.ADD,
            path=path,
            value=new,
        ))
        return patches

    if new is None:
        # Component was removed
        patches.append(Patch(
            op=PatchOp.REMOVE,
            path=path,
        ))
        return patches

    # Both exist - check for changes
    old_id = old.get("id", "")
    new_id = new.get("id", "")

    # If IDs are different, it's a replacement
    if old_id != new_id:
        patches.append(Patch(
            op=PatchOp.REPLACE,
            path=path,
            value=new,
        ))
        return patches

    # Same ID - check for prop changes
    old_type = old.get("type", "")
    new_type = new.get("type", "")

    if old_type != new_type:
        # Type changed - full replacement
        patches.append(Patch(
            op=PatchOp.REPLACE,
            path=path,
            value=new,
        ))
        return patches

    # Check props
    prop_changes = diff_props(
        old.get("props", {}),
        new.get("props", {}),
    )

    # Check style
    style_changes = diff_props(
        old.get("style") or {},
        new.get("style") or {},
    )

    # Check events
    event_changes = diff_props(
        old.get("events") or {},
        new.get("events") or {},
    )

    # If any changes, create update patch
    if prop_changes or style_changes or event_changes:
        update_value = {"id": new_id}
        if prop_changes:
            update_value["props"] = prop_changes
        if style_changes:
            update_value["style"] = style_changes
        if event_changes:
            update_value["events"] = event_changes

        patches.append(Patch(
            op=PatchOp.UPDATE,
            path=new_id,
            value=update_value,
        ))

    # Diff children
    old_children = old.get("children", [])
    new_children = new.get("children", [])

    child_patches = diff_children(old_children, new_children, new_id)
    patches.extend(child_patches)

    return patches


def diff_children(
    old_children: list[dict[str, Any]],
    new_children: list[dict[str, Any]],
    parent_id: str,
) -> list[Patch]:
    """
    Diff two lists of children components.

    Uses a keyed diffing algorithm for optimal patching.
    """
    patches = []

    # Build lookup maps by ID
    old_by_id = {c.get("id"): (i, c) for i, c in enumerate(old_children)}
    new_by_id = {c.get("id"): (i, c) for i, c in enumerate(new_children)}

    # Track which old children were matched
    matched_old = set()

    # Process new children in order
    for new_idx, new_child in enumerate(new_children):
        new_id = new_child.get("id")

        if new_id in old_by_id:
            # Child exists - diff it
            old_idx, old_child = old_by_id[new_id]
            matched_old.add(new_id)

            # Recursively diff the child
            child_patches = diff_component(
                old_child,
                new_child,
                path=new_id,
            )
            patches.extend(child_patches)

            # Check if it moved position
            if old_idx != new_idx:
                patches.append(Patch(
                    op=PatchOp.MOVE,
                    path=new_id,
                    value={"parentId": parent_id, "index": new_idx},
                ))
        else:
            # New child - add it
            patches.append(Patch(
                op=PatchOp.ADD,
                path=new_id,
                value={
                    "parentId": parent_id,
                    "index": new_idx,
                    "component": new_child,
                },
            ))

    # Remove unmatched old children
    for old_id, (old_idx, old_child) in old_by_id.items():
        if old_id not in matched_old:
            patches.append(Patch(
                op=PatchOp.REMOVE,
                path=old_id,
            ))

    return patches


def diff_trees(
    old_tree: dict[str, Any] | None,
    new_tree: dict[str, Any],
) -> DiffResult:
    """
    Diff two component trees and return a DiffResult.

    This is the main entry point for tree diffing.

    Args:
        old_tree: The previous component tree (or None for first render)
        new_tree: The new component tree

    Returns:
        DiffResult with patches and statistics
    """
    result = DiffResult()

    if old_tree is None:
        # First render - no diff, just use new tree
        result.has_changes = True
        return result

    # Diff the trees
    patches = diff_component(old_tree, new_tree, path="root")
    result.patches = patches
    result.has_changes = len(patches) > 0

    # Calculate statistics
    for patch in patches:
        if patch.op == PatchOp.ADD:
            result.components_added += 1
        elif patch.op == PatchOp.REMOVE:
            result.components_removed += 1
        elif patch.op in (PatchOp.UPDATE, PatchOp.REPLACE):
            result.components_updated += 1

    return result


def should_use_full_update(diff_result: DiffResult, tree_size: int) -> bool:
    """
    Determine if we should send a full tree update instead of patches.

    Heuristic: If more than 50% of components changed, send full tree.
    """
    if tree_size == 0:
        return True

    total_changes = (
        diff_result.components_added +
        diff_result.components_removed +
        diff_result.components_updated
    )

    # If many changes relative to tree size, use full update
    if total_changes > tree_size * 0.5:
        return True

    # If too many patches, use full update (simpler for frontend)
    if len(diff_result.patches) > 100:
        return True

    return False


def count_components(tree: dict[str, Any]) -> int:
    """Count the total number of components in a tree."""
    count = 1
    for child in tree.get("children", []):
        count += count_components(child)
    return count
