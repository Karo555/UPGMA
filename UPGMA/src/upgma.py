# upgma.py

from typing import List, Tuple
from .io import DistanceMatrix
from .tree import TreeNode

class UPGMA:
    def __init__(self, dm: DistanceMatrix):
        # Initialize nodes, sizes, and a mutable copy of the distance matrix
        self.nodes: List[TreeNode] = [
            TreeNode(name=label, height=0.0) for label in dm.labels
        ]
        self.sizes: List[int] = [1] * len(dm.labels)
        # Deep copy so we can mutate
        self.matrix: List[List[float]] = [row.copy() for row in dm.matrix]
        self.merge_log: List[Tuple[str, str, float]] = []

    def _get_leaf_names(self, node: TreeNode) -> List[str]:
        """Recursively collect all leaf names under `node`."""
        if node.is_leaf():
            return [node.name]
        names: List[str] = []
        for child in node.children:
            names.extend(self._get_leaf_names(child))
        return names

    def _find_closest_pair(self) -> Tuple[int, int]:
        """Return indices (i, j) of the smallest non-zero distance."""
        n = len(self.matrix)
        min_dist = float("inf")
        pair = (0, 1)
        for i in range(n):
            for j in range(i + 1, n):
                if self.matrix[i][j] < min_dist:
                    min_dist = self.matrix[i][j]
                    pair = (i, j)
        return pair

    def _merge_clusters(self, i: int, j: int, new_node: TreeNode) -> None:
        """Replace clusters i & j with new_node, update sizes, nodes, and merge_log."""
        # Record merge event using the full leaf sets of each cluster
        leaves_i = self._get_leaf_names(self.nodes[i])
        leaves_j = self._get_leaf_names(self.nodes[j])
        label_i = "|".join(leaves_i)
        label_j = "|".join(leaves_j)
        self.merge_log.append((label_i, label_j, new_node.height))

        # Update node list and sizes
        size_i = self.sizes[i]
        size_j = self.sizes[j]
        new_size = size_i + size_j

        self.nodes[i] = new_node
        self.sizes[i] = new_size

        # Remove the j-th entry
        del self.nodes[j]
        del self.sizes[j]

    def run(self) -> TreeNode:
        """
        Execute UPGMA clustering.
        Returns the final TreeNode (the root of the tree).
        """
        while len(self.nodes) > 1:
            i, j = self._find_closest_pair()
            dist_ij = self.matrix[i][j]
            height = dist_ij / 2.0

            # Create new internal node
            new_node = TreeNode(
                name=None,
                height=height,
                children=[self.nodes[i], self.nodes[j]],
            )

            # Capture old cluster sizes for weighted averaging
            size_i = self.sizes[i]
            size_j = self.sizes[j]
            new_size = size_i + size_j

            # Compute new distances for cluster i
            for k in range(len(self.matrix)):
                if k in (i, j):
                    continue
                d_ik = self.matrix[i][k]
                d_jk = self.matrix[j][k]
                weighted = (d_ik * size_i + d_jk * size_j) / new_size
                self.matrix[i][k] = weighted
                self.matrix[k][i] = weighted

            # Merge clusters in data structures and log properly
            self._merge_clusters(i, j, new_node)

            # Remove row j and column j from the distance matrix
            del self.matrix[j]
            for row in self.matrix:
                del row[j]

        # At the end, one node remains
        return self.nodes[0]


def upgma(dm: DistanceMatrix) -> TreeNode:
    """
    Convenience function: build and run UPGMA on dm.
    """
    return UPGMA(dm).run()