"""Authored contract helpers. These run only during grading, never inside the learner namespace."""

import asyncio


def raises(kind, function, *args):
    try:
        function(*args)
    except kind:
        return True
    return False


def cache_case(function):
    calls = []
    cache = {}
    assert function(cache, "a", lambda: calls.append(1)) is None
    assert function(cache, "a", lambda: 9) is None
    assert calls == [1]
    cache["zero"] = 0
    assert function(cache, "zero", lambda: 9) == 0
    return True


def idempotency_case(function):
    cache = {}
    calls = []

    def operation(payload):
        calls.append(payload)
        return 0

    assert function(cache, "a", "x", operation) == 0
    assert function(cache, "a", "x", operation) == 0
    assert calls == ["x"]
    assert raises(ValueError, function, cache, "a", "different", operation)
    assert calls == ["x"]

    def broken(payload):
        raise TimeoutError("transient")

    assert raises(TimeoutError, function, cache, "b", "y", broken)
    assert "b" not in cache
    assert function(cache, "b", "y", operation) == 0
    return True


def retry_case(function):
    calls = []
    sleeps = []

    def transient():
        calls.append(1)
        if len(calls) < 3:
            raise TimeoutError("wait")
        return "ok"

    assert function(transient, 3, sleeps.append) == "ok"
    assert len(calls) == 3 and sleeps == [1, 2]
    calls.clear()
    sleeps.clear()

    def failed():
        calls.append(1)
        raise TimeoutError("still down")

    assert raises(TimeoutError, function, failed, 2, sleeps.append)
    assert len(calls) == 2 and sleeps == [1]
    calls.clear()

    def programming_error():
        calls.append(1)
        raise ValueError("do not retry")

    assert raises(ValueError, function, programming_error, 3, sleeps.append)
    assert calls == [1]
    for count in (0, -1, True, 1.5):
        assert raises(ValueError, function, lambda: "unused", count, sleeps.append)
    return True


def twice_case(function):
    calls = []

    def transient():
        calls.append(1)
        if len(calls) == 1:
            raise TimeoutError("wait")
        return 7

    assert function(transient) == 7 and len(calls) == 2
    calls.clear()

    def broken():
        calls.append(1)
        raise ValueError("bug")

    assert raises(ValueError, function, broken) and calls == [1]

    def timeout():
        raise TimeoutError("still down")

    assert raises(TimeoutError, function, timeout)
    return True


def async_collect_case(function):
    async def main():
        started = []

        async def transform(value):
            started.append(value)
            await asyncio.sleep(0)
            assert len(started) == 3, (
                "Schedule all transforms before awaiting their completion"
            )
            return value * 2

        assert await function([3, 1, 2], transform) == [6, 2, 4]

    asyncio.run(main())
    return True


def async_empty_case(function):
    async def transform(value):
        raise AssertionError("Empty input must not call transform")

    assert asyncio.run(function([], transform)) == []
    return True
