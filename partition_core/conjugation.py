# -*- coding: utf-8 -*-
"""
partition_core/conjugation.py
Ferrers diagram geometry and the conjugation involution.
Reference: Andrews, The Theory of Partitions, Chapter 1.
  - Section 1.3    : graphical representation of partitions
  - Definition 1.8 : conjugate partition
  - Theorem 1.4    : at-most-m-parts <-> largest-part-<=m bijection
"""
from __future__ import annotations
from partition_core.enumeration import Partition


def conjugate(lam: Partition) -> Partition:
    """
    Return the conjugate partition lambda'.

    The conjugate is obtained by transposing the Ferrers diagram:
        lambda'_i = number of parts of lambda that are >= i.

    Reference: Andrews, Definition 1.8, p.7.

    Mathematical properties:
        sum(conjugate(lam)) == sum(lam)             [same integer]
        conjugate(conjugate(lam)) == lam            [involution]
        len(conjugate(lam)) == lam[0]              [#parts = largest part]
        conjugate(lam)[0] == len(lam)              [largest part = #parts]

    Examples:
        conjugate((4, 2, 1)) -> (3, 2, 1, 1)
        conjugate((3, 3, 2)) -> (3, 3, 1, 1, 1)    [wait: parts>=1:3, >=2:3, >=3:2]
        Actually conjugate((3,3,2)) = (3,2,2,1,1) -- see tests.
    """
    if not lam:
        return ()
    max_part = lam[0]
    return tuple(
        sum(1 for p in lam if p >= i)
        for i in range(1, max_part + 1)
    )


def ferrers_matrix(lam: Partition) -> list[list[int]]:
    """
    Return a 2-D binary grid for the Ferrers diagram of lam.

    ferrers_matrix(lam)[row][col] = 1 if dot is present, else 0.
    Row 0 is the top row (largest part), consistent with Andrews's convention.
    """
    if not lam:
        return []
    rows = len(lam)
    cols = lam[0]
    return [
        [1 if col < lam[row] else 0 for col in range(cols)]
        for row in range(rows)
    ]


def conjugation_animation_frames(lam: Partition) -> list[dict]:
    """
    Return a sequence of frames describing the conjugation animation.

    Each frame is a dict with:
        'step'             : int          - frame index (0 = initial)
        'label'            : str          - human-readable description
        'original'         : Partition    - original partition (unchanged)
        'highlighted_col'  : int or None  - column being read in this step
        'conjugate_so_far' : Partition    - conjugate parts built so far

    Animation narrative:
        Frame 0      : display original Ferrers diagram
        Frame 1..k   : highlight column i, read its height -> part i of lambda'
        Frame k+1    : display complete conjugate diagram

    Reference: Andrews, Section 1.3 -- conjugate via column counting.
    """
    frames: list[dict] = []

    # Frame 0: initial state
    frames.append({
        'step': 0,
        'label': f'Original partition lambda = {lam}. Sum = {sum(lam)}.',
        'original': lam,
        'highlighted_col': None,
        'conjugate_so_far': (),
    })

    conjugate_parts: list[int] = []
    max_part = lam[0] if lam else 0

    for col in range(max_part):
        col_height = sum(1 for p in lam if p > col)
        conjugate_parts.append(col_height)
        frames.append({
            'step': col + 1,
            'label': (
                f"Column {col + 1} has {col_height} dot(s) -> "
                f"part {col + 1} of lambda' = {col_height}."
            ),
            'original': lam,
            'highlighted_col': col,
            'conjugate_so_far': tuple(conjugate_parts),
        })

    conj = tuple(conjugate_parts)
    frames.append({
        'step': max_part + 1,
        'label': (
            f"Conjugate lambda' = {conj}. "
            f"Sum = {sum(conj)} (equals sum of lambda = {sum(lam)})."
        ),
        'original': lam,
        'highlighted_col': None,
        'conjugate_so_far': conj,
    })

    return frames


def verify_theorem_1_4(
    n: int,
    m: int,
    partitions_at_most_m,
    partitions_max_part_m,
) -> dict:
    """
    Computationally verify Andrews Theorem 1.4:

        #{partitions of n with at most m parts}
        = #{partitions of n with largest part <= m}

    The bijection is lambda -> lambda' (conjugation).

    Returns a dict with:
        n, m              : parameters
        count_*           : sizes of both sets
        verified          : True iff counts match AND bijection is explicit
        bijection_*_ok    : detailed bijection check flags

    Reference: Andrews, Theorem 1.4, p.8.
    """
    p_at_most = partitions_at_most_m(n, m)
    p_max = partitions_max_part_m(n, m)
    p_max_set = set(p_max)

    bijection_ok = True
    involution_ok = True

    for lam in p_at_most:
        conj = conjugate(lam)
        if conj not in p_max_set:
            bijection_ok = False
            break
        if conjugate(conj) != lam:
            involution_ok = False
            break

    return {
        'n': n,
        'm': m,
        'count_at_most_m_parts': len(p_at_most),
        'count_max_part_m': len(p_max),
        'verified': len(p_at_most) == len(p_max) and bijection_ok and involution_ok,
        'partitions_at_most_m_parts': p_at_most,
        'partitions_max_part_m': p_max,
        'bijection_explicit_ok': bijection_ok,
        'involution_ok': involution_ok,
    }
