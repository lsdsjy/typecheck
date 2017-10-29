from inspect import signature


def typecheck(func):
    def wrapper(*args, **kwargs_):
        sg = signature(func)
        kwargs = kwargs_.copy()

        arg_it = iter(args)
        for spec in sg.parameters.values():
            if spec.kind == spec.POSITIONAL_OR_KEYWORD:
                try:
                    arg = next(arg_it)
                except StopIteration:
                    if spec.name in kwargs:
                        arg = kwargs[spec.name]
                    else:
                        raise TypeError('Incorrect number of positional arguments.')
            elif spec.kind == spec.KEYWORD_ONLY:
                if spec.name in kwargs:
                    arg = kwargs[spec.name]
                    del kwargs[spec.name]
                else:
                    raise TypeError('Missing keyword argument {}'.format(spec.name))
            elif spec.kind == spec.VAR_POSITIONAL:
                if spec.annotation != spec.empty:
                    for arg in arg_it:
                        if type(arg) != spec.annotation:
                            raise TypeError('Wrong type of variable positional argument, expected {}, got {}'
                                            .format(spec.annotation, type(arg)))
                continue
            elif spec.kind == spec.VAR_KEYWORD:
                if spec.annotation != spec.empty and \
                   any(type(arg) != spec.annotation for arg in kwargs.values()):
                    raise TypeError('Wrong type of variable keyword argument {}, expected {}, got {}'
                                    .format(spec.name, spec.annotation, type(arg)))
                continue

            if spec.annotation != spec.empty \
               and type(arg) != spec.annotation:
                raise TypeError('Parameter \'{}\', expected {}, got {}.'
                                .format(spec.name, spec.annotation, type(arg)))

        return func(*args, **kwargs_)
    return wrapper


# Example
@typecheck
def test(z: str, *x: str, y: int, **u: float):
    print(z, x, y, u)


# test(1, 's', y=3, u=4)  # Wrong type of positional argument z
# test('s', 2, y=3, u=4)  # Wrong type of variable positional arguments *x
# test('s', 's', z=3, u=4)  # Missing keyword argument y
# test('s', 's', y=3, t=1)  # Incorrect type of variable keyword arguments **u
