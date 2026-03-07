# Changelog

All notable changes to the KMGBF Ontology are documented here.

Versioning follows [Semantic Versioning](https://semver.org/):
- **Patch** (x.x.1): corrections, metadata additions, no change to concept identifiers or role assignments
- **Minor** (x.1.0): new concepts, new properties, backwards-compatible additions
- **Major** (2.0.0): removal or renaming of existing concepts, breaking changes

---

## [1.0.1] — 2026-03-05

### Fixed
- `dct:source` on goals and targets changed from URI resource to string literal.
  SKOSMOS was treating URI-valued `dct:source` as an internal concept lookup,
  producing broken links. String literals render as plain text with no side effects.

### Added
- `dct:source` added to all 204 indicators (pointing to Decision 16/31 PDF).
  Previously only the `indicatorScheme` ConceptScheme carried this property.
- `dct:created` and `dct:modified` added to both ConceptSchemes
  (`kmgbf:kmgbfScheme` and `kmgbf:indicatorScheme`) to support change tracking.
- `dct:modified` added to the ontology document itself.
- `kmgbf:kmgbfScheme` (Goals + Targets ConceptScheme) now formally defined in
  `data/goals.ttl` with metadata (previously only implicit via SKOSMOS compat layer).
- `owl:versionInfo` bumped from `"1.0"` to `"1.0.1"`.

### Distribution
- `kmgbf-all.ttl` rebuilt: 2,333 triples (up from 2,118 in v1.0)

---

## [1.0] — 2026-02-24

### Initial release
- 4 Goals (A–D) with multilingual labels and definitions (EN, FR, ES)
- 23 Targets (1–23) with multilingual labels and definitions (EN, FR, ES)
- 204 Indicators with multilingual labels (EN, FR, ES) and 222 role assignments
  - 28 headline assignments (isHeadlineFor)
  - 16 binary assignments (isBinaryFor)
  - 47 component assignments (isComponentFor)
  - 131 complementary assignments (isComplementaryFor)
- 27 headline indicators with skos:definition and custodianAgency
  (source: CBD/COP/16/INF/3/Rev.1)
- SHACL validation shapes
- OWL ontology schema: 4 classes, 11 properties

### Sources
- Goals and Targets: Decision 15/4 (COP-15, Montreal, December 2022)
- Indicators: Decision 16/31 (COP-16, Cali, February 2025)
