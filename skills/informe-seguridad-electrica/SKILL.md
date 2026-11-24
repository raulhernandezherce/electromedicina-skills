---
name: informe-seguridad-electrica
description: Genera el informe de un ensayo de seguridad eléctrica de un equipo electromédico según IEC 62353 (ensayo recurrente o tras reparación). Úsala cuando el usuario dé mediciones de resistencia de tierra, corrientes de fuga o aislamiento, pida "informe de seguridad eléctrica", "¿es apto?", "pasa la 62353", o pegue la salida de un analizador de seguridad eléctrica.
---

# Informe de seguridad eléctrica (IEC 62353)

El veredicto **no lo decides tú**: lo calcula `scripts/informe.py` con la tabla de límites de `scripts/iec62353.py`. Tu trabajo es recoger los datos, ejecutar el script y explicar el resultado.

## Pasos

1. **Reúne los datos** y pregunta solo lo que falte y sea obligatorio:
   - Clase de protección: `I` o `II`. Si dudan: clase I = clavija con toma de tierra.
   - Parte aplicable: `B`, `BF`, `CF` o `ninguna` (símbolo del muñeco en la placa; CF = con corazón).
   - Método de fuga: `directo`, `diferencial` o `alternativo` (según el analizador).
   - Mediciones: `resistencia_tierra_ohm` (obligatoria en clase I), `fuga_equipo_uA`, `fuga_parte_aplicable_uA` (obligatoria en BF y CF) y, opcional, `aislamiento_Mohm`.
   - Convierte unidades si hace falta: 1 mA = 1000 µA; 300 mΩ = 0,3 Ω.
2. **Escribe un JSON** con el formato de [ejemplo.json](ejemplo.json) en un archivo temporal.
3. **Ejecuta** `python3 scripts/informe.py <archivo.json>`. Código de salida 0 = APTO; 2 = NO APTO o INCOMPLETO.
4. **Entrega el informe** en Markdown, tal cual lo genera el script, y debajo un resumen de 2-3 líneas.
   - Si es **NO APTO**: di qué ensayo falla y cuánto se pasa del límite. Recuerda retirar el equipo de uso y etiquetarlo. Sugiere causas típicas para revisar (cable de red o conector de tierra si falla la resistencia de tierra; aislamiento de la fuente o filtros de red si falla la fuga del equipo; aislamiento del módulo o del cable de paciente si falla la parte aplicable) como **hipótesis**, nunca como diagnóstico.
   - Si es **INCOMPLETO**: lista las mediciones que faltan.

## Reglas

- No inventes mediciones ni redondees a favor del APTO.
- No cambies los límites salvo que el usuario cite una edición de la norma o del fabricante. En ese caso, indícalo en «Observaciones».
- El informe lo firma un técnico cualificado. Recuérdalo si el usuario pretende usarlo sin revisión.
