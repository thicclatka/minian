Command-line tools
==================

MiniAn registers several console scripts in ``pyproject.toml`` (``[project.scripts]``). From a clone, run them with ``uv run <command>``; if MiniAn is installed in an active environment or via ``uv tool install``, use the command name directly.

You can also invoke modules as ``uv run python -m minian.pipelines.cnmf_process``, ``python -m minian.pipelines.cross_reg``, or ``python -m minian.install`` (same entry points as ``minian-pipeline``, ``minian-cross-reg``, and ``minian-install``).

``minian-pipeline``
-------------------

Headless CNMF pipeline with a local Dask cluster (``minian.pipelines.cnmf_process``).

.. code-block:: text

   $ uv run minian-pipeline -h
   usage: minian-pipeline [-h] [-d DATA] [-c PATH] [--worker-cpu-ratio RATIO]

   Run minian headless pipeline with a Dask LocalCluster.

   options:
     -h, --help            show this help message and exit
     -d DATA, --data DATA  Directory containing input videos (absolutized). Default: "." (current working directory).
     -c PATH, --config PATH
                           Pipeline JSON (see PipelineConfig). Default: minian_config.json in the current working directory if present; else built-in defaults (those defaults are written to <data>/minian_config.json at run start).
     --worker-cpu-ratio RATIO
                           When MINIAN_NWORKERS is unset: fraction of (logical CPUs − reserve) used as LocalCluster n_workers. If omitted, use MINIAN_WORKER_CPU_RATIO env or 2/3.

``minian-cross-reg``
--------------------

Cross-session registration over session folders containing ``minian.nc`` (``minian.pipelines.cross_reg``).

.. code-block:: text

   $ uv run minian-cross-reg -h
   usage: minian-cross-reg [-h] [-d DATA] [--param-dist PIXELS]

   Cross-register Minian outputs across sessions (writes mappings.pkl, cents.pkl,
   shiftds.nc under the data directory).

   options:
     -h, --help            show this help message and exit
     -d DATA, --data DATA  Directory containing session subfolders with minian
                           results (e.g. session1/minian.nc). Default: "."
     --param-dist PIXELS   Keep only cell pairs whose centroid Euclidean distance
                           (height/width coordinates) is strictly less than this
                           value in pixels (default: 5).

``minian-pipeline-defaults``
----------------------------

Writes the default :class:`minian.config.PipelineConfig` as JSON (``minian.config:main``)—for editing, diffing, or checking in next to a dataset. Output filename is ``minian_config.json`` (see ``minian.constants.MINIAN_CONFIG_FILENAME``).

.. code-block:: text

   $ uv run minian-pipeline-defaults -h
   usage: minian-pipeline-defaults [-h] [--dest DIR] [--stdout] [--resolve-paths]
                                   [--include-resolved-workers]

   Write default :class:`PipelineConfig` as JSON (for notebooks / pipeline drivers).

   options:
     -h, --help            show this help message and exit
     --dest DIR, -d DIR    Directory where minian_config.json is written (created if needed). Default: current directory. Use --stdout instead of creating a file.
     --stdout              Print JSON to stdout instead of writing the file.
     --resolve-paths       Use absolute intpath and param_save_minian['dpath'] (if set) before export.
     --include-resolved-workers
                           Add resolved_n_workers (env MINIAN_NWORKERS or CPU-based).

``minian-install``
------------------

Downloads notebooks and/or demo assets from GitHub into ``--dest`` (``minian.install``).

.. code-block:: text

   $ uv run minian-install -h
   usage: minian-install [-h] [--notebooks] [--demo] [-v V] [--dest DIR]

   options:
     -h, --help          show this help message and exit
     --notebooks         Installs the notebooks
     --demo              Installs the demo data
     -v V                Git repo branch or tag name, default 2.0.0
     --dest DIR, -d DIR  Directory to download into (default: current working directory)

Pipeline environment variables
-------------------------------

These are read by the headless CNMF driver (``minian-pipeline``), tests, or logging—not by ``minian-cross-reg``, which only uses CLI flags. Defaults and parsing live in :mod:`minian.config`.

* **MINIAN_NWORKERS** — If set to a positive integer, used as ``LocalCluster(n_workers=...)``. When unset, worker count is derived from CPUs (see **MINIAN_WORKER_CPU_RATIO**); that path requires the ``minian_rs`` extension.
* **MINIAN_WORKER_CPU_RATIO** — Float in ``(0, 1]``, used only when **MINIAN_NWORKERS** is unset. Clamped to a valid range; if unset or invalid, defaults to ``2/3``.
* **MINIAN_WORKER_MEMORY** — Dask worker memory limit string (default ``2GB``).
* **MINIAN_THREADS_PER_WORKER** — Integer threads per Dask worker (default ``2``).
* **MINIAN_CHUNK_MB** — Target chunk size in megabytes for pipeline I/O (default ``200``).
* **MINIAN_LOG_LEVEL** — Log level for CLI entrypoints that configure logging (default ``INFO``).
* **NO_COLOR** — When non-empty, log output skips ANSI colors on terminals (`no-color.org <https://no-color.org/>`_).

During a pipeline run, **MINIAN_INTERMEDIATE** is set to the configured intermediate directory (under ``--data`` by default); notebook flows may set it explicitly. You normally do not need to export it yourself.

See also :doc:`install`, :doc:`../pipeline/index`, and :doc:`../cross_reg/index`.
