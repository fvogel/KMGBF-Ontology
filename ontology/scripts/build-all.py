import json
import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph
from rdflib.compare import to_canonical_graph

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

# JSON-LD copies of the Turtle files, served under /download/
JSONLD_OUT = {
    BASE_DIR / "kmgbf-all.ttl": BASE_DIR / "kmgbf-all.json",
    BASE_DIR / "kmgbf-ontology.ttl": BASE_DIR / "kmgbf-ontology.json",
}


def stable(node):
    """Sort JSON-LD arrays so the file is identical from run to run.

    JSON-LD arrays are unordered sets, except the value of @list (e.g. the
    members of owl:unionOf), whose order is meaningful and is kept.
    """
    if isinstance(node, dict):
        return {k: (v if k == "@list" else stable(v)) for k, v in node.items()}
    if isinstance(node, list):
        return sorted((stable(x) for x in node),
                      key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False))
    return node


def write_jsonld(ttl: Path, out: Path) -> None:
    # bind_namespaces="none": only the prefixes declared in the Turtle end up in
    # @context, not the ~20 rdflib binds by default. Canonicalising gives blank
    # nodes stable labels instead of random ones.
    src = Graph(bind_namespaces="none")
    src.parse(str(ttl), format="turtle")
    g = Graph(bind_namespaces="none")
    for prefix, ns in src.namespaces():
        g.bind(prefix, ns)
    g += to_canonical_graph(src)
    doc = json.loads(g.serialize(format="json-ld", auto_compact=True))
    out.write_text(json.dumps(stable(doc), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"Wrote {out.name} (JSON-LD, {len(g)} triples)")

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

    for ttl, out in JSONLD_OUT.items():
        write_jsonld(ttl, out)

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
