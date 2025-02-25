from functools import wraps
from typing import Callable

def validate_verbose(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        try:
            verbose = kwargs.get('verbose')
            if verbose is not None:
                if isinstance(verbose, str):
                    if verbose.lower() == 'true':
                        kwargs['verbose'] = True
                    elif verbose.lower() == 'false':
                        kwargs['verbose'] = False
                    else:
                        raise ValueError(
                            "The 'verbose' parameter must be a boolean. "
                            "Use True or False (case-sensitive)"
                        )
                elif not isinstance(verbose, bool):
                    raise TypeError(
                        "The 'verbose' parameter must be a boolean (True or False)"
                    )
            return func(*args, **kwargs)
        except NameError as e:
            var_name = str(e).split("'")[1]
            raise ValueError(
                f"Error: '{var_name}' is not defined. Did you mean {var_name.capitalize()}? " # noqa
                f"The 'verbose' parameter must be a boolean (True or False)"
            ) from None
    return wrapper
