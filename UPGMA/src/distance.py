from MSA.multiple_sequence_alignment.utils.functions import ScoringScheme
from typing import List
from NW.needleman_wunsch.src.aligner.models import Sequence
from MSA.multiple_sequence_alignment.utils.functions import (build_pairwise_score_matrix, convert_scores_to_distances)
from .io import DistanceMatrix  # adjust to your actual io module path


def compute_pairwise_scores(
    seqs: List[Sequence],
    scoring: "ScoringScheme",
) -> List[List[int]]:
    """
    Compute Needleman–Wunsch alignment scores for all sequence pairs.
    Returns an n×n symmetric score matrix (integers).
    """
    return build_pairwise_score_matrix(seqs, scoring)


def convert_scores_to_matrix(
    scores: List[List[int]],
) -> List[List[float]]:
    """
    Convert raw alignment scores into distances via:
        distance = max_score - score
    """
    return convert_scores_to_distances(scores)


def compute_distance_matrix(
    seqs: List[Sequence],
    scoring: "ScoringScheme",
) -> DistanceMatrix:
    """
    Full pipeline: 
      1. compute pairwise NW scores 
      2. convert to distances 
      3. wrap into DistanceMatrix(labels, matrix)
    
    Labels are taken from seq.id in input order.
    """
    scores = compute_pairwise_scores(seqs, scoring)
    dists = convert_scores_to_matrix(scores)
    labels = [s.id for s in seqs]
    return DistanceMatrix(labels, dists)
