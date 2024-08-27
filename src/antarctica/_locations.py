import pandas as pd
from pandas import DataFrame

from ._probes import verify_probes
from ._utilities import verify_schema

__all__ = [
    "catalog_locations",
    "verify_locations",
]

_schema = {
    "probe_id": int,
    "x": float,
    "y": float,
    "distance_expected": float,
    "distance_expected_err": float,
}


def verify_locations(data: DataFrame):
    assert data.index.name == "location_id"
    assert data.index.dtype == int
    verify_schema(data, _schema)


def catalog_locations(probes: DataFrame) -> DataFrame:
    """Transform probes into locations by duplicating each row and swapping x, y coordinates."""
    # Verify parameters
    verify_probes(probes)

    # Start with existing probes indexed by row
    df = probes.reset_index()

    # Duplicate locations and swap x,y coordinates
    alternates = df.copy()
    alternates["x"] = df.y
    alternates["y"] = df.x
    df = pd.concat([df, alternates], ignore_index=True)

    # Rename index
    df.index.name = "location_id"

    # Verify outputs
    verify_locations(df)

    return df
