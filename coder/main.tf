# Fragmento para el template de Coder. Se integra al main.tf existente del equipo.
# Supone salida de red únicamente hacia GitHub.

variable "framework_repo" {
  description = "URL HTTPS del repo del framework"
  type        = string
  default     = "https://github.com/<ORG>/minos.git"
}

variable "framework_ref" {
  description = "Tag o SHA del framework. Pinear siempre; no usar main en equipos."
  type        = string
  default     = "v1.0.0"
}

# El repo se clona con submódulos: el catálogo de skills queda en .claude/skills
# y Claude Code lo descubre solo. No hay descarga fuera de GitHub.
resource "coder_script" "framework_bootstrap" {
  agent_id           = coder_agent.main.id
  display_name       = "Framework SDLC agéntico"
  icon               = "/icon/git.svg"
  run_on_start       = true
  start_blocks_login = false

  script = <<-EOT
    set -euo pipefail
    DEST="$HOME/minos"

    if [ ! -d "$DEST/.git" ]; then
      git clone --recurse-submodules --branch "${var.framework_ref}" \
        "${var.framework_repo}" "$DEST"
    else
      cd "$DEST" && git fetch --tags && git checkout "${var.framework_ref}"
    fi

    cd "$DEST"
    ./scripts/bootstrap.sh
  EOT
}

# Nota sobre el rol devops: no le des credenciales productivas a este template.
# Crea un template aparte (p. ej. "sdlc-deploy") con esas credenciales y una
# allowlist de red más estrecha. El aislamiento debe venir de la infraestructura,
# no del prompt del agente.
