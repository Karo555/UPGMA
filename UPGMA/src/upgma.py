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
        """Replace clusters i & j with new_node, update sizes, nodes, and labels."""
        # Record merge event using current leaf labels
        label_i = self.nodes[i].name
        label_j = self.nodes[j].name
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

    def _update_matrix(self, i: int, j: int) -> None:
        """Compute new distances for cluster i, then remove row/col j."""
        size_i = self.sizes[i]
        # size_j was already merged into sizes[i] by _merge_clusters
        size_j = size_i - (size_i - self.sizes[i])  # not needed, we can compute from record
        # Actually, capture old sizes before merge for weighted average:
        # Let's recompute old sizes from merge_log, but simpler: pass sizes into this method.
        # Instead, restructure: compute weighted average before merging sizes.

        # For clarity, here's a self-contained weighted update:
        # We'll recalc old sizes by subtracting; but better to pass old sizes in.

        # Instead, do the weighted update inside run() prior to calling _merge_clusters.

        raise NotImplementedError("_update_matrix should be inlined in run() for clarity")

    def run(self) -> TreeNode:
        """
        Execute UPGMA clustering.
        Returns:
            The final TreeNode (the root of the tree).
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

            # Merge clusters in data structures
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