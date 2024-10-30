class ReactionError(Exception):
    def __init__(self, text: str = "", *a):
        super().__init__(text)
        self.argc = a
    def get(self, as_string: bool = True):
        return ", ".join(i.strip() if isinstance(i, str) else i for i in self.argc) if as_string else self.argc


class ValenceError(Exception):
    def __init__(self, text: str = "", element: str | None = None, valence: int | float | None = None):
        super().__init__(text)
        self.element, self.valence = element, valence
    def get(self): return self.element, self.valence


class InvalidSubstance(Exception):
    def __init__(self, text: str = "", substance: str | None = None):
       super().__init__(text)
       self.substance = substance
    def get(self): return self.substance


class InvalidOperation(Exception):
    def __init__(self, text: str = "", operation: str | None = None):
       super().__init__(text)
       self.operation = operation
    def get(self): return self.operation


class ElementsError(Exception):
    def __init__(self, text, *elements):
       super().__init__(text)
       self.elements = elements
    def get(self, as_string: bool = True):
        return ", ".join(i.strip() for i in self.elements) if as_string else self.elements