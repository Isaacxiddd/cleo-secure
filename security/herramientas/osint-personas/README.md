# OSINT de Personas — Módulo DNI + Teléfono

Módulo defensivo para identificar personas a partir de **DNI** o **número telefónico**.

## Uso rápido

```bash
# 1. Derivar CUIL a partir de un DNI (no requiere dependencias)
python osint_personas.py cuil 34211433 M        # => 20-34211433-5
python osint_personas.py valida "20-34211433-5" # => True

# 2. Analizar un número telefónico (requiere: pip install phonenumbers)
python osint_personas.py tel "011 3421 4333" AR

# 3. Generar dorks de búsqueda para el número
python osint_personas.py dorks "011 3421 4333" AR
```

## Módulos
1. `cuil` — derivar CUIL/CUIT desde DNI (algoritmo Módulo 11).
2. `valida` — validar un CUIL contra su dígito verificador.
3. `tel` — normalizar a E.164, tipo de línea, región, detección de VoIP/burner.
4. `dorks` — permutaciones listas para Google/Bing/DuckDuckGo.

## Dependencias
- `phonenumbers` (opcional, para los módulos 2 y 3): `pip install phonenumbers`
- Módulo 1 (CUIL) funciona sin dependencias.

## Documentación
- Guía completa: `../vault-obsidian/01-Fundamentos/Modulo-OSINT-Personas-DNI-Telefono.md`
- Plantilla de hallazgo: `../vault-obsidian/07-Labs/Hallazgos/`

## Legal / Ética
Sólo para verificación de identidad, anti-fraude y respuesta a incidentes.
No usar para doxxing, acoso o acceso no autorizado (Ley 25.326 — datos personales).
