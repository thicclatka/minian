"""Legacy import path for the CNMF process pipeline.

Prefer :mod:`minian.pipelines.cnmf_process` or ``python -m minian.pipelines.cnmf_process``.
"""

from minian.pipelines.cnmf_process import main, parse_pipeline_argv, run_pipeline

__all__ = ["main", "parse_pipeline_argv", "run_pipeline"]
