import argparse
import os
import shutil
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
    parser.add_argument("input_file", help="Path to FASTA or matrix file")
    parser.add_argument(
        "--mode",
        choices=["sequences", "matrix"],
        required=True,
        help="Input is raw sequences or a precomputed matrix",
    )
    parser.add_argument("--match", type=int, default=1, help="Match score")
    parser.add_argument("--mismatch", type=int, default=-1, help="Mismatch penalty")
    parser.add_argument("--gap", type=int, default=-2, help="Gap penalty")
    parser.add_argument(
        "-o",
        "--output-newick",
        default="tree.nwk",
        help="Filename for Newick output",
    )
    parser.add_argument(
        "--output-log", help="CSV to record merges: cluster_i,cluster_j,height"
    )
    parser.add_argument(
        "--output-plot", help="PNG/SVG path to save dendrogram"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Prepare output directory next to this file
    base = os.path.splitext(os.path.basename(args.input_file))[0]
    out_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__),"..", "..", "output", base)
    )
    os.makedirs(out_dir, exist_ok=True)

    # Archive the input
    shutil.copy(args.input_file, out_dir)

    try:
        if args.mode == "sequences":
            seqs = load_input(args.input_file, mode="sequences")
            scoring = ScoringScheme(
                match=args.match, mismatch=args.mismatch, gap=args.gap
            )
            dm = compute_distance_matrix(seqs, scoring)
        else:
            dm = load_input(args.input_file, mode="matrix")
    except InputFormatError as e:
        print(f"ERROR: {e}")
        return

    # Run UPGMA
    upg = UPGMA(dm)
    root = upg.run()

    # Determine output paths under out_dir
    nw_path = os.path.join(out_dir, os.path.basename(args.output_newick))
    log_path = (
        os.path.join(out_dir, os.path.basename(args.output_log))
        if args.output_log
        else None
    )
    plot_path = (
        os.path.join(out_dir, os.path.basename(args.output_plot))
        if args.output_plot
        else None
    )

    # Write Newick
    write_newick(root, nw_path)
    print(f"Newick tree written to {nw_path}")

    # Optional: write merge log
    if log_path:
        with open(log_path, "w") as f:
            f.write("cluster_i,cluster_j,height\n")
            for ci, cj, h in upg.merge_log:
                f.write(f"{ci},{cj},{h:.6f}\n")
        print(f"Merge log written to {log_path}")

    # Optional: plot
    if plot_path:
        plot_tree(root, plot_path)
        print(f"Dendrogram saved to {plot_path}")


if __name__ == "__main__":
    main()