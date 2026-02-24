# SPARQL Query Examples

All queries run against the live endpoint at `https://metadata.cbd.int/sparql/kmgbf`.

This endpoint is scoped to the KMGBF dataset. Future datasets (e.g. CBD Thesaurus) will be available at their own dedicated endpoints.

## Prefixes (used in all queries)

```sparql
PREFIX : <http://metadata.cbd.int/kmgbf/ontology#>
PREFIX kmgbf: <http://metadata.cbd.int/kmgbf/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
```

---

## 1. List all goals

```sparql
SELECT ?code ?label
WHERE {
  ?goal a :Goal ;
        :goalCode ?code ;
        skos:prefLabel ?label .
  FILTER (lang(?label) = "en")
}
ORDER BY ?code
```

```bash
curl -X POST https://metadata.cbd.int/sparql/kmgbf \
  -H "Accept: application/sparql-results+json" \
  --data-urlencode "query=PREFIX : <http://metadata.cbd.int/kmgbf/ontology#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?code ?label WHERE {
  ?goal a :Goal ; :goalCode ?code ; skos:prefLabel ?label .
  FILTER (lang(?label) = \"en\")
} ORDER BY ?code"
```

---

## 2. Find all indicators for a target

Replace `3` with any target number (1–23).

```sparql
SELECT ?code ?label ?role
WHERE {
  ?target :targetCode 3 .
  ?indicator :indicatorCode ?code ;
             skos:prefLabel ?label .
  {
    ?indicator :isHeadlineFor ?target . BIND("headline" AS ?role)
  } UNION {
    ?indicator :isBinaryFor ?target . BIND("binary" AS ?role)
  } UNION {
    ?indicator :isComponentFor ?target . BIND("component" AS ?role)
  } UNION {
    ?indicator :isComplementaryFor ?target . BIND("complementary" AS ?role)
  }
  FILTER (lang(?label) = "en")
}
ORDER BY ?code
```

---

## 3. National reporting checklist (Annex I indicators)

Headline and binary indicators are the ones all Parties must report on.

```sparql
SELECT DISTINCT ?code ?label ?role
WHERE {
  {
    ?indicator :isHeadlineFor ?x ;
               :indicatorCode ?code ;
               skos:prefLabel ?label .
    BIND("headline" AS ?role)
  } UNION {
    ?indicator :isBinaryFor ?x ;
               :indicatorCode ?code ;
               skos:prefLabel ?label .
    BIND("binary" AS ?role)
  }
  FILTER (lang(?label) = "en")
}
ORDER BY ?code
```

---

## 4. Labels in all three languages

```sparql
SELECT ?code ?labelEN ?labelFR ?labelES
WHERE {
  ?indicator :indicatorCode ?code .
  OPTIONAL { ?indicator skos:prefLabel ?labelEN . FILTER (lang(?labelEN) = "en") }
  OPTIONAL { ?indicator skos:prefLabel ?labelFR . FILTER (lang(?labelFR) = "fr") }
  OPTIONAL { ?indicator skos:prefLabel ?labelES . FILTER (lang(?labelES) = "es") }
}
ORDER BY ?code
```

---

## 5. Cross-cutting indicators (linked to more than one goal or target)

```sparql
SELECT ?code ?label (COUNT(DISTINCT ?goalOrTarget) AS ?linkCount)
WHERE {
  ?indicator :indicatorCode ?code ;
             skos:prefLabel ?label ;
             ( :isHeadlineFor | :isBinaryFor |
               :isComponentFor | :isComplementaryFor ) ?goalOrTarget .
  FILTER (lang(?label) = "en")
}
GROUP BY ?code ?label
HAVING (COUNT(DISTINCT ?goalOrTarget) > 1)
ORDER BY DESC(?linkCount)
```

---

## 6. Search by keyword in labels

Replace `"marine"` with any term.

```sparql
SELECT ?code ?label ?type
WHERE {
  {
    ?s a :Goal ; :goalCode ?code ; skos:prefLabel ?label . BIND("Goal" AS ?type)
  } UNION {
    ?s a :Target ; :targetCode ?codeRaw ; skos:prefLabel ?label .
    BIND(STR(?codeRaw) AS ?code) BIND("Target" AS ?type)
  } UNION {
    ?s a :Indicator ; :indicatorCode ?code ; skos:prefLabel ?label . BIND("Indicator" AS ?type)
  }
  FILTER (lang(?label) = "en")
  FILTER (CONTAINS(LCASE(?label), "marine"))
}
ORDER BY ?type ?code
```

---

## 7. Get definitions for headline indicators

`skos:definition` is populated for headline indicators from CBD/COP/16/INF/3/Rev.1 (field 5a).

```sparql
SELECT ?code ?label ?definition
WHERE {
  ?indicator :isHeadlineFor ?x ;
             :indicatorCode ?code ;
             skos:prefLabel ?label .
  OPTIONAL { ?indicator skos:definition ?definition .
             FILTER (lang(?definition) = "en") }
  FILTER (lang(?label) = "en")
}
ORDER BY ?code
```

---

## 8. Find indicators by custodian agency

Custodian agency data is available for headline indicators (source: CBD/COP/16/INF/3/Rev.1, field 10a).
Replace `"IUCN"` with any organisation name (partial matches require `CONTAINS`).

```sparql
# Exact match
SELECT ?code ?label ?agency
WHERE {
  ?indicator :indicatorCode ?code ;
             skos:prefLabel ?label ;
             :custodianAgency ?agency .
  FILTER (?agency = "IUCN")
  FILTER (lang(?label) = "en")
}
ORDER BY ?code
```

```sparql
# Partial match (case-insensitive)
SELECT ?code ?label ?agency
WHERE {
  ?indicator :indicatorCode ?code ;
             skos:prefLabel ?label ;
             :custodianAgency ?agency .
  FILTER (CONTAINS(LCASE(?agency), "unep"))
  FILTER (lang(?label) = "en")
}
ORDER BY ?code
```

```sparql
# All custodian agencies with their indicator counts
SELECT ?agency (COUNT(DISTINCT ?indicator) AS ?count)
WHERE {
  ?indicator :custodianAgency ?agency .
}
GROUP BY ?agency
ORDER BY DESC(?count) ?agency
```

---

## Tips

- Change `FILTER (lang(?label) = "en")` to `"fr"` or `"es"` for French or Spanish results.
- The live SPARQL endpoint also supports GET requests for simple queries:
  `https://metadata.cbd.int/sparql/kmgbf?query=...`
- For interactive querying, use the [vocabulary browser](https://metadata.cbd.int).
