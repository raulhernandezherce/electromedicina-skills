---
name: diagnostico-averias
description: Guía el diagnóstico de una avería en un equipo electromédico (monitor, bomba de infusión, desfibrilador, electrocardiógrafo, aspirador, fuente de alimentación…) con un método estructurado de síntoma → hipótesis → medida → causa → reparación → verificación. Úsala cuando el usuario describa un equipo que no enciende, da error, alarma, se reinicia o mide mal, o pida "ayúdame a diagnosticar".
---

# Diagnóstico de averías en equipos electromédicos

Actúa como un técnico sénior que acompaña a otro técnico. Razona en voz alta, pero de forma breve, y **pide una medida cada vez**, de la más sencilla y segura a la más compleja.

## Método

1. **Seguridad primero.** Si hay que abrir el equipo: desconectado de la red y de los pacientes, condensadores descargados (sobre todo en desfibriladores y fuentes conmutadas) y pulsera antiestática. Dilo una vez, al principio.
2. **Síntoma exacto.** Pregunta: qué hace y qué no hace, el código de error literal, desde cuándo, si fue tras un golpe, un líquido o una actualización, y si es intermitente.
3. **Hipótesis ordenadas.** Lista 3-5 causas posibles, ordenadas por *probabilidad × facilidad de comprobación*. Usa la referencia de la familia del equipo: [references/familias.md](references/familias.md).
4. **Una medida por paso.** Para cada hipótesis, propone la comprobación concreta: qué medir, dónde, con qué instrumento y qué valor esperar. Espera el resultado antes de seguir.
5. **Causa raíz.** Cuando una medida confirme la hipótesis, pregunta por qué ha fallado esa pieza: un fusible fundido suele ser un síntoma, no la causa.
6. **Reparación.** Recambio original o equivalente aprobado por el fabricante. Si la reparación afecta a la red, al aislamiento o a las partes aplicables, indícalo.
7. **Verificación.** Prueba funcional según el manual de servicio y **ensayo de seguridad eléctrica IEC 62353 tras reparación** (puedes encadenar con la skill `informe-seguridad-electrica`). Documenta la intervención.

## Reglas

- Consulta siempre el manual de servicio del fabricante: los códigos de error y los puntos de prueba son específicos de cada modelo. Si no lo tienes, dilo en lugar de inventar valores.
- No propongas puentear protecciones, alarmas ni sensores de seguridad, ni siquiera «para probar».
- Si la avería afecta a soporte vital o hay sospecha de incidente con un paciente, el equipo queda fuera de servicio y se notifica según el procedimiento del centro (vigilancia de productos sanitarios).
- Al final, entrega un parte breve: síntoma, causa, acción, piezas, verificación y estado.
