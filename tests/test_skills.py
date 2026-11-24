"""Valida el plugin, las skills y el script de informes."""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SKILLS = sorted(p for p in (RAIZ / "skills").iterdir() if p.is_dir())
INFORME = RAIZ / "skills" / "informe-seguridad-electrica" / "scripts" / "informe.py"


def frontmatter(path):
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    assert m, f"{path} sin frontmatter"
    return dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l)


class PluginTest(unittest.TestCase):
    def test_manifiestos(self):
        plugin = json.loads((RAIZ / ".claude-plugin" / "plugin.json").read_text())
        market = json.loads((RAIZ / ".claude-plugin" / "marketplace.json").read_text())
        self.assertEqual(market["plugins"][0]["name"], plugin["name"])
        self.assertEqual(market["plugins"][0]["version"], plugin["version"])
        self.assertEqual(market["plugins"][0]["source"], "./")

    def test_cada_skill_es_valida(self):
        self.assertGreaterEqual(len(SKILLS), 3)
        for d in SKILLS:
            fm = frontmatter(d / "SKILL.md")
            self.assertEqual(fm["name"], d.name)
            self.assertGreater(len(fm["description"]), 80, d.name)
            self.assertLessEqual(len(fm["description"]), 1024, d.name)

    def test_enlaces_relativos_existen(self):
        for d in SKILLS:
            for enlace in re.findall(r"\]\(([^)#:]+)\)", (d / "SKILL.md").read_text(encoding="utf-8")):
                self.assertTrue((d / enlace).exists(), f"{d.name}: {enlace}")


class InformeTest(unittest.TestCase):
    def ejecutar(self, datos, tmp):
        f = Path(tmp) / "e.json"
        f.write_text(json.dumps(datos))
        return subprocess.run([sys.executable, str(INFORME), str(f)], capture_output=True, text=True)

    def test_ejemplo_es_apto(self):
        r = subprocess.run([sys.executable, str(INFORME), str(INFORME.parents[1] / "ejemplo.json")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("**Veredicto: APTO**", r.stdout)

    def test_fuga_cf_excesiva(self):
        import tempfile
        with tempfile.TemporaryDirectory() as t:
            r = self.ejecutar({"equipo": {"clase": "I", "parte_aplicable": "CF"},
                               "mediciones": {"resistencia_tierra_ohm": 0.1, "fuga_equipo_uA": 100,
                                              "fuga_parte_aplicable_uA": 62}}, t)
        self.assertEqual(r.returncode, 2)
        self.assertIn("❌ NO APTO", r.stdout)
        self.assertIn("≤ 50 µA", r.stdout)

    def test_incompleto(self):
        import tempfile
        with tempfile.TemporaryDirectory() as t:
            r = self.ejecutar({"equipo": {"clase": "I"}, "mediciones": {"fuga_equipo_uA": 10}}, t)
        self.assertEqual(r.returncode, 2)
        self.assertIn("INCOMPLETO", r.stdout)


if __name__ == "__main__":
    unittest.main()
