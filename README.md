# cleo-secure

Skills de seguridad, OSINT y arquitectura defensiva.

## Skills

| Skill | Qué hace |
|---|---|
| [`skills/attacker`](skills/attacker) | Pentest ofensivo. Recon pasivo/activo, fuzzing, enumeración de vulns, explotación, post-explotación, DDoS (verificación teórica únicamente). |
| [`skills/arquitecto`](skills/arquitecto) | Revisor de solo-lectura. Analiza código contra arquitectura, lógica de negocio, seguridad y deuda técnica. Emite veredicto APROBADO / CON CONDICIONES / RECHAZADO. |
| [`skills/investigador`](skills/investigador) | Investigación con método SIFT y validación de ideas. Triangulación de fuentes, verificación cruzada. |

## Seguridad / OSINT

```
security/
├── herramientas/osint-personas/   Módulo OSINT DNI + teléfono (CUIL, E.164, VoIP, dorks)
└── vault-obsidian/                Vault de conocimiento en Markdown
    ├── 01-Fundamentos/
    └── 07-Labs/Hallazgos/
```

## Estructura de skills

Cada skill es una carpeta con `SKILL.md` y frontmatter:

```yaml
---
name: attacker
description: ...
---
```

## Installación

Copiar la carpeta de la skill al directorio de skills de tu agente:

```bash
cp -r skills/attacker ~/.claude/skills/
```

## Alcance

El trabajo offensive se realiza **únicamente sobre sistemas propios o con autorización escrita explícita**. Los targets de laboratorio (puertos 5001-5009) son apps vulnerablesdeployadas localmente para práctica.
