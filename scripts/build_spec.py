#!/usr/bin/env python3
"""Rebuild references/ from a catalog dump (see references/sources.md for how to get one).

Usage:
    python3 scripts/build_spec.py dump.json [--date YYYY-MM-DD]

dump.json: {"list": [...], "info": {"<slug>": {"status": 200, "text": "<raw /info body>"}}}

Merge rules:
- Sections are applied in order (non-default host first, then slug); on a path+method
  collision the last one wins (`x-avito-section`), the others go to `x-avito-also-in`.
  So api.avito.ru sections beat e.g. Autoteka for the shared `/token`.
- A component whose name is already taken with different content is renamed to
  `<name>__<slug>` and that section's `$ref`s are rewritten, so schemas never get mixed.
- securitySchemes are shared by name; OAuth2 scopes are unioned.
- Operations of a non-default host get an operation-level `servers`.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "references"
DEFAULT_SERVER = "https://api.avito.ru"
METHODS = ("get", "post", "put", "patch", "delete")


def load_sections(dump):
    sections = []
    for meta in dump["list"]:
        slug = meta["slug"]
        entry = dump["info"][slug]
        if entry["status"] != 200:
            sys.exit(f"{slug}: HTTP {entry['status']}")
        info = json.loads(entry["text"])
        spec = json.loads(info["swagger"])
        if not str(spec.get("openapi", "")).startswith("3.") or not spec.get("paths"):
            sys.exit(f"{slug}: not an OpenAPI 3 document")
        server = (spec.get("servers") or [{"url": DEFAULT_SERVER}])[0]["url"].rstrip("/")
        sections.append({"slug": slug, "title": meta["title"], "description": meta.get("description") or "",
                         "spec": spec, "server": server, "md": info.get("md") or "", "changelog": info.get("changelog") or ""})
    sections.sort(key=lambda s: (s["server"] == DEFAULT_SERVER, s["slug"]))
    return sections


def merge_components(merged, sec):
    for name, value in sec["spec"].get("components", {}).get("securitySchemes", {}).items():
        target = merged.setdefault("securitySchemes", {})
        if name not in target:
            target[name] = json.loads(json.dumps(value))
            continue
        for flow, data in value.get("flows", {}).items():
            flows = target[name].setdefault("flows", {})
            f = flows.setdefault(flow, json.loads(json.dumps(data)))
            f["scopes"] = {**(f.get("scopes") or {}), **(data.get("scopes") or {})}

    # Rewriting refs can make a previously identical component differ, so repeat until stable.
    renames, spec = {}, sec["spec"]
    while True:
        new = {}
        for ctype, items in spec.get("components", {}).items():
            for name, value in items.items():
                key = f"#/components/{ctype}/{name}"
                if ctype != "securitySchemes" and key not in renames and merged.get(ctype, {}).get(name, value) != value:
                    new[key] = f"{key}__{sec['slug']}"
        if not new:
            break
        renames.update(new)
        text = re.sub(r'"(#/components/[^"]+)"', lambda m: json.dumps(renames.get(m.group(1), m.group(1)), ensure_ascii=False),
                      json.dumps(sec["spec"], ensure_ascii=False))
        spec = json.loads(text)
    sec["spec"] = spec
    for ctype, items in spec.get("components", {}).items():
        if ctype == "securitySchemes":
            continue
        for name, value in items.items():
            key = f"#/components/{ctype}/{name}"
            merged.setdefault(ctype, {})[renames.get(key, key).rsplit("/", 1)[1]] = value
    return len(renames)


def build(sections, fetched):
    paths, components, tags, renamed = {}, {}, {}, {}
    for sec in sections:
        renamed[sec["slug"]] = merge_components(components, sec)
        ref = {"slug": sec["slug"], "title": sec["title"]}
        for t in sec["spec"].get("tags", []):
            tags.setdefault(t["name"], t)
        tags.setdefault(sec["title"], {"name": sec["title"], "description": sec["spec"].get("info", {}).get("description", "")})
        for path, item in sec["spec"]["paths"].items():
            target = paths.setdefault(path, {})
            for key, value in item.items():
                if key not in METHODS:
                    target[key] = value
                    continue
                op = dict(value)
                op["tags"] = list(dict.fromkeys(op.get("tags", []) + [sec["title"]]))
                if sec["server"] != DEFAULT_SERVER:
                    op["servers"] = [{"url": sec["server"]}]
                prev = target.get(key)
                if prev:  # last write wins; keep the loser's provenance and tags
                    op["x-avito-also-in"] = prev.get("x-avito-also-in", []) + [prev["x-avito-section"]]
                    op["tags"] = list(dict.fromkeys(op["tags"] + prev["tags"]))
                op["x-avito-section"] = ref
                target[key] = op
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Avito API для бизнеса (официальный каталог)",
            "version": fetched,
            "description": "Полный спек Avito Business API, собранный scripts/build_spec.py из официального каталога "
                           "www.avito.ru/developers/api-catalog. Каждая операция получила тег с русским названием раздела "
                           "и поле x-avito-section. При коллизиях path+method канонический раздел — последний по порядку "
                           "(сначала разделы с нестандартным хостом, затем sorted(slug)); проигравшие указаны в x-avito-also-in. "
                           "Одноимённые компоненты с разным содержимым переименованы в <name>__<slug>.",
            "contact": {"email": "supportautoload@avito.ru"},
            "termsOfService": "https://www.avito.ru/legal/pro_tools/public-api",
            "x-catalog-fetched": fetched,
        },
        "servers": [{"url": DEFAULT_SERVER, "description": "Avito Business API"}],
        "tags": list(tags.values()),
        "paths": dict(sorted(paths.items())),
        "components": {k: dict(sorted(v.items())) for k, v in sorted(components.items())},
    }
    return spec, renamed


def ops_of(spec):
    for path, item in spec["paths"].items():
        for m in METHODS:
            if m in item:
                yield path, m, item[m]


def write_sections(sections):
    for sec in sections:
        if not sec["md"].strip() and not sec["changelog"].strip():
            continue
        head = "\n\n".join(x for x in (f"# {sec['title']} (`{sec['slug']}`)", sec["description"].strip()) if x)
        parts = [f"{head}\n\n---\n\n{sec['md'].strip()}"]
        if sec["changelog"].strip():
            log = re.sub(r"^#", "##", sec["changelog"].strip(), flags=re.M)
            parts.append(f"## История изменений\n\n{log}")
        (ROOT / "sections" / f"{sec['slug']}.md").write_text("\n\n---\n\n".join(parts) + "\n")


def write_index(spec, sections, fetched):
    by_slug = {s["slug"]: {"sec": s, "own": [], "also": []} for s in sections}
    for path, m, op in ops_of(spec):
        by_slug[op["x-avito-section"]["slug"]]["own"].append((path, m, op))
        for other in op.get("x-avito-also-in", []):
            by_slug[other["slug"]]["also"].append((path, m, op))
    n_ops = sum(len(v["own"]) for v in by_slug.values())
    date_ru = datetime.date.fromisoformat(fetched).strftime("%d.%m.%Y")
    out = [
        "# Avito API — индекс категорий", "",
        "Источник: официальный каталог `www.avito.ru/developers/api-catalog` (`/web/1/openapi/list` + `/web/1/openapi/info/<slug>`). "
        f"Полный спек: [avito-api-openapi.json](./avito-api-openapi.json) (~{(ROOT / 'avito-api-openapi.json').stat().st_size / 2**20:.1f} МБ, "
        f"{len(spec['paths'])} путей / {n_ops} операций / {len(sections)} разделов).", "",
        f"Схема выгружена **{date_ru}**. См. [источники](sources.md). Для Авито Реклама также доступны [официальные SDK](ads-sdk.md).", "",
        "Документация по разделам — в [sections/](./sections/) (интеграция, примеры, sandbox, история изменений).", "",
        "**Не читай OpenAPI целиком.** Используй `scripts/lookup_endpoint.py` (`tags`/`search`/`show`).", "",
        "Категории отсортированы по числу эндпоинтов. При коллизиях path+method канонический раздел — `x-avito-section`; "
        "остальные — `x-avito-also-in` в OpenAPI (и пометка «также публикует» ниже).", "",
    ]
    line = lambda path, m, text: f"- `{m.upper():6s} {path}` — {text}"
    for v in sorted(by_slug.values(), key=lambda v: (-len(v["own"]), v["sec"]["title"])):
        sec = v["sec"]
        docs = f" — [docs](./sections/{sec['slug']}.md)" if (ROOT / "sections" / f"{sec['slug']}.md").exists() else ""
        out += [f"## {sec['title']} ({len(v['own'])}){docs}", ""]
        out += [line(p, m, op.get("summary", "")) for p, m, op in sorted(v["own"], key=lambda x: (x[0], METHODS.index(x[1])))]
        if v["also"]:
            out += ["", "Также публикует (канонический раздел другой; см. `x-avito-also-in`):", ""]
            out += [line(p, m, "канон: " + op["x-avito-section"]["title"]) for p, m, op in v["also"]]
        out.append("")
    (ROOT / "index.md").write_text("\n".join(out))
    return n_ops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dump")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    args = ap.parse_args()
    sections = load_sections(json.loads(Path(args.dump).read_text()))
    spec, renamed = build(sections, args.date)
    (ROOT / "avito-api-openapi.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
    write_sections(sections)
    n_ops = write_index(spec, sections, args.date)
    print(f"{len(spec['paths'])} paths / {n_ops} operations / {len(sections)} sections")
    print("renamed components:", {k: v for k, v in renamed.items() if v})


if __name__ == "__main__":
    main()
