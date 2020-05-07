import functools


class ValidateMethod:
    def __init__(self, *, valid_methods):
        self.valid_methods = valid_methods

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            method = kwargs["method"]
            if method not in self.valid_methods:
                raise Exception(f'Invalid method "{method}"')
            return func(*args, **kwargs)

        return wrapper


validate_method = ValidateMethod
