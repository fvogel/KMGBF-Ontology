# REST API Examples

All endpoints are available at [https://metadata.cbd.int/api/kmgbf/](https://metadata.cbd.int/api/kmgbf/).
Interactive documentation (Swagger UI) is at [https://metadata.cbd.int/api/kmgbf/docs](https://metadata.cbd.int/api/kmgbf/docs).

## Common parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `lang` | `en`, `fr`, `es`, `all` | `en` | Language for labels |
| `format` | `json`, `csv` | `json` | Response format (list endpoints only) |

---

## 1. List all goals

```bash
curl https://metadata.cbd.int/api/kmgbf/goals
```

```json
[
  { "code": "A", "label": "Integrity, connectivity and resilience of ecosystems maintained..." },
  { "code": "B", "label": "Biodiversity and nature's contributions to people..." },
  { "code": "C", "label": "Monetary and non-monetary benefits from biodiversity shared fairly..." },
  { "code": "D", "label": "Adequate means of implementation..." }
]
```

---

## 2. Get a single goal

```bash
curl https://metadata.cbd.int/api/kmgbf/goals/A
```

Returns the full record for Goal A, including its label in the requested language.

---

## 3. Get all indicators for a goal

```bash
curl https://metadata.cbd.int/api/kmgbf/goals/A/indicators
```

Returns all indicators linked to Goal A (headline, binary, component, complementary),
each with its `role` field.

---

## 4. List all targets

```bash
curl https://metadata.cbd.int/api/kmgbf/targets
```

Returns all 23 targets with their numeric code and label.

---

## 5. Get all indicators for a target

```bash
curl https://metadata.cbd.int/api/kmgbf/targets/3/indicators
```

Returns all indicators for Target 3 (the 30×30 target), with their role.

---

## 6. Get a single indicator

```bash
curl https://metadata.cbd.int/api/kmgbf/indicators/A.1
```

Returns the full record for indicator A.1, including all roles it plays across
different goals and targets.

---

## 7. List all indicators, filtered by role

```bash
curl "https://metadata.cbd.int/api/kmgbf/indicators?role=headline"
```

Valid roles: `headline`, `binary`, `component`, `complementary`.

---

## 8. Search across all entities

```bash
curl "https://metadata.cbd.int/api/kmgbf/search?q=marine"
```

Returns matching goals, targets, and indicators whose labels contain the search term.

---

## 9. Multilingual labels

Add `?lang=fr` or `?lang=es` to any endpoint:

```bash
curl "https://metadata.cbd.int/api/kmgbf/targets/3?lang=fr"
curl "https://metadata.cbd.int/api/kmgbf/indicators?lang=es"
```

Use `?lang=all` to get labels in English, French, and Spanish in a single response.

---

## 10. CSV export

Add `?format=csv` to list endpoints:

```bash
curl "https://metadata.cbd.int/api/kmgbf/indicators?format=csv" -o indicators.csv
curl "https://metadata.cbd.int/api/kmgbf/targets?format=csv" -o targets.csv
```

---

## Tips

- For more complex queries (cross-cutting indicators, custom filters), use the
  [SPARQL endpoint](sparql.md) directly.
- The full interactive API documentation is at
  `https://metadata.cbd.int/api/kmgbf/docs`.
- All endpoints support CORS — you can call them from browser JavaScript directly.
