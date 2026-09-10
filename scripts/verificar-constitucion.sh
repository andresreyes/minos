#!/usr/bin/env bash
# Comprueba que la constitución sea exigible: cada artículo nombra gates y esos
# gates existen. Un artículo sin gate es decoración; este script lo impide.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - <<'PY'
import pathlib, re, sys

c = pathlib.Path("constitucion.md").read_text()
g = pathlib.Path("contratos/gates.yaml").read_text()

existentes = set(re.findall(r"^  ([A-Z][A-Za-z0-9_]*):\s*$", g, re.M))
articulos = re.findall(r"^## (Artículo \d+ — .+?)$(.*?)(?=^## |\Z)", c, re.M | re.S)

if not articulos:
    print("ERROR: no se encontró ningún artículo en constitucion.md"); sys.exit(1)

errores = []
print(f"Constitución: {len(articulos)} artículo(s) · {len(existentes)} gates definidos")
print("-" * 72)

for titulo, cuerpo in articulos:
    m = re.search(r"^\*\*Gates\.\*\*\s*(.+)$", cuerpo, re.M)
    if not m:
        errores.append(f"{titulo}: no nombra ningún gate")
        print(f"[HUÉRFANO] {titulo}")
        continue
    citados = re.findall(r"`([A-Za-z0-9_]+)`", m.group(1))
    if not citados:
        errores.append(f"{titulo}: la línea Gates no cita ninguno")
        print(f"[HUÉRFANO] {titulo}")
        continue
    faltan = [x for x in citados if x not in existentes]
    if faltan:
        errores.append(f"{titulo}: gate(s) inexistente(s): {', '.join(faltan)}")
        print(f"[ROTO]     {titulo} → {', '.join(faltan)}")
    else:
        print(f"[ok]       {titulo.split(' — ')[0]:14s} {len(citados)} gate(s)")

    for sec in ("**Principio.**", "**Por qué.**", "**Prohíbe.**"):
        if sec not in cuerpo:
            errores.append(f"{titulo}: falta la sección {sec}")

print("-" * 72)
if errores:
    print(f"CONSTITUCIÓN NO EXIGIBLE ({len(errores)}):")
    for e in errores: print(f"  - {e}")
    sys.exit(1)
print("Constitución exigible: todos los artículos tienen gate que los comprueba.")
PY
