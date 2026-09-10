#!/usr/bin/env bash
# Prepara el workspace. Idempotente: se puede correr en cada arranque.
# Requiere solo git y acceso a GitHub.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Resolviendo catálogo de skills (submódulo)"
if [ -d .git ] || git rev-parse --git-dir >/dev/null 2>&1; then
  git submodule sync --recursive
  git submodule update --init --recursive
else
  echo "    AVISO: esto no es un repo git todavía (¿lo descomprimiste de un ZIP?)."
  echo "           El catálogo de skills debe montarse como submódulo:"
  echo "           git init && git submodule add <url-del-catalogo> .claude/skills"
  echo "           Continúo sin él; el resto del andamiaje se verifica igual."
fi

SKILLS_DIR=".claude/skills"
if [ -f "$SKILLS_DIR/VERSION" ]; then
  echo "    catálogo v$(cat "$SKILLS_DIR/VERSION")"
  if git submodule status "$SKILLS_DIR" 2>/dev/null | grep -q '^+'; then
    echo "    AVISO: el submódulo NO está en el SHA pinneado por este repo."
    echo "           Alguien lo movió a mano. Corrige con: git submodule update --init"
  fi
else
  echo "    AVISO: catálogo de skills no montado en $SKILLS_DIR"
fi

echo "==> Verificando contratos"
python3 - <<'PY'
import json, sys, pathlib
p = pathlib.Path("contratos/handoff.schema.json")
json.loads(p.read_text())
print("    handoff.schema.json ok")
for f in ("contratos/gates.yaml", "contratos/roles.yaml"):
    if not pathlib.Path(f).exists():
        print(f"    ERROR: falta {f}", file=sys.stderr); sys.exit(1)
    print(f"    {f} presente")
PY

mkdir -p handoffs docs/{disenos,runbooks} \
  evidencia/{pruebas,seguridad,reversion,despliegue,afirmaciones,verificacion}

echo "==> Generando adaptadores de plataforma"
./scripts/generar-adaptadores.sh

echo "==> Verificando la constitución"
./scripts/verificar-constitucion.sh | tail -1

echo "==> Prueba de humo"
./scripts/prueba-humo.sh | tail -3

echo "==> Roles disponibles:"
ls roles/*.md | xargs -n1 basename | sed 's/\.md$//' | sed 's/^/    - /'
echo
echo "Empieza con:  /iniciar <tu solicitud>"
