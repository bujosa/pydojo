import inspect
import io
import json
import unittest
from unittest.mock import patch

import bridge


class InspectionTests(unittest.TestCase):
    def test_inspection_never_calls_user_repr(self):
        class Dangerous:
            def __repr__(self):
                raise AssertionError("Learner repr must not execute in the debugger")

        self.assertEqual(bridge.safe_value(Dangerous()), "<Dangerous>")
        self.assertEqual(
            bridge.safe_value({"x": [Dangerous()]}), "{'x': [<Dangerous>]}"
        )

    def test_large_values_are_bounded(self):
        self.assertEqual(bridge.safe_value(1 << 2048), "<large int>")
        self.assertLess(len(bridge.safe_value("x" * 100000)), 250)
        self.assertIn("…", bridge.safe_value(list(range(100))))

    def test_read_only_expression_cannot_call_or_access_attributes(self):
        value = 7
        frame = inspect.currentframe()
        output = io.StringIO()
        with (
            patch.object(bridge, "WIRE", output),
            patch.object(bridge, "FRAMES", {"selected": frame}),
        ):
            bridge.inspect({"frame": "selected", "expression": "value"})
            bridge.inspect({"frame": "selected", "expression": "value.__class__"})
            bridge.inspect({"frame": "selected", "expression": "print('side effect')"})
        records = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(records[0], {"type": "evaluation", "text": str(value)})
        self.assertEqual(
            [r["type"] for r in records[1:]], ["commandError", "commandError"]
        )


if __name__ == "__main__":
    unittest.main()
