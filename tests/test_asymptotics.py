"""
tests/test_asymptotics.py
Tests for partition_core.asymptotics (Hardy-Ramanujan approximation).
Reference: Andrews, The Theory of Partitions, Chapter 5, Theorem 5.1.
"""
from __future__ import annotations
import math
import pytest
from partition_core.enumeration import partition_count, partition_count_table
from partition_core.asymptotics import (
    hardy_ramanujan_approx,
    relative_error,
    growth_table,
)


def test_asymptotics_edge_cases():
    assert hardy_ramanujan_approx(0) == 1.0
    assert hardy_ramanujan_approx(-5) == 0.0
    assert relative_error(0, 5.0) == 0.0
    assert relative_error(100, 100.0) == 0.0


def test_asymptotics_known_values():
    # Andrews Ch. 5:
    # p(10) = 42, approx ~ 48.10
    approx_10 = hardy_ramanujan_approx(10)
    assert 48.0 < approx_10 < 49.0
    assert relative_error(42, approx_10) < 15.0  # ~14.5%

    # p(100) = 190569292, approx ~ 199280893 (~4.57%)
    p100 = partition_count(100)
    approx_100 = hardy_ramanujan_approx(100)
    err_100 = relative_error(p100, approx_100)
    assert err_100 < 5.0

    # p(200) = 3972999029388, error < 3.5%
    p200 = partition_count(200)
    approx_200 = hardy_ramanujan_approx(200)
    err_200 = relative_error(p200, approx_200)
    assert err_200 < 3.5


def test_asymptotic_relative_error_decreases():
    # As n grows (20, 50, 100, 200), relative error must strictly decrease
    ns = [20, 50, 100, 200]
    errors = [relative_error(partition_count(n), hardy_ramanujan_approx(n)) for n in ns]
    for i in range(len(errors) - 1):
        assert errors[i] > errors[i + 1], f"Error not decreasing between n={ns[i]} and n={ns[i+1]}"


def test_growth_table():
    table = partition_count_table(20)
    rows = growth_table(20, table)
    assert len(rows) == 21
    assert rows[0]["n"] == 0
    assert rows[20]["n"] == 20
    assert rows[20]["exact"] == partition_count(20)
    assert rows[20]["rel_error_pct"] == relative_error(partition_count(20), hardy_ramanujan_approx(20))
