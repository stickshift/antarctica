from typing import Mapping, Set

import numpy as np
from pandas import DataFrame

from ._locations import verify_locations
from ._probes import verify_probes
from ._utilities import default_arg, verify_schema

__all__ = [
    "create_neighbors",
    "neighbor_graph",
    "neighbor_graph_probes",
    "score_probes",
    "verify_neighbors",
]

# Neighbors schema
_schema = {
    "location_id": int,
    "probe_id": int,
    "distance_actual": float,
    "distance_actual_err": float,
    "distance_norm_err": float,
}

NeighborGraph = Mapping[int, int]


def verify_neighbors(data: DataFrame):
    assert data.index.name == "neighbor_id"
    verify_schema(data, _schema)


def create_neighbors(locations: DataFrame, *, location_id: int) -> DataFrame:
    """Calculate distance to all candidate neighbor locations."""
    # Verify parameters
    verify_locations(locations)

    # Look up location
    location = locations.loc[location_id]

    # Look up all locations for other probes
    df = locations[locations.probe_id != location.probe_id]

    # Copy on write
    df = df.copy()

    # Calculate distance_actual
    df["distance_actual"] = np.sqrt((df.x - location.x) ** 2 + (df.y - location.y) ** 2)

    # Calculate distance_actual_err
    df["distance_actual_err"] = np.abs(df.distance_actual - location.distance_expected)

    # Calculate distance_norm_err
    df["distance_norm_err"] = df.distance_actual_err / location.distance_expected_err

    # Reset index to move location_id to column
    df = df.reset_index()

    # Rename index
    df.index.name = "neighbor_id"

    # Verify outputs
    verify_neighbors(df)

    return df


def score_probes(probes: DataFrame) -> float:
    """Score the quality of probes solution by summing the normalized distance error.

    Note: Perfect score is 0.0. Higher the score, the worse it is.
    """
    # Verify parameters
    verify_probes(probes)

    # Convert probes into limited set of locations
    locations = probes.reset_index()
    locations.index.name = "location_id"
    verify_locations(locations)

    score = 0.0

    for location_id in locations.index:
        # Calculate location's neighbors
        neighbors = create_neighbors(locations, location_id=location_id)

        # Find nearest neighbor
        neighbor = neighbors.loc[neighbors.distance_actual.idxmin()]

        # Add normalized distance error to score
        score += neighbor.distance_norm_err

    return score


def neighbor_graph(
    locations: DataFrame,
    *,
    location_id: int,
    graph: Set[int] | None = None,
) -> tuple[NeighborGraph, DataFrame]:
    """Construct neighbor graph starting from specified location."""
    # Verify parameters
    verify_locations(locations)

    # Defaults
    graph = default_arg(graph, lambda: {})

    # Compare location with all possible neighbors
    neighbors = create_neighbors(locations, location_id=location_id)

    # If neighbors is empty, we're done
    if len(neighbors) == 0:
        return graph, locations

    # Choose neighbor that minimizes normalized distance error
    neighbor = neighbors.loc[neighbors.distance_norm_err.idxmin()]

    # Add edge from location_id to neighbor.location_id to graph
    graph[location_id] = neighbor.location_id

    # Remove alternate location for current probe from consideration
    location = locations.loc[location_id]
    exclude = locations[(locations.index != location_id) & (locations.probe_id == location.probe_id)]
    locations = locations[~locations.index.isin(exclude.index)]

    # If neighbor is already in graph, we're done
    if neighbor.location_id in graph:
        return graph, locations

    # Remove locations that were closer than neighbor from consideration
    exclude = neighbors[neighbors.distance_actual < neighbor.distance_actual]
    locations = locations[~locations.index.isin(exclude.location_id)]

    # Recursively search for neighbor's best neighbor
    return neighbor_graph(locations, location_id=neighbor.location_id, graph=graph)


def neighbor_graph_probes(locations: DataFrame, *, graph: NeighborGraph) -> Set[int]:
    """Identify set of probes represented by graph."""
    return set(locations[locations.index.isin(graph.keys())].probe_id)
