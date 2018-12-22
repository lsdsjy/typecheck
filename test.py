import unittest
from typecheck import typecheck


# Example function
@typecheck
def func(z: str, *x: str, y: int, **u: float):
    print(z, x, y, u)


class BasicTest(unittest.TestCase):
    def test_pos_arg(self):
        with self.assertRaises(TypeError) as ctx:
            func(1, 's', y=3, u=4)  # Wrong type of positional argument z
        self.assertIn('Parameter "z"', str(ctx.exception))

    def test_var_pos_args(self):
        with self.assertRaises(TypeError) as ctx:
            func('s', 2, y=3, u=4)  # Wrong type of variable positional arguments *x
        self.assertIn('Wrong type of variable positional argument for parameter "x"', str(ctx.exception))

    def test_kwarg(self):
        with self.assertRaises(TypeError) as ctx:
            func('s', 's', y=1.5, u=1.5)  # Wrong type of kwarg z
        self.assertIn('Parameter "y"', str(ctx.exception))

    def test_missing_kwarg(self):
        with self.assertRaises(TypeError) as ctx:
            func('s', 's', z=3, u=4)  # Missing keyword argument y
        self.assertIn('Missing keyword argument "y"', str(ctx.exception))

    def test_var_kwarg(self):
        with self.assertRaises(TypeError) as ctx:
            func('s', 's', y=3, t=1)  # Incorrect type of variable keyword arguments **u
        self.assertIn('Wrong type of variable keyword argument "u"', str(ctx.exception))



@typecheck
def func2(x: (int, str)):
    return x


class TupleTest(unittest.TestCase):
    def test_tuple(self):
        self.assertEqual(func2(1), 1)
        self.assertEqual(func2('hhh'), 'hhh')

        with self.assertRaises(TypeError):
            func2(1.5)



if __name__ == '__main__':
    unittest.main()
