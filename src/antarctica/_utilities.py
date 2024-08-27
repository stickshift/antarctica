from secrets import token_hex

from pandas import DataFrame

__all__ = [
    "default_arg",
    "random_string",
    "verify_schema",
]


def default_arg(x, default_factory):
    """Shorthand for if x is None: x = default_factory()."""
    if x is None:
        return default_factory()

    return x


def random_string(length: int | None = None) -> str:
    """Generate random string of specified length."""
    # Defaults
    length = default_arg(length, lambda: 8)

    return token_hex(length // 2 + 1)[0:length]


def verify_schema(data: DataFrame, schema: dict[str, type]):
    """Verifies data's columns matches expected schema."""
    for column_name, column_type in schema.items():
        # Check column name
        assert column_name in data.columns

        # Check types
        assert data[column_name].dtype == column_type
