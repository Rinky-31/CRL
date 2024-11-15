from typing import Iterable, Hashable
class OrderedSet():
    def __init__(self, obj: Iterable | None = None):
        self.container: list = list(dict.fromkeys(obj)) if obj else []
    def __add__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if isinstance(orderedSet, OrderedSet):
            other_set, current_set = dict.fromkeys(orderedSet.container), dict.fromkeys(self.container)
            current_set.update(other_set)
            return OrderedSet(current_set)
        raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(orderedSet).__name__}'")
    def __iadd__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if isinstance(orderedSet, OrderedSet):
            other_set, current_set = dict.fromkeys(orderedSet.container), dict.fromkeys(self.container)
            current_set.update(other_set)
            self.container = list(current_set)
            return self
        raise TypeError(f"unsupported operand type(s) for +=: '{type(self).__name__}' and '{type(orderedSet).__name__}'")
    def __isub__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if isinstance(orderedSet, OrderedSet):
            self.container = [i for i in self.container if i not in orderedSet.container]
            return self
        raise TypeError(f"unsupported operand type(s) for -=: '{type(self.__name__)}' and '{type(orderedSet).__name__}'")
    def __iter__(self): return iter(self.container)
    def __sub__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if isinstance(orderedSet, OrderedSet):
            return OrderedSet(i for i in self.container if i not in orderedSet.container)
        raise TypeError(f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(orderedSet).__name__}'")
    def __getitem__(self, index: int):
        if not isinstance(index, int): raise TypeError(f"'index' must be 'int', not '{type(index).__name__}'")
        if index>=len(self.container) or abs(index)>len(self.container): raise IndexError("container index out of range")
        return self.container[index]
    def __setitem__(self, index: int, value: Hashable):
        if not isinstance(index, int): raise TypeError(f"'index' must be 'int', not '{type(index).__name__}'")
        hash(value); self.container[index] = value
    def __delitem__(self, index: int):
        if not isinstance(index, int): raise TypeError(f"'index' must be 'int', not '{type(index).__name__}'")
        del self.container[index]
    def __str__(self) -> str: return f"{{{', '.join(map(repr, self.container))}}}"
    def __repr__(self) -> str: return f"{type(self).__name__}({self})"
    def __eq__(self, orderedSet: "OrderedSet") -> bool:
        if isinstance(orderedSet, OrderedSet):
            return set(self.container)==set(orderedSet.container)
        raise TypeError(f"unsupported operand type(s) for ==: '{type(self).__name__}' and '{type(orderedSet).__name__}'")
    def __len__(self) -> int: return len(self.container)
    def difference(self, orderedSet: "OrderedSet") -> "OrderedSet":
        return self.__sub__(orderedSet)
    def union(self, orderedSet: "OrderedSet") -> "OrderedSet":
        return self.__add__(orderedSet)
    def add(self, el: Hashable):
        if el not in self.container: hash(el); self.container.append(el)
    def remove(self, el: Hashable):
        if el in self.container: self.container.remove(el)
    def pop(self, index: int = 0): return self.container.pop(index)
    def insert(self, item, position: int = 0): hash(item); self.container.insert(position, item)