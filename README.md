<div align="center">

# 🩺 electromedicina-skills

**Skills de ingeniería clínica para Claude Code y otros agentes de IA.**
Informes de seguridad eléctrica IEC 62353, diagnóstico guiado de averías y fichas de inventario de equipos electromédicos.

![tests](https://github.com/raulhernandezherce/electromedicina-skills/actions/workflows/tests.yml/badge.svg)
![Claude Code plugin](https://img.shields.io/badge/Claude_Code-plugin-D97757)
![skills](https://img.shields.io/badge/skills-3-39FF88)
![licencia](https://img.shields.io/badge/licencia-MIT-blue)

</div>

---

Las skills enseñan a un agente de IA a trabajar **como lo haría un técnico de electromedicina**: con método, sin inventar valores y dejando que el veredicto lo calcule código probado, no el modelo.

## Instalación (Claude Code)

```
/plugin marketplace add raulhernandezherce/electromedicina-skills
```

```
/plugin install electromedicina@electromedicina-skills
```

Funcionan también con cualquier agente compatible con Agent Skills: copia la carpeta de la skill que quieras dentro de `~/.claude/skills/` (o el directorio de skills de tu agente).

## Skills

| Skill | Qué hace | Ejemplo de petición |
|---|---|---|
| [`informe-seguridad-electrica`](skills/informe-seguridad-electrica/SKILL.md) | Recoge las mediciones, ejecuta un script que aplica los límites de IEC 62353 y devuelve el informe en Markdown con el veredicto APTO / NO APTO / INCOMPLETO. | *«Monitor clase I con parte CF: tierra 0,12 Ω, fuga del equipo 180 µA, fuga CF 62 µA. Hazme el informe.»* |
| [`diagnostico-averias`](skills/diagnostico-averias/SKILL.md) | Guía el diagnóstico paso a paso: seguridad → síntoma → hipótesis ordenadas → una medida cada vez → causa raíz → reparación → verificación y ensayo tras reparación. | *«La bomba de infusión da alarma de oclusión sin motivo.»* |
| [`ficha-equipo`](skills/ficha-equipo/SKILL.md) | Lee la placa de características (desde una foto) y genera la ficha de inventario en tabla y en JSON. Interpreta los símbolos de clase y de tipo de parte aplicable. | *«Da de alta este equipo» + foto de la placa* |

### Ejemplo de informe generado

| Ensayo | Medido | Límite | Resultado |
|---|---:|---:|---|
| Resistencia del conductor de protección | 0,12 Ω | ≤ 0,3 Ω | ✅ APTO |
| Corriente de fuga del equipo (directo) | 180 µA | ≤ 500 µA | ✅ APTO |
| Corriente de fuga de la parte aplicable CF (directo) | 62 µA | ≤ 50 µA | ❌ NO APTO |

## Principios de diseño

- **El modelo no decide el veredicto.** Los límites están en código (`scripts/iec62353.py`), con tests. El agente recoge los datos, ejecuta y explica.
- **No inventar.** Si falta el manual de servicio o un dato no se lee en la placa, el agente lo dice en lugar de rellenarlo.
- **Seguridad primero.** Nada de puentear alarmas o protecciones. Ensayo de seguridad eléctrica tras cada reparación. El equipo queda fuera de servicio si hay riesgo para el paciente.

## Encaja con

- [**mcp-electromedicina**](https://github.com/raulhernandezherce/mcp-electromedicina): el mismo conocimiento expuesto como servidor MCP. La ficha en JSON se puede pasar directamente a su herramienta `planificar_preventivos`.

> [!WARNING]
> Herramientas de apoyo para personal técnico cualificado. Comprueba siempre la edición vigente de IEC 62353 y el manual de servicio del fabricante. Los informes deben revisarlos y firmarlos un técnico responsable.

## Desarrollo

```bash
python3 -m unittest discover -s tests -v
```

```bash
claude plugin validate .
```

---

<sub>Hecho por <a href="https://github.com/raulhernandezherce">Raúl Hernández Herce</a> · Técnico Superior en Electromedicina Clínica · Licencia MIT</sub>
