"""
tests/test_enumeration.py
Mathematical invariant tests for partition_core.enumeration.
Run with: python -m pytest tests/ -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from partition_core.enumeration import (
    generate_partitions, partition_count, partition_count_table,
    partitions_distinct, partitions_odd,
    partitions_at_most_m_parts, partitions_max_part,
)
from partition_core.conjugation import conjugate, verify_theorem_1_4


# -- Known values of p(n) -----------------------------------------------------
KNOWN_P = {0:1, 1:1, 2:2, 3:3, 4:5, 5:7, 6:11, 7:15, 8:22,
           9:30, 10:42, 20:627, 50:204226, 100:190569292}

@pytest.mark.parametrize("n,expected", KNOWN_P.items())
def test_partition_count_known(n, expected):
    assert partition_count(n) == expected

def test_partition_count_table_matches_cached():
    table = partition_count_table(50)
    for n in range(51):
        assert table[n] == partition_count(n), f"Mismatch at n={n}"

def test_generate_partitions_count():
    for n in range(1, 15):
        parts = generate_partitions(n)
        assert len(parts) == partition_count(n), f"Wrong count at n={n}"

def test_generate_partitions_sums():
    for n in range(1, 20):
        for lam in generate_partitions(n):
            assert sum(lam) == n, f"Bad partition {lam} of {n}"

def test_generate_partitions_non_increasing():
    for n in range(1, 20):
        for lam in generate_partitions(n):
            assert all(lam[i] >= lam[i+1] for i in range(len(lam)-1))

def test_empty_partition():
    assert generate_partitions(0) == [()]
    assert partition_count(0) == 1


# -- Euler's Theorem (Corollary 1.2) ------------------------------------------
def test_eulers_theorem_odd_equals_distinct():
    """p(O, n) == p(D, n) for all n -- Andrews Corollary 1.2."""
    for n in range(1, 25):
        odd   = partitions_odd(n)
        dist  = partitions_distinct(n)
        assert len(odd) == len(dist), (
            f"Euler's theorem fails at n={n}: "
            f"|odd|={len(odd)}, |distinct|={len(dist)}"
        )

def test_odd_parts_all_odd():
    for n in range(1, 20):
        for lam in partitions_odd(n):
            assert all(p % 2 == 1 for p in lam), f"Even part in {lam}"

def test_distinct_parts_all_distinct():
    for n in range(1, 20):
        for lam in partitions_distinct(n):
            assert len(lam) == len(set(lam)), f"Repeated part in {lam}"


# -- Conjugation (Andrews Definition 1.8 + Theorem 1.4) -----------------------
def test_conjugate_sum_preserved():
    for n in range(1, 20):
        for lam in generate_partitions(n):
            assert sum(conjugate(lam)) == n, f"Sum changed for {lam}"

def test_conjugate_is_involution():
    for n in range(1, 20):
        for lam in generate_partitions(n):
            assert conjugate(conjugate(lam)) == lam, f"Not involution: {lam}"

def test_conjugate_largest_part_becomes_num_parts():
    """Largest part of lambda = number of parts of conjugate."""
    for n in range(1, 20):
        for lam in generate_partitions(n):
            assert lam[0] == len(conjugate(lam))

def test_theorem_1_4_bijection():
    """Andrews Theorem 1.4: at-most-m-parts <-> max-part-m."""
    for n in range(1, 15):
        for m in range(1, n + 1):
            result = verify_theorem_1_4(
                n, m,
                partitions_at_most_m_parts,
                partitions_max_part,
            )
            assert result['verified'], (
                f"Theorem 1.4 fails for n={n}, m={m}: "
                f"counts {result['count_at_most_m_parts']} vs "
                f"{result['count_max_part_m']}"
            )

def test_negative_n_raises():
    with pytest.raises(ValueError):
        generate_partitions(-1)
    with pytest.raises(ValueError):
        partition_count_table(-1)
