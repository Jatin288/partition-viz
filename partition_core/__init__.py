"""
partition_core — Mathematical engine for PartitionViz.
Implements core partition algorithms from Andrews's Theory of Partitions.
"""
from .enumeration import (
    generate_partitions,
    partition_count,
    partition_count_table,
    partitions_distinct,
    partitions_odd,
    partitions_at_most_m_parts,
    partitions_max_part,
    generalized_pentagonal_numbers,
    Partition,
)
from .conjugation import (
    conjugate,
    ferrers_matrix,
    conjugation_animation_frames,
    verify_theorem_1_4,
)
from .asymptotics import (
    hardy_ramanujan_approx,
    relative_error,
    growth_table,
)
from .franklin import (
    slope_length,
    base_length,
    is_exceptional,
    franklin_map,
    franklin_details,
    verify_euler_pentagonal,
)
from .generating_functions import (
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
    durfee_completeness_bound,
    expand_euler_first_identity,
    expand_euler_second_identity,
)

__all__ = [
    "Partition",
    "generate_partitions",
    "partition_count",
    "partition_count_table",
    "partitions_distinct",
    "partitions_odd",
    "partitions_at_most_m_parts",
    "partitions_max_part",
    "generalized_pentagonal_numbers",
    "conjugate",
    "ferrers_matrix",
    "conjugation_animation_frames",
    "verify_theorem_1_4",
    "hardy_ramanujan_approx",
    "relative_error",
    "growth_table",
    "slope_length",
    "base_length",
    "is_exceptional",
    "franklin_map",
    "franklin_details",
    "verify_euler_pentagonal",
    "poly_add",
    "poly_mul",
    "poly_div_by_1_minus_q_k",
    "poly_mul_by_1_minus_q_k",
    "poly_mul_by_1_plus_q_k",
    "expand_euler_product",
    "expand_partition_gf",
    "expand_distinct_partitions_gf",
    "expand_odd_partitions_gf",
    "expand_durfee_square_series",
    "durfee_decomposition",
    "durfee_completeness_bound",
    "expand_euler_first_identity",
    "expand_euler_second_identity",
]


