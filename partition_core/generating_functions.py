# -*- coding: utf-8 -*-
"""
partition_core/generating_functions.py
Exact formal power series arithmetic and series-product identities for partition theory.
Reference: Andrews, The Theory of Partitions, Chapters 1 and 2.
  - Section 1.2: Generating functions for partitions, Euler's odd-distinct theorem (Corollary 1.2)
  - Section 2.2: Infinite series expansions, Durfee square identity (eq. 2.2.9, p. 28):
      sum_{n=0}^inf p(n) q^n = sum_{d=0}^inf q^{d^2} / ( (1-q)^2 (1-q^2)^2 ... (1-q^d)^2 )
"""
from __future__ import annotations
import math
from partition_core.enumeration import Partition


def poly_add(p1: list[int], p2: list[int]) -> list[int]:
    """Return p1(q) + p2(q) with exact integer arithmetic."""
    length = max(len(p1), len(p2))
    res = [0] * length
    for i in range(len(p1)):
        res[i] += p1[i]
    for i in range(len(p2)):
        res[i] += p2[i]
    return res


def poly_mul(p1: list[int], p2: list[int], max_deg: int | None = None) -> list[int]:
    """Return p1(q) * p2(q) mod q^(max_deg + 1) with exact integer arithmetic."""
    if not p1 or not p2:
        return [0]
    out_deg = len(p1) + len(p2) - 2
    if max_deg is not None:
        out_deg = min(out_deg, max_deg)
    res = [0] * (out_deg + 1)
    for i, a in enumerate(p1):
        if a == 0:
            continue
        for j, b in enumerate(p2):
            if i + j <= out_deg:
                res[i + j] += a * b
    return res


def poly_div_by_1_minus_q_k(poly: list[int], k: int, max_deg: int) -> list[int]:
    """
    Multiply poly by 1 / (1 - q^k) mod q^(max_deg + 1).
    Since 1/(1 - q^k) = 1 + q^k + q^(2k) + ..., this is equivalent to
    the recurrence: out[i] = poly[i] + (out[i - k] if i >= k else 0).
    """
    deg = max_deg
    res = [0] * (deg + 1)
    for i in range(min(len(poly), deg + 1)):
        res[i] = poly[i]
    for i in range(k, deg + 1):
        res[i] += res[i - k]
    return res


def poly_mul_by_1_minus_q_k(poly: list[int], k: int, max_deg: int) -> list[int]:
    """
    Multiply poly by (1 - q^k) mod q^(max_deg + 1).
    out[i] = poly[i] - (poly[i - k] if i >= k else 0).
    """
    deg = min(len(poly) + k, max_deg)
    res = [0] * (deg + 1)
    for i in range(min(len(poly), deg + 1)):
        res[i] += poly[i]
        if i + k <= deg:
            res[i + k] -= poly[i]
    return res


def poly_mul_by_1_plus_q_k(poly: list[int], k: int, max_deg: int) -> list[int]:
    """
    Multiply poly by (1 + q^k) mod q^(max_deg + 1).
    out[i] = poly[i] + (poly[i - k] if i >= k else 0).
    """
    deg = min(len(poly) + k, max_deg)
    res = [0] * (deg + 1)
    for i in range(min(len(poly), deg + 1)):
        res[i] += poly[i]
        if i + k <= deg:
            res[i + k] += poly[i]
    return res


def expand_euler_product(num_factors: int, max_deg: int) -> list[int]:
    """
    Expand prod_{k=1}^M (1 - q^k) mod q^(max_deg + 1).
    By Euler's pentagonal theorem, coefficients are in {-1, 0, 1} for exponents <= M.
    """
    poly = [1]
    for k in range(1, num_factors + 1):
        poly = poly_mul_by_1_minus_q_k(poly, k, max_deg)
    # Pad to max_deg + 1
    if len(poly) < max_deg + 1:
        poly.extend([0] * (max_deg + 1 - len(poly)))
    return poly[: max_deg + 1]


def expand_partition_gf(num_factors: int, max_deg: int) -> list[int]:
    """
    Expand prod_{k=1}^M (1 / (1 - q^k)) mod q^(max_deg + 1).
    For M >= max_deg, coefficient of q^n is the exact partition number p(n).
    """
    poly = [1] + [0] * max_deg
    for k in range(1, num_factors + 1):
        poly = poly_div_by_1_minus_q_k(poly, k, max_deg)
    return poly[: max_deg + 1]


