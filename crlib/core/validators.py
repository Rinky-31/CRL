from .data import *
from ..errors import ElementsError
from types import UnionType, FunctionType


def cat(ncoe: bool = False):
    """Check Arguments Type

    NCOE (Not Call On Error) - not call the function if arguments check failed
    """

    def wrapper(func: FunctionType):
        if not isinstance(func, FunctionType):
            raise TypeError(f"Only function allowed here, not '{type(func).__name__}'")

        def argtype_checker(*a, **kw):
            annotation: dict[str, type] = func.__annotations__
            res = False
            for arg, argname in zip(
                a, func.__code__.co_varnames[: func.__code__.co_argcount]
            ):
                if argname in annotation:
                    try:
                        res = isinstance(arg, annotation[argname])
                    except TypeError:
                        continue
                    if not res:
                        if ncoe:
                            break
                        raise TypeError(
                            f"positional-argument '{argname}' must be '{annotation[argname].__name__ if not isinstance(annotation[argname], UnionType) else annotation[argname]}', not '{type(arg).__name__ if not isinstance(arg, UnionType) else arg}'"
                        )
            else:
                res = True
            if not res:
                return
            for arg in kw:
                if arg in annotation:
                    try:
                        res = isinstance(kw[arg], annotation[arg])
                    except TypeError:
                        continue
                    if not res:
                        if ncoe:
                            break
                        raise TypeError(
                            f"keyword-argument '{arg}' must be '{annotation[arg].__name__ if not isinstance(annotation[arg], UnionType) else annotation[arg]}', not '{type(arg).__name__ if not isinstance(arg, UnionType) else arg}'"
                        )
            else:
                res = True
            return func(*a, **kw) if res else None

        return argtype_checker

    return wrapper


def is_metal(element):
    return element in metals if is_element(element) else False


def is_correct_valence(element: str, valence: int) -> bool:
    if is_element(element):
        return (
            metals.get(element, False)
            or not_metals.get(element, False)
            or (element in valences_group and valence in valences_group[element])
        )


def is_correct_alkane(alkane: str):
    return alkane in alkans


def is_acid_residue(formula):
    return False if "OH" in formula else formula in insoluble


def is_element(formula) -> bool:
    return formula in metals or formula in not_metals


@cat()
def is_soluble(formula: str, group: str):
    if not group in insoluble:
        raise ElementsError(f"{group} is not in insoluble dict")
    return not formula in insoluble[group]["elements"]


def arm_check(metal: str, get_index: bool = False, get_element: bool = False):
    try:
        if not is_element(metal):
            raise ElementsError
        if get_element:
            if not metal in ARM:
                raise ElementsError
            return ARM[metal]
        if get_index:
            if not metal in ARM:
                return -1
            return ARM.index(metal)
        if not metal in ARM:
            raise ElementsError
        return ARM.index(metal) < ARM.index("H2")
    except:
        return False


def acid_check(acid_1, acid_2):
    if acid_1 in acids and acid_2 in acids:
        return acids.index(acid_1) < acids.index(acid_2)
    return False
