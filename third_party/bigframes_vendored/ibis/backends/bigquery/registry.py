# Contains code from https://github.com/ibis-project/ibis/blob/master/ibis/backends/bigquery/registry.py
"""Module to convert from Ibis expression to SQL string."""

import bigframes_vendored.ibis.expr.operations as vendored_ibis_ops
from ibis.backends.bigquery.registry import OPERATION_REGISTRY
import ibis.expr.operations.reductions as ibis_reductions


def _approx_quantiles(translator, op: vendored_ibis_ops.ApproximateMultiQuantile):
    arg = translator.translate(op.arg)
    num_bins = translator.translate(op.num_bins)
    return f"APPROX_QUANTILES({arg}, {num_bins})"


def _first_non_null_value(translator, op: vendored_ibis_ops.FirstNonNullValue):
    arg = translator.translate(op.arg)
    return f"FIRST_VALUE({arg} IGNORE NULLS)"


def _last_non_null_value(translator, op: vendored_ibis_ops.LastNonNullValue):
    arg = translator.translate(op.arg)
    return f"LAST_VALUE({arg} IGNORE NULLS)"


def _to_json_string(translator, op: vendored_ibis_ops.ToJsonString):
    arg = translator.translate(op.arg)
    return f"TO_JSON_STRING({arg})"


def _generate_array(translator, op: vendored_ibis_ops.GenerateArray):
    arg = translator.translate(op.arg)
    return f"GENERATE_ARRAY(0, {arg})"


def _quantile(translator, op: ibis_reductions.Quantile):
    arg = translator.translate(op.arg)
    quantile = translator.translate(op.quantile)
    return f"PERCENTILE_CONT({arg}, {quantile})"


patched_ops = {
    vendored_ibis_ops.ApproximateMultiQuantile: _approx_quantiles,  # type:ignore
    vendored_ibis_ops.FirstNonNullValue: _first_non_null_value,  # type:ignore
    vendored_ibis_ops.LastNonNullValue: _last_non_null_value,  # type:ignore
    vendored_ibis_ops.ToJsonString: _to_json_string,  # type:ignore
    vendored_ibis_ops.GenerateArray: _generate_array,  # type:ignore
    ibis_reductions.Quantile: _quantile,  # type:ignore
}

OPERATION_REGISTRY.update(patched_ops)
