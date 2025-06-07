import argparse
from .io import load_input, InputFormatError
from .distance import compute_distance_matrix
from .upgma import UPGMA
from .tree import write_newick
from .viz import plot_tree
from MSA.multiple_sequence_alignment.utils.functions import ScoringScheme


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build a UPGMA phylogenetic tree from FASTA or a distance matrix."
    )
    parser.add_argument(
        "input_file",
        help="Path to FASTA file (mode=sequences) or matrix file (mode=matrix)"
    )
    parser.add_argument(
        "--mode",
        choices=["sequences", "matrix"],
        required=True,
        help="Specify whether the input is raw sequences or a precomputed matrix"
    )
    parser.add_argument(
        "--match", type=int, default=1,
        help="Match score (only used in sequences mode)"
    )
    parser.add_argument(
        "--mismatch", type=int, default=-1,
        help="Mismatch penalty (only used in sequences mode)"
    )
    parser.add_argument(
        "--gap", type=int, default=-2,
        help="Gap penalty (only used in sequences mode)"
    )
    parser.add_argument(
        "-o", "--output-newick",
        default="tree.nwk",
        help="File to write the resulting Newick tree"
    )
    parser.add_argument(
        "--output-log",
        help="Optional CSV to record each merge: cluster_i,cluster_j,height"
    )
    parser.add_argument(
        "--output-plot",
        help="Optional path (PNG/SVG) to save a dendrogram of the tree"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        if args.mode == "sequences":
            seqs = load_input(args.input_file, mode="sequences")
            scoring = ScoringScheme(
                match=args.match,
                mismatch=args.mismatch,
                gap=args.gap
            )
            dm = compute_distance_matrix(seqs, scoring)
        else:
            dm = load_input(args.input_file, mode="matrix")

    except InputFormatError as e:
        print(f"ERROR: {e}")
        return

    # Run UPGMA and capture the merge log
    upg = UPGMA(dm)
    root = upg.run()

    # Write Newick
    write_newick(root, args.output_newick)
    print(f"Newick tree written to {args.output_newick}")

    # Optional: write merge log
    if args.output_log:
        with open(args.output_log, "w") as f:
            f.write("cluster_i,cluster_j,height\n")
            for ci, cj, h in upg.merge_log:
                f.write(f"{ci},{cj},{h:.6f}\n")
        print(f"Merge log written to {args.output_log}")

    # Optional: plot
    if args.output_plot:
        # plot_tree should take (root, path) and save an image
        plot_tree(root, args.output_plot)
        print(f"Dendrogram saved to {args.output_plot}")


if __name__ == "__main__":
    main()