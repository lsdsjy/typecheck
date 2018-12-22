from inspect import signature
import collections


def typecheck(func):
    def check(arg, annotation):
        return isinstance(arg, annotation)

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
                    raise TypeError('Missing keyword argument "{}"'.format(spec.name))
            elif spec.kind == spec.VAR_POSITIONAL:
                if spec.annotation != spec.empty:
                    for arg in arg_it:
                        if not check(arg, spec.annotation):
                            raise TypeError('Wrong type of variable positional argument for '
                                            'parameter "{}", expected {}, got {}'
                                            .format(spec.name, spec.annotation, type(arg)))
                continue
            elif spec.kind == spec.VAR_KEYWORD:
                if spec.annotation != spec.empty and \
                   not all(check(arg, spec.annotation) for arg in kwargs.values()):
                    raise TypeError('Wrong type of variable keyword argument "{}", expected {}, got {}'
                                    .format(spec.name, spec.annotation, type(arg)))
                continue

            if spec.annotation != spec.empty \
               and not check(arg, spec.annotation):
                raise TypeError('Parameter "{}", expected {}, got {}.'
                                .format(spec.name, spec.annotation, type(arg)))

        return func(*args, **kwargs_)
    return wrapper
