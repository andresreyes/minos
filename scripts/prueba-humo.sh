#!/usr/bin/env bash
# Comprueba que el andamiaje responde: contratos válidos, scripts ejecutables,
# constitución exigible, validadores capaces de aceptar y de rechazar.
# Correr tras clonar y tras cualquier cambio en contratos/.
set -uo pipefail
cd "$(dirname "$0")/.."

OK=0; FALLO=0
chk() { if [ "$1" -eq 0 ]; then echo "  [ok]    $2"; OK=$((OK+1));
        else echo "  [FALLA] $2"; FALLO=$((FALLO+1)); fi; }

echo "Prueba de humo — framework SDLC agéntico"
echo "========================================"

echo "Estructura"
for f in constitucion.md contratos/gates.yaml contratos/roles.yaml \
         contratos/handoff.schema.json contratos/esquemas/afirmaciones.schema.json \
         contratos/esquemas/verificacion.schema.json; do
  [ -f "$f" ]; chk $? "$f"
done
[ -d roles ] && [ "$(ls -1 roles/*.md 2>/dev/null | wc -l)" -ge 7 ]; chk $? "roles/ con 7+ definiciones"

echo "Catálogo de skills"
if [ -f .claude/skills/VERSION ]; then
  chk 0 "submódulo montado (v$(cat .claude/skills/VERSION))"
else
  echo "  [aviso] catálogo no montado — corre: git submodule update --init"
fi

echo "Guías del catálogo"
if [ -f .claude/skills/FOUNDATIONS.md ]; then
  for g in FOUNDATIONS AUTHORING CONTEXT PRECISION; do
    [ -f ".claude/skills/$g.md" ]; chk $? "$g.md"
  done
else
  echo "  [aviso] catálogo no montado — las cuatro guías se verifican al montarlo"
fi

echo "JSON válido"
python3 -c "
import json,glob,sys
for f in glob.glob('contratos/**/*.json', recursive=True): json.load(open(f))
" 2>/dev/null; chk $? "todos los esquemas parsean"

echo "Constitución"
./scripts/verificar-constitucion.sh >/dev/null 2>&1; chk $? "exigible (todo artículo con gate)"

echo "Validador — acepta lo correcto"
./scripts/validar-salida.sh ejemplos/afirmaciones-constructor.json >/dev/null 2>&1
chk $? "afirmaciones válidas pasan"
./scripts/validar-salida.sh ejemplos/verificacion-constructor.json >/dev/null 2>&1
chk $? "veredictos válidos pasan"

echo "Validador — rechaza lo incorrecto"
T=$(mktemp -d)
cat > "$T/mal.json" <<'EOF'
{"id_orden":"ORD-999","rol":"constructor","fecha":"2026-08-13","afirmaciones":[
 {"id":"AF-01","tipo":"no_verificable","referencia":"criterio propio",
  "texto":"El diseño es solido y sigue buenas practicas","criticidad":"bloqueante"}]}
EOF
./scripts/validar-salida.sh "$T/mal.json" >/dev/null 2>&1
[ $? -ne 0 ]; chk $? "bloqueante no_verificable es rechazada"
rm -rf "$T"

echo "Gates"
./scripts/verificar-gates.sh >/dev/null 2>&1
[ $? -le 1 ]; chk $? "verificador de gates ejecuta"

echo "Adaptadores"
[ -f CLAUDE.md ] && [ -f AGENTS.md ]; chk $? "CLAUDE.md y AGENTS.md presentes"
grep -q "GENERADO por scripts/generar-adaptadores.sh" CLAUDE.md 2>/dev/null; chk $? "CLAUDE.md marcado como generado"

echo "========================================"
echo "$OK correcto(s), $FALLO fallo(s)"
[ "$FALLO" -eq 0 ] || exit 1
echo "Listo para usar. Empieza con: /iniciar <tu solicitud>"
