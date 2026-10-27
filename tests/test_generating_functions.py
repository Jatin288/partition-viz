"""
tests/test_generating_functions.py
Tests for exact formal power series arithmetic and series-product identities.
Reference: Andrews, The Theory of Partitions, Chapters 1 and 2 (eq. 2.2.9, Corollary 1.2).
"""
from __future__ import annotations
import pytest
from partition_core.enumeration import partition_count, partitions_distinct, partitions_odd, generate_partitions
from partition_core.generating_functions import (
    poly_add,
    poly_mul,
    poly_div_by_1_minus_q_k,
    poly_mul_by_1_minus_q_k,
    poly_mul_by_1_plus_q_k,
    expand_euler_product,
    expand_partition_gf,
    expand_distinct_partitions_gf,
    expand_odd_partitions_gf,
    expand_durfee_square_series,
    durfee_decomposition,
)


def test_polynomial_basic_arithmetic():
    # (1 - q)(1 + q) = 1 - q^2
    p1 = [1, -1]
    p2 = [1, 1]
    p_prod = poly_mul(p1, p2)
    assert p_prod == [1, 0, -1]

    # (1 + 2q) + (3 - q + 4q^2) = 4 + q + 4q^2
    p_sum = poly_add([1, 2], [3, -1, 4])
    assert p_sum == [4, 1, 4]


def test_euler_product_matches_pentagonal_numbers():
    # Expand prod_{k=1}^20 (1 - q^k) mod q^21
    # Coefficients at exponents:
    # 0: +1
    # 1: -1, 2: -1
    # 5: +1, 7: +1
    # 12: -1, 15: -1
    # all others 0
    coeffs = expand_euler_product(num_factors=20, max_deg=20)
    expected_nonzeros = {
        0: 1,
        1: -1,
        2: -1,
        5: 1,
        7: 1,
        12: -1,
        15: -1,
    }
    for deg in range(21):
        expected = expected_nonzeros.get(deg, 0)
        assert coeffs[deg] == expected, f"Mismatch at degree {deg}: got {coeffs[deg]}, expected {expected}"


def test_partition_gf_matches_exact_p_n():
    # Expand prod_{k=1}^25 (1/(1-q^k)) mod q^21
    coeffs = expand_partition_gf(num_factors=25, max_deg=20)
    for n in range(21):
        assert coeffs[n] == partition_count(n), f"p({n}) mismatch: got {coeffs[n]}, expected {partition_count(n)}"


def test_euler_odd_distinct_identity_algebraic():
    # Andrews Corollary 1.2:
    # prod (1 + q^k) == prod 1 / (1 - q^(2k-1))
    max_deg = 25
    distinct_coeffs = expand_distinct_partitions_gf(num_factors=max_deg, max_deg=max_deg)
    odd_coeffs = expand_odd_partitions_gf(num_factors=max_deg, max_deg=max_deg)

    for n in range(max_deg + 1):
        assert distinct_coeffs[n] == odd_coeffs[n], f"Euler odd-distinct mismatch at n={n}"
        assert distinct_coeffs[n] == len(partitions_distinct(n))
        assert odd_coeffs[n] == len(partitions_odd(n))


def test_durfee_square_series_matches_p_n():
    """
    Andrews eq. (2.2.9), p. 28:
    sum_{d=0}^inf q^(d^2) / (q; q)_d^2 == sum_{n=0}^inf p(n) q^n
    """
    max_deg = 25
    # Since floor(sqrt(25)) = 5, summing d up to 5 is sufficient for degree 25
    durfee_coeffs = expand_durfee_square_series(max_d=5, max_deg=max_deg)
    for n in range(max_deg + 1):
        assert durfee_coeffs[n] == partition_count(n), (
            f"Durfee square series mismatch at n={n}: "
            f"got {durfee_coeffs[n]}, expected {partition_count(n)}"
        )


def test_durfee_decomposition_invariants():
    # Test on a large variety of partitions
    for n in range(1, 20):
        for lam in generate_partitions(n):
            res = durfee_decomposition(lam)
            assert res["verified"] is True
            d = res["d"]
            lambda_R = res["lambda_R"]
            lambda_B = res["lambda_B"]

            # Invariants:
            # lambda_R has at most d parts
            assert len(lambda_R) <= d
            # lambda_B has largest part <= d
            if lambda_B:
                assert lambda_B[0] <= d
            # Total sum reconstructed
            assert d * d + sum(lambda_R) + sum(lambda_B) == n
