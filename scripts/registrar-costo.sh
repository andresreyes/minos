#!/usr/bin/env bash
# Registra el costo de un paso de la cadena. Una línea por invocación de rol.
# Campos alineados con la dirección de FOCUS/FinOps para gasto por tokens.
#
# Uso: ./scripts/registrar-costo.sh <id_orden> <rol> <tokens_in> <tokens_out> \
#        [tokens_cacheados] [modelo] [segundos]
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p metricas
F="metricas/costos.csv"
[ -f "$F" ] || echo "fecha,id_orden,rol,modelo,tokens_entrada,tokens_cacheados,tokens_salida,segundos,verificacion_activa" > "$F"

ID="${1:?falta id_orden}"; ROL="${2:?falta rol}"
IN="${3:-0}"; OUT="${4:-0}"; CACHE="${5:-0}"; MODELO="${6:-desconocido}"; SEG="${7:-0}"

VER=$(grep -A1 "verificacion_adversarial:" contratos/roles.yaml 2>/dev/null \
      | grep activa_desde_impacto | awk '{print $2}' || echo "?")

echo "$(date -Iseconds),$ID,$ROL,$MODELO,$IN,$CACHE,$OUT,$SEG,$VER" >> "$F"
echo "registrado: $ID/$ROL  entrada=$IN (cacheados=$CACHE) salida=$OUT"
