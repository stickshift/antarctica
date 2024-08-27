from pathlib import Path
from textwrap import dedent

import antarctica as aa


def test_verify_empty_probes():
    #
    # Givens
    #

    # I created probes
    probes = aa.create_probes([
        {"probe_id": 0, "x": 5.0, "y": 10.0, "distance_expected": 1.0, "distance_expected_err": 0.05},
    ])

    #
    # Whens
    #

    # I filter out all the rows
    probes = probes[probes.index == 5]

    #
    # Thens
    #

    # probes should still be valid
    aa.verify_probes(probes)


def test_create_probes():
    #
    # Givens
    #

    # I generate rows with 1 probe
    rows = [
        {"probe_id": 0, "x": 5.0, "y": 10.0, "distance_expected": 1.0, "distance_expected_err": 0.05},
    ]

    #
    # Whens
    #

    # I create probes
    probes = aa.create_probes(rows)

    #
    # Thens
    #

    # probes should have 1 row
    assert len(probes) == 1

    # probe 0 should be at coordinates 5,10
    assert probes.loc[0].x == 5
    assert probes.loc[0].y == 10

    # probe 0 should have distance_expected of 1.0 w/ 0.05 error
    assert probes.loc[0].distance_expected == 1.0
    assert probes.loc[0].distance_expected_err == 0.05


def test_read_probes(tmp_path: Path):
    #
    # Givens
    #

    # Generate path
    path = tmp_path / aa.random_string()

    # I wrote csv with 1 probe
    path.write_text(
        dedent(
            """
            index,x,y,min_dist,min_dist_err
            0,5.0,10.0,1.0,0.05
            """
        )
    )

    #
    # Whens
    #

    # I load probes data
    probes = aa.create_probes(path)

    #
    # Thens
    #

    # probes should have 1 row
    assert len(probes) == 1

    # probe 0 should be at coordinates 5,10
    assert probes.loc[0].x == 5
    assert probes.loc[0].y == 10

    # probe 0 should have distance_expected of 1.0 w/ 0.05 error
    assert probes.loc[0].distance_expected == 1.0
    assert probes.loc[0].distance_expected_err == 0.05
