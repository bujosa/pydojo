"""Useful starting experiments, independently editable and never graded for completion."""

import ast

OVERRIDES = {
    (
        "classes-and-state",
        False,
    ): "counter = answer.Counter(2)\nprint(counter.increment())\nprint(counter.increment(4))",
    (
        "classes-and-state",
        True,
    ): 'box = answer.Box("first")\nprint(box.replace("second"))\nprint(box.value)',
    (
        "dataclasses-and-values",
        False,
    ): 'product = answer.Product("book", 1250)\nprint(product)\nprint(product.subtotal(3))',
    (
        "dataclasses-and-values",
        True,
    ): "print(answer.Point(1, 2))\nprint(answer.Point(1, 2) == answer.Point(1, 2))",
    (
        "properties-and-invariants",
        False,
    ): "wallet = answer.Wallet(100)\nprint(wallet.withdraw(40))\nprint(wallet.balance)",
    (
        "properties-and-invariants",
        True,
    ): "temperature = answer.Celsius(20)\nprint(temperature.value)",
    (
        "inject-dependencies",
        False,
    ): 'calls = []\nprint(answer.send_receipt("ada@example.test", 1200, lambda *args: calls.append(args)))\nprint(calls)',
    (
        "inject-dependencies",
        True,
    ): 'messages = []\nprint(answer.publish("ready", messages.append))\nprint(messages)',
    (
        "closures-and-state",
        False,
    ): "counter = answer.make_counter(4)\nprint(counter())\nprint(counter())",
    (
        "closures-and-state",
        True,
    ): 'prefix = answer.make_prefixer("lab:")\nprint(prefix("one"))',
    (
        "decorators-and-metadata",
        False,
    ): "events = []\n@answer.logged(events.append)\ndef add(left, right):\n    return left + right\nprint(add(2, 3))\nprint(events)",
    (
        "decorators-and-metadata",
        True,
    ): "@answer.identity_decorator\ndef add(left, right):\n    return left + right\nprint(add(2, 3))\nprint(add.__name__)",
    (
        "custom-context-managers",
        False,
    ): "events = []\nwith answer.managed(events) as resource:\n    print(resource)\nprint(events)",
    (
        "custom-context-managers",
        True,
    ): 'events = []\nwith answer.bracket(events):\n    print("inside")\nprint(events)',
    (
        "iterator-protocol",
        False,
    ): "counter = answer.Countdown(3)\nprint(list(counter))\nprint(list(counter))",
    (
        "iterator-protocol",
        True,
    ): 'item = answer.One("ready")\nprint(list(item))\nprint(list(item))',
    (
        "async-and-await",
        False,
    ): "import asyncio\nasync def transform(value):\n    await asyncio.sleep(0)\n    return value * 2\nprint(asyncio.run(answer.collect([3, 1, 2], transform)))",
    (
        "async-and-await",
        True,
    ): "import asyncio\nprint(asyncio.run(answer.double_async(3)))",
    (
        "files-and-contexts",
        True,
    ): 'from pathlib import Path\nPath("sample.txt").write_text(" first \\n\\nsecond\\n", encoding="utf-8")\nprint(answer.read_nonblank("sample.txt"))',
    (
        "project-idempotent-handler",
        False,
    ): 'cache = {}\ncalls = []\ndef operation(payload):\n    calls.append(payload)\n    return "accepted"\nprint(answer.handle_once(cache, "request-one", "payload", operation))\nprint(answer.handle_once(cache, "request-one", "payload", operation))\nprint("Actual calls:", len(calls))',
    (
        "project-idempotent-handler",
        True,
    ): 'cache = {}\nprint(answer.cached(cache, "one", lambda: 0))\nprint(answer.cached(cache, "one", lambda: 99))',
    (
        "project-retry-policy",
        False,
    ): 'calls = []\ndef operation():\n    calls.append(1)\n    if len(calls) < 3:\n        raise TimeoutError("try again")\n    return "ok"\nprint(answer.retry(operation, 3, lambda delay: print("Backoff:", delay)))',
    (
        "project-retry-policy",
        True,
    ): 'calls = []\ndef operation():\n    calls.append(1)\n    if len(calls) == 1:\n        raise TimeoutError("try again")\n    return "ok"\nprint(answer.try_twice(operation))',
}


def make(identity, exercise, guided):
    if (identity, guided) in OVERRIDES:
        experiment = OVERRIDES[identity, guided]
    else:
        experiment = None
        for node in ast.walk(ast.parse(exercise["checks"])):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "s"
            ):
                try:
                    for value in node.args:
                        ast.literal_eval(value)
                    for keyword in node.keywords:
                        ast.literal_eval(keyword.value)
                except (ValueError, TypeError):
                    continue
                call = ast.unparse(node).replace("s.", "answer.", 1)
                if any(
                    isinstance(item, (ast.Yield, ast.YieldFrom))
                    for item in ast.walk(ast.parse(exercise["solution"]))
                ):
                    call = f"list({call})"
                experiment = f"print({call})"
                break
        if experiment is None:
            experiment = 'print({name: value for name, value in vars(answer).items() if not name.startswith("_")})'
    return (
        "import answer\n\n# Run your implementation, then change these inputs and predict the result.\n"
        + experiment
        + "\n"
    )
