from typing import Iterable, Hashable
class OrderedSet():
    def __init__(self, obj: Iterable[Hashable] | None = None):
        self.container: list = list(dict.fromkeys(obj)) if obj else []
    def __call__(self, orderedSet: "OrderedSet" | Iterable[Hashable]): self.update(orderedSet)
    def __add__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if not isinstance(orderedSet, OrderedSet): 
            raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(orderedSet).__name__}'")
        return self.union(orderedSet)
    def __iadd__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if not isinstance(orderedSet, OrderedSet):
            raise TypeError(f"unsupported operand type(s) for +=: '{type(self).__name__}' and '{type(orderedSet).__name__}'")
        self.update(orderedSet)
        return self
    def __sub__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if not isinstance(orderedSet, OrderedSet):
            raise TypeError(f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(orderedSet).__name__}'")
        return self.difference(orderedSet)
    def __isub__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if not isinstance(orderedSet, OrderedSet):
            raise TypeError(f"unsupported operand type(s) for -=: '{type(self.__name__)}' and '{type(orderedSet).__name__}'")
        self.container = [i for i in self.container if i not in orderedSet.container]
        return self
    def __and__(self, orderedSet: "OrderedSet"): 
        if not isinstance(orderedSet, OrderedSet): 
            raise TypeError(f"unsupported operand type(s) for &: '{type(self).__name__}' and '{type(orderedSet).__name__}'")
        return self.__add__(orderedSet)
    def __rand__(self, orderedSet: "OrderedSet"):
        if not isinstance(orderedSet, OrderedSet): 
            raise TypeError(f"unsupported operand type(s) for &: '{type(orderedSet).__name__}' and '{type(self).__name__}'")
        return self.__add__(orderedSet)
    def __iter__(self): return iter(self.container)
    def __getitem__(self, index: int | slice):
        if not isinstance(index, int | slice): raise TypeError(f"'index' must be 'int' or 'slice', not '{type(index).__name__}'")
        if isinstance(index, slice): return OrderedSet(self.container[index])
        if index>=(l:=len(self.container)) or abs(index)>l: raise IndexError("container index out of range")
        return self.container[index]
    def __setitem__(self, index: int, value: Hashable):
        if not isinstance(index, int): raise TypeError(f"'index' must be 'int', not '{type(index).__name__}'")
        if index>=(l:=len(self.container)) or abs(index)>l: raise IndexError("container index out of range")
        hash(value)
        self.container[index] = value
    def __delitem__(self, index: int | slice):
        if not isinstance(index, int | slice): raise TypeError(f"'index' must be 'int', not '{type(index).__name__}'")
        del self.container[index]
    def __str__(self) -> str: return f"{{{', '.join(map(repr, self.container))}}}"
    def __repr__(self) -> str: return f"{type(self).__name__}({self})"
    def __eq__(self, orderedSet: "OrderedSet") -> bool:
        if not isinstance(orderedSet, OrderedSet):
            raise TypeError(f"unsupported operand type(s) for ==: '{type(self).__name__}' and '{type(orderedSet).__name__}'")
        return self.compare(orderedSet)
    def __len__(self) -> int: return len(self.container)
    def difference(self, orderedSet: "OrderedSet" | Iterable[Hashable]) -> "OrderedSet":
        orderedSet = orderedSet.container if isinstance(orderedSet, OrderedSet) else orderedSet
        return OrderedSet(i for i in self.container if i not in orderedSet)
    def union(self, orderedSet: "OrderedSet" | Iterable[Hashable]) -> "OrderedSet":
        other_set, current_set = dict.fromkeys(orderedSet.container if isinstance(orderedSet, OrderedSet) else orderedSet), dict.fromkeys(self.container)
        current_set.update(other_set)
        return OrderedSet(current_set)
    def update(self, orderedSet: "OrderedSet" | Iterable[Hashable]):
        other_set, current_set = dict.fromkeys(orderedSet.container if isinstance(orderedSet, OrderedSet) else orderedSet), dict.fromkeys(self.container)
        current_set.update(other_set)
        self.container = list(current_set)
    def add(self, el: Hashable):
        if el not in self.container: 
            hash(el)
            self.container.append(el)
    def remove(self, el: Hashable):
        if el in self.container: self.container.remove(el)
    def pop(self, index: int = 0): return self.container.pop(index)
    def reverse(self): self.container = self.container[::-1]
    def insert(self, item: Hashable, position: int = 0):
        hash(item)
        self.container.insert(position, item)
    def exchange(self, first_index: int, second_index: int):
        if isinstance(first_index, slice) or isinstance(second_index, slice): raise TypeError("'slice' not allowed here")
        self[first_index], self[second_index] = self[second_index], self[first_index]
    def compare(self, orderedSet: "OrderedSet", ordered: bool = False) -> bool:
        if not isinstance(orderedSet, OrderedSet): return False
        return self.container == orderedSet.container if ordered else set(self.container) == set(orderedSet.container)