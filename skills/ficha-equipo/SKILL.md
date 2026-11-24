---
name: ficha-equipo
description: Crea la ficha de inventario de un equipo electromédico a partir de una foto de su placa de características, una etiqueta o un fragmento del manual. Úsala cuando el usuario diga "da de alta este equipo", "haz la ficha", "lee la placa" o comparta una imagen de una etiqueta de un equipo médico.
---

# Ficha de equipo electromédico

Extrae los datos de la placa o de la etiqueta y devuelve la ficha en **dos formatos**: una tabla legible y un JSON compatible con la herramienta `planificar_preventivos` de [mcp-electromedicina](https://github.com/raulhernandezherce/mcp-electromedicina).

## Campos

| Campo | Dónde suele estar | Notas |
|---|---|---|
| `equipo` | Manual o etiqueta frontal | Nombre genérico: «Bomba de infusión volumétrica» |
| `marca`, `modelo` | Placa | Tal cual aparecen |
| `serie` | Placa, tras «SN» o el símbolo de número de serie | Cópialo carácter a carácter |
| `fabricacion` | Símbolo de la fábrica con fecha | AAAA-MM |
| `alimentacion` | Placa | Tensión, frecuencia, potencia o corriente |
| `clase` | Símbolo de dos cuadrados = clase II; si no, y lleva tierra, clase I | |
| `parte_aplicable` | Símbolo del muñeco: sin cuadro = B, en cuadro = BF, con corazón = CF | Indica si es a prueba de desfibrilación (palas en el símbolo) |
| `ip` | Placa, «IPxx» | |
| `marcado_ce` | «CE» seguido del número del organismo notificado | |
| `ubicacion`, `id` | Pregúntalos | El `id` es el número de inventario del centro |
| `ultimo_preventivo`, `periodicidad_meses` | Pregúntalos | Periodicidad: la del fabricante |

## Reglas

- Si un dato no se lee con claridad, pon `null` y dilo. **Nunca adivines un número de serie.**
- Distingue lo que has leído de lo que has deducido (por ejemplo, la clase por los símbolos), y marca lo deducido.
- Al final, ofrece calcular la puntuación de Fennigkoh y Smith si el usuario quiere decidir si el equipo entra en el programa de preventivo.

## Ejemplo de salida JSON

```json
{
  "id": "BIN-031",
  "equipo": "Bomba de infusión volumétrica",
  "marca": "Ejemplo",
  "modelo": "VP-200",
  "serie": "A1B2C3",
  "fabricacion": "2022-03",
  "alimentacion": "100-240 V~ 50/60 Hz 25 VA",
  "clase": "I",
  "parte_aplicable": "CF (a prueba de desfibrilación)",
  "ip": "IP22",
  "ubicacion": "Planta 4",
  "ultimo_preventivo": "2026-01-15",
  "periodicidad_meses": 12
}
```
