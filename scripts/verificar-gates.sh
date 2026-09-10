#!/usr/bin/env bash
# Verifica los gates del handoff más reciente contra contratos/gates.yaml.
# Sin dependencias externas: solo python3 de la librería estándar.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - "$@" <<'PY'
import json, pathlib, re, sys

hs = sorted(pathlib.Path("handoffs").glob("*.json"))
if not hs:
    print("No hay handoffs. Empieza con /iniciar."); sys.exit(0)
h = json.loads(hs[-1].read_text())

# Lectura mínima de gates.yaml sin PyYAML: nombre, activo_si, anulable.
texto = pathlib.Path("contratos/gates.yaml").read_text()
gates, actual = {}, None
for linea in texto.splitlines():
    m = re.match(r"^  ([A-Z0-9][A-Za-z0-9_]*):\s*$", linea)
    if m:
        actual = m.group(1); gates[actual] = {}
        continue
    if actual:
        m = re.match(r"^    (activo_si|anulable|rol):\s*(\S+)", linea)
        if m:
            gates[actual][m.group(1)] = m.group(2)

# Cadena de roles del tipo de trabajo, desde roles.yaml.
roles_txt = pathlib.Path("contratos/roles.yaml").read_text()
cadenas, tipo_actual = {}, None
for linea in roles_txt.splitlines():
    m = re.match(r"^  ([a-z_]+):\s*$", linea)
    if m:
        tipo_actual = m.group(1); continue
    m = re.match(r"^    cadena:\s*\[(.*)\]", linea)
    if m and tipo_actual:
        cadenas[tipo_actual] = [r.strip() for r in m.group(1).split(",")]
cadena = set(cadenas.get(h.get("tipo", ""), [])) | {"lider-tecnico"}

orden = {"ninguno": 0, "indirecto": 1, "directo": 2}
impacto = h.get("impacto", "directo")
nivel = orden.get(impacto, 2)

def exigido(activo_si):
    if activo_si == "siempre": return True
    return nivel >= orden.get(activo_si, 2)

estado = {g["id"]: g for g in h.get("gates", [])}
anulados = {a["gate"] for a in h.get("anulaciones", [])}

print(f"Orden {h['id']}  impacto={impacto}  emisor={h['rol_emisor']} -> destino={h.get('rol_destino')}")
print("-" * 72)
fallos = 0
for nombre, meta in gates.items():
    if not exigido(meta.get("activo_si", "siempre")):
        continue
    if cadena and meta.get("rol") not in cadena:
        continue  # rol fuera de la cadena de este tipo de trabajo
    g = estado.get(nombre)
    if nombre in anulados:
        if meta.get("anulable") == "false":
            print(f"[BLOQUEA] {nombre:32s} anulado pero NO es anulable"); fallos += 1
        else:
            print(f"[anulado] {nombre:32s} con motivo registrado")
        continue
    if not g:
        print(f"[pendiente] {nombre:32s} lo cierra: {meta.get('rol','?')}"); fallos += 1
    elif g["estado"] == "aprobado":
        print(f"[ok]      {nombre:32s} {g['evidencia'][:30]}")
    elif g["estado"] == "no_aplica":
        just = len(g.get("evidencia", "")) >= 20
        print(f"[{'n/a' if just else 'BLOQUEA'}]     {nombre:32s} "
              f"{'justificado' if just else 'no_aplica SIN justificación'}")
        fallos += 0 if just else 1
    else:
        print(f"[RECHAZA] {nombre:32s} {g['evidencia'][:30]}"); fallos += 1

if h.get("bloqueos"):
    print("-" * 72)
    for b in h["bloqueos"]:
        print(f"[BLOQUEO] {b}")
    fallos += len(h["bloqueos"])

print("-" * 72)
print("La cadena PUEDE avanzar." if fallos == 0 else f"La cadena NO avanza: {fallos} condición(es) sin resolver.")
sys.exit(0 if fallos == 0 else 1)
PY
