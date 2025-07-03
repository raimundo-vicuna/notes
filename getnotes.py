import json
from getFile import do

data = do()

nombres = data["nombre"]
eshija = data["eshija"]
ponderaciones_raw = data.get("ponderacion", [])
ordengeneral = data["ordengeneral"]
parciales = [data.get(f"parcial{i}", []) for i in range(1, 7)]

def safe_float(val):
    try:
        return float(val.replace(",", "."))
    except:
        return None

materias = {}
madre_actual = None

for idx, nombre in enumerate(nombres):
    if eshija[idx] == "0":
        madre_actual = nombre
        materias[madre_actual] = {}
        continue

    if madre_actual is None:
        continue

    ponderacion_str = ponderaciones_raw[idx].strip()
    try:
        ponderacion = int(ponderacion_str)
    except:
        continue

    nombre_lower = nombre.lower()
    if "paes" in nombre_lower:
        tipo = "paes"
    elif "control" in nombre_lower:
        tipo = "controles"
    else:
        tipo = "pruebas" if ponderacion >= 40 else "controles"

    notas = []
    for parcial in parciales:
        if idx < len(parcial):
            nota_str = parcial[idx].strip()
            if nota_str:
                nota = safe_float(nota_str)
                if nota is not None:
                    notas.append(nota)

    if notas:
        if tipo not in materias[madre_actual]:
            materias[madre_actual][tipo] = {
                "ponderacion": 0,
                "notas": []
            }
        materias[madre_actual][tipo]["notas"].extend(notas)
        materias[madre_actual][tipo]["ponderacion"] += ponderacion

for idx, nombre in enumerate(nombres):
    if eshija[idx] == "0" and not materias.get(nombre):
        notas = []
        for parcial in parciales:
            if idx < len(parcial):
                nota_str = parcial[idx].strip()
                if nota_str:
                    nota = safe_float(nota_str)
                    if nota is not None:
                        notas.append(nota)
        if notas:
            materias[nombre] = {
                "pruebas": {
                    "ponderacion": 100,
                    "notas": notas
                }
            }

for mat in materias.values():
    for tipo in mat.values():
        if tipo["ponderacion"] > 100:
            tipo["ponderacion"] = 100


