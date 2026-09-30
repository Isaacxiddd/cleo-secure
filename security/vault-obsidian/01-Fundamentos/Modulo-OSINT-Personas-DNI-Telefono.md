# OSINT de Personas: DNI y Número Telefónico

> **Propósito:** Módulo defensivo de Inteligencia de Fuentes Abiertas (OSINT) para identificar a una persona a partir de un **DNI** o un **número telefónico**, y evaluar el riesgo que representa para la seguridad de la organización.
>
> **Uso legítimo:** Esta información se usa para **verificación de identidad, prevención de fraude, investigación de amenazas y respuesta a incidentes**. NUNCA para acoso, doxxing o actividades ilegales.
>
> **Marco legal (AR):** Ley 25.326 de Protección de Datos Personales. Sólo se procesan datos de fuentes públicas o con finalidad legítima (periodística, académica, estadística o de seguridad).

---

## 1. Mentalidad Defensiva

Un atacante (o un defensor) puede partir de **dos semillas** mínimas:

| Semilla | Qué permite reconstruir |
|---------|------------------------|
| **DNI** (8 dígitos) | CUIL/CUIT, nombre completo, edad/DOB, padrones, obra social, empresa, estudios, boom en récords públicos. |
| **Número telefónico** (+54 11 ...) | Carrier, tipo de línea, apps de mensajería (WhatsApp/Telegram), redes sociales vinculadas, breaches, filtraciones, reputación spam. |

**Regla de oro del OSINT:** *cada hallazgo es un nuevo lead, no una meta final*. Un número genera un WhatsApp, el WhatsApp genera una foto, la foto genera un LinkedIn, el LinkedIn genera una empresa, etc.

---

## 2. Topología de Identificadores (Argentina)

### 2.1 DNI (Documento Nacional de Identidad)
- Formato: 8 dígitos (post-2012), ej: `34211433`
- Es la base para derivar el **CUIL/CUIT** (ver sección 3).
- Referencias cruzadas públicas:
  - `cuitonline.com` — ficha de persona (nombre, provincia, categoría fiscal)
  - Padrón Electoral (consulta por DNI)
  - `buscardatos.com` — indexa DNI + CUIT + teléfono (datos a veces viejos)
  - Afiliaciones, títulos, patentes, juicios (récords públicos)

### 2.2 CUIL / CUIT (identificador fiscal)
- Formato CUIL: `20-34211433-5` (2 dígitos prefijo + DNI + 1 dígito verificador)
- El prefijo indica tipo: `20/23` persona física, `24` mujer anterior, `27` nueva mujer, `30/33/34` empresa.
- **El prefijo + el DNI te permiten calcular el dígito verificador.**

### 2.3 Número telefónico
- Estándar internacional: **E.164** → `+54 11 1234-5678` (país 54, área + número)
- El prefijo 11/15 = AMBA, 351 = Córdoba, 341 = Rosario, 261 = Mendoza, etc.
- SIM/ESAIM: requiere identificación con DNI obligatoriamente (no se puede comprar anónima).

---

## 3. Derivar CUIL/CUIT desde el DNI (módulo de cálculo)

El dígito verificador del CUIL se calcula con el **algoritmo Módulo 11**. Llevarlo a script permite validar y generar CUILs a partir de DNI sin necesidad de consultar bases.

```python
def calcular_digito_verificador(prefijo: int, dni: int) -> int:
    """Algoritmo Módulo 11 para CUIL/CUIT argentino."""
    multiplicadores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    base = f"{prefijo:02d}{dni:08d}"
    suma = sum(int(d) * m for d, m in zip(base, multiplicadores))
    resto = suma % 11
    if resto == 0:
        return 0
    elif resto == 1:
        # Código de corrección: si prefijo 23->23, 24->24 (producción real)
        return 9
    else:
        return 11 - resto

def cuil_para_dni(dni: int, sexo: str = "M") -> str:
    """Genera CUIL a partir de DNI. sexo: M/F."""
    prefijo = 20 if sexo == "M" else 27
    dv = calcular_digito_verificador(prefijo, dni)
    return f"{prefijo:02d}-{dni:08d}-{dv}"

print(cuil_para_dni(34211433, "M"))  # => 20-34211433-X
```

