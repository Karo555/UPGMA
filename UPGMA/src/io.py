from NW.needleman_wunsch.src.aligner.models import Sequence
from NW.needleman_wunsch.src.aligner.io import read_fasta
from MSA.multiple_sequence_alignment.src.cli import build_pairwise_score_matrix
from MSA.multiple_sequence_alignment.utils.functions import convert_scores_to_distances
from typing import List, Union, Literal
import os
import csv
from typing import List, Union, Literal


class InputFormatError(Exception):
    """Raised for any parse/validation errors in input data."""

class DistanceMatrix:
    """Container for labels and a square distance matrix."""
    def __init__(self, labels: List[str], matrix: List[List[float]]):
        self.labels = labels
        self.matrix = matrix

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx: int) -> List[float]:
        return self.matrix[idx]

def parse_distance_matrix(path: str) -> DistanceMatrix:
    """
    Load a raw-number distance matrix from CSV (comma-delim) or TXT (whitespace-delim),
    auto-detecting by file extension. Supports an optional header row of labels.
    """
    ext = os.path.splitext(path)[1].lower()
    delim = ',' if ext == '.csv' else None

    with open(path, newline='') as f:
        if delim:
            reader = csv.reader(f, delimiter=delim)
            rows = [row for row in reader if row]
        else:
            rows = [line.strip().split() for line in f if line.strip()]

    if not rows:
        raise InputFormatError(f"Distance matrix file is empty: {path}")

    # detect optional header row
    first = rows[0]
    try:
        [float(x) for x in first]
        header = None
        data_rows = rows
    except ValueError:
        header = first
        data_rows = rows[1:]
        if not data_rows:
            raise InputFormatError("Header present but no data rows found")

    n = len(data_rows)
    if header and len(header) != n:
        raise InputFormatError(
            f"Header length {len(header)} does not match number of data rows {n}"
        )

    labels = header if header else [str(i) for i in range(n)]
    matrix: List[List[float]] = []

    for i, row in enumerate(data_rows):
        if len(row) != n:
            raise InputFormatError(
                f"Row {i} has {len(row)} columns but expected {n}"
            )
        try:
            vals = [float(x) for x in row]
        except ValueError:
            raise InputFormatError(f"Non-numeric value found in row {i}")
        matrix.append(vals)

    return DistanceMatrix(labels, matrix)

def validate_distance_matrix(dm: DistanceMatrix) -> None:
    """
    Ensure the matrix is square, symmetric, zeros on diagonal, and non-negative.
    """
    n = len(dm)
    if len(dm.matrix) != n:
        raise InputFormatError("Distance matrix is not square (row count mismatch)")

    for i, row in enumerate(dm.matrix):
        if len(row) != n:
            raise InputFormatError(f"Row {i} length {len(row)} != expected {n}")

    for i in range(n):
        if dm.matrix[i][i] != 0:
            raise InputFormatError(f"Diagonal entry at index {i} is not zero")

    for i in range(n):
        for j in range(i + 1, n):
            if dm.matrix[i][j] != dm.matrix[j][i]:
                raise InputFormatError(
                    f"Matrix not symmetric at ({i},{j}) vs ({j},{i})"
                )
            if dm.matrix[i][j] < 0:
                raise InputFormatError(
                    f"Negative distance at ({i},{j}): {dm.matrix[i][j]}"
                )

def load_input(
    path: str,
    mode: Literal["sequences", "matrix"]
) -> Union[List[Sequence], DistanceMatrix]:
    """
    Load FASTA sequences or a distance matrix, validating as needed.
    mode="sequences"  → returns List[Sequence]
    mode="matrix"     → returns DistanceMatrix
    """
    if mode == "sequences":
        seqs = read_fasta(path)   # Sequence.__init__ handles validation
        return seqs

    if mode == "matrix":
        dm = parse_distance_matrix(path)
        validate_distance_matrix(dm)
        return dm

    raise InputFormatError(f"Unknown mode {mode!r}; expected 'sequences' or 'matrix'")