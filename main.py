# trying to implement auto diff for scalar values.
import numpy as np

class Value:
    def __init__(self, value):
        self.value = value
        self.grad = 0
        self.parent = ()
        self.operation = ""

    def __repr__(self):
        return f"Value(data={self.value}, grad={self.grad})"

    def __add__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        out = Value(self.value + other.value)
        out.parent = (self, other)
        out.operation = "+"
        return out

    def __sub__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        out = Value(self.value - other.value)
        out.parent = (self, other)
        out.operation = "-"
        return out

    def __mul__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        out = Value(self.value * other.value)
        out.parent = (self, other)
        out.operation = "*"
        return out

    def __truediv__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        out = Value(self.value / other.value)
        out.parent = (self, other)
        out.operation = "/"
        return out
    
    def __pow__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        out = Value(self.value ** other.value)
        out.parent = (self, other)
        out.operation = "pow"
        return out
    
    def __neg__(self):
        out = Value(-self.value)
        out.parent = (self,)
        out.operation = "neg"
        return out
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        other = Value(other)
        return other / self

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        other = Value(other)
        return other - self

    def __rpow__(self, other):
        other = Value(other)
        return other ** self

    def __dfs(curr_node, parent_manifestation_operation, previous_gradient_value, other, visited):
        if curr_node in visited: return
        local_derivative=None
        if (parent_manifestation_operation=='none'):
            local_derivative=previous_gradient_value
            curr_node.grad+=previous_gradient_value
        elif (parent_manifestation_operation=='+'):
            local_derivative=previous_gradient_value
            curr_node.grad+=previous_gradient_value
        elif (parent_manifestation_operation=='-'):
            local_derivative=(-previous_gradient_value)
            curr_node.grad+=(-previous_gradient_value)
        elif (parent_manifestation_operation=='*'):
            local_derivative=previous_gradient_value * other 
            curr_node.grad+=previous_gradient_value * other 
        elif (parent_manifestation_operation=='div_num'):
            local_derivative=(previous_gradient_value * (1 / other))
            curr_node.grad+=(previous_gradient_value * (1 / other))
        elif (parent_manifestation_operation=='div_deno'):
            local_derivative=previous_gradient_value * (-other / (curr_node.value ** 2))
            curr_node.grad+=previous_gradient_value * (-other / (curr_node.value ** 2))
        elif (parent_manifestation_operation=='pow_base'):
            local_derivative=previous_gradient_value * (other * (curr_node.value ** (other - 1)))
            curr_node.grad+=previous_gradient_value * (other * (curr_node.value ** (other - 1)))
        elif (parent_manifestation_operation=='pow_expo'):
            local_derivative=previous_gradient_value * (other ** curr_node.value) * np.log(other)
            curr_node.grad+=previous_gradient_value * (other ** curr_node.value) * np.log(other)
        elif (parent_manifestation_operation=='neg'):
            local_derivative=previous_gradient_value * (-1)
            curr_node.grad+=previous_gradient_value * (-1)

        if len(curr_node.parent) == 0: return
        if len(curr_node.parent) == 1:
            curr_node.parent[0].__dfs(curr_node.operation, local_derivative, None, visited)
            visited.add(curr_node)
            return

        if (curr_node.operation=='/'):
            curr_node.parent[0].__dfs('div_num', local_derivative, curr_node.parent[1].value, visited)
            curr_node.parent[1].__dfs('div_deno', local_derivative, curr_node.parent[0].value, visited)
            visited.add(curr_node)
            return
        elif (curr_node.operation=='pow'):
            curr_node.parent[0].__dfs('pow_base', local_derivative, curr_node.parent[1].value, visited)
            curr_node.parent[1].__dfs('pow_expo', local_derivative, curr_node.parent[0].value, visited)
            visited.add(curr_node)
            return

        curr_node.parent[0].__dfs(curr_node.operation, local_derivative, curr_node.parent[1].value, visited)
        curr_node.parent[1].__dfs(curr_node.operation, local_derivative, curr_node.parent[0].value, visited)
        visited.add(curr_node)
        return

    def gradient(self):
        visited = set()
        self.__dfs('none', 1, None, visited)
        


a = Value(2.0)
b = Value(4.0)
c = a + b
d = 2 * c
e = d ** 5
f = e / 67

f.gradient()
print(a.grad)
print(b.grad)
print(c.grad)
print(d.grad)
print(e.grad)
    
