"""Offline checks: python3 -m unittest discover -s scripts -p 'test_*.py'."""
import contextlib
import io
import json
import unittest
from types import SimpleNamespace

from lookup_endpoint import cmd_show, load_spec


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


if __name__ == "__main__":
    unittest.main()
