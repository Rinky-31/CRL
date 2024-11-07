import re
from .validators import *
from ..errors import ElementsError


@cat()
def get_elements(formula: str, with_acid_residue: bool = False, with_rep: bool = False) -> list:
    """
    ...
    """
    if not formula: return
    res = re.findall(r'[A-Z][a-z]*', formula)
    if not with_acid_residue: pass
    else:
        while (rs:=has_acid_residue(formula)):
            index = formula.find(rs)
            res.append(rs)
            formula = (formula[:index] + formula[index+len(rs):]) if index<len(formula)-1 else formula[:index]
            # if not with_rep:
            #     for i in rs:
            #         if i in res: res.remove(i)
            max_res = max(res, key=len)
            res = list(i for i in res if not i in max_res or i==max_res)
    if with_rep: return res
    for i in (res:=list(dict.fromkeys(res))): 
        if not is_element(i) and not is_acid_residue(i): raise ElementsError(f"{i} is not element", i)
    return res


@cat()
def has_acid_residue(substance: str) -> bool | str:
        try:
            if not (el:=get_elements(substance)): raise ElementsError("Invalid elements")
            if len(el)==1: return substance if substance in insoluble else False
            elif ("O" in substance and len(el)==2):
                return False if not substance in insoluble else substance
            elif ("OH" in substance): return False
            elif substance in insoluble: return substance
            substance = substance[substance.find((el[0]))+len(el[0]):]
            res = list(i for i in insoluble if i in substance)
            if not res: raise ElementsError("Incorrect elements")
            if (rs:=max(res, key=len))==min(res, key=len):
                return res[-1]
            return rs
        except: return False


@cat()
def parse(formula: str, get_first_mult: bool = False, remove_first_multiplier: bool = False, ignore_first_multiplier: bool = False) -> dict | str | bool:
    if not formula: raise TypeError("Incorrect formula")
    if "(" in formula or ")" in formula:
        if formula.count("(")!=formula.count(")"): raise ValueError(f"Некоректна кількість дужок у формулі {formula.count('(')} та {formula.count(')')}")
        elif "()" in formula: raise ValueError("Порожні дужки")
    def remove_in(rem: re.Match):
        formula, mult = rem.group(1), int(rem.group(2)) if rem.group(2) else 1
        return ''.join(f'{el}{multiplier}' for el, multiplier in {elem: amount * mult for elem, amount in parsed(formula).items()}.items())
    def parsed(formula: str):
        t = {}
        while "(" in formula or ")" in formula:
            formula = re.sub(r'\(([^()]+)\)(\d*)', remove_in, formula)
        for el in get_elements(formula):
            elems = re.findall(fr'{el}(?![a-z])(\d*)', formula)
            t[el] = t.get(el, 0) + sum(int(elem) if elem else 1 for elem in elems)
        return t
    pre_mult = re.match(r"\d+", formula)
    pre_mult = int(pre_mult.group()) if pre_mult else 1
    if remove_first_multiplier: return formula[len(str(pre_mult)) if pre_mult!=1 else 0:]
    if get_first_mult: return pre_mult
    elements = get_elements(formula)
    t = dict.fromkeys(elements)
    t.update(parsed(formula))
    if t:
        if not ignore_first_multiplier and pre_mult:
            t = {key: val*pre_mult for key, val in t.items()}
        return t
    return False


@cat()
def get_formulas(string: str):
    return list(i for i in re.findall(r"[A-Za-z0-9()]+", string) if any(x.isupper() for x in i))


@cat()
def underline(text: str, text_to_underline: str, underline_symbol: str = "^", count: int = -1, start: int | None = None, end: int | None = None):
    if len(underline_symbol)!=1: raise ValueError(f"underline symbol lenght must be '1', not '{len(underline_symbol)}'")
    return_str, text = text, text[(start := start if start else 0) : (end := end if end else len(text))] 
    r, c = list(" "*len(text)), text.count(text_to_underline)
    res: list[tuple[int, int]] = []
    for i in range(min(c if count<0 else count, c)):
        res.append((index:=text.find(text_to_underline), index+len(text_to_underline)))
        text = text.replace(text_to_underline, " "*len(text_to_underline), 1)
    for start_pos, end_pos in res:
        r[start_pos:end_pos] = underline_symbol*(end_pos-start_pos)
    return return_str+"\n"+" "*len(return_str[:start])+"".join(r)+" "*len(return_str[end:])