import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph

BASE_DIR = Path(__file__).resolve().parent.parent
FILES = [
    BASE_DIR / "kmgbf-ontology.ttl",
    BASE_DIR / "data/goals.ttl",
    BASE_DIR / "data/targets.ttl",
    BASE_DIR / "data/indicators.ttl",
    BASE_DIR / "data/indicators-guidance.ttl",
]
OUT = BASE_DIR / "kmgbf-all.ttl"
SHAPES = BASE_DIR / "validation/kmgbf-shapes.ttl"

def main() -> None:
    text = "\n".join(f.read_text(encoding="utf-8") for f in FILES)
    if not text.endswith("\n"):
        text += "\n"

    # SHACL validation
    data = Graph()
    data.parse(data=text, format="turtle")
    shapes = Graph()
    shapes.parse(str(SHAPES), format="turtle")
    conforms, _, results_text = validate(data, shacl_graph=shapes)
    if not conforms:
        print("SHACL validation FAILED:", file=sys.stderr)
        print(results_text, file=sys.stderr)
        sys.exit(1)
    print(f"SHACL validation passed ({len(data)} triples)")

    OUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUT.name}")

    # Warn if public mirror is out of sync
    sync_script = Path(__file__).resolve().parent.parent.parent / "platform/scripts/check-public-sync.sh"
    if sync_script.exists():
        import subprocess
        result = subprocess.run(["bash", str(sync_script)], capture_output=True, text=True)
        print(result.stdout.strip())
        if result.returncode != 0:
            print(f"WARNING: public mirror out of sync — run check-public-sync.sh for details", file=sys.stderr)

if __name__ == "__main__":
    main()
