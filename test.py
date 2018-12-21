



from models import Cliente
from typing import Any
from numbers import Integral





class Int(int):

    def __init__(self, id):
        self.id = id




n = Int(3)

print(n)
print(n.__class__)
print(Int)


print(n.__class__ == Int)
print(n.__class__ == n)