import matplotlib.pyplot as plt
from typing import Optional
from .tree import TreeNode

def find_parent(root: TreeNode, target_name: str) -> Optional[TreeNode]:
    """
    Return the parent TreeNode of the leaf named target_name, or None if not found.
    """
    for child in root.children:
        if child.is_leaf() and child.name == target_name:
            return root
        parent = find_parent(child, target_name)
        if parent:
            return parent
    return None

def plot_tree(root: TreeNode, path: str) -> None:
    """
    Render a UPGMA tree as a proper dendrogram with vertical and horizontal branches.
    """
    # Assign x (height) and y (leaf order) for every node
    coords: dict[TreeNode, tuple[float, float]] = {}
    y_counter = [0]
    def _assign(node: TreeNode):
        if node.is_leaf():
            y = y_counter[0]
            coords[node] = (node.height, y)
            y_counter[0] += 1
        else:
            for child in node.children:
                _assign(child)
            ys = [coords[c][1] for c in node.children]
            coords[node] = (node.height, sum(ys) / len(ys))
    _assign(root)

    fig, ax = plt.subplots()

    # Draw branches
    for node, (x, y) in coords.items():
        if not node.is_leaf():
            # vertical line at this node's height
            ys = [coords[c][1] for c in node.children]
            ax.plot([x, x], [min(ys), max(ys)], '-')
            # horizontal lines to each child
            for child in node.children:
                xc, yc = coords[child]
                ax.plot([x, xc], [yc, yc], '-')

    # Label only leaves on y-axis
    leaves = [n for n in coords if n.is_leaf()]
    leaves.sort(key=lambda n: coords[n][1])
    y_ticks = [coords[n][1] for n in leaves]
    labels  = [n.name for n in leaves]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()

    plt.tight_layout()
    fig.savefig(path)