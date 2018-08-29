class BinaryOperator:

    def __init__(self, env):
        self.env = env

    @property
    def mark(self):
        return ''

    def apply(self, left, right):
        pass

    def __str__(self):
        return self.mark


class UnaryOperator:

    def __init__(self, env):
        self.env = env

    @property
    def mark(self):
        return ''

    def apply(self, exp):
        pass

    def __str__(self):
        return self.mark


class Equal(BinaryOperator):

    @property
    def mark(self):
        return '=='

    def apply(self, left, right):
        return str(left) == str(right)


class And(BinaryOperator):
    @property
    def mark(self):
        return '&'

    def apply(self, left, right):
        return left and right


class Or(BinaryOperator):
    @property
    def mark(self):
        return '|'

    def apply(self, left, right):
        return left or right


class Not(UnaryOperator):
    @property
    def mark(self):
        return '!'

    def apply(self, exp):
        return not exp


class LessThan(BinaryOperator):
    @property
    def mark(self):
        return '<'

    def apply(self, left, right):
        try:
            return float(left) < float(right)
        except ValueError:
            return str(left) < str(right)



class GreaterThan(BinaryOperator):
    @property
    def mark(self):
        return '>'

    def apply(self, left, right):
        try:
            return float(left) > float(right)
        except ValueError:
            return str(left) > str(right)


class Plus(BinaryOperator):
    @property
    def mark(self):
        return '+'

    def apply(self, left, right):
        return float(left) + float(right)


class Minus(BinaryOperator):
    @property
    def mark(self):
        return '-'

    def apply(self, left, right):
        return float(left) - float(right)


class Multiply(BinaryOperator):
    @property
    def mark(self):
        return '*'

    def apply(self, left, right):
        return float(left) * float(right)


class Divide(BinaryOperator):
    @property
    def mark(self):
        return '/'

    def apply(self, left, right):
        return float(left) / float(right)


class Mode(BinaryOperator):
    @property
    def mark(self):
        return '%'

    def apply(self, left, right):
        return int(left) % int(right)


class Access(BinaryOperator):
    @property
    def mark(self):
        return '.'

    def apply(self, left, right):
        if left is None:
            return None
        else:
            if isinstance(left, dict):
                return left.get(right)
            elif isinstance(left, list):
                try:
                    return left[int(right)]
                except IndexError:
                    return None


def get_all_operator(env):
    all_operator = [
        Equal(env),
        And(env),
        Or(env),
        Not(env),
        LessThan(env),
        GreaterThan(env),
        Plus(env),
        Minus(env),
        Multiply(env),
        Divide(env),
        Mode(env),
        Access(env)
    ]
    return all_operator
