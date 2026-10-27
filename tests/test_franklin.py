"""
tests/test_franklin.py
Mathematical invariant and bijection tests for Franklin's Involution.
Reference: Andrews, The Theory of Partitions, Chapter 1, Section 1.3 & Theorem 1.6.
"""
from __future__ import annotations
import pytest
from partition_core.enumeration import partitions_distinct
from partition_core.franklin import (
    slope_length,
    base_length,
    is_exceptional,
    franklin_map,
    franklin_details,
    verify_euler_pentagonal,
)


def test_slope_and_base():
    # lam = (5, 4, 2) -> slope: 5,4 -> s=2. base: 2 -> b=2
    lam = (5, 4, 2)
    assert slope_length(lam) == 2
    assert base_length(lam) == 2

    # lam = (7, 6, 5, 4) -> slope: all 4 parts -> s=4. base: 4 -> b=4
    lam2 = (7, 6, 5, 4)
    assert slope_length(lam2) == 4
    assert base_length(lam2) == 4

    # lam = (6, 3, 1) -> slope: only 6 -> s=1. base: 1 -> b=1
    lam3 = (6, 3, 1)
    assert slope_length(lam3) == 1
    assert base_length(lam3) == 1


def test_exceptional_partitions():
    # Case 1: lambda = (2k-1, ..., k), n = omega(k)
    # k=1: (1,), n=1
    assert is_exceptional((1,)) == (True, "omega_k", 1)
    # k=2: (3, 2), n=5
    assert is_exceptional((3, 2)) == (True, "omega_k", 2)
    # k=3: (5, 4, 3), n=12
    assert is_exceptional((5, 4, 3)) == (True, "omega_k", 3)
    # k=4: (7, 6, 5, 4), n=22
    assert is_exceptional((7, 6, 5, 4)) == (True, "omega_k", 4)

    # Case 2: lambda = (2k, ..., k+1), n = omega(-k)
    # k=1: (2,), n=2
    assert is_exceptional((2,)) == (True, "omega_minus_k", -1)
    # k=2: (4, 3), n=7
    assert is_exceptional((4, 3)) == (True, "omega_minus_k", -2)
    # k=3: (6, 5, 4), n=15
    assert is_exceptional((6, 5, 4)) == (True, "omega_minus_k", -3)
    # k=4: (8, 7, 6, 5), n=26
    assert is_exceptional((8, 7, 6, 5)) == (True, "omega_minus_k", -4)

    # Non-exceptional
    assert is_exceptional((5, 4, 2))[0] is False
    assert is_exceptional((6, 2, 1))[0] is False


def test_franklin_map_involution_on_all_n_up_to_30():
    for n in range(1, 31):
        dist = partitions_distinct(n)
        for lam in dist:
            mapped = franklin_map(lam)
            exp, _, _ = is_exceptional(lam)
            if exp:
                assert mapped is None
            else:
                assert mapped is not None
                # Check sum preservation
                assert sum(mapped) == n
                # Check strictly distinct
                assert all(mapped[i] > mapped[i + 1] for i in range(len(mapped) - 1))
                # Check parity alternation
                assert abs(len(mapped) - len(lam)) == 1
                # Check involution
                assert franklin_map(mapped) == lam


def test_franklin_details_structure():
    details = franklin_details((5, 3, 2))
    assert details["n"] == 10
    assert details["r"] == 3
    assert details["b"] == 2
    assert details["s"] == 1  # 5, 3 does not continue slope
    assert details["action"] == "move_slope_to_base"
    assert details["target"] == (4, 3, 2, 1)


def test_verify_euler_pentagonal_theorem():
    results = verify_euler_pentagonal(35)
    assert len(results) == 35
    for r in results:
        assert r["verified"] is True, f"Verification failed at n={r['n']}"
