def curry_explicit(function_to_curry, function_arity, given_args=None):
    if given_args is None:
        given_args = []
    if function_arity < 0:
        raise ValueError(
            f"wrong curry arity. Arity should be >= 0, while {function_arity} was given"
        )

    def curried_function(new_given_argument=None):
        if new_given_argument is None:
            new_given_argument = []
        if function_arity > 1:
            return curry_explicit(
                function_to_curry,
                function_arity - 1,
                given_args=given_args + [new_given_argument],
            )
        if function_arity == 0:
            return function_to_curry()
        return function_to_curry(*given_args, new_given_argument)

    return curried_function


def uncurry_explicit(function_to_uncurry, function_arity):
    def uncurried_function(*args):
        if function_arity != len(args):
            raise TypeError(
                f"uncurried function takes {function_arity} positional arguments, {len(args)} were given"
            )
        if function_arity == 0:
            return function_to_uncurry()
        res = function_to_uncurry(args[0])
        for arg in args[1:]:
            res = res(arg)
        return res

    return uncurried_function
