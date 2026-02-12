# analysis/theoretical_boundary_solver.py
# Sprint 8 Final — Theoretical Stability Boundary Solver
# Deterministic numeric solver for collapse inequality

import math


def theoretical_cost(D, c_a, k, p):
    """
    Theoretical cost model:

    c_a * D + k * (D + 1/p) * log(D + 1/p)
    """

    if D <= 0:
        return 0.0

    adjusted_depth = D + (1.0 / p)

    return (
        c_a * D
        + k * adjusted_depth * math.log(adjusted_depth)
    )


def solve_max_stable_depth(
    cap,
    c_a,
    k,
    p,
    max_search_depth=10000,
    resolution=1
):
    """
    Numerically finds maximum D such that:

        cost(D) < cap

    Deterministic linear sweep.
    """

    max_stable = 0

    for D in range(0, max_search_depth, resolution):

        cost = theoretical_cost(D, c_a, k, p)

        if cost < cap:
            max_stable = D
        else:
            break

    return max_stable


def generate_theoretical_boundary(
    caps,
    c_a,
    k,
    p,
    max_search_depth=10000
):
    """
    Generates boundary curve:
        cap → predicted max depth
    """

    boundary = {}

    for cap in caps:
        max_D = solve_max_stable_depth(
            cap=cap,
            c_a=c_a,
            k=k,
            p=p,
            max_search_depth=max_search_depth
        )

        boundary[cap] = max_D

    return boundary
