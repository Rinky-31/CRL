import math as m
from ..core.utils import *
from ..core.warnings import warn
from ..errors import *


def get_acid_by_oxide(oxide: str) -> str | bool:
    return acid_oxyds.get(oxide, False)
    # return acid_oxyds[oxide] if oxide in acid_oxyds else False


def get_oxide_by_acid(acid) -> str | bool:
    return oxyds_acid.get(acid, False)
    # return oxyds_acid[acid] if acid in oxyds_acid else False


def minimal_valence(element) -> int:
    if not is_element(element): raise ElementsError(f"{element} is not element")
    return min(valences_group[element]) if element in valences_group else 1


def maximum_valence(element) -> int:
    if not is_element(element): raise ElementsError(f"{element} is not element")
    return max(valences_group[element]) if element in valences_group else 1


def get_element_valences(element: str) -> int | None:
    if not is_element(element): raise ElementsError(f"{element} is not element")
    return valences_group[element] if element in valences_group else None


@cat()
def substance_type(substance: str) -> str:
    if not isinstance(substance:=parse(substance, remove_first_multiplier=True), str): raise TypeError(f"Incorrect type of substance: {type(substance).__name__}, must be 'str'")
    if substance=="OH": return "Hydroxide"
    elif substance=="H2O": return "Water"
    _substance = get_elements(substance)
    if not _substance: raise InvalidSubstance(f"Undefiend substance: {substance or None}", substance)
    if len(_substance)==2:
        if is_metal(_substance[0]) and _substance[-1]=="C":
            return "Carbide"
    if len(_substance)==1:
        return "Simple metal" if _substance[0] in metals else "Simple not_metal" if _substance[0] in not_metals else False
    elif len(_substance)==2 and _substance[0]=="C" and _substance[1]=="H":
        res = parse(substance)
        if res["H"]==res["C"]*2+2 and is_correct_alkane(substance): return "Alkane"
        elif res["H"]==res["C"]*2 and "is_correct_alkene(substance)": return "Alkene"
        elif res["H"]==res["C"]*2-2 and "is_correct_alkyne(substance)": return "Alkyne"
    elif len(_substance)==2 and "O" in _substance:
        if substance.find("O")==0: pass
        elif _substance[0] in metals:
            return "Base oxide"
        elif _substance[0] in not_metals:
            return "Acid oxide"
    else:
        if len(_substance)==3 and "OH" in substance and _substance[0] in metals:
            if substance.find("OH")==0 or not all(substance.count(i)==1 for i in _substance): pass
            else: return "Base"
        elif (acid_residue:=has_acid_residue(substance)) and _substance[0]=="H":
            if len(get_elements(substance, with_acid_residue=True))!=2: pass
            else: return "Acid"
        elif _substance[0] in metals and acid_residue:
            if len(get_elements(substance, with_acid_residue=True))!=2: pass
            else: return "Salt"
    print(substance, _substance)
    raise InvalidSubstance(f"Undefiend substance: {substance or None}", substance)


def get_element_valence(element: str, not_replace_one: bool = False, with_acid_residue: bool = False) -> int:
    if with_acid_residue:
        if is_acid_residue(element): return insoluble[element]["valence"]
    if not is_element(element): raise ElementsError(f"{element} is not element", element)
    res = metals[element] if is_metal(element) else not_metals[element]
    if not_replace_one: return res
    return res or minimal_valence(element)


