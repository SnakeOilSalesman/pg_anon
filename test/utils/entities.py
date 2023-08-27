import os
from typing import Callable


def get_factory(cast_to: type, env_name: str, default: str) -> Callable:
    """
    Get callable factory extracting env variable and casting its value to the given type.

    This function supposed to be used as lazy default factory for various test entities based
    on dataclasses.

    Example:
        from dataclasses import dataclass, field

        from this_exact_module import get_factory


        @dataclass
        class DatabaseCredentials:
            MY_STR_VALUE: str = field(
                default_factory=get_factory(str, 'MY_STR_VALUE', 'fancy_text')
            )
            MY_INT_VALUE: int = field(default_factory=get_factory(int, 'MY_INT_VALUE', '5432'))

    """

    def wrap():
        return cast_to(os.environ.get(env_name) or default)

    return wrap
