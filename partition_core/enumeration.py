# -*- coding: utf-8 -*-
"""
partition_core/enumeration.py
Core partition enumeration algorithms.
Reference: Andrews, The Theory of Partitions, Chapter 1.
  - Definition 1.1  : partition definition
  - Corollary 1.8   : Euler pentagonal recurrence for p(n)
"""
from __future__ import annotations
from functools import lru_cache

Partition = tuple[int, ...]


def generate_partitions(n: int) -> list[Partition]:
    """
    Return all partitions of n as tuples in non-increasing order.
    Listed in lexicographically decreasing order.

    Example:
        generate_partitions(4)
        -> [(4,), (3,1), (2,2), (2,1,1), (1,1,1,1)]
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if n == 0:
        return [()]
    result: list[Partition] = []
    _gen(n, n, [], result)
    return result


def _gen(rem: int, max_p: int, cur: list[int], res: list[Partition]) -> None:
    if rem == 0:
        res.append(tuple(cur))
        return
    for p in range(min(rem, max_p), 0, -1):
        cur.append(p)
        _gen(rem - p, p, cur, res)
        cur.pop()


def partition_count_table(N: int) -> list[int]:
    """
    Return p(0), p(1), ..., p(N) computed via Euler's pentagonal recurrence.
    Reference: Andrews, Corollary 1.8, p.12.

    The recurrence is:
        p(n) = sum_{m>=1} (-1)^{m+1} [ p(n - w(m)) + p(n - w(-m)) ]
    where w(m) = m(3m-1)/2 are the generalized pentagonal numbers.
    """
    if N < 0:
        raise ValueError(f"N must be non-negative, got {N}")
    p = [0] * (N + 1)
    p[0] = 1
    for n in range(1, N + 1):
        total = 0
        m = 1
        while True:
            wp = m * (3 * m - 1) // 2   # w(m)
            wn = m * (3 * m + 1) // 2   # w(-m)
            if wp > n:
                break
            sign = (-1) ** (m + 1)
            total += sign * p[n - wp]
            if wn <= n:
                total += sign * p[n - wn]
            m += 1
        p[n] = total
    return p


@lru_cache(maxsize=None)
def partition_count(n: int) -> int:
    """
    Return p(n) using the pentagonal recurrence, with memoization.
    Verified: p(100) = 190569292, p(200) = 3972999029388.
    """
    if n < 0:
        return 0
    if n == 0:
        return 1
    total = 0
    m = 1
    while True:
        wp = m * (3 * m - 1) // 2
        wn = m * (3 * m + 1) // 2
        if wp > n:
            break
        sign = (-1) ** (m + 1)
        total += sign * partition_count(n - wp)
        if wn <= n:
            total += sign * partition_count(n - wn)
        m += 1
    return total


def partitions_distinct(n: int) -> list[Partition]:
    """
    Return all partitions of n into strictly distinct parts.
    These are counted by p(D, n).
    Reference: Andrews, Definition 1.4 (the set D).
    """
    res: list[Partition] = []
    _gen_dist(n, n, [], res)
    return res


def _gen_dist(rem: int, max_p: int, cur: list[int], res: list[Partition]) -> None:
    if rem == 0:
        res.append(tuple(cur))
        return
    for p in range(min(rem, max_p), 0, -1):
        cur.append(p)
        _gen_dist(rem - p, p - 1, cur, res)
        cur.pop()


def partitions_odd(n: int) -> list[Partition]:
    """
    Return all partitions of n into odd parts.
    These are counted by p(O, n).
    Reference: Andrews, Definition 1.4 (the set O).

    Euler's theorem (Corollary 1.2): p(O,n) = p(D,n) for all n.
    """
    res: list[Partition] = []
    start = n if n % 2 == 1 else n - 1
    _gen_odd(n, start, [], res)
    return res


def _gen_odd(rem: int, max_p: int, cur: list[int], res: list[Partition]) -> None:
    if rem == 0:
        res.append(tuple(cur))
        return
    s = min(rem, max_p)
    if s % 2 == 0:
        s -= 1
    for p in range(s, 0, -2):
        cur.append(p)
        _gen_odd(rem - p, p, cur, res)
        cur.pop()


def partitions_at_most_m_parts(n: int, m: int) -> list[Partition]:
    """
    Return all partitions of n with at most m parts.
    Reference: Andrews, Theorem 1.4 (first set in the bijection).
    """
    res: list[Partition] = []
    _gen_bnd(n, n, m, [], res)
    return res


def _gen_bnd(rem: int, max_p: int, left: int,
             cur: list[int], res: list[Partition]) -> None:
    if rem == 0:
        res.append(tuple(cur))
        return
    if left == 0:
        return
    for p in range(min(rem, max_p), 0, -1):
        cur.append(p)
        _gen_bnd(rem - p, p, left - 1, cur, res)
        cur.pop()


def partitions_max_part(n: int, m: int) -> list[Partition]:
    """
    Return all partitions of n with largest part at most m.
    Reference: Andrews, Theorem 1.4 (second set in the bijection).
    """
    res: list[Partition] = []
    _gen(n, m, [], res)
    return res


def generalized_pentagonal_numbers(up_to: int) -> list[tuple[int, int, int]]:
    """
    Return list of (m, omega_m, sign) for all generalized pentagonal numbers
    omega_m = m(3m-1)/2 and omega_{-m} = m(3m+1)/2 that are <= up_to.

    sign = (-1)^{m+1}, used in Euler's pentagonal theorem (Corollary 1.7).
    """
    result = []
    m = 1
    while True:
        wp = m * (3 * m - 1) // 2
        wn = m * (3 * m + 1) // 2
        if wp > up_to:
            break
        sign = (-1) ** (m + 1)
        result.append((m, wp, sign))
        if wn <= up_to:
            result.append((-m, wn, sign))
        m += 1
    return result
