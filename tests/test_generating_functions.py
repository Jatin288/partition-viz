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


def test_durfee_completeness_bound_and_deficit():
    """
    Test the exact mathematical completeness threshold:
    When d_max < floor(sqrt(N)), coefficients are exact for n < (d_max + 1)^2
    and have a strict deficit at n = (d_max + 1)^2.
    """
    from partition_core.generating_functions import durfee_completeness_bound

    # With d_max = 2, bound = (2+1)^2 - 1 = 8.
    info = durfee_completeness_bound(max_d=2, max_deg=15)
    assert info["is_complete"] is False
    assert info["exact_up_to_degree"] == 8
    assert info["first_incomplete_degree"] == 9

    # Check series expansion matches p(n) up to n=8, and has deficit at n=9
    poly_d2 = expand_durfee_square_series(max_d=2, max_deg=15)
    for n in range(9):
        assert poly_d2[n] == partition_count(n), f"Mismatch at degree {n} for d_max=2"
    # At degree 9, partition (3, 3, 3) has Durfee side 3, so it is omitted from d <= 2!
    assert poly_d2[9] < partition_count(9), "Expected deficit at n=9 for d_max=2"


def test_q_binomial_euler_corollaries():
    """
    Test Andrews Theorem 2.1 limiting corollaries:
    - Corollary 2.2: sum q^n / (q; q)_n expands to p(n)
    - Corollary 2.3: sum q^(n(n+1)/2) / (q; q)_n expands to p(D, n)
    """
    from partition_core.generating_functions import expand_euler_first_identity, expand_euler_second_identity

    max_deg = 20
    # Corollary 2.2
    c22_coeffs = expand_euler_first_identity(max_n=max_deg, max_deg=max_deg)
    for n in range(max_deg + 1):
        assert c22_coeffs[n] == partition_count(n), f"Corollary 2.2 mismatch at degree {n}"

    # Corollary 2.3
    c23_coeffs = expand_euler_second_identity(max_n=10, max_deg=max_deg)
    for n in range(max_deg + 1):
        assert c23_coeffs[n] == len(partitions_distinct(n)), f"Corollary 2.3 mismatch at degree {n}"

