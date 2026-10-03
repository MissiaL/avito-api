"""Offline checks: python3 -m unittest discover -s scripts -p 'test_*.py'."""
import contextlib
import io
import json
import unittest
from types import SimpleNamespace

from lookup_endpoint import cmd_show, load_spec
from build_spec import build, DEFAULT_SERVER


class LookupChecks(unittest.TestCase):
    def show(self, spec, path, method="get"):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            status = cmd_show(spec, SimpleNamespace(path=path, method=method))
        return status, json.loads(output.getvalue()) if output.getvalue() else None

    def test_auth_alternatives_and_missing_method(self):
        spec = load_spec()
        path = "/messenger/v2/accounts/{user_id}/chats"
        status, output = self.show(spec, path)
        self.assertEqual(status, 0)
        op = output["operations"]["GET"]
        self.assertEqual(op["security"], [{"AuthorizationCode": ["messenger:read"]}, {"ClientCredentials": []}])
        self.assertEqual(op["securitySchemes"]["AuthorizationCode"]["type"], "oauth2")
        self.assertEqual(self.show(spec, path, "delete"), (2, None))

    def test_inheritance_and_overrides(self):
        spec = {
            "servers": [{"url": "https://root.example"}],
            "security": [{"Bearer": []}],
            "components": {"securitySchemes": {"Bearer": {"type": "http", "scheme": "bearer"}}},
            "paths": {"/items": {
                "servers": [{"url": "https://path.example"}],
                "parameters": [{"name": "limit", "in": "query", "schema": {"type": "integer", "maximum": 100}}],
                "get": {"deprecated": True, "parameters": [{"name": "limit", "in": "query", "schema": {"type": "integer", "maximum": 10}}]},
                "post": {"servers": [{"url": "https://operation.example"}], "security": []},
            }},
        }
        _, output = self.show(spec, "/items")
        op = output["operations"]["GET"]
        self.assertTrue(op["deprecated"])
        self.assertEqual(op["servers"], [{"url": "https://path.example"}])
        self.assertEqual(op["security"], spec["security"])
        self.assertEqual(len(op["parameters"]), 1)
        self.assertEqual(op["parameters"][0]["schema"]["maximum"], 10)
        _, output = self.show(spec, "/items", "post")
        op = output["operations"]["POST"]
        self.assertEqual(op["servers"], [{"url": "https://operation.example"}])
        self.assertEqual(op["security"], [])
        self.assertEqual(op["securitySchemes"], {})

    def test_product_token_hosts(self):
        spec = load_spec()
        _, output = self.show(spec, "/api/1/partner/tariff/info")
        business = output["operations"]["GET"]["securitySchemes"]["ClientCredentials"]
        self.assertEqual(business["flows"]["clientCredentials"]["tokenUrl"], "https://api.avito.ru/token")
        autoteka_path = next(path for path, item in spec["paths"].items()
                             if item.get("get", {}).get("x-avito-section", {}).get("slug") == "autoteka")
        _, output = self.show(spec, autoteka_path)
        op = output["operations"]["GET"]
        self.assertEqual(op["servers"], [{"url": "https://pro.autoteka.ru"}])
        self.assertEqual(op["security"], [{"ClientCredentials__autoteka": []}])
        autoteka = op["securitySchemes"]["ClientCredentials__autoteka"]
        self.assertEqual(autoteka["flows"]["clientCredentials"]["tokenUrl"], "https://pro.autoteka.ru/token")

    def test_all_security_requirements_resolve(self):
        spec = load_spec()
        schemes = spec["components"]["securitySchemes"]
        for path, item in spec["paths"].items():
            for method in ("get", "post", "put", "patch", "delete"):
                for requirement in item.get(method, {}).get("security", []):
                    for name in requirement:
                        self.assertIn(name, schemes, f"{method.upper()} {path}: {name}")

    def test_build_keeps_auth_hosts_and_normalizes_source_typo(self):
        sections = []
        for slug, server, requirement in (
            ("autoteka", "https://pro.autoteka.ru", "ClientCredentials"),
            ("auth", DEFAULT_SERVER, "ClientCredentials"),
            ("autostrategy", DEFAULT_SERVER, "Client Credentials"),
        ):
            sections.append({"slug": slug, "title": slug, "server": server, "spec": {
                "paths": {f"/{slug}": {"get": {"security": [{requirement: []}]}}},
                "components": {"securitySchemes": {"ClientCredentials": {
                    "type": "oauth2", "flows": {"clientCredentials": {"tokenUrl": server + "/token", "scopes": {}}}
                }}},
            }})
        spec, _ = build(sections, "2026-10-03")
        for slug, expected in (("autoteka", "https://pro.autoteka.ru/token"), ("auth", DEFAULT_SERVER + "/token")):
            op = spec["paths"][f"/{slug}"]["get"]
            name = next(iter(op["security"][0]))
            self.assertEqual(spec["components"]["securitySchemes"][name]["flows"]["clientCredentials"]["tokenUrl"], expected)
        op = spec["paths"]["/autostrategy"]["get"]
        self.assertEqual(op["security"], [{"ClientCredentials": []}])
        self.assertEqual(op["x-avito-original-security"], [{"Client Credentials": []}])


if __name__ == "__main__":
    unittest.main()
