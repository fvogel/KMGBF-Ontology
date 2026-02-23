# KMGBF Ontology

Machine-readable ontology and controlled vocabulary for the
[Kunming-Montreal Global Biodiversity Framework](https://www.cbd.int/gbf) (KMGBF),
published by the [Convention on Biological Diversity](https://www.cbd.int/) Secretariat.

The framework comprises **4 goals**, **23 targets**, and **204 monitoring indicators**
adopted at COP-15 (Montreal, December 2022) and finalized at COP-16 (Cali, October 2024).

## Live service

| Service | URL |
|---------|-----|
| Vocabulary browser | https://metadata.cbd.int |
| SPARQL endpoint | https://metadata.cbd.int/sparql |
| REST API | https://metadata.cbd.int/api |
| API documentation (Swagger) | https://metadata.cbd.int/api/kmgbf/docs |
| Download (Turtle, JSON-LD) | https://metadata.cbd.int/download/ |

## URI namespace

All concepts have persistent URIs under `http://metadata.cbd.int/kmgbf/`.

```
http://metadata.cbd.int/kmgbf/goal_A
http://metadata.cbd.int/kmgbf/target_3
http://metadata.cbd.int/kmgbf/indicator_A.1
```

URIs support content negotiation: send `Accept: text/turtle` or
`Accept: application/ld+json` to get machine-readable RDF for any concept.

## Repository contents

```
ontology/
  kmgbf-ontology.ttl   # OWL schema (classes, properties)
  kmgbf-all.ttl        # Full dataset (schema + all data, ready to load)
  data/
    goals.ttl          # 4 goals (A–D)
    targets.ttl        # 23 targets (1–23)
    indicators.ttl     # 204 indicators with role assignments
  validation/
    kmgbf-shapes.ttl   # SHACL validation shapes
  scripts/
    build-all.py       # Rebuilds kmgbf-all.ttl from source files
examples/
  sparql.md            # SPARQL query examples with curl usage
  api.md               # REST API examples
```

## Quick start

Load the full dataset into a local triplestore (e.g. Apache Jena Fuseki):

```bash
curl -X POST http://localhost:3030/kmgbf/data \
  -H "Content-Type: text/turtle" \
  --data-binary @ontology/kmgbf-all.ttl
```

Then query it — see [examples/sparql.md](examples/sparql.md) for annotated examples.

Or use the live REST API directly — see [examples/api.md](examples/api.md).

## Source

Data derived from [Decision 16/31](https://www.cbd.int/doc/decisions/cop-16/cop-16-dec-31-en.pdf)
(Annexes I, II, and III).

## Contact

For questions: [secretariat@cbd.int](mailto:secretariat@cbd.int)
