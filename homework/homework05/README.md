# Stage 05: Data Storage Layer

## Directory Structure
- `data/raw/`: Stores immutable raw landing files in human-readable CSV format.
- `data/processed/`: Stores optimized binary column-oriented Parquet files for analytical querying.

## Formats Used & Rationales
- **CSV**: Used for raw intake (`data/raw/`). Easy to inspect with standard tools, but loses native data types upon reading.
- **Parquet**: Used for processed analytical datasets (`data/processed/`). High compression ratio and perfectly preserves schema and columnar dtypes (e.g., `datetime64`).

## Environment-Driven IO
Environment variables configured in `.env` (`DATA_DIR_RAW` and `DATA_DIR_PROCESSED`) ensure portable paths across different systems without hardcoding absolute file paths.
