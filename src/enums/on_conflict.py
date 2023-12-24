from enum import Enum


class OnConflict(Enum):
    """Enum for on conflict mode in postgres."""

    do_nothing = 'do_nothing'
    do_update = 'do_update'
