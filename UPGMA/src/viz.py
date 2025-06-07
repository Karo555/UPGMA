import matplotlib.pyplot as plt
from .tree import TreeNode

def find_parent(root: TreeNode, target_name: str) -> TreeNode | None:
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
    Render a UPGMA tree as a horizontal dendrogram and save to `path`.
    Leaves are placed at y = their order.
    """
    def collect(node: TreeNode, ys: list[str]=[]) -> dict[str, tuple[float,int]]:
        coords = {}
        if node.is_leaf():
            ys.append(node.name)
            coords[node.name] = (node.height, len(ys) - 1)
        else:
            for child in node.children:
                coords.update(collect(child, ys))
        return coords

    coords = collect(root)
    fig, ax = plt.subplots()

    for leaf_name, (x_leaf, y_leaf) in coords.items():
        parent = find_parent(root, leaf_name)
        if not parent:
            continue
        x_parent = parent.height
        ax.plot([x_parent, x_leaf], [y_leaf, y_leaf], '-')

    leaf_order = sorted(coords.items(), key=lambda kv: kv[1][1])
    y_ticks = [pos for _, (_, pos) in leaf_order]
    y_labels = [name for name, _ in leaf_order]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.invert_yaxis()

    plt.tight_layout()
    fig.savefig(path)