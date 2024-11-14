from typing import Iterable
class OrderedSet():
    def __init__(self, iterable: Iterable):
        self.container: list = list(dict.fromkeys(iterable))
    def __add__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if isinstance(orderedSet, OrderedSet):
            other_set, current_set = dict.fromkeys(orderedSet.container), dict.fromkeys(self.container)
            current_set.update(other_set)
            return OrderedSet(current_set)
        raise TypeError
    def __iadd__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if isinstance(orderedSet, OrderedSet):
            other_set, current_set = dict.fromkeys(orderedSet.container), dict.fromkeys(self.container)
            current_set.update(other_set)
            self.container = list(current_set)
            return self
        raise TypeError
    def __isub__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if isinstance(orderedSet, OrderedSet):
            self.container = [i for i in self.container if i not in orderedSet.container]
            return self
    def __iter__(self): return iter(self.container)
    def __sub__(self, orderedSet: "OrderedSet") -> "OrderedSet":
        if isinstance(orderedSet, OrderedSet):
            return OrderedSet(i for i in self.container if i not in orderedSet.container)
        raise TypeError
    def difference(self, orderedSet: "OrderedSet") -> "OrderedSet":
        return self.__sub__(orderedSet)
    def union(self, orderedSet: "OrderedSet") -> "OrderedSet":
        return self.__add__(orderedSet)
    def add(self, el):
        if el not in self.container: self.container.append(el)
    def remove(self, el):
        if el in self.container: self.container.remove(el)
    def __getitem__(self, item):
        if item in self.container: return self.container[item]
    def __setitem__(self, item, value): self.container[item] = value
    def __str__(self) -> str: return f"OrderedSet({', '.join(map(str, self.container))})"
    def __repr__(self) -> str: return f"{self} with len {len(self)}"
    def __eq__(self, orderedSet: "OrderedSet") -> bool:
        if isinstance(orderedSet, OrderedSet):
            return set(self.container)==set(orderedSet.container)
        raise TypeError
    def __len__(self) -> int: return len(self.container)