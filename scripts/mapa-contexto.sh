#!/usr/bin/env bash
# Mapa de contexto de un rol: qué pieza, cuánto pesa, en qué zona.
# Implementa el presupuesto de contratos/contexto.yaml.
#
# Uso: ./scripts/mapa-contexto.sh <rol>     (sin argumento: todos)
set -uo pipefail
cd "$(dirname "$0")/.."

python3 - "${1:-}" <<'PY'
import pathlib, re, sys, glob

rol = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else None
roles = [rol] if rol else sorted(p.stem for p in pathlib.Path("roles").glob("*.md"))

cfg = pathlib.Path("contratos/contexto.yaml").read_text()
def num(clave, defecto):
    m = re.search(rf"^\s*{clave}:\s*(\d+)", cfg, re.M)
    return int(m.group(1)) if m else defecto
MAX_ANCLA = num("ancla_max_palabras", 4000)
MAX_TOOLS = num("herramientas_max", 20)

def palabras(p):
    f = pathlib.Path(p)
    return len(f.read_text(errors="replace").split()) if f.exists() else 0

for r in roles:
    print(f"\n=== {r} " + "="*(56-len(r)))
    piezas = [
        ("constitucion.md",          palabras("constitucion.md")),
        ("contratos/gates.yaml",     palabras("contratos/gates.yaml")),
        ("contratos/roles.yaml",     palabras("contratos/roles.yaml")),
        (f"roles/{r}.md",            palabras(f"roles/{r}.md")),
    ]
    skill = None
    for cand in glob.glob(f".claude/skills/*/SKILL.md"):
        meta = pathlib.Path(cand).read_text()[:400]
        nombre = re.search(r"^name:\s*(\S+)", meta, re.M)
        if nombre and (nombre.group(1) == r or nombre.group(1).startswith(r[:6])):
            skill = cand; break
    if skill:
        piezas.append((skill, palabras(skill)))
    else:
        piezas.append(("(skill del catálogo: no montado)", 0))

    ancla = sum(w for _, w in piezas)
    for nombre, w in piezas:
        pct = w/ancla*100 if ancla else 0
        print(f"  {nombre:44s} {w:>6} pal  {pct:5.1f}%")
    print(f"  {'ZONA ANCLA (se cachea)':44s} {ancla:>6} pal", end="")
    print(f"   [EXCEDE {MAX_ANCLA}]" if ancla > MAX_ANCLA else "   [ok]")

    rp = pathlib.Path(f"roles/{r}.md")
    if rp.exists():
        m = re.search(r"^tools:\s*(.+)$", rp.read_text(), re.M)
        if m:
            n = len([t for t in m.group(1).split(",") if t.strip()])
            print(f"  {'herramientas declaradas':44s} {n:>6}", end="")
            print(f"      [EXCEDE {MAX_TOOLS}]" if n > MAX_TOOLS else "      [ok]")

print("\n" + "-"*64)
print("El historial y los documentos recuperados (zona volumen) no se miden aquí:")
print("dependen de la sesión. Mídelos con el reporte de tokens de tu plataforma.")
print("\nPregunta de auditoría para cada línea de la zona ancla:")
print("  si quito esta línea, ¿cambia alguna respuesta? Si no cambia, sobra.")
PY
