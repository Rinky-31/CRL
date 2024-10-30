metals = {
    "Li": 1,
    "Na": 1,
    "K": 1,
    "Cu": None,
    "Rb": 1,
    "Ag": None,
    "Cs": 1,
    "Au": None,
    "Fr": 1,
    "Rg": None,
    "Be": 2,
    "Mg": 2,
    "Ca": 2,
    "Zn": 2,
    "Sr": 2,
    "Cd": None,
    "Ba": 2,
    "Hg": None,
    "Ra": 2,
    "Cn": None,
    "Al": 3,
    "Sc": 3,
    "Ga": 3,
    "Y": 3,
    "In": 3,
    "La": 3,
    "Tl": None,
    "Ac": 3,
    "Nh": None,
    "Ti": 3,
    "Ge": 3,
    "Mn": None,
    "Fe": None,
    "Ni": None,
    "Pb": None
}
not_metals = {
    "H": 1,
    "C": None,
    "N": None,
    "P": None,
    "O": 2,
    "S": None,
    "Cl": None,
    "Si": None,
    "Br": None,
    "F": 1,
    "I": None

}
insoluble = {
    "OH": {"elements": ["Mg", "Al", "Cr", "Mn", "Fe", "Ni", "Cu", "Zn", "Cd", "Ag", "Pb", "Sn", "Hg","Au"], "valence": 1},
    "F": {"elements": ["Ca"], "valence": 1},
    "Cl": {"elements": ["Ag"], "valence": 1},
    "Br": {"elements": ["Ag"], "valence": 1},
    "I": {"elements": ["Ag", "Hg"], "valence": 1},
    "CO3": {"elements": ["Ca", "Sr", "Ba", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Cd", "Ag", "Pb", "Hg"], "valence": 2},
    "SiO3": {"elements": ["H", "Ca", "Sr", "Ba", "Al", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ag", "Pb", "Hg"], "valence": 2},
    "NO2": {"elements": [], "valence": 1},
    "NO3": {"elements": [], "valence": 1},
    "PO3": {"elements": ["Mg", "Ca", "Sr", "Ba", "Al", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Cd", "Ag", "Pb"], "valence": 1},
    "PO4": {"elements": ["Mg", "Ca", "Sr", "Ba", "Al", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Cd", "Ag", "Pb", "Sn", "Hg"], "valence": 3},
    "S": {"elements": ["Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Cd", "Ag", "Pb", "Sn", "Hg", "Au"], "valence": 2},
    "SO3": {"elements": ["Ca", "Sr", "Ba", "Mn", "Co", "Ni", "Cu", "Pb"], "valence": 2},
    "SO4": {"elements": ["Ba", "Ag"], "valence": 2}

}
ARM = ["Li", "K", "Cs", "Ba", "Sr", "Ca", "Na", "Mg", "Be", "Al", "Ti", "Mn", "Zn","Cr", "Fe", "Cd", "Co", "Ni", "Sn", "Pb", "H2","Bi", "Cu", "Ag", "Hg", "Pt", "Au"]
acid_oxyds = {
    "P2O5": "H3PO4",
    "P2O3": "H3PO3",
    "CO2": "H2CO3",
    "SO2": "H2SO3",
    "SO3": "H2SO4",
    "N2O5": "HNO3",
    "N2O3": "HNO2",
    "SiO2": "H2SiO3"
}
oxyds_acid = {v: k for k, v in acid_oxyds.items()}
valences_group = {
    "Fe": (2, 3),
    "Co": (2, 3),
    "Ni": (2, 3),
    "C": (2, 4),
    "Sn": (2, 4),
    "Pb": (2, 4),
    "P": (3, 5),
    "Cr": (2, 3, 6),
    "S": (2, 4, 6),
    "Cl": (2, 4),
    "Br": (2, 4),
    "Ag": (1, 2),
    "Cu": (1, 2),
    "I": (1, 3, 5, 7),
    "Si": (2, 4),
    #"Mn": (2, 4, 7)
}
alkans = [
    "CH4",
    "C2H6",
    "C3H8",
    "C4H10",
    "C5H12",
    "C6H14",
    "C7H16",
    "C8H18",
    "C9H20",
    "C10H22",
    "C11H24",
    "C12H26",
    "C13H28",
    "C14H30",
    "C20H42"
]
acids = [
    "HNO3",
    "HNO2",
    "H2SO4",
    "HCl",
    "H2SO3",
    "H2CO3",
    "H2S",
    "H2SiO3",
    "H3PO4"
]