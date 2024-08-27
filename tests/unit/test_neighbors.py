import antarctica as aa


def test_neighbors():
    #
    # Givens
    #

    # I generated data for 2 probes 5 miles apart
    probes = aa.create_probes([
        {"probe_id": 0, "x": 0.0, "y": 0.0, "distance_expected": 9.0, "distance_expected_err": 0.5},
        {"probe_id": 1, "x": 5.0, "y": 0.0, "distance_expected": 1.0, "distance_expected_err": 0.05},
        {"probe_id": 2, "x": 13.0, "y": 0.0, "distance_expected": 1.0, "distance_expected_err": 0.05},
    ])

    # I transformed probes into locations
    locations = aa.catalog_locations(probes)

    #
    # Whens
    #

    # I calculate neighbors for location 0
    neighbors = aa.create_neighbors(locations, location_id=0)

    #
    # Thens
    #

    # neighbors should have 4 rows (1 for each location for probes 1 and 2)
    assert len(neighbors) == 4

    # All neighbors should be for probes 1 and 2
    for _, neighbor in neighbors.iterrows():
        assert neighbor.probe_id in {1, 2}

    # All neighbors for probe 1 should be 5 miles away since (5, 0) and (0, 5) are same distance from (0, 0)
    for _, neighbor in neighbors[neighbors.probe_id == 1].iterrows():
        assert neighbor.distance_actual == 5.0

    # All neighbors for probe 1 should have distance_actual_err of 4, distance_norm_err of 8
    for _, neighbor in neighbors[neighbors.probe_id == 1].iterrows():
        assert neighbor.distance_actual_err == 4.0
        assert neighbor.distance_norm_err == 8.0

    # All neighbors for probe 2 should be 13 miles away since (13, 0) and (0, 13) are same distance from (0, 0)
    for _, neighbor in neighbors[neighbors.probe_id == 2].iterrows():
        assert neighbor.distance_actual == 13.0

    # All neighbors for probe 2 should have distance_actual_err of 4, distance_norm_err of 8
    for _, neighbor in neighbors[neighbors.probe_id == 2].iterrows():
        assert neighbor.distance_actual_err == 4.0
        assert neighbor.distance_norm_err == 8.0


def test_score_probes():
    #
    # Whens
    #

    # I generated data for 3 probes exactly where they're supposed to be
    probes = aa.create_probes([
        {"probe_id": 0, "x": 0.0, "y": 0.0, "distance_expected": 2.0, "distance_expected_err": 0.05},
        {"probe_id": 1, "x": 2.0, "y": 0.0, "distance_expected": 1.0, "distance_expected_err": 0.05},
        {"probe_id": 2, "x": 3.0, "y": 0.0, "distance_expected": 1.0, "distance_expected_err": 0.05},
    ])

    # I calculate probes score
    score = aa.score_probes(probes)

    #
    # Thens
    #

    # score should be perfect 0
    assert score == 0.0

    #
    # Whens
    #

    # I generated data for 3 probes w/ each one 1 std off from expected location
    probes = aa.create_probes([
        {"probe_id": 0, "x": 0.0, "y": 0.0, "distance_expected": 2.0, "distance_expected_err": 0.5},
        {"probe_id": 1, "x": 2.5, "y": 0.0, "distance_expected": 1.0, "distance_expected_err": 0.5},
        {"probe_id": 2, "x": 4.0, "y": 0.0, "distance_expected": 1.0, "distance_expected_err": 0.5},
    ])

    # I calculate probes score
    score = aa.score_probes(probes)

    #
    # Thens
    #

    # score should be 3
    assert score == 3.0


def test_neighbor_graph():
    #
    # Givens
    #

    # I generated data for 4 probes in a line along x axis
    #
    #   p0 -- p1 --- p2 ---- p3
    #
    #   p2 is best match for p0
    #   p1 is best match for p2, but it's ruled out, so p3 is next best candidate
    #

    probes = aa.create_probes([
        {"probe_id": 0, "x": 0.0, "y": 0.0, "distance_expected": 5.0, "distance_expected_err": 0.05},
        {"probe_id": 1, "x": 2.0, "y": 0.0, "distance_expected": 1.0, "distance_expected_err": 0.05},
        {"probe_id": 2, "x": 5.0, "y": 0.0, "distance_expected": 3.0, "distance_expected_err": 0.05},
        {"probe_id": 3, "x": 9.0, "y": 0.0, "distance_expected": 1.0, "distance_expected_err": 0.05},
    ])

    # I transformed probes into locations
    locations = aa.catalog_locations(probes)

    #
    # Whens
    #

    # I calculate neighbor_graph for location 0
    graph, candidates = aa.neighbor_graph(locations, location_id=0)

    #
    # Thens
    #

    # graph locations should be {0, 2, 3}
    assert graph.keys() == {0, 2, 3}

    # graph should have edge from 0 -> 2
    assert graph[0] == 2

    # graph should have edge from 2 -> 3
    assert graph[2] == 3

    # graph should have edge from 3 -> 2
    assert graph[3] == 2

    # Remaining candidates should only have 1 location for each of the selected probes
    assert len(candidates[candidates.probe_id == 0]) == 1
    assert len(candidates[candidates.probe_id == 2]) == 1
    assert len(candidates[candidates.probe_id == 3]) == 1

    # Remaining candidates should not include location 1 since it was discarded
    assert len(candidates[candidates.index == 1]) == 0
