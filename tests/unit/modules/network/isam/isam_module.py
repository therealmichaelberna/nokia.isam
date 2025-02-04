
import json
import os

from ansible_collections.isam.isam.tests.unit.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
)
from ansible_collections.isam.isam.tests.unit.modules.utils import (
    set_module_args as _set_module_args,
)


def set_module_args(args, ignore_provider=None):
    if "provider" not in args and not ignore_provider:
        args["provider"] = {"transport": args.get("transport") or "cli"}

    return _set_module_args(args)


fixture_path = os.path.join(os.path.dirname(__file__), "fixtures")
fixture_data = {}


def load_fixture(module_name, name, device=""):
    path = os.path.join(fixture_path, module_name, device, name)
    if not os.path.exists(path):
        path = os.path.join(fixture_path, module_name, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data

class TestIsamModule(ModuleTestCase):
    def execute_module_devices(
        self,
        failed=False,
        changed=False,
        commands=None,
        sort=True,
        defaults=False,
    ):
        module_name = self.module.__name__.rsplit(".", 1)[1]
        local_fixture_path = os.path.join(fixture_path, module_name)

        models = []
        for path in os.listdir(local_fixture_path):
            path = os.path.join(local_fixture_path, path)
            if os.path.isdir(path):
                models.append(os.path.basename(path))
        if not models:
            models = [""]

        retvals = {}
        for model in models:
            retvals[model] = self.execute_module(failed, changed, commands, sort, device=model)

        return retvals

    def execute_module(self, failed=False, changed=False, commands=None, sort=True, device=""):

        self.load_fixtures(commands, device=device)

        if failed:
            result = self.failed()
            self.assertTrue(result["failed"], result)
        else:
            result = self.changed(changed)
            self.assertEqual(result["changed"], changed, result)
        if commands is not None and len(commands) > 0:
            if sort:
                self.assertEqual(
                    sorted(commands),
                    sorted(result["commands"]),
                    result["commands"],
                )
            else:
                self.assertEqual(commands, result["commands"], result["commands"])

        return result
        
    def failed(self):
        with self.assertRaises(AnsibleFailJson) as exc:
            self.module.main()
        result = exc.exception.args[0]
        self.assertTrue(result["failed"], result)
        return result

    def changed(self, changed=False):
        with self.assertRaises(AnsibleExitJson) as exc:
            self.module.main()

        result = exc.exception.args[0]
        self.assertEqual(result["changed"], changed, result)
        return result

    def load_fixtures(self, commands=None, device=""):
        pass