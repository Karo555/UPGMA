from typing import List, Optional

class TreeNode:
    """
    A node in a phylogenetic tree.
    Attributes:
        name: leaf identifier or empty for internal nodes
        height: distance/time from the root
        children: list of child TreeNode instances
    """
    def __init__(
        self,
        name: Optional[str],
        height: float,
        children: Optional[List['TreeNode']] = None
    ):
        self.name = name or ""
        self.height = height
        self.children = children or []

    def is_leaf(self) -> bool:
        return not self.children

    def __repr__(self) -> str:
        if self.is_leaf():
            return f"TreeNode(name={self.name!r}, height={self.height})"
        return (
            f"TreeNode(name={self.name!r}, height={self.height}, "
            f"children={self.children})"
        )


def to_newick(node: TreeNode) -> str:
    """
    Serialize the tree rooted at `node` to Newick format.
    Branch lengths are computed as (parent.height – child.height).
    The returned string ends with a semicolon.
    """
    def recurse(n: TreeNode) -> str:
        if n.is_leaf():
            return n.name
        parts = []
        for child in n.children:
            bl = n.height - child.height
            parts.append(f"{recurse(child)}:{bl:.6f}")
        return f"({','.join(parts)})"
    return recurse(node) + ";"


def write_newick(node: TreeNode, path: str) -> None:
    """
    Write the Newick string for `node` to the given file path.
    """
    newick_str = to_newick(node)
    with open(path, "w") as f:
        f.write(newick_str)