@cat()
def pre_reaction(formula1: str, formula2: str, get_substance_type: bool = False) -> str | tuple[str, str, str]:
    def oxide(formula1, formula2):
        if not (is_element(formula1) and is_element(formula2)): raise ElementsError(f"{formula1} or {formula2} is not element")
        return formula1+formula2
    def m_a(metal, acid):
        if not arm_check(metal): raise ElementsError("Метал має знаходитися до H2 в ряді активності", metal)
        return f"{metal}{has_acid_residue(acid)} + H2"
    def bo_ao(oxide, acid_oxide):
        return f"{oxide}{has_acid_residue(get_acid_by_oxide(acid_oxide))}"
    def bo_a(base_oxide, acid):
        return f"{base_oxide}{has_acid_residue(acid)} + H2O"
    def b_ao(base, acid_oxide):
        return f"{bo_ao(base, acid_oxide)} + H2O"
    def m_salt(metal, salt):
        elems = get_elements(salt)
        if metal=="Cu":
            if arm_check(elems[0], True)<=arm_check("Cu", True): raise ReactionError(f"{elems[0]} має знаходитися правіше від Cu в ряді активності, щоб бути витісниним", elems[0])
            return f"{elems[0]} + {metal+has_acid_residue(salt)}"
        elif "Cu" in elems:
            if arm_check(metal, True)>=arm_check("Cu", True): raise ReactionError(f"{metal} має знаходитися лівіше від Cu в ряді активності, щоб витіснити його", metal)
            return f"{elems[0]} + {metal+has_acid_residue(salt)}"
        if not arm_check(metal): raise ElementsError(f"{elems[0]}: check failed", elems[0])
        return  f"{elems[0]} + {metal+has_acid_residue(salt)}"
    def salt_check(salt):
        return not is_soluble(get_elements(salt)[0], has_acid_residue(salt))
    def salt_salt(salt1, salt2, elements1, elements2):
        if (s1:=has_acid_residue(salt1))==(s2:=has_acid_residue(salt2)): raise ReactionError("Дві солі з однаковим кислотним залишком не можуть взаємодіяти")
        s1, s2 = elements1[0] + s2, elements2[0] + s1
        if salt_check(s1)+salt_check(s2)==0: raise ReactionError("Одна з солей має випадати в осад в результаті реакції")
        return s1 + " + " + s2
    def salt_base(salt, elements1, elements2):
        if not is_soluble(elements2[0], "OH"): raise ReactionError("Основа має бути розчинною")
        return elements1[0] + "OH" + " + " + elements2[0] + has_acid_residue(salt)
    def salt_acid(salt, acid, elements1, elements2):
        if (a:=has_acid_residue(acid))==(s:=has_acid_residue(salt)): raise ReactionError("Сіль та кислота з однаковим кислотним залишком не можуть взаємодіяти")
        return f"{elements1[0]+a} + {elements2[0]+s}"
    def w_o(element: list): 
        if len(element)>1: return f"{element[0]}OH"
        index = arm_check(element[0], True)
        if index==1: raise ReactionError(f"can’t get {element[0]} index")
        if index<arm_check("Mg", True):
            return f"{element[0]}OH + H2"
        else:
            if arm_check(element[0], get_element=True) in ("Ni", "Sn", "Pb"): raise ReactionError("Взаємодія не можлива")
            return f"{element[0]}O + H2"
    elements1, elements2 = get_elements(formula1), get_elements(formula2) 
    r1, r2 = substance_type(formula1:=parse(formula1, remove_first_multiplier=True)), substance_type(formula2:=parse(formula2, remove_first_multiplier=True))
    if r1 in ("Carbide",) or r2 in ("Carbide",):
        raise InvalidOperation("Currect version can’t evaluate this", " + ".join((formula1, formula2)))
    try:
        res = None
        match r1:
            case "Water":
                match r2:
                    case "Base oxide" | "Simple metal":
                        res = w_o(elements2)
                    case "Acid oxide":
                        res = "H" + has_acid_residue(get_acid_by_oxide(formula2))
            case "Simple metal":
                if len(elements2)==1 and len(elements1)==1 and elements2[0]=="O":
                    res = oxide(elements1[0], elements2[0])
                elif len(elements2)==1 and len(elements1)==1 and elements2[0]=="C": res = formula1+formula2
                match r2:
                    case "Water":
                        res = w_o(elements1)
                    case "Acid":
                        res = m_a(elements1[0], formula2)
                    case "Salt":
                        res = m_salt(elements1[0], formula2)
            case "Simple not_metal":
                if len(elements2)==1 and len(elements1)==1 and elements2[0]=="O":
                    res = oxide(elements1[0], elements2[0])
                elif len(elements2)==1 and len(elements1)==1 and elements1[0]=="C":
                    res = formula2+formula1
                elif formula1=="O2" and r2=="Alkane": res = "CO2 + H2O"
            case "Base oxide":
                if r2=="Base" or r2=="Base oxide": res = False
                match r2:
                    case "Acid oxide":
                        res = bo_ao(elements1[0], formula2)
                    case "Acid":
                        res = bo_a(elements1[0], formula2)
                    case "Water":
                        res = w_o(elements1)
            case "Acid oxide":
                if formula2=="H2O":
                    res = "H" + has_acid_residue(get_acid_by_oxide(formula1))
                if r2 in ("Acid", "Acid oxide"): res = False
                match r2:
                    case "Base":
                        res = b_ao(elements2[0], formula1)
                    case "Base oxide":
                        res = bo_ao(elements2[0], formula1)
            case "Acid":
                if r2=="Acid oxide" or r2=="Acid": res = False
                match r2:
                    case "Base oxide" | "Base":
                        res = bo_a(elements2[0], formula1)
                    case "Simple metal": 
                        res = m_a(elements2[0], formula1)
                    case "Salt":
                        res = salt_acid(formula2, formula1, elements2, elements1)
            case "Base":
                if r2 in ("Base", "Base oxide"): res = False
                match r2:
                    case "Acid oxide":
                        res = b_ao(elements1[0], formula2)
                    case "Acid":
                        res = bo_a(elements1[0], formula2)
                    case "Salt":
                        res = salt_base(formula2, elements2, elements1)
            case "Salt":
                match r2:
                    case "Salt":
                        res = salt_salt(formula1, formula2, elements1, elements2)
                    case "Base":
                        res = salt_base(formula1, elements1, elements2)
                    case "Acid":
                        res = salt_acid(formula1, formula2, elements1, elements2)
                    case "Simple metal":
                        res = m_salt(elements2[0], formula1)
            case "Alkane":
                if formula2=="O2": res = "CO2 + H2O"
    except Exception as e: raise ReactionError(f"EXC by {e.__class__.__name__}: {e}") from None
    if res!=None: return res if not get_substance_type else (res, r1, r2)
    raise ReactionError("Reaction does not occure")


