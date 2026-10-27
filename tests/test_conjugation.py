"""
tests/test_conjugation.py
In-depth mathematical invariant and edge case tests for partition_core.conjugation.
Reference: Andrews, The Theory of Partitions, Chapter 1, Section 1.3 & Theorem 1.4.
"""
from __future__ import annotations
import pytest
from partition_core.enumeration import generate_partitions, partitions_distinct
from partition_core.conjugation import (
    conjugate,
    ferrers_matrix,
    conjugation_animation_frames,
    verify_theorem_1_4,
)
from partition_core.enumeration import partitions_at_most_m_parts, partitions_max_part


def test_conjugate_empty():
    assert conjugate(()) == ()


def test_conjugate_single_part():
    # (n,) has Ferrers diagram 1 row of n dots -> transpose is n rows of 1 dot
    for n in range(1, 15):
        assert conjugate((n,)) == (1,) * n


def test_conjugate_all_ones():
    # (1, 1, ..., 1) (length k) -> transpose is (k,)
    for k in range(1, 15):
        assert conjugate((1,) * k) == (k,)


def test_conjugate_known_examples():
    # Andrews p.7-8 examples
    assert conjugate((4, 2, 1)) == (3, 2, 1, 1)
    assert conjugate((5, 3, 3, 1)) == (4, 3, 3, 1, 1)
    assert conjugate((3, 3, 2)) == (3, 3, 2)  # self-conjugate partition
    assert conjugate((4, 3, 2, 1)) == (4, 3, 2, 1)  # self-conjugate stair
    assert conjugate((3, 2, 1)) == (3, 2, 1)        # self-conjugate stair


def test_ferrers_matrix_structure():
    assert ferrers_matrix(()) == []

    lam = (4, 2, 1)
    mat = ferrers_matrix(lam)
    assert len(mat) == 3       # 3 rows
    assert len(mat[0]) == 4    # 4 cols
    assert sum(sum(row) for row in mat) == 7

    # Row sums match partition parts
    assert [sum(row) for row in mat] == [4, 2, 1]

    # Column sums match conjugate parts
    cols = len(mat[0])
    col_sums = [sum(mat[r][c] for r in range(len(mat))) for c in range(cols)]
    assert tuple(col_sums) == conjugate(lam)


def test_conjugation_animation_frames():
    lam = (5, 3, 1)
    frames = conjugation_animation_frames(lam)
    assert len(frames) == 5 + 2  # Frame 0, frames 1..5 for cols, frame 6 final
    assert frames[0]["step"] == 0
    assert frames[0]["conjugate_so_far"] == ()

    final_frame = frames[-1]
    assert final_frame["step"] == len(frames) - 1
    assert final_frame["conjugate_so_far"] == conjugate(lam)
    assert final_frame["highlighted_col"] is None


def test_sylvester_self_conjugate_theorem():
    """
    Sylvester's Theorem (Andrews Ch. 1, Ex. 8):
    The number of self-conjugate partitions of n equals the number of partitions
    of n into distinct odd parts.
    """
    for n in range(1, 30):
        all_p = generate_partitions(n)
        self_conj_count = sum(1 for p in all_p if conjugate(p) == p)

        # distinct odd parts
        dist_odd_count = sum(
            1 for p in partitions_distinct(n) if all(part % 2 == 1 for part in p)
        )
        assert self_conj_count == dist_odd_count, (
            f"Sylvester identity failed at n={n}: "
            f"self-conjugate={self_conj_count}, distinct-odd={dist_odd_count}"
        )


def test_durfee_square_invariance():
    """
    Durfee square side length d(lambda) is invariant under conjugation:
    d(lambda) = d(lambda').
    """
    for n in range(1, 25):
        for lam in generate_partitions(n):
            conj = conjugate(lam)
            d_lam = sum(1 for i, p in enumerate(lam, 1) if p >= i)
            d_conj = sum(1 for i, p in enumerate(conj, 1) if p >= i)
            assert d_lam == d_conj, f"Durfee square mismatch for {lam}: {d_lam} vs {d_conj}"