def expand_distinct_partitions_gf(num_factors: int, max_deg: int) -> list[int]:
    """
    Expand prod_{k=1}^M (1 + q^k) mod q^(max_deg + 1).
    For M >= max_deg, coefficient of q^n is exact number of partitions of n
    into distinct parts: p(D, n).
    """
    poly = [1]
    for k in range(1, num_factors + 1):
        poly = poly_mul_by_1_plus_q_k(poly, k, max_deg)
    if len(poly) < max_deg + 1:
        poly.extend([0] * (max_deg + 1 - len(poly)))
    return poly[: max_deg + 1]


def expand_odd_partitions_gf(num_factors: int, max_deg: int) -> list[int]:
    """
    Expand prod_{k=1}^M (1 / (1 - q^(2k - 1))) mod q^(max_deg + 1).
    For 2M - 1 >= max_deg, coefficient of q^n is exact number of partitions of n
    into odd parts: p(O, n).
    Euler's Theorem (Corollary 1.2): p(D, n) == p(O, n) for all n.
    """
    poly = [1] + [0] * max_deg
    for k in range(1, num_factors + 1):
        odd_k = 2 * k - 1
        poly = poly_div_by_1_minus_q_k(poly, odd_k, max_deg)
    return poly[: max_deg + 1]


def expand_durfee_square_series(max_d: int, max_deg: int) -> list[int]:
    """
    Expand the Durfee square series identity (Andrews, eq. 2.2.9, p. 28):
        sum_{d=0}^M  q^(d^2) / ( prod_{j=1}^d (1 - q^j)^2 )  mod q^(max_deg + 1).
    For M >= floor(sqrt(max_deg)), this polynomial matches sum_{n=0}^max_deg p(n) q^n exactly!
    """
    total = [0] * (max_deg + 1)
    for d in range(0, max_d + 1):
        d_sq = d * d
        if d_sq > max_deg:
            break
        # Term numerator: q^(d^2)
        term = [0] * (max_deg + 1)
        term[d_sq] = 1
        # Denominator: prod_{j=1}^d (1 - q^j)^2
        # Apply 1/(1 - q^j) twice for each j in 1..d
        for j in range(1, d + 1):
            term = poly_div_by_1_minus_q_k(term, j, max_deg)
            term = poly_div_by_1_minus_q_k(term, j, max_deg)
        total = poly_add(total, term)
    return total[: max_deg + 1]


def durfee_decomposition(lam: Partition) -> dict:
    """
    Combinatorially decompose partition lambda according to its Durfee square
    of side d, providing the geometric proof of Andrews's eq. 2.2.9:
      - Durfee square: d x d dots (size d^2)
      - Right partition lambda_R: dots to the right of the square (at most d parts)
      - Bottom partition lambda_B: dots below the square (parts at most d)
    Invariant:
      sum(lambda) == d^2 + sum(lambda_R) + sum(lambda_B)
    """
    if not lam:
        return {
            "lam": (), "n": 0, "d": 0, "d_sq": 0,
            "lambda_R": (), "sum_R": 0, "lambda_B": (), "sum_B": 0,
            "verified": True,
        }

    # d is largest i such that lambda[i - 1] >= i
    d = sum(1 for i, p in enumerate(lam, 1) if p >= i)
    d_sq = d * d

    # lambda_R: rows 0 .. d-1, stripped of the first d columns
    parts_R = [lam[i] - d for i in range(d) if lam[i] > d]
    lambda_R = tuple(parts_R)

    # lambda_B: rows from d onwards (each part <= d by definition of Durfee square)
    parts_B = [lam[i] for i in range(d, len(lam))]
    lambda_B = tuple(parts_B)

    sum_R = sum(lambda_R)
    sum_B = sum(lambda_B)
    total_reconstructed = d_sq + sum_R + sum_B

    return {
        "lam": lam,
        "n": sum(lam),
        "d": d,
        "d_sq": d_sq,
        "lambda_R": lambda_R,
        "sum_R": sum_R,
        "lambda_B": lambda_B,
        "sum_B": sum_B,
        "verified": total_reconstructed == sum(lam),
    }
