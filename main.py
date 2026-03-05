# trying to implement auto diff for scalar values.

class Value:
    def __init__(self, value):
        self.value = value
        self.grad = 0
        self.parent = set()

    def __repr__(self):
        return f"Value(data={self.value}, grad={self.grad})"

    def __add__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        out = Value(self.value + other.value)
        out.parent.add(other)
        out.parent.add(self)
        return out

    def __sub__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        out = Value(self.value - other.value)
        out.parent.add(other)
        out.parent.add(self)
        return out

    def __mul__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        out = Value(self.value * other.value)
        out.parent.add(other)
        out.parent.add(self)
        return out

    def __truediv__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        out = Value(self.value / other.value)
        out.parent.add(other)
        out.parent.add(self)
        return out
    
    def __pow__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        out = Value(self.value ** other.value)
        out.parent.add(other)
        out.parent.add(self)
        return out
    
    def __neg__(self):
        out = Value(-self.value)
        out.parent.add(self)
        return out
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        other = Value(other)
        out = Value(other.value / self.value)
        out.parent.add(self)
        out.parent.add(other)
        return out

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        other = Value(other)
        out = other - self
        out.parent.add(other)
        out.parent.add(self)
        return out

    def __rpow__(self, other):
        other = Value(other)
        out = Value(other.value ** self.value)
        out.parent.add(other)
        out.parent.add(self)
        return out


a = Value(2.0)
b = Value(4.0)
c = a + b
d = 2 * c

print(d)
    
