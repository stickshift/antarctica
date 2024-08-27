from typing import Sequence

from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib.pyplot import Axes
from pandas import DataFrame
import seaborn as sns

from ._utilities import default_arg

__all__ = [
    "locations",
]

Color = tuple[float, float, float]


def locations(
    data: DataFrame,
    highlight: int | Sequence[int] | None = None,
    highlight_color: Color | None = None,
    ax: Axes | None = None,
):
    """Plot locations on grid."""
    palette = sns.color_palette()

    # Highlight
    highlight = default_arg(highlight, lambda: [])
    if isinstance(highlight, int):
        highlight = [highlight]

    # Colors
    default_color = palette[0]
    highlight_color = default_arg(highlight_color, lambda: palette[1])

    # Axes
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 6))

    # Plot diagonal to differentiate alternate locations
    sns.lineplot(x=[0, 20], y=[0, 20], c="gray", linestyle="--", ax=ax)

    for location_id, location in data.iterrows():
        # Highlight if location_id in highlight
        color = highlight_color if location_id in highlight else default_color

        # Expected distance
        c = patches.Circle((location.x, location.y), radius=location.distance_expected, alpha=0.2, color=color)
        ax.add_patch(c)

        # Probe location
        c = patches.Circle((location.x, location.y), radius=0.1, color=color)
        ax.add_patch(c)

    ax.set_xlim(-3, 23)
    ax.set_ylim(-3, 23)
