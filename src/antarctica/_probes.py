from hashlib import sha256
from pathlib import Path
from typing import get_origin

import pandas as pd
from pandas import DataFrame

from ._utilities import verify_schema

__all__ = [
    "checksum_solution",
    "create_probes",
    "verify_probes",
]

# Probes schema
_schema = {
    "x": float,
    "y": float,
    "distance_expected": float,
    "distance_expected_err": float,
}


ProbesData = list[dict]


def verify_probes(data: DataFrame):
    assert data.index.name == "probe_id"
    assert data.index.dtype == int
    verify_schema(data, _schema)


def _create_probes(data: ProbesData) -> DataFrame:
    """Create probes from sample data."""
    df = DataFrame(data)

    df = df.set_index("probe_id")

    # Verify outputs
    verify_probes(df)

    return df


def _read_probes(path: Path) -> DataFrame:
    """Read probes from csv."""
    # Read original source data
    df = pd.read_csv(path, index_col="index")

    # Rename index
    df.index.name = "probe_id"

    # Rename columns
    df = df.rename(
        {
            "min_dist": "distance_expected",
            "min_dist_err": "distance_expected_err",
        },
        axis=1,
    )

    # Verify outputs
    verify_probes(df)

    return df


def create_probes(data: ProbesData | Path) -> DataFrame:
    """Creates probes data frame from sample data or csv file."""
    if isinstance(data, get_origin(ProbesData)):
        return _create_probes(data)

    return _read_probes(data)


def checksum_solution(probes: DataFrame) -> str:
    """Calculate unique signature for probes data frame."""
    # Verify parameters
    verify_probes(probes)

    # Make sure probes is sorted
    probes = probes.sort_index()

    # Compute checksum of x column (rest of columns
    digest = sha256(probes.x.values.tobytes())

    return digest.hexdigest()
