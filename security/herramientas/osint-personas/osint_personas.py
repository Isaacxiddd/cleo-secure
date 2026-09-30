#!/usr/bin/env python3
"""
Módulo OSINT defensivo para identificar personas por DNI o número telefónico.

MÓDULO 1: Derivar CUIL/CUIT a partir de un DNI (algoritmo Módulo 11).
MÓDULO 2: Normalizar/analizar un número telefónico (formato E.164, tipo, región).
MÓDULO 3: Generar permutaciones de búsqueda (Google Dorking) para un número.

USO LEGÍTIMO: verificación de identidad, prevención de fraude, respuesta a incidentes.
NO usar para acoso, doxxing o actividades ilegales (Ley 25.326, Código Penal AR).

Dependencias: pip install phonenumbers   (opcional; el Módulo 1 no requiere nada)
"""
import sys

try:
    import phonenumbers
    _HAVE_PHONENUMBERS = True
except ImportError:
    _HAVE_PHONENUMBERS = False
    phonenumbers = None


# ---------------------------------------------------------------------------
# MÓDULO 1 — CUIL/CUIT desde DNI
# ---------------------------------------------------------------------------

def _digito_verificador(prefijo: int, dni: int) -> int:
    """Algoritmo Módulo 11 de CUIL/CUIT argentino."""
    multiplicadores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    base = f"{prefijo:02d}{dni:08d}"
    if len(base) != 10:
        raise ValueError("DNI debe tener hasta 8 dígitos")
    suma = sum(int(d) * m for d, m in zip(base, multiplicadores))
    resto = suma % 11
    if resto == 0:
        return 0
    if resto == 1:
        return 9  # caso de corrección (aplica sólo a ciertos prefijos)
    return 11 - resto


def cuil_para_dni(dni: int, sexo: str = "M") -> str:
    """
    Genera CUIL a partir de DNI y sexo.
    sexo: M (hombre) -> 20, F (mujer) -> 27.
    """
    prefijo = 20 if sexo.upper() == "M" else 27
    dv = _digito_verificador(prefijo, dni)
    return f"{prefijo:02d}-{dni:08d}-{dv}"


def validar_cuil(cuil: str) -> bool:
    """Valida un CUIL/CUIT contra el dígito verificador."""
    limpio = cuil.replace("-", "").replace(" ", "")
    if len(limpio) != 11 or not limpio.isdigit():
        return False
    prefijo = int(limpio[:2])
    body = int(limpio[2:10])
    dv = int(limpio[10])
    return _digito_verificador(prefijo, body) == dv


# ---------------------------------------------------------------------------
# MÓDULO 2 — Análisis de número telefónico
# ---------------------------------------------------------------------------

def analizar_numero(numero: str, region: str = "AR") -> dict:
    """Normaliza y analiza un número telefónico. Devuelve dict con metadatos."""
    if not _HAVE_PHONENUMBERS:
        return {"error": "Instalá 'phonenumbers': pip install phonenumbers"}

    n = phonenumbers.parse(numero, region)
    es_valido = phonenumbers.is_valid_number(n)
    tipo = phonenumbers.number_type(n)

    tipos = {
        phonenumbers.PhoneNumberType.MOBILE: "MOBILE",
        phonenumbers.PhoneNumberType.FIXED_LINE: "FIXED_LINE",
        phonenumbers.PhoneNumberType.VOIP: "VOIP",
        phonenumbers.PhoneNumberType.UNKNOWN: "UNKNOWN",
    }

    return {
        "e164": phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164),
        "nacional": phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.NATIONAL),
        "region": phonenumbers.region_code_for_number(n),
        "valido": es_valido,
        "tipo_linea": tipos.get(tipo, "?"),
        "advertencia_burner": tipos.get(tipo) in (
            phonenumbers.PhoneNumberType.VOIP,
            phonenumbers.PhoneNumberType.UNKNOWN,
        ),
    }


# ---------------------------------------------------------------------------
# MÓDULO 3 — Permutaciones de búsqueda (Google Dorking)
# ---------------------------------------------------------------------------

def permutaciones_busqueda(e164: str) -> list:
    """Genera variantes del número para búsquedas exactas en buscadores.

    Ejemplo de entrada: +5434214333  (formato E.164 completo)
    """
    numeros = "".join(ch for ch in e164 if ch.isdigit())
    # Quita el código de país (54) asumiendo entrada E.164
    nacion = numeros[2:] if numeros.startswith("54") else numeros
    variantes = set()

    if len(nacion) == 10:  # 3 (área) + 7 (abonado), formato AR
        area, abonado = nacion[:3], nacion[3:]
        ab3, ab4 = abonado[:3], abonado[3:]
        variantes.update({
            f"{area}-{ab3}-{ab4}",
            f"{area} {ab3} {ab4}",
            f"({area}) {ab3}-{ab4}",
            f"{area} {abonado}",
        })
        # Añade el 15 del celular
        variantes.add(f"{area} 15 {ab3} {ab4}")

    variantes.add(nacion)
    variantes.add(numeros)
    variantes.add(e164)
    return sorted(variantes)


def dorks(numero: str, region: str = "AR") -> list:
    """Devuelve dorks listos para Google/Bing/DuckDuckGo."""
    meta = analizar_numero(numero, region)
    if "error" in meta:
        return [meta["error"]]
    variantes = permutaciones_busqueda(meta["e164"])
    salida = [f'"{v}"' for v in variantes]
    salida += [f'site:linkedin.com "{v}"' for v in variantes[:3]]
    salida += [f'site:facebook.com "{v}"' for v in variantes[:3]]
    return salida


# ---------------------------------------------------------------------------
# MAIN (CLI)
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python osint_personas.py cuil <DNI> [M|F]")
        print("  python osint_personas.py valida <CUIL>")
        print("  python osint_personas.py tel <numero> [region=AR]")
        print("  python osint_personas.py dorks <numero> [region=AR]")
        return

    cmd = sys.argv[1].lower()

    if cmd == "cuil":
        dni = int(sys.argv[2])
        sexo = sys.argv[3].upper() if len(sys.argv) > 3 else "M"
        print("CUIL:", cuil_para_dni(dni, sexo))
    elif cmd == "valida":
        print("Válido:", validar_cuil(sys.argv[2]))
    elif cmd == "tel":
        import json
        print(json.dumps(analizar_numero(sys.argv[2],
                        sys.argv[3] if len(sys.argv) > 3 else "AR"),
                        indent=2))
    elif cmd == "dorks":
        for d in dorks(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "AR"):
            print(d)


if __name__ == "__main__":
    main()
