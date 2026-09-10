#!/usr/bin/env bash
# Valida un archivo JSON contra su esquema y aplica las reglas semánticas
# que el esquema no puede expresar. Sin dependencias externas.
#
# Uso: ./scripts/validar-salida.sh <archivo.json> [esquema.json]
#      Si se omite el esquema, se deduce del contenido.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - "$@" <<'PY'
import json, sys, pathlib

archivo = pathlib.Path(sys.argv[1])
datos = json.loads(archivo.read_text())

if len(sys.argv) > 2:
    ruta_esq = pathlib.Path(sys.argv[2])
elif "afirmaciones" in datos:
    ruta_esq = pathlib.Path("contratos/esquemas/afirmaciones.schema.json")
elif "veredictos" in datos:
    ruta_esq = pathlib.Path("contratos/esquemas/verificacion.schema.json")
else:
    print("No puedo deducir el esquema: pásalo como segundo argumento."); sys.exit(1)

esq = json.loads(ruta_esq.read_text())
errores = []

def validar(dato, esquema, ruta="$"):
    t = esquema.get("type")
    if t == "object":
        if not isinstance(dato, dict):
            errores.append(f"{ruta}: se esperaba objeto"); return
        for req in esquema.get("required", []):
            if req not in dato:
                errores.append(f"{ruta}: falta el campo requerido '{req}'")
        props = esquema.get("properties", {})
        if esquema.get("additionalProperties") is False:
            for k in dato:
                if k not in props:
                    errores.append(f"{ruta}.{k}: campo no permitido")
        for k, v in dato.items():
            if k in props:
                validar(v, props[k], f"{ruta}.{k}")
    elif t == "array":
        if not isinstance(dato, list):
            errores.append(f"{ruta}: se esperaba arreglo"); return
        if len(dato) < esquema.get("minItems", 0):
            errores.append(f"{ruta}: mínimo {esquema['minItems']} elemento(s)")
        for i, v in enumerate(dato):
            validar(v, esquema.get("items", {}), f"{ruta}[{i}]")
    elif t == "string":
        if not isinstance(dato, str):
            errores.append(f"{ruta}: se esperaba texto"); return
        if "enum" in esquema and dato not in esquema["enum"]:
            errores.append(f"{ruta}: '{dato}' no está en {esquema['enum']}")
        if len(dato) < esquema.get("minLength", 0):
            errores.append(f"{ruta}: demasiado corto (mínimo {esquema['minLength']})")
        if "pattern" in esquema:
            import re as _re
            if not _re.match(esquema["pattern"], dato):
                errores.append(f"{ruta}: '{dato}' no cumple el patrón {esquema['pattern']}")
    elif t == "integer":
        if not isinstance(dato, int) or isinstance(dato, bool):
            errores.append(f"{ruta}: se esperaba entero")

validar(datos, esq)

# --- Reglas semánticas que el esquema no expresa ---
if "afirmaciones" in datos:
    vistos = set()
    for a in datos.get("afirmaciones", []):
        if not isinstance(a, dict): continue
        i = a.get("id")
        if i in vistos: errores.append(f"afirmación {i}: id duplicado")
        vistos.add(i)
        # Lo bloqueante tiene que poder comprobarse.
        if a.get("criticidad") == "bloqueante" and a.get("tipo") == "no_verificable":
            errores.append(f"{i}: no_verificable no puede ser bloqueante")
        if a.get("tipo") == "codigo" and ":" not in str(a.get("referencia", "")):
            errores.append(f"{i}: tipo 'codigo' exige referencia con formato ruta:linea")

if "veredictos" in datos:
    for v in datos.get("veredictos", []):
        if not isinstance(v, dict): continue
        a = v.get("afirmacion")
        if v.get("veredicto") == "CORREGIDO" and "correccion" not in v:
            errores.append(f"{a}: veredicto CORREGIDO exige el objeto 'correccion'")
        if v.get("veredicto") != "CORREGIDO" and "correccion" in v:
            errores.append(f"{a}: 'correccion' solo aplica a CORREGIDO")
    c = datos.get("cobertura")
    if c and c.get("bloqueantes_verificadas", 0) < c.get("bloqueantes_totales", 0):
        errores.append(
            f"cobertura: {c['bloqueantes_verificadas']}/{c['bloqueantes_totales']} "
            "bloqueantes verificadas. Deben verificarse todas.")

if errores:
    print(f"INVÁLIDO ({len(errores)}):")
    for e in errores: print(f"  - {e}")
    sys.exit(1)
print(f"VÁLIDO: {archivo} contra {ruta_esq.name}")
PY