@cat()
def get_coefficients(reactants: dict, products: dict) -> tuple[int, int, int]:
    return (s1:=sum(reactants.values())), (s2:=sum(products.values())), s1+s2


def get_valence_from_formula(formula: str) -> dict:
    if not isinstance(formula:=parse(formula, remove_first_multiplier=True), str): raise TypeError("Incorrect type of formula")
    elements = get_elements(formula)
    valence, sbt = {i: get_element_valence(i, True) for i in elements}, substance_type(formula)
    if not sbt: raise InvalidSubstance(f"Невідома фомула ({formula}) (або неправильно вказана)")
    res = parse(formula)
    try:
        if sbt in ("Simple metal", "Simple not_metal", "Water"): return valence
        elif sbt in ("Acid oxide", "Base oxide"): 
            rs: float = res["O"]*2/res[elements[0]]
            if not rs.is_integer(): raise ReactionError("Can’t balance")
            rs=int(rs)
            if valence[elements[0]]:
                if rs!=valence[elements[0]]: raise ReactionError(f"Елемент {elements[0]} має сталу валентність ({valence[elements[0]]}), але у формулі він має неможливу валентність ({rs})")
            else:
                if not is_correct_valence(elements[0], rs): raise ReactionError(f"Елемент {elements[0]} має допустимі валентності {valences_group[elements[0]]}, але у формулі він має неможливу валентність ({rs})")
            return {elements[0]: valence[elements[0]] if valence[elements[0]] else rs, "O": 2}
        match sbt:
            case "Hydroxide":
                return {"OH": 1}
            case "Base":
                rs = res["O"]/res[elements[0]]
                if not rs.is_integer(): raise ReactionError("Can’t balance")
                rs = int(rs)
                if valence[elements[0]] and rs!=valence[elements[0]]:
                    raise ReactionError(f"Елемент {elements[0]} має сталу валентність ({valence[elements[0]]}), але у формулі він має неможливу валентність ({rs})")
                elif not is_correct_valence(elements[0], rs):
                    raise ReactionError(f"Елемент {elements[0]} має допустимі валентності {valences_group[elements[0]]}, але у формулі він має неможливу валентність ({rs})")
                return {elements[0]: rs, "OH": 1}
            case "Acid":
                if "O" in formula:
                    rs = int(res["O"]*2-res["H"])
                    if valence[elements[1]]:
                        if rs!=valence[elements[1]]: raise ReactionError("Can’t balance")
                    elif elements[1] in valences_group:
                        if not is_correct_valence(elements[1], rs): raise ReactionError(f"Елемент {elements[1]} має допустимі валентності {valences_group[elements[1]]}, але у формулі він має неможливу валентність ({rs})")
                    return {"H": 1, elements[1]: res["O"]*2-res["H"], "O": 2}
                else:
                    rs = get_element_valence(has_acid_residue(formula), with_acid_residue=True)
                    hydrogen: float = rs*res[elements[1]]/res["H"]
                    if not hydrogen.is_integer(): raise ReactionError("Can’t balance")
                    hydrogen = int(hydrogen)
                    if hydrogen!=1: raise (f"Елемент {elements[0]} має сталу валентність ({valence[elements[0]]}), але у формулі він має неможливу валентність ({hydrogen})")
                    return {"H": 1, elements[1]: valence[elements[1]] if valence[elements[1]] else rs}
            case "Salt":
                valence = {i: get_element_valence(i, True) for i in elements}
                rs = has_acid_residue(formula)
                result: float = get_element_valence(rs, with_acid_residue=True)*res[get_elements(rs)[0]]/res[elements[0]]
                if not result.is_integer(): raise ReactionError("Can’t balance")
                result=int(result)
                if valence[elements[0]]:
                    if result!=valence[elements[0]]: raise ReactionError(f"Елемент {elements[0]} має сталу валентність ({valence[elements[0]]}), але у формулі він має неможливу валентність ({result})")
                else:
                    if not is_correct_valence(elements[0], result) if elements[0] in valences_group else True: raise ReactionError(f"Елемент {elements[0]} має допустимі валентності {valences_group[elements[0]]}, але у формулі він має неможливу валентність ({result})")
                if "O" in formula:
                    return {elements[0]: valence[elements[0]] if valence[elements[0]] else result, elements[1]: (res["O"]*2-res[elements[0]]*(valence[elements[0]] if valence[elements[0]] else result))//res[elements[1]], "O": 2}
                return {elements[0]: result, elements[1]: valence[elements[1]] if valence[elements[1]] else result}
            case "Alkane":
                return {"C": 4, "H": 1}
    except Exception as e:
        raise InvalidOperation(f"EXC by {e.__class__.__name__}: {e}") from None
    raise ValenceError(f"Can’t get valence from {formula}")


@cat()
def balance_formula(formula: str, valence: dict) -> str | None:
    _substance_type = substance_type(formula:=parse(formula, remove_first_multiplier=True))
    if not _substance_type: raise ReactionError("Реакція не відбувається або сталася невідома помилка (перевірте правильність хімічних формул)")
    elements = get_elements(formula)
    for i in valence: 
        if not valence[i]: valence[i] = minimal_valence(i)
        valence[i] = abs(valence[i])
    if _substance_type in ("Acid oxide", "Base oxide"):
        mult: float = (valence[elements[0]]*2)//m.gcd(valence[elements[0]], 2)
        if not ((mult/valence[elements[0]]).is_integer() and (mult/2).is_integer()): raise ReactionError("Can’t balance")
        return f"{elements[0]}{mult//valence[elements[0]] if mult/valence[elements[0]]!=1 else ''}O{mult//2 if mult//2 !=1 else ''}"
    elif "Simple" in _substance_type or _substance_type=="Alkane": return formula.strip()
    elif _substance_type=="Water": return formula
    match _substance_type:
        case "Base":
            mult = valence[elements[0]]/m.gcd(valence[elements[0]], 1)
            if not mult.is_integer(): raise ReactionError("Can’t balance")
            mult=int(mult)
            return f"{elements[0]}OH" if mult==1 else f"{elements[0]}(OH){mult}"
        case "Acid":
            rs = has_acid_residue(formula)
            return f"H{a if (a:=get_element_valence(rs, with_acid_residue=True))!=1 else ''}{rs}"
        case "Salt":
            acid_residue = has_acid_residue(formula)
            acid_residue_val = get_element_valence(acid_residue, with_acid_residue=True)
            mult = (valence[elements[0]]*acid_residue_val)/m.gcd(valence[elements[0]], acid_residue_val)
            if not mult.is_integer(): raise ReactionError("Can’t balance")
            mult=int(mult)
            if not ((mult/valence[elements[0]]).is_integer() and (mult/acid_residue_val).is_integer()): raise ReactionError("Can’t balance")
            result = mult//valence[elements[0]] if mult//valence[elements[0]]!=1 else ''
            return f"{elements[0]}{result}{acid_residue}" if mult//acid_residue_val==1 else f"{elements[0]}{result}({acid_residue}){mult//acid_residue_val}" if len(get_elements(acid_residue))>1 else f"{elements[0]}{result}{acid_residue}{mult//acid_residue_val}"


@cat()
def balance_reaction(reactans: dict, products: dict) -> tuple[dict, dict, bool]:
    if not reactans or not products: raise InvalidOperation("Empty objects")
    if not all(substance_type(i) for i in set(reactans).union(set(products))): raise InvalidSubstance
    try:
        from chempy import balance_stoichiometry as balance
        reactans, products = balance(reactans, products)
    except ImportError:
        warn("Unable to import 'chempy', reaction balance is not available now")
        return reactans, products, False
    except Exception as e: raise InvalidOperation(e) from None
    return dict(reactans), dict(products), True


@cat()
def reaction(formula1: str, formula2: str | None = None, balanced: bool = True, as_dict: bool = False, ignore_amount: bool = True, ignore_dec_substances: bool = False) -> str | dict:
    normal_reaction, rs = True, None
    elements1, elements2 = get_elements(formula1), get_elements(formula2)
    if not formula2 and not ignore_dec_substances:
        sbt, form = substance_type(formula1), f"{formula1} -> "
        match sbt:
            case "Acid":
                oxide = get_oxide_by_acid(formula1)
                rs= form+f"{oxide} + H2O" if oxide else (f"{formula1} -> {' + '.join(elements1)}")
            case "Base":
                if is_soluble(elements1[0], "OH"): raise ReactionError("Reaction does not occure (decompose soluble base)")
                rs = form+f"{balance_formula(elements1[0]+'O', get_valence_from_formula(formula1))} + H2O"
        normal_reaction = False
    if normal_reaction:
        if not formula2: raise ReactionError("Reaction does not occure")
        res, sbt1, sbt2 = pre_reaction(formula1, formula2, True)
        if not res: raise ReactionError("Реакція не відбувається або сталася невідома помилка (перевірте правильність хімічних формул)")
        val1, val2 = get_valence_from_formula(formula1), get_valence_from_formula(formula2)
        res = res.split("+")
        elems = get_elements(res[0])    
        if elems[0] in elements1: 
            rs = f"{formula1} + {formula2} -> {balance_formula(res[0], val1)}" if len(res)<2 else f"{formula1} + {formula2} -> {balance_formula(res[0], val1)} + {res[1].strip()}"
        elif elems[0] in elements2: 
            rs = f"{formula1} + {formula2} -> {balance_formula(res[0], val2)}" if len(res)<2 else f"{formula1} + {formula2} -> {balance_formula(res[0], val2)} + {res[1].strip()}"
        else: raise InvalidOperation("Undefiend error, please report the problem to the author (you can find email by command: 'pip show crlib')")
        unbalanced_formula = list(i.strip() for i in rs.split("->")[1].strip().split("+"))
        if len(unbalanced_formula)>1:
            sbt, form = substance_type(unbalanced_formula[1]), f"{formula1} + {formula2} -> {unbalanced_formula[0]} + "
            if unbalanced_formula[1] in ("H2O", "H2"): pass
            elif sbt=="Acid":
                acid = balance_formula(unbalanced_formula[1], {})
                if not ignore_dec_substances and not acid_check(acid, parse(formula1, remove_first_multiplier=True) if sbt1=='Acid' else parse(formula2, remove_first_multiplier=True)):
                    acid = " + ".join(get_reaction(reaction(acid, balanced=False))[-1])
                rs = form+acid
            elif (elems:=get_elements(unbalanced_formula[1]))[0] in elements1: rs = form+f"{balance_formula(unbalanced_formula[1], val1)}"
            elif elems[0] in elements2: rs = form+f"{balance_formula(unbalanced_formula[1], val2)}"
            else: rs = form+f"{balance_formula(unbalanced_formula[1], val2)}"
    reactans, products = get_reaction(rs)
    if not isinstance(reactans, dict) or not isinstance(products, dict): raise TypeError("Incorrect type")
    if not balanced:
        return (reactans, products) if as_dict else to_reaction_str(reactans, products, False)
    
    react, prod, is_succes = balance_reaction(reactans, products)
    if not ignore_amount and react!=reactans:
        raise ReactionError("Incorrect amount")
    try:
        reactans.update(react)
        products.update(prod)
        return (reactans, products) if as_dict else to_reaction_str(reactans, products, is_succes)
    except:
        raise InvalidOperation("Incorrect operation")
    

@cat()
def equation(eq: str, tags_start: str = "{", tags_end: str = "}") -> str | bool | dict:
    """
    tags (between 'tags_start' and 'tags_end'):
        -ad: as dict
        -ia: ignore amount
        -ids: ignore decompose substances
    """
    tags = {"-ad": False, "-ia": True, "-ids": False}


    def check_tags(eq: str) -> str:
        if tags_start+tags_end in eq: raise InvalidOperation(f"Empty string: '{tags_start+tags_end}'\n\n"+underline(eq, tags_start+tags_end))
        string_tags: list[str] = re.findall(f"{re.escape(tags_start)}(.*?){re.escape(tags_end)}", eq)
        eq1 = eq
        for current_string in range(len(string_tags)):
            current_string_copy = f"{{{string_tags[current_string]}}}"
            for tag in tags:
                if tag in string_tags[current_string]:
                    if string_tags[current_string].count(tag)%2: tags[tag] = not tags[tag]
                    string_tags[current_string] = string_tags[current_string].replace(tag, "")
                    eq = eq.replace(tag, "")
            if string_tags[current_string]:
                print(eq1, current_string_copy, string_tags[current_string])
                raise InvalidOperation(f"Only tags between '{tags_start}' and '{tags_end}', not '{string_tags[current_string]}'\n\nThere might be problems in the following positions:\n"+(underline(eq1, string_tags[current_string], start=(pos:=eq1.find(current_string_copy)+1), end=pos+len(current_string_copy)) if string_tags[current_string] in eq1 else underline(eq1, current_string_copy)))
        eq = eq.replace(tags_start+tags_end, "")
        if tags_start in eq or tags_end in eq or tags_start+tags_end in eq: raise InvalidOperation("Incorrect eq")
        return eq


    def do_reaction() -> str | dict:
        reactants = list("".join(i.split()) for i in split_by_flag[0].split("+") if i)
        if check_result and len(split_by_flag)==2:
            if len(reactants)<2:
                react, prod = reaction(*reactants, None, flag=="=", True, *tuple(tags.values())[1:])
            else: 
                react, prod = reaction(*reactants, flag=="=", True, *tuple(tags.values())[1:])
            return "+".join(prod) == "".join(split_by_flag[1].split())
        if len(reactants)>2: raise InvalidOperation("Incorrect eq")
        return reaction(*reactants, flag=="=", *tags.values()) if len(reactants)>1 else reaction(*reactants, None, flag=="=", *tags.values())

            
    flag, eq = "->" if "->" in eq else "=", check_tags(eq)
    if eq.count(flag)>1: raise ValueError(f"Некоректна кількість флагів (-> або =) = {eq.count(flag)}")
    split_by_flag = list(i for i in eq.split(flag) if i.strip())
    if not split_by_flag or "+" in split_by_flag[0] and len(get_formulas(split_by_flag[0]))<2:
        raise InvalidOperation("Incorrect eq")
    check_result = len(split_by_flag)>1
    return do_reaction()


@cat()
def to_reaction_str(react: dict, prod: dict, balanced: bool = True) -> str:
    return " + ".join((str(amount) if amount!=1 else "")+formula.strip() for formula, amount in react.items()) + (" = " if balanced else " -> ") + (" + ".join((str(amount) if amount!=1 else "")+formula.strip() for formula, amount in prod.items()))


@cat()
def get_reaction(reaction: str, flag: str = "->") -> tuple[dict[str, int], dict[str, int]]:
    if not reaction: raise TypeError("Incorrect type of reaction")
    elif not flag in reaction: raise InvalidOperation("flag is not in reaction")


    def res(current: list[str]):
        result = {}
        for i in current:
            result[parse(i.strip(), remove_first_multiplier=True)] = parse(i.strip(), get_first_mult=True)
        return result
    react, prod = reaction.split(flag)
    react, prod = react.split("+"), prod.split("+")
    return res(react), res(prod)


@cat()
def cot(*formulas, balanced: bool = True):
    """Chains of transformations 

    Fix: data -> valences_group
    """
    if not formulas or len(formulas)<2: return
    def get_second_reactant(formula1, formula2):
        sbt1, sbt2 = substance_type(formula1:=parse(formula1, remove_first_multiplier=True)), substance_type(formula2:=parse(formula2, remove_first_multiplier=True))
        elements1, elements2 = get_elements(formula1), get_elements(formula2)
        match sbt1:
            case "Simple metal" | "Simple not_metal":
                if ((sbt2 == "Base oxide" and is_metal(formula1)) or (sbt2 == "Acid oxide" and not is_metal(formula1))) and elements2[0]==formula1:
                    return "O2"
                elif sbt2 == "Salt":
                    if elements1[0]!=elements2[0]: return
                    from random import choice
                    acid_residue = has_acid_residue(formula2)
                    if formula1=="Cu":
                        metal = list(i for i in ARM[ARM.index("Cu")+1:] if is_metal(i))
                    else:
                        metal = metals.copy()
                        metal.pop("Cu")
                    metal = choice(list(metal))
                    return balance_formula(metal+acid_residue, {metal: get_element_valence(metal)})
            case "Acid oxide":
                if sbt2=="Acid" and formula2 == get_acid_by_oxide(formula1): return "H2O"
            case "Base oxide":
                if sbt2 == "Base" and elements1[0] == elements2[0]: return "H2O"
            case "Base":
                if sbt2=="Salt" and elements1[0]==elements2[0]:
                    if not is_soluble(formula1): return
                    return balance_formula("H"+has_acid_residue(formula2), {})
            case "Acid":
                if sbt2=="Salt":
                    if has_acid_residue(formula1)!=has_acid_residue(formula2): return
                    from random import choice
                    res = [elements2[0]]
                    if is_soluble(elements2[0], "OH"): res.append(balance_formula(elements2[0]+"OH", get_valence_from_formula(formula2)))
                    return choice(res)
            case "Salt":
                from random import choice
                match sbt2:
                    case "Simple metal":
                        if elements1[0]!=elements2[0]: return formula2
                    case "Base":
                        metal = choice(list(i for i in metals if is_soluble(i, "OH")))
                        return balance_formula(metal+"OH", {metal: get_element_valence(metal)})
                    case "Acid":
                        if has_acid_residue(formula1)==has_acid_residue(formula2): return choice(acids)

    res = {}
    for i in range(len(formulas)-1):
        if not (formula:=get_second_reactant(formulas[i], formulas[i+1])): 
            raise ReactionError(f"Неможливо отримати {formulas[i+1]} з {formulas[i]}")
        res[formulas[i+1]] = reaction(formulas[i], formula, balanced)
    return res


def electrolytic_dissociation(electrolytic: str, get_ion_amount: bool = False, products_only: bool = False, result_only: bool = True, ignore_not_dec_sbt: bool = False, balance_not_dec_sbt: bool = True) -> str | list[str] | tuple[str | list[str], str] | tuple[str | list[str], dict[str, int]] | tuple[str | list[str], str, dict[str, int]]:
    parsed, first_mult = parse(electrolytic, ignore_first_multiplier=True), parse(electrolytic, get_first_mult=True)
    res, elems = [], tuple(parsed)
    cations = anions = 0
    final_res = ""
    match substance_type(electrolytic):
        case "Base": 
            x = parsed["H"] if parsed["H"]>1 else ''
            res.append(final_res:=f"{electrolytic} -> {(cations:=first_mult*parsed[elems[0]] if first_mult!=1 else parsed[elems[0]] if parsed[elems[0]]!=1 else '')}{elems[0]}({x}+) + {(anions:=x*first_mult if x else first_mult if first_mult!=1 else '')}OH(-)")
            anions, cations = anions or 1, cations or 1
        case "Acid":
            if not ignore_not_dec_sbt and parse(electrolytic, remove_first_multiplier=True) in ("H2CO3", "H2SO3"): 
                res.append(final_res:=reaction(electrolytic, balanced=balance_not_dec_sbt).replace("=", "->"))
                if products_only: return final_res.split("->")[-1].strip() if not get_ion_amount else (final_res.split("->")[-1].strip(), None)
                if get_ion_amount: return (final_res, res, {"cations": cations, "anions": anions}) if not result_only else (final_res, {"cations": cations, "anions": anions})
                return (final_res, res) if not result_only else final_res
            acid_residue = get_elements(electrolytic, True)[-1]
            if parsed["H"]==1:
                x = parsed["H"] if parsed["H"]>1 else ''
                res.append(final_res:=f"{electrolytic} -><- {(cations:=first_mult*parsed['H'] if first_mult!=1 else '')}H(+) + {(anions:=first_mult*parsed[elems[1]] if first_mult!=1 else '')}{acid_residue}({x}-)")
                cations, anions = cations or 1, anions or 1
            else:
                charge = 1
                h = parsed["H"]
                el = f"{electrolytic} -><- {(cations:=first_mult*h)}H(+) + {(anions:=first_mult*parsed[elems[1]] if first_mult!=1 else '')}{acid_residue}"
                while parsed["H"]>1:
                    x = parsed["H"] if parsed["H"]>1 else ''
                    res.append(f"{electrolytic} -><- H(+) + H{parsed['H']-1 if parsed['H']-1>1 else ''}{acid_residue}({charge if charge>1 else ''}-)")
                    electrolytic = f"H{parsed['H']-1 if parsed['H']-1>1 else ''}{acid_residue}({charge if charge>1 else ''}-)"
                    parsed["H"]-=1
                    charge+=1
                res.append(f"{electrolytic} -><- H(+) + {acid_residue}({charge if charge>1 else ''}-)")
                final_res, anions = f"{el}({charge if charge>1 else ''}-)", anions or 1
        case "Salt":
            x, y = parsed[elems[0]] if parsed[elems[0]]>1 else '', parsed[elems[1]] if parsed[elems[1]]>1 else ''
            res.append(final_res:=f"{electrolytic} -> {(cations:=x*first_mult if x else first_mult if first_mult!=1 else '')}{elems[0]}({y}+) + {(anions:=y*first_mult if y else  first_mult if first_mult!=1 else '')}{get_elements(electrolytic, True)[-1]}({x}-)")
            cations, anions = cations or 1, anions or 1
    if not res: raise ReactionError("Does not decompose")
    if products_only:
        res = list(map(lambda substance: substance.split("-><-" if "-><-" in substance else "->")[-1].strip(), res))
        final_res = final_res.split("-><-" if "-><-" in final_res else "->")[-1].strip()
    if get_ion_amount:
        if result_only:
             return final_res, {"cations": cations, "anions": anions}     
        return final_res, res, {"cations": cations, "anions": anions}
    if result_only:
        return final_res
    return final_res, res


def get_type_by_ion_ratio(electrolytic: str) -> str:
    res = electrolytic_dissociation(electrolytic, True)[-1]
    if res["cations"]==res["anions"]: return "Neutral"
    return "Acidic" if res["cations"]>res["anions"] else "Alkaline"


def get_ion_equation(molecular_eq: str, full: bool = False, solve: bool = True, ignore_not_dec_sbt: bool = False) -> str | None:


    def substance_check(substance: str) -> bool:
        if not (sbt:=substance_type(substance)) in ("Acid", "Base", "Salt"): return False
        return is_soluble((elems:=get_elements(substance, sbt in ("Acid", "Salt")))[0], "".join(elems[1:]))


    molecular_eq = equation(molecular_eq) if solve else molecular_eq
    react_formulas, prod_formulas = molecular_eq.split(flag:="->" if "->" in molecular_eq else "=")
    react_formulas, prod_formulas = get_formulas(react_formulas), get_formulas(prod_formulas)
    get_eq = lambda formulas: " + ".join(map(lambda substance: electrolytic_dissociation(substance, products_only=True, ignore_not_dec_sbt=ignore_not_dec_sbt, balance_not_dec_sbt=flag=="=") if substance_check(substance) else substance, formulas))
    if full: return f"{get_eq(react_formulas)} -> {get_eq(prod_formulas)}"
    from ..types import OrderedSet
    replace = lambda string: re.sub(r'\+(?=[^()]*\(|[^()]*$)', '', string)
    react, prod = OrderedSet(replace(get_eq(react_formulas)).split()), OrderedSet(replace(get_eq(prod_formulas)).split())
    return res if (res:=f"{' + '.join(react - prod)} -> {' + '.join(prod - react)}").strip().replace("->", "") else None