> **Uso defensivo:** con el CUIL validado podes verificar que un DNI presentado por un proveedor/empleado es coherente con su identidad, y cruzar contra cuitonline para detectar inconsistencias (señal de documento fraguado o identidad robada).

---

## 4. Cadena de Ataque para Número Telefónico

Flujo recomendado, de lo barato/confiable a lo costoso:

### Paso 1 — Normalizar y validar (E.164)
Lib `phonenumbers` de Python:
```python
import phonenumbers
n = phonenumbers.parse("011 3421 4333", "AR")
print(phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164))  # +54342143333
print(phonenumbers.region_code_for_number(n))          # AR
print(phonenumbers.PhoneNumberType.MOBILE == phonenumbers.number_type(n))
```

### Paso 2 — Determinar carrier y tipo de línea
- **NumVerify** (API, 100 consultas/mes gratis) → carrier, tipo de línea, país, validez.
- **VoIP/virtual = bandera roja** (número descartable, burner). Si es VoIP, bajá las expectativas: es deliberadamente anónimo.

### Paso 3 — Buscar en buscadores (Google Dorking)
Poner el número entre comillas en varias permutaciones:
```
"011 3421 4333"
"+54 11 3421-4333"
"54-11-3421-4333"
site:linkedin.com "011 3421 4333"
site:facebook.com "011 3421 4333"
```
Las personas copian su número en CVs, avisos, firmas de foros, directorios y páginas "acerca de".

### Paso 4 — Apps de mensajería (el pivote de mayor rendimiento)
Guardar el número como contacto y verificar presencia:
- **WhatsApp** → foto de perfil + nombre + estado (si el dueño los expone). Carga sin notificar al dueño.
- **Telegram** → @username + foto + última conexión.
- **Signal** → confirma si la línea está activa.

La **foto de perfil se revierte en Google Lens / PimEyes** para encontrar la misma cara en LinkedIn, citas o foros. El **@telegram** se corre por Sherlock/Maigret en 2000+ sitios.

### Paso 5 — Redes sociales / presence
- Facebook: buscar por número en el buscador.
- Marketplaces (MercadoLibre, OLX): los números aparecen en publicaciones.
- **Sherlock** / **Maigret**: buscan el username/handle en cientos de sitios.

### Paso 6 — Breaches y filtraciones
- Un número filtrado aparece con emails en dumps. El email pasa a ser la nueva semilla:
  - **Holehe**: ¿en qué sitios está registrado el email? (120+ sitios)
  - **Have I Been Pwned** / **IntelX**: historial de filtraciones.
- Teléfono + nombre en un mismo registro de breach = alta confianza.

### Paso 7 — Cruzar y consolidar (el nombre vive en la intersección)
Un nombre que se repite en un aviso + una foto de WhatsApp + un registro de breach es **mucho más fiable** que cualquiera solo. Requerís ≥2 fuentes independientes para atribuir.

---

## 5. Cadena de Ataque para DNI (Argentina)

1. **Derivar CUIL** a partir del DNI (módulo 11, sección 3).
2. **CUIL → cuitonline / buscarDatos / padrón** → nombre completo, provincia, categoría fiscal (monotributista/empleado), fecha de nacimiento estimada.
3. **Nombre + provincia → buscador** → redes, avisos, noticias, juicios, títulos.
4. **DNI presencial → RENAPER / Padrón Electoral** (acceso limitado, legítimo).
5. **Cruzamiento**: DNI → CUIT → razón social o empleador → cadena de asociados.

---

## 6. Herramientas (tabla comparativa)

