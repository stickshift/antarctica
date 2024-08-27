import antarctica as aa


def test_locations():
    #
    # Givens
    #

    # I generated data for 1 probe
    probes = aa.create_probes([
        {"probe_id": 0, "x": 5.0, "y": 10.0, "distance_expected": 1.0, "distance_expected_err": 0.05},
    ])

    #
    # Whens
    #

    # I catalog locations
    locations = aa.catalog_locations(probes)

    #
    # Thens
    #

    # locations should have 2 rows for probe 0
    df = locations[locations.probe_id == 0]
    assert len(df) == 2

    # probe 0 rows should have alternate coordinates
    assert df.loc[0].x == df.loc[1].y
    assert df.loc[0].y == df.loc[1].x

    # distance should be the same for both rows
    assert df.loc[0].distance_expected == df.loc[1].distance_expected
    assert df.loc[0].distance_expected_err == df.loc[1].distance_expected_err
