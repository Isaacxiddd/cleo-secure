# Hallazgo: 2026-08-31 - OSINT Persona [Ejemplo] en [Número/DNI]

> Plantilla de ejemplo. Reemplazá los datos por los reales de cada investigación.

## Resumen Ejecutivo
A partir de un número telefónico se identificó la identidad probable y su vinculación con redes sociales, con confianza media-alta (2 fuentes independientes).

## Cadena de Ataque
```
[Tel +54 11 XXXX-XXXX]
    ├─ E.164: +5411XXXXXXXX (fixed line)
    ├─ WhatsApp: foto de perfil + nombre "X"
    ├─ Google dorking: número en aviso de MercadoLibre (nombre "X", ciudad "Y")
    └─ Cross-ref: nombre coincide con CuitOnline (CUIL 20-XXXXXXXX-X)
        ⇒ Identidad: [Nombre Completo], [Provincia]
```

## Detalle Técnico
```bash
# Derivar CUIL desde DNI (si se tenía el DNI)
python osint_personas.py cuil <DNI> M

# Analizar el número
python osint_personas.py tel "011 XXXX XXXX" AR

# Generar dorks
python osint_personas.py dorks "011 XXXX XXXX" AR
```
Permutaciones buscadas (todas entre comillas, y con `site:` en LinkedIn/Facebook).

## Datos Expuestos
| Dato | Valor | Fuente | Confianza |
|------|-------|--------|-----------|
| Nombre | XXX | WhatsApp + CuitOnline + MercadoLibre | Alta (3 fuentes) |
| CUIL/CUIT | 20-XXXXXXXX-X | Derivado (mód. 11) + CuitOnline | Alta |
| Ciudad/Provincia | YYY | MercadoLibre + CuitOnline | Media |
| Email | xxx@yyy.com | Breach (IntelX) | Alta |
| Usuario Telegram | @xxx | Telegram | Media |

## Nivel de Confianza
**Media-Alta.** Nombre corroborado por ≥2 fuentes independientes (app de mensajería vista en vivo + récords públicos). No se atribuyó ninguna identidad de una fuente única.

## Remediación / Acción
[Ej: verificar identidad del solicitante contra récords oficiales antes de otorgar acceso; marcar el CUIL como sospechoso si hubo fraude.]

---
**Herramienta:** `security/herramientas/osint-personas/osint_personas.py`
**Guía:** `01-Fundamentos/Modulo-OSINT-Personas-DNI-Telefono.md`
