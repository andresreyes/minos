#!/usr/bin/env bash
# Comprueba SIN GASTAR TOKENS que cada referencia de un archivo de afirmaciones
# resuelve: el archivo existe, la línea existe, el comando es ejecutable.
#
# Es el ahorro más grande del framework: cada comprobación que hace este script
# es una que el verificador ya no tiene que hacer leyendo. El juicio queda para
# el agente; la aritmética, aquí.
#
# Uso: ./scripts/resolver-referencias.sh evidencia/afirmaciones/<archivo>.json
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - "${1:?falta el archivo de afirmaciones}" <<'PY'
import json, pathlib, sys, shutil, re

d = json.loads(pathlib.Path(sys.argv[1]).read_text())
rotas, ok, juicio = [], 0, []

for a in d.get("afirmaciones", []):
    i, tipo, ref = a.get("id"), a.get("tipo"), str(a.get("referencia",""))

    if tipo == "codigo":
        m = re.match(r"^(.+?):(\d+)$", ref)
        if not m:
            rotas.append(f"{i}: referencia sin formato ruta:linea → {ref}"); continue
        ruta, ln = pathlib.Path(m.group(1)), int(m.group(2))
        if not ruta.exists():
            rotas.append(f"{i}: el archivo no existe → {ruta}"); continue
        lineas = ruta.read_text(errors="replace").splitlines()
        if ln < 1 or ln > len(lineas):
            rotas.append(f"{i}: línea {ln} fuera de rango (el archivo tiene {len(lineas)})"); continue
        ok += 1
        juicio.append((i, f"{ruta}:{ln}", lineas[ln-1].strip()[:90]))

    elif tipo == "archivo":
        p = pathlib.Path(ref)
        if not p.exists():
            rotas.append(f"{i}: el archivo no existe → {ref}")
        else:
            ok += 1; juicio.append((i, ref, f"({p.stat().st_size} bytes)"))

    elif tipo == "comando":
        binario = ref.split()[0] if ref.split() else ""
        if binario and not shutil.which(binario) and not pathlib.Path(binario).exists():
            rotas.append(f"{i}: el ejecutable no está disponible → {binario}")
        else:
            ok += 1; juicio.append((i, ref, "(ejecutable presente; ejecutarlo es del verificador)"))

    elif tipo == "contrato":
        p = pathlib.Path(ref.split("#")[0])
        if not p.exists():
            rotas.append(f"{i}: el esquema no existe → {p}")
        else:
            ok += 1; juicio.append((i, ref, "(esquema presente)"))

    else:
        juicio.append((i, ref, f"(tipo {tipo}: solo el agente puede valorarlo)"))

print(f"Referencias resueltas: {ok}  ·  rotas: {len(rotas)}")
print("-"*72)
for r in rotas: print(f"  [ROTA] {r}")
if rotas:
    print("-"*72)
    print("Estas se devuelven al autor SIN invocar al verificador: una referencia que")
    print("no resuelve ya es CORREGIDO o RECHAZADO, y comprobarlo cuesta cero tokens.")
    sys.exit(1)

print("Contenido para el verificador (ya extraído; no necesita releer los archivos):")
for i, donde, cont in juicio:
    print(f"  {i}  {donde}")
    print(f"      {cont}")
print("-"*72)
print("Todas resuelven. Al verificador le queda el juicio, no la búsqueda.")
PY