| Herramienta | Tipo | Entrada | Salida | Costo | Confianza |
|-------------|------|---------|--------|-------|-----------|
| `phonenumbers` (lib) | CLI/lib Python | Número | E.164, tipo, región | Gratis | Alta (determinístico) |
| `NumVerify` | API | Número | Carrier, línea, país | Gratis (100/mes) | Media |
| `Truecaller` | App/Web | Número | Nombre guardado, spam, carrier | Gratis | Media (crowdsourced) |
| Sherlock | CLI Python | Username | 300+ redes | Gratis | Media |
| Maigret | CLI Python | Username | 2500+ redes + dossier | Gratis | Media |
| Holehe | CLI Python | Email | Registro en 120+ sitios | Gratis | Alta |
| PhoneInfoga | CLI | Número | Carrier + fingerprints | Gratis | Media |
| theHarvester | CLI | Dominio/email | Emails, subdominios | Gratis | Media |
| cuitonline / buscarDatos | Web | DNI/CUIL | Ficha de persona | Gratis | Media (a veces viejo) |
| Have I Been Pwned | Web/API | Email | Historial de breaches | Gratis/API paga | Alta |
| IntelX | Web/API | Email/número | Dumps de breaches | Freemium | Alta |
| Epieos / OSINT Industries | Web paga | Número | Social OSD, breaches | Pago | Alta (consolidado) |

---

## 7. Verificación y Confianza (anti-falsos positivos)

El skill de atacante dice: *"No hay falsos positivos — sólo hallazgos mal validados."* Lo mismo aplica al OSINT:

- **Un solo resultado ≠ confirmado.** Requerí:
  - Teléfono→WhatsApp + cuitonline = 2 fuentes
  - Foto de WhatsApp + LinkedIn = 2 fuentes visuales independientes
- **Carrier metadata / apps vivas** → confianza ALTA.
- **Crowdsourced (Truecaller) / people-search** → suelen estar viejos o ruidosos → confianza MEDIA.
- **VoIP/burner** → confianza BAJA por diseño (no le inventes identidad a un número que se creó para ser anónimo).

---

## 8. Documentación de Hallazgos

Cada investigación se documenta como hallazgo en el vault, siguiendo la plantilla del skill:

`security/vault-obsidian/07-Labs/Hallazgos/<fecha>-osint-persona-<target>.md`

```markdown
# Hallazgo: [Fecha] - OSINT Persona [DNI/Tel] en [Target]

## Resumen Ejecutivo
[1-2 líneas: qué se identificó y con qué confianza]

## Cadena de Ataque
```
[DNI/Tel] → [derivación CUIL / dorking] → [whatsapp/telegram] → [cross-ref] → [identidad]
```

## Detalle Técnico
[comandos y scripts usados, permutaciones de búsqueda]

## Datos Expuestos
[nombre, DOB, provincia, empresa, emails, redes — con fuente de cada uno]

## Nivel de Confianza
[Alta/Media/Baja + justificación de las ≥2 fuentes cruzadas]

## Remediación / Acción
[qué hacer con la info: bloquear acceso, verificar identidad, alertar]
```

---

## 9. Referencias

- OSINTBench — *Phone Number OSINT* (2026-04): https://osintbench.com/guides/phone-number-osint
- ShadowDragon / Nico Dekens — *Reverse Phone Number Lookup for OSINT* (2026-06): https://shadowdragon.io/resources/how-to-use-reverse-phone-number-lookup-for-osint/
- EspectroSINT — *OSINT Investigation From a Phone Number* (2026-07): https://www.espectrosint.com/blog/osint-investigation-from-phone-number
- IPQualityScore — *Phone Number OSINT*: https://www.ipqualityscore.com/articles/view/565/phone-number-osint
- OSINT for countries — *Argentina*: https://github.com/OSINT-for-countries/OSINT_in_Argentina
- facusturla/osint-argentina (HIFA ARG): https://github.com/facusturla/osint-argentina
- Sherlock: https://github.com/sherlock-project/sherlock
- Maigret: https://github.com/soxoj/maigret
- Holehe: https://github.com/megadose/holehe
- PhoneInfoga: https://github.com/rafaldrd/phoneinfoga
- Ley 25.326 (Protección de Datos Personales, AR)

---

## 10. Advertencia Ética y Legal

> Este módulo es para **defensa e investigación legítima**. En Argentina, el acceso no autorizado a sistemas (Art. 153 bis CP), el acoso y el doxxing son **delitos**. La consulta masiva o automatizada de padrones estatales puede considerarse acceso no autorizado. Sólo usá fuentes públicas y finalidades legítimas documentadas.
