# -*- coding: utf-8 -*-
"""
partition_core/franklin.py
Franklin's combinatorial proof of Euler's Pentagonal Number Theorem.
Reference: Andrews, The Theory of Partitions, Chapter 1, Section 1.3 & Theorem 1.6.

Euler's Pentagonal Number Theorem:
    prod_{n=1}^inf (1 - q^n) = sum_{k=-inf}^inf (-1)^k q^{k(3k-1)/2}

Combinatorial interpretation:
    p_e(D, n) - p_o(D, n) = (-1)^k  if n = k(3k-1)/2 for some k in Z
                          = 0        otherwise.

Franklin (1881) proved this by defining an almost-everywhere involution phi
on the set D(n) of partitions into distinct parts that flips parity of part-count:
    len(phi(lambda)) = len(lambda) +/- 1
The fixed points / exceptions occur precisely when n is a pentagonal number.
"""
from __future__ import annotations
from partition_core.enumeration import Partition, partitions_distinct


def slope_length(lam: Partition) -> int:
    """
    Return the length of the slope s(lambda).
    The slope consists of the line of dots starting at the rightmost dot of
    the first row, moving down and to the left by 1 dot per row:
        lambda_1, lambda_2 = lambda_1 - 1, ..., lambda_s = lambda_1 - s + 1.
    """
    if not lam:
        return 0
    s = 1
    r = len(lam)
    while s < r and lam[s] == lam[s - 1] - 1:
        s += 1
    return s


def base_length(lam: Partition) -> int:
    """
    Return the base length b(lambda) = lambda[-1] (the smallest part).
    """
    if not lam:
        return 0
    return lam[-1]


def is_exceptional(lam: Partition) -> tuple[bool, str | None, int]:
    """
    Check if partition lambda is one of Franklin's exceptional partitions.

    Returns:
        (is_exceptional, case_label, k_index)
        - If s = r and b = s:
            lambda = (2k-1, 2k-2, ..., k), n = k(3k-1)/2 = omega(k), returns (True, "omega_k", k)
        - If s = r and b = s + 1:
            lambda = (2k, 2k-1, ..., k+1), n = k(3k+1)/2 = omega(-k), returns (True, "omega_minus_k", -k)
        - Otherwise returns (False, None, 0)
    """
    if not lam:
        return (False, None, 0)
    r = len(lam)
    s = slope_length(lam)
    b = base_length(lam)

    if s == r:
        if b == s:
            return (True, "omega_k", s)
        elif b == s + 1:
            return (True, "omega_minus_k", -s)

    return (False, None, 0)


def franklin_map(lam: Partition) -> Partition | None:
    """
    Apply Franklin's involution phi(lambda) to partition with distinct parts.

    Returns:
        The paired partition phi(lambda) in D(n), or None if lambda is exceptional.

    Operation:
        Let r = len(lambda), s = slope_length(lambda), b = base_length(lambda).
        1. If lambda is exceptional, returns None.
        2. If b <= s:
           Move base to slope (delete last part b, add 1 to first b parts).
           New part count = r - 1.
        3. If b > s:
           Move slope to base (subtract 1 from first s parts, append new part s).
           New part count = r + 1.
    """
    if not lam:
        return None

    # Check strictly distinct
    for i in range(len(lam) - 1):
        if lam[i] <= lam[i + 1]:
            raise ValueError(f"Partition {lam} does not have strictly distinct parts.")

    exp, _, _ = is_exceptional(lam)
    if exp:
        return None

    r = len(lam)
    s = slope_length(lam)
    b = base_length(lam)

    if b <= s:
        # Move base to slope: remove part r (length b), add 1 to parts 0..b-1
        new_parts = list(lam[:-1])
        for i in range(b):
            new_parts[i] += 1
        return tuple(new_parts)
    else:
        # Move slope to base: subtract 1 from parts 0..s-1, append part of length s
        new_parts = [lam[i] - 1 for i in range(s)] + list(lam[s:]) + [s]
        return tuple(new_parts)


def franklin_details(lam: Partition) -> dict:
    """
    Return comprehensive analysis and diagram coordinates for Franklin's map on lambda.
    Useful for visualization and educational animation.
    """
    if not lam:
        return {
            "lam": (), "n": 0, "r": 0, "b": 0, "s": 0,
            "is_exceptional": False, "exceptional_case": None, "k_index": 0,
            "action": "none", "target": None,
            "base_coords": [], "slope_coords": [], "intersection_coords": []
        }

    r = len(lam)
    s = slope_length(lam)
    b = base_length(lam)
    exp, case_lbl, k_val = is_exceptional(lam)
    target = franklin_map(lam)

    # Coordinates for dots (0-indexed: row 0..r-1, col 0..lam[row]-1)
    base_coords = [(r - 1, c) for c in range(b)]
    slope_coords = [(i, lam[i] - 1) for i in range(s)]

    # Intersection dot occurs if s == r and the slope ends at the base
    intersect = list(set(base_coords).intersection(set(slope_coords)))

    action = "exceptional" if exp else ("move_base_to_slope" if b <= s else "move_slope_to_base")

    return {
        "lam": lam,
        "n": sum(lam),
        "r": r,
        "b": b,
        "s": s,
        "is_exceptional": exp,
        "exceptional_case": case_lbl,
        "k_index": k_val,
        "action": action,
        "target": target,
        "base_coords": base_coords,
        "slope_coords": slope_coords,
        "intersection_coords": intersect,
    }


def verify_euler_pentagonal(max_n: int) -> list[dict]:
    """
    Verify Euler's Pentagonal Number Theorem computationally for n = 1 .. max_n.
    Verifies that Franklin's involution perfectly pairs all partitions of D(n)
    except the exact generalized pentagonal exceptions.
    """
    results = []
    for n in range(1, max_n + 1):
        dist_parts = partitions_distinct(n)
        even_parts = [p for p in dist_parts if len(p) % 2 == 0]
        odd_parts = [p for p in dist_parts if len(p) % 2 == 1]
        diff = len(even_parts) - len(odd_parts)

        # Theoretical expected difference from pentagonal numbers
        # k(3k-1)/2 for k in {..., -2, -1, 1, 2, ...}
        expected_diff = 0
        expected_k = None
        # Check positive k
        for k in range(1, n + 2):
            wp = k * (3 * k - 1) // 2
            wn = k * (3 * k + 1) // 2
            sign = 1 if k % 2 == 0 else -1
            if wp == n:
                expected_diff = sign
                expected_k = k
                break
            if wn == n:
                expected_diff = sign
                expected_k = -k
                break
            if wp > n and wn > n:
                break

        # Check Franklin map involution on this set
        unpaired = []
        for p in dist_parts:
            mapped = franklin_map(p)
            if mapped is None:
                unpaired.append(p)
            else:
                double_mapped = franklin_map(mapped)
                assert double_mapped == p, f"Involution failed for {p} -> {mapped} -> {double_mapped}"
                assert sum(mapped) == n, f"Sum changed: {p} ({sum(p)}) -> {mapped} ({sum(mapped)})"
                assert len(mapped) % 2 != len(p) % 2, f"Parity did not change: {p} -> {mapped}"

        verified = (diff == expected_diff) and (len(unpaired) == (1 if expected_diff != 0 else 0))

        results.append({
            "n": n,
            "total_distinct": len(dist_parts),
            "p_e": len(even_parts),
            "p_o": len(odd_parts),
            "difference": diff,
            "expected_diff": expected_diff,
            "pentagonal_k": expected_k,
            "unpaired": unpaired,
            "verified": verified,
        })
    return results
