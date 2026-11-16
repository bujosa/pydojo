"""Original PyDojo curriculum. Builds deterministic embedded JSON; no AI service at runtime."""

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = []
GUIDES = []
SECTIONS = [
    "01 · First steps",
    "02 · Flow and functions",
    "03 · Collection patterns",
    "04 · Reliable data",
    "05 · Model a domain",
    "06 · Advanced Python",
    "07 · Engineering projects",
]


def code(text):
    return textwrap.dedent(text).strip() + "\n"


def spec(name, params, body, alternative, negative, task, cases):
    def function(statements):
        return f"def {name}({params}):\n" + textwrap.indent(code(statements), "    ")

    return {
        "task": task,
        "starter": function(
            "# TODO: replace this placeholder with your implementation.\nreturn None"
        ),
        "solution": function(body),
        "alternative": function(alternative),
        "negative": function(negative),
        "checks": "\n".join(
            "assert " + expression.replace("\n", "\\n") + ", " + repr(message)
            for expression, message in cases
        )
        + "\n",
        "runtime": "",
    }


def raw(task, starter, solution, alternative, negative, checks):
    return {
        "task": task,
        "starter": code(starter),
        "solution": code(solution),
        "alternative": code(alternative),
        "negative": code(negative),
        "checks": code(checks),
        "runtime": "",
    }


def add(
    identity,
    title,
    outcome,
    example,
    explanation,
    vocabulary,
    lab,
    practice,
    hint,
    prediction,
    transfer,
):
    index = len(LESSONS)
    lesson = dict(
        id=identity,
        section=SECTIONS[
            next(i for i, end in enumerate((6, 12, 18, 25, 31, 37, 43)) if index < end)
        ],
        title=title,
        concept="\n\n".join(explanation),
        hint=hint,
        **lab,
    )
    LESSONS.append(lesson)
    practice = dict(
        practice,
        hint=hint,
        playground="import answer\n\n# Try a value of your own after checking the guided exercise.\nprint({name: value for name, value in vars(answer).items() if not name.startswith('_')})\n",
    )
    GUIDES.append(
        dict(
            id=identity,
            outcome=outcome,
            prerequisites=[LESSONS[index - 1]["id"]] if index else [],
            vocabulary=[
                {"term": term, "meaning": meaning} for term, meaning in vocabulary
            ],
            example=code(example),
            explanation=explanation,
            prediction={
                "question": prediction[0],
                "choices": prediction[1],
                "correct": prediction[2],
                "explanation": prediction[3],
            },
            practice=practice,
            transfer=transfer,
        )
    )


add(
    "names-and-values",
    "Your first Python values",
    "Create names for text, numbers and a boolean, and read a simple program from top to bottom.",
    """
    course = "Python"
    completed = 2
    ready = True
    print(course, completed, ready)
    assert completed == 2
""",
    [
        'A program is a sequence of instructions. Python reads these lines from top to bottom. In course = "Python", the name is course, = binds that name to a value, and quotes mark text. You do not type a semicolon at the end of a normal Python line.',
        '"Python" is a str, 2 is an int, and True is a bool. Capitalization matters: True is a value, while true is an undefined name. A name can later be rebound; Python checks what an operation can do when that operation runs.',
        "print(...) calls a function and displays values. Parentheses hold its arguments; commas separate them. assert completed == 2 checks a statement about the result: == compares values, whereas = assigns a name. The editor on the right is where you will type your answer.",
        "Start with guided practice, then solve the independent lab. Check validates the saved answer against actual Python assertions. Run executes your playground and displays logs. A successful Run alone does not finish a lab.",
    ],
    [
        ("value", "A piece of data such as text, a number, or True."),
        ("name", "An identifier that refers to a value; use descriptive snake_case."),
        ("assignment", "The = statement binds a name to the value on its right."),
    ],
    raw(
        'Create course_name as the string "PyDojo", lesson_count as the integer 43, and is_ready as True. Use these exact names.',
        "course_name = None\nlesson_count = None\nis_ready = None",
        'course_name = "PyDojo"\nlesson_count = 43\nis_ready = True',
        'is_ready = bool(1)\nlesson_count = 40 + 3\ncourse_name = "Py" + "Dojo"',
        'course_name = "PyDojo"\nlesson_count = "43"\nis_ready = True',
        'assert s.course_name == "PyDojo", "course_name should contain PyDojo"\nassert type(s.lesson_count) is int and s.lesson_count == 43, "lesson_count must be integer 43"\nassert s.is_ready is True, "is_ready must be True"',
    ),
    raw(
        'Create language as "Python" and attempts as the integer 1.',
        "language = None\nattempts = None",
        'language = "Python"\nattempts = 1',
        'language = str("Python")\nattempts = 3 - 2',
        'language = "Python"\nattempts = "1"',
        'assert s.language == "Python", "Use Python as text"\nassert type(s.attempts) is int and s.attempts == 1, "Use integer 1"',
    ),
    "Keep text in quotes and numbers outside quotes. True begins with a capital T.",
    (
        "What does print(course, completed, ready) display?",
        ["Python 2 True", "course completed ready", 'Python "2" true'],
        0,
        "print reads the values bound to the names and separates them with spaces.",
    ),
    [
        "Change completed to 3 in the worked example and predict the output.",
        "In the lab, a number stored as text is a different value and will fail the check.",
    ],
)

add(
    "numbers-and-operators",
    "Calculate with numbers",
    "Distinguish division, floor division and remainder, and use parentheses deliberately.",
    "minutes = 125\nhours = minutes // 60\nremainder = minutes % 60\nprint(hours, remainder)\nassert (hours, remainder) == (2, 5)",
    [
        "Python supports +, -, *, /, //, %, and **. The / operator performs division and returns a float, even when the division is exact. The // operator performs floor division: it rounds down, including for negative numbers.",
        "The remainder operator % gives the remainder after floor division. For a positive duration in minutes, minutes // 60 finds whole hours and minutes % 60 finds the leftover minutes. Parentheses control the order of operations; multiplication happens before addition.",
        "Use integers for exact counts or money in cents. Binary floating point approximates many decimal fractions, so avoid relying on 0.1 + 0.2 being exactly 0.3.",
    ],
    [
        ("operator", "A symbol that computes a result from values."),
        ("remainder", "What is left after whole groups are removed."),
        ("floor division", "Division rounded toward negative infinity."),
    ],
    raw(
        "Set subtotal_cents to 3 items at 1250 cents each, total_cents to subtotal plus 250 shipping, and whole_dollars to total_cents // 100.",
        "subtotal_cents = None\ntotal_cents = None\nwhole_dollars = None",
        "subtotal_cents = 3 * 1250\ntotal_cents = subtotal_cents + 250\nwhole_dollars = total_cents // 100",
        "subtotal_cents = 1250 + 1250 + 1250\ntotal_cents = 250 + subtotal_cents\nwhole_dollars = divmod(total_cents, 100)[0]",
        "subtotal_cents = 3750\ntotal_cents = 4000\nwhole_dollars = 40.0",
        'assert s.subtotal_cents == 3750, "Multiply item count by price"\nassert s.total_cents == 4000, "Include shipping"\nassert type(s.whole_dollars) is int and s.whole_dollars == 40, "Keep whole dollars as an int"',
    ),
    raw(
        "Convert 95 minutes into whole_hours and remaining_minutes using 60 minutes per hour.",
        "whole_hours = None\nremaining_minutes = None",
        "whole_hours = 95 // 60\nremaining_minutes = 95 % 60",
        "whole_hours, remaining_minutes = divmod(95, 60)",
        "whole_hours = 95 / 60\nremaining_minutes = 35",
        'assert s.whole_hours == 1 and type(s.whole_hours) is int, "One whole hour"\nassert s.remaining_minutes == 35, "Thirty-five minutes remain"',
    ),
    "Calculate in cents first. // gives an integer for integer operands.",
    (
        "What are hours and remainder?",
        ["2.08 and 0", "2 and 5", "3 and -55"],
        1,
        "125 contains two complete groups of sixty and five remaining minutes.",
    ),
    [
        "Try minutes = 0 and minutes = 60.",
        "Try -1 // 60 and explain why flooring differs from truncation.",
    ],
)

add(
    "strings-and-text",
    "Work with text",
    "Normalize text and build a readable message with an f-string.",
    'name = "  Ada  "\nclean = name.strip().lower()\nmessage = f"Hello, {clean}!"\nprint(message)\nassert message == "Hello, ada!"',
    [
        "Strings are immutable sequences of characters. A method such as .strip() returns a new string with surrounding whitespace removed; it does not modify the original. A dot selects a method, and parentheses call it.",
        "You can chain methods: name.strip().lower() first trims the text and then lowercases the returned string. In an f-string, expressions inside braces are inserted into the text. The f before the opening quote enables interpolation.",
        "Text normalization is a product decision. This exercise deliberately lowercases a label; real personal names should usually keep their original capitalization.",
    ],
    [
        ("method", "A function accessed through a value, such as text.strip()."),
        ("immutable", "A value that cannot be modified in place."),
        ("f-string", "Text prefixed by f that interpolates expressions in braces."),
    ],
    raw(
        'Normalize raw_handle = "  PYTHON_BUILDER  " into handle using strip and lowercase. Create greeting as "Welcome, python_builder!".',
        'raw_handle = "  PYTHON_BUILDER  "\nhandle = None\ngreeting = None',
        'raw_handle = "  PYTHON_BUILDER  "\nhandle = raw_handle.strip().lower()\ngreeting = f"Welcome, {handle}!"',
        'raw_handle = "  PYTHON_BUILDER  "\nhandle = raw_handle.lower().strip()\ngreeting = "Welcome, " + handle + "!"',
        'raw_handle = "  PYTHON_BUILDER  "\nhandle = raw_handle.lower()\ngreeting = f"Welcome, {handle}!"',
        'assert s.raw_handle == "  PYTHON_BUILDER  ", "Keep the input unchanged"\nassert s.handle == "python_builder", "Trim and lowercase"\nassert s.greeting == "Welcome, python_builder!", "Interpolate the normalized handle"',
    ),
    raw(
        'Given label = "  LAB  ", create clean_label as "lab".',
        'label = "  LAB  "\nclean_label = None',
        'label = "  LAB  "\nclean_label = label.strip().lower()',
        'label = "  LAB  "\nclean_label = label.lower().strip()',
        'label = "  LAB  "\nclean_label = label.strip()',
        'assert s.clean_label == "lab", "Trim and lowercase the label"',
    ),
    "Apply .strip() and .lower() to the input, then insert the result into an f-string.",
    (
        "What does the worked example print?",
        ["Hello, Ada!", "Hello, {clean}!", "Hello, ada!"],
        2,
        "strip removes the outside spaces, lower changes Ada to ada, and the f-string inserts that result.",
    ),
    [
        "Try a label containing spaces in its middle; strip keeps them.",
        "Remove the f prefix and observe what happens to the braces.",
    ],
)

add(
    "booleans-and-comparisons",
    "Ask a yes-or-no question",
    "Combine comparisons with and, or and not without confusing assignment and equality.",
    "age = 20\nverified = True\nallowed = age >= 18 and verified\nprint(allowed)\nassert allowed is True",
    [
        "A comparison such as age >= 18 produces True or False. Other comparisons include ==, !=, <, <= and >. Use == for equality of values; is is reserved for identity, with is None a common and intentional use.",
        "and requires both conditions to be truthy; or needs at least one; not negates truthiness. These operators short-circuit: Python does not evaluate the right operand when the left already determines the result.",
        'Empty strings and collections, zero and None are falsy. A nonempty string such as "False" is truthy. Keep boolean flags as real booleans when the task requires True or False.',
    ],
    [
        ("comparison", "An expression that compares values."),
        ("boolean", "True or False."),
        ("short-circuit", "Skip an operand when the result is already determined."),
    ],
    raw(
        "Given score = 84 and submitted = True, set passed when score is at least 80 AND submitted. Set needs_retry to the opposite of passed.",
        "score = 84\nsubmitted = True\npassed = None\nneeds_retry = None",
        "score = 84\nsubmitted = True\npassed = score >= 80 and submitted\nneeds_retry = not passed",
        "score = 84\nsubmitted = True\npassed = submitted and score >= 80\nneeds_retry = passed is False",
        'score = 84\nsubmitted = True\npassed = "True"\nneeds_retry = False',
        'assert s.passed is True, "passed must be a boolean True"\nassert s.needs_retry is False, "Negate the boolean"',
    ),
    raw(
        "Set is_empty to whether count = 0 equals zero.",
        "count = 0\nis_empty = None",
        "count = 0\nis_empty = count == 0",
        "count = 0\nis_empty = not bool(count)",
        'count = 0\nis_empty = "True"',
        'assert s.is_empty is True, "Return an actual bool"',
    ),
    "Use >= to compare, and to combine, and not to invert.",
    (
        "If verified becomes False, what is allowed?",
        ["False", "True", '"False"'],
        0,
        "The and expression needs both the age comparison and verification to be true.",
    ),
    [
        "Predict the result with age = 18.",
        'Compare bool("") with bool("False") in the playground.',
    ],
)

add(
    "lists-and-indexes",
    "Keep an ordered list",
    "Create a list, access its first item and make a slice without mutating the original.",
    'tools = ["editor", "runner", "debugger"]\nfirst = tools[0]\nrest = tools[1:]\nprint(first, len(rest))\nassert first == "editor" and len(rest) == 2',
    [
        "A list stores values in order inside square brackets. Indexes start at zero: tools[0] reads the first item. A negative index counts from the end; tools[-1] is the last item. Accessing an index outside the list raises IndexError.",
        "A slice such as tools[1:] creates a new list from index one to the end. len(tools) returns the number of items. A list is mutable: append adds one item in place and returns None, so do not replace your list with the result of append.",
        "Copying a list with a slice makes a shallow copy. Nested mutable values are still shared; later labs explore how to avoid accidental aliasing.",
    ],
    [
        ("index", "A zero-based position in a sequence."),
        ("slice", "A selected range written with a colon inside brackets."),
        ("mutable", "A value whose contents can change in place."),
    ],
    raw(
        'Create topics as ["values", "loops", "functions"]. Set first_topic to its first item and next_topics to a slice containing the other two.',
        "topics = []\nfirst_topic = None\nnext_topics = None",
        'topics = ["values", "loops", "functions"]\nfirst_topic = topics[0]\nnext_topics = topics[1:]',
        'topics = list(("values", "loops", "functions"))\nfirst_topic, *next_topics = topics',
        'topics = ["values", "loops", "functions"]\nfirst_topic = topics[1]\nnext_topics = topics[1:]',
        'assert s.topics == ["values", "loops", "functions"], "Keep the requested order"\nassert s.first_topic == "values", "Indexes begin at zero"\nassert s.next_topics == ["loops", "functions"], "Slice from index one"\nassert s.next_topics is not s.topics, "Create a separate list"',
    ),
    raw(
        "Given scores = [8, 9, 10], set last_score to the last item and score_count to the length.",
        "scores = [8, 9, 10]\nlast_score = None\nscore_count = None",
        "scores = [8, 9, 10]\nlast_score = scores[-1]\nscore_count = len(scores)",
        "scores = [8, 9, 10]\nlast_score = scores[len(scores) - 1]\nscore_count = len(scores)",
        "scores = [8, 9, 10]\nlast_score = 9\nscore_count = 3",
        'assert s.last_score == 10, "Read the final item"\nassert s.score_count == 3, "Count the items"',
    ),
    "Use index 0 for the first element and [1:] for everything after it.",
    (
        "What does print(first, len(rest)) display?",
        ["runner 3", "editor 2", "editor 3"],
        1,
        "Index zero selects editor; the remaining slice contains runner and debugger.",
    ),
    [
        "Try tools[:2] and predict which items it contains.",
        'Call tools.append("tests") and inspect both the list and the return value.',
    ],
)

add(
    "dictionaries-and-keys",
    "Describe data with keys",
    "Read a dictionary and distinguish a missing key from an explicit None value.",
    'profile = {"name": "Ada", "level": 1}\nname = profile["name"]\ncity = profile.get("city", "Unknown")\nprint(name, city)\nassert city == "Unknown"',
    [
        'A dictionary maps keys to values: {"name": "Ada"} associates the key "name" with "Ada". Braces create the dictionary; the colon separates each key from its value. Dictionaries preserve insertion order, but their main purpose is lookup by key.',
        'profile["name"] requires the key to exist and raises KeyError if it does not. profile.get("city", "Unknown") returns a default only when the key is absent. A present value of None stays None.',
        'The expression "name" in profile tests for a key, not a value. Use clear keys that describe what a value means, and avoid guessing that a missing field is the same as an empty field.',
    ],
    [
        ("dictionary", "A mutable mapping from unique keys to values."),
        ("key", "A hashable identifier used to retrieve a mapped value."),
        ("default", "A fallback used when a key is absent."),
    ],
    raw(
        'Create settings with theme = "dark" and font_size = 14. Set theme from the dictionary and autosave from .get("autosave", True).',
        "settings = {}\ntheme = None\nautosave = None",
        'settings = {"theme": "dark", "font_size": 14}\ntheme = settings["theme"]\nautosave = settings.get("autosave", True)',
        'settings = dict(theme="dark", font_size=14)\ntheme = settings.get("theme")\nautosave = True if "autosave" not in settings else settings["autosave"]',
        'settings = {"theme": "dark", "font_size": 14}\ntheme = settings["theme"]\nautosave = settings.get("autosave")',
        'assert s.settings == {"theme": "dark", "font_size": 14}, "Use the requested keys"\nassert s.theme == "dark", "Read theme"\nassert s.autosave is True, "Use the missing-key default"',
    ),
    raw(
        'Given user = {"name": "Lin"}, set role using .get with default "learner".',
        'user = {"name": "Lin"}\nrole = None',
        'user = {"name": "Lin"}\nrole = user.get("role", "learner")',
        'user = dict(name="Lin")\nrole = user["role"] if "role" in user else "learner"',
        'user = {"name": "Lin"}\nrole = user.get("role")',
        'assert s.role == "learner", "Supply a fallback for a missing key"',
    ),
    "Put a comma after the key argument in .get and then supply the fallback.",
    (
        "What is city?",
        ["None", "KeyError", '"Unknown"'],
        2,
        "city is absent, so get returns its explicit default.",
    ),
    [
        "Add city: None and observe that get does not replace it.",
        "Explain when raising KeyError is more useful than silently providing a default.",
    ],
)


# Function lab helper: every exercise has authored cases and a distinct guided API.
def f(
    identity,
    title,
    outcome,
    example,
    paragraphs,
    terms,
    lab,
    practice,
    hint,
    prediction,
    transfer,
):
    add(
        identity,
        title,
        outcome,
        example,
        paragraphs,
        terms,
        lab,
        practice,
        hint,
        prediction,
        transfer,
    )


f(
    "functions-and-return",
    "Give behavior a name",
    "Define a function with parameters and return a value to its caller.",
    "def double(number):\n    return number * 2\n\nprint(double(4))\nassert double(4) == 8",
    [
        "def introduces a function definition. The name double describes the operation; number is a parameter that receives an argument when the function is called. A colon starts the body, and indentation groups its statements. Use four spaces consistently.",
        "return sends a value back to the caller and stops that call. print displays text but returns None; printing an answer is not the same as returning it. A function that reaches the end without return also returns None.",
        "The definition does not run the body immediately. Each call supplies its own arguments and gets its own local names. Keep calculations separate from display so they can be reused and tested.",
    ],
    [
        ("parameter", "A named input in a function definition."),
        ("argument", "A concrete value passed by a caller."),
        ("return", "End a call and send a result back."),
    ],
    spec(
        "area",
        "width, height",
        "return width * height",
        "result = width * height\nreturn result",
        "print(width * height)",
        "Implement area(width, height) returning the rectangle area. Inputs are nonnegative numbers.",
        [
            ("s.area(3, 4) == 12", "3 by 4 has area 12"),
            ("s.area(0, 9) == 0", "Zero width gives zero area"),
            ("s.area(2.5, 4) == 10", "Support fractional widths"),
        ],
    ),
    spec(
        "triple",
        "number",
        "return number * 3",
        "return number + number + number",
        "print(number * 3)",
        "Return three times number from triple(number).",
        [
            ("s.triple(4) == 12", "Return the result"),
            ("s.triple(0) == 0", "Handle zero"),
            ("s.triple(-2) == -6", "Handle negatives"),
        ],
    ),
    "Use return with the calculated value. Printing alone returns None.",
    (
        "What value does double(4) return?",
        ["None", "8", '"8"'],
        1,
        "return sends the integer result 4 * 2 to the caller.",
    ),
    [
        "Try calling area with keyword arguments.",
        "Explain what happens if you delete the return statement.",
    ],
)

f(
    "branches-and-boundaries",
    "Make decisions with if",
    "Cover ordered conditions and check the boundary between two outcomes.",
    'def label(score):\n    if score >= 80:\n        return "pass"\n    return "retry"\n\nprint(label(80))\nassert label(79) == "retry"',
    [
        "if evaluates a condition and runs its indented body only when that condition is truthy. An elif tries another condition when earlier ones failed; else handles everything that remains.",
        "Order conditions from the most specific to the most general when ranges overlap. In the example, the boundary belongs to pass because >= includes 80. A missing equality often hides an off-by-one error.",
        "An early return can make else unnecessary. Whichever style you choose, check values just below, exactly at, and just above each boundary.",
    ],
    [
        ("branch", "One possible path through a program."),
        ("boundary", "A value where a decision changes."),
        ("early return", "Return before the end to keep later code simpler."),
    ],
    spec(
        "shipping",
        "total_cents",
        "if total_cents >= 5000:\n    return 0\nreturn 499",
        "return 0 if total_cents >= 5000 else 499",
        "return 0 if total_cents > 5000 else 499",
        "Return 0 shipping for orders at least 5000 cents; otherwise return 499. Inputs are nonnegative integers.",
        [
            ("s.shipping(0) == 499", "Small orders pay shipping"),
            ("s.shipping(4999) == 499", "Below threshold"),
            ("s.shipping(5000) == 0", "Threshold is inclusive"),
            ("s.shipping(9000) == 0", "Larger orders qualify"),
        ],
    ),
    spec(
        "temperature_label",
        "degrees",
        'if degrees < 0:\n    return "freezing"\nreturn "above freezing"',
        'return "freezing" if degrees < 0 else "above freezing"',
        'return "freezing" if degrees <= 0 else "above freezing"',
        'Return "freezing" below zero, otherwise "above freezing".',
        [
            ('s.temperature_label(-1) == "freezing"', "Below zero"),
            ('s.temperature_label(0) == "above freezing"', "Zero is not below zero"),
            ('s.temperature_label(5) == "above freezing"', "Positive value"),
        ],
    ),
    "Include the threshold itself in the free-shipping branch.",
    (
        "What does label(80) return?",
        ['"pass"', '"retry"', "None"],
        0,
        "The >= comparison includes exactly 80.",
    ),
    [
        "Add a second threshold and test both boundaries.",
        "State the domain assumption for negative order totals.",
    ],
)

f(
    "loops-and-accumulators",
    "Build a result with a loop",
    "Use for, a local accumulator and a clear inclusion rule.",
    "def total_even(values):\n    total = 0\n    for value in values:\n        if value % 2 == 0:\n            total += value\n    return total\n\nprint(total_even([1, 2, 4]))\nassert total_even([]) == 0",
    [
        "for value in values assigns each item to value and executes the indented body. It iterates over values directly; you rarely need manual indexes to add a sequence.",
        "An accumulator remembers the result built so far. Initialize it before the loop, update it inside the loop, and return it after the loop. Returning inside the body would stop after the first selected item.",
        "The empty collection is a useful design test: the loop body never runs, so the initial value becomes the result. For addition that identity is zero.",
    ],
    [
        ("iteration", "One execution of a loop body."),
        ("accumulator", "A value updated as items are processed."),
        ("identity", "An initial value that leaves the operation unchanged."),
    ],
    spec(
        "positive_total",
        "values",
        "total = 0\nfor value in values:\n    if value > 0:\n        total += value\nreturn total",
        "return sum(value for value in values if value > 0)",
        "return sum(values)",
        "Return the sum of positive values only. Ignore zero and negatives; do not mutate values.",
        [
            ("s.positive_total([3, -2, 5]) == 8", "Exclude negative values"),
            ("s.positive_total([]) == 0", "Empty sum is zero"),
            ("s.positive_total([-3, 0]) == 0", "No positive values"),
            ("s.positive_total([1, 2, 3]) == 6", "Include every positive item"),
        ],
    ),
    spec(
        "count_even",
        "values",
        "count = 0\nfor value in values:\n    if value % 2 == 0:\n        count += 1\nreturn count",
        "return sum(1 for value in values if value % 2 == 0)",
        "return len(values)",
        "Count the even numbers, including zero and negative even numbers.",
        [
            ("s.count_even([1, 2, 4]) == 2", "Count matching items"),
            ("s.count_even([]) == 0", "Empty input"),
            ("s.count_even([0, -2, 3]) == 2", "Zero and negatives"),
        ],
    ),
    "Initialize zero before the loop; add only when value > 0.",
    (
        "What does total_even([1, 2, 4]) return?",
        ["2", "6", "7"],
        1,
        "Only 2 and 4 enter the accumulator.",
    ),
    [
        "Move return inside the loop and explain the failure.",
        "Try the same rule on a tuple.",
    ],
)

f(
    "comprehensions",
    "Transform a collection",
    "Read a comprehension in execution order and keep filtering separate from mapping.",
    "numbers = [-2, 0, 3]\nsquares = [n * n for n in numbers if n > 0]\nprint(squares)\nassert squares == [9]",
    [
        "A list comprehension builds a new list from an iterable. Read [n * n for n in numbers if n > 0] as: take each n, keep it if positive, then calculate n * n.",
        "The expression on the left transforms each selected item. The trailing if filters which items participate. A comprehension preserves iteration order and leaves the original collection unchanged.",
        "Prefer a loop when the body needs several statements or side effects. Comprehensions are most readable when they express one clear transformation and one simple filter.",
    ],
    [
        ("comprehension", "Compact syntax for building a collection."),
        ("mapping", "Transforming each selected value."),
        ("filtering", "Keeping only values that satisfy a condition."),
    ],
    spec(
        "clean_labels",
        "labels",
        "return [label.strip().lower() for label in labels if label.strip()]",
        "result = []\nfor label in labels:\n    clean = label.strip().lower()\n    if clean:\n        result.append(clean)\nreturn result",
        "return [label.lower() for label in labels]",
        "Trim and lowercase each string, discard whitespace-only strings, and preserve order and duplicates.",
        [
            ('s.clean_labels([" A ", " ", "B"]) == ["a", "b"]', "Trim and filter"),
            ("s.clean_labels([]) == []", "Empty collection"),
            ('s.clean_labels(["X", " x "]) == ["x", "x"]', "Preserve duplicates"),
        ],
    ),
    spec(
        "squares",
        "values",
        "return [value * value for value in values]",
        "result = []\nfor value in values:\n    result.append(value ** 2)\nreturn result",
        "return values",
        "Return a new list containing each number squared, in input order.",
        [
            ("s.squares([-2, 3]) == [4, 9]", "Transform each value"),
            ("s.squares([]) == []", "Empty result"),
            ("s.squares([0, 1]) == [0, 1]", "Keep order"),
        ],
    ),
    "Filter using the trimmed string, then map it to lowercase.",
    (
        "What is squares in the example?",
        ["[4, 0, 9]", "[3]", "[9]"],
        2,
        "The filter excludes -2 and 0 before the square is calculated.",
    ),
    [
        "Rewrite the comprehension as a loop.",
        "Explain why a set comprehension would change this lab contract.",
    ],
)

f(
    "sets-and-membership",
    "Choose unique membership",
    "Use a set for uniqueness while choosing explicitly whether order matters.",
    'roles = {"reader", "editor", "reader"}\nprint(len(roles))\nassert "reader" in roles\nassert len(roles) == 2',
    [
        "A set stores unique hashable values and supports fast membership checks with in. Repeated values collapse into one entry. An empty set is set(); {} creates an empty dictionary instead.",
        "Sets do not provide a meaningful output order. If an API promises first-seen order, keep a list for output and a set for membership. Choosing a collection is part of specifying behavior.",
        "Dictionary keys and set members must be hashable. Strings and integers work; mutable lists do not. Converting to a set is useful only when losing duplicates and order is intentional.",
    ],
    [
        ("set", "A collection of unique hashable values."),
        ("hashable", "A value usable as a set member or dictionary key."),
        ("first-seen order", "Keep the earliest occurrence and retain its position."),
    ],
    spec(
        "unique_ordered",
        "values",
        "seen = set()\nresult = []\nfor value in values:\n    if value not in seen:\n        seen.add(value)\n        result.append(value)\nreturn result",
        "return list(dict.fromkeys(values))",
        "return sorted(set(values))",
        "Return unique strings in first-seen order. Do not sort them.",
        [
            (
                's.unique_ordered(["b", "a", "b", "c"]) == ["b", "a", "c"]',
                "Keep first-seen order",
            ),
            ("s.unique_ordered([]) == []", "Empty input"),
            ('s.unique_ordered(["x", "x"]) == ["x"]', "Remove repeated values"),
        ],
    ),
    spec(
        "shared_tags",
        "left, right",
        "return set(left) & set(right)",
        "return {tag for tag in left if tag in right}",
        "return set(left) | set(right)",
        "Return the set of tags present in both inputs.",
        [
            (
                's.shared_tags(["a", "b"], ["b", "c"]) == {"b"}',
                "Intersection, not union",
            ),
            ('s.shared_tags([], ["a"]) == set()', "Empty intersection"),
            ('s.shared_tags(["x", "x"], ["x"]) == {"x"}', "Unique result"),
        ],
    ),
    "Keep a separate output list, or use dictionary insertion order to preserve first occurrences.",
    (
        "How many roles remain?",
        ["2", "3", "1"],
        0,
        "The duplicate reader contributes no additional set member.",
    ),
    [
        "Try a list as a set member and read the TypeError.",
        "Compare order guarantees of list, dict and set.",
    ],
)

f(
    "unpacking-and-enumerate",
    "Work with positions and pairs",
    "Unpack records and use enumerate when a position is part of the result.",
    'names = ["Ada", "Lin"]\nrows = [(position, name) for position, name in enumerate(names, start=1)]\nprint(rows)\nassert rows == [(1, "Ada"), (2, "Lin")]',
    [
        'A tuple groups values in a fixed ordered record, such as (1, "Ada"). Unpacking assigns its elements to names: position, name = row. The number of targets must match unless one starred target gathers the remaining values.',
        "enumerate(iterable, start=1) yields pairs containing a counter and an item. Use it when the output needs positions. For plain transformations, iterate over the values directly.",
        "Python indexes usually start at zero, while labels shown to people often start at one. Set start explicitly rather than adjusting the counter inconsistently in several places.",
    ],
    [
        ("tuple", "An immutable ordered group of values."),
        ("unpacking", "Assign elements of an iterable to separate targets."),
        ("enumerate", "Iterate over counter-and-value pairs."),
    ],
    spec(
        "rank_names",
        "names",
        'return [f"{rank}. {name}" for rank, name in enumerate(names, start=1)]',
        'return [str(index + 1) + ". " + names[index] for index in range(len(names))]',
        'return [f"{rank}. {name}" for rank, name in enumerate(names)]',
        'Return numbered labels starting at 1, such as ["1. Ada", "2. Lin"]. Preserve names and input order.',
        [
            ('s.rank_names(["Ada", "Lin"]) == ["1. Ada", "2. Lin"]', "Start at one"),
            ("s.rank_names([]) == []", "Empty list"),
            ('s.rank_names(["A", "A"]) == ["1. A", "2. A"]', "Keep repeated names"),
        ],
    ),
    spec(
        "swap_pair",
        "pair",
        "left, right = pair\nreturn right, left",
        "return pair[1], pair[0]",
        "return pair",
        "Given a two-item tuple, return a tuple with its items swapped.",
        [
            ("s.swap_pair((1, 2)) == (2, 1)", "Reverse the pair"),
            ('s.swap_pair(("a", None)) == (None, "a")', "Preserve values"),
            ("type(s.swap_pair((1, 2))) is tuple", "Return a tuple"),
        ],
    ),
    "Use enumerate(names, start=1) and an f-string for each label.",
    (
        "What is the first row?",
        ['(0, "Ada")', '(1, "Ada")', '("Ada", 1)'],
        1,
        "enumerate yields counter first, with the explicit start of one.",
    ),
    [
        "Use ordinary unpacking on one generated row.",
        "Explain when a tuple is clearer than a dictionary.",
    ],
)

f(
    "defaults-without-aliasing",
    "Use safe defaults",
    "Avoid shared mutable defaults and preserve caller-owned lists.",
    'def append_copy(value, items=None):\n    if items is None:\n        items = []\n    return [*items, value]\n\nprint(append_copy("a"))\nassert append_copy("b") == ["b"]',
    [
        "Default argument values are evaluated once when Python executes a function definition. A default like items=[] therefore shares the same list across calls. An earlier call can unexpectedly affect a later one.",
        "Use None as a sentinel for an omitted argument, then create a fresh collection inside the body. Check with is None so an intentionally empty list is handled according to the contract.",
        "Ownership matters even without defaults. Returning [*items, value] creates a new outer list and leaves the caller's list unchanged. This is still a shallow copy, not a copy of nested objects.",
    ],
    [
        ("default argument", "An input value used when the caller omits an argument."),
        ("sentinel", "A special value that represents a distinct condition."),
        ("aliasing", "Multiple names referring to the same mutable object."),
    ],
    spec(
        "add_tag",
        "tag, tags=None",
        "if tags is None:\n    tags = []\nreturn [*tags, tag]",
        "return list(tags if tags is not None else ()) + [tag]",
        "if tags is None:\n    tags = []\ntags.append(tag)\nreturn tags",
        "Return a fresh list with tag appended. tags defaults to None. Never mutate the provided list; calls without tags must be independent.",
        [
            (
                's.add_tag("a") == ["a"] and s.add_tag("b") == ["b"]',
                "Independent defaults",
            ),
            ('s.add_tag("b", ["a"]) == ["a", "b"]', "Append to a copy"),
            ('s.add_tag("a", []) == ["a"]', "Accept an explicit empty list"),
            (
                '((original := ["x"]), s.add_tag("y", original), original)[-1] == ["x"]',
                "Do not mutate the input",
            ),
        ],
    ),
    spec(
        "copy_items",
        "items=None",
        "return [] if items is None else list(items)",
        "if items is None:\n    return []\nreturn items.copy()",
        "return items if items is not None else []",
        "Return a fresh list, or a fresh empty list if omitted.",
        [
            ("s.copy_items() == []", "Omitted input"),
            ("s.copy_items([1, 2]) == [1, 2]", "Copy contents"),
            (
                "((items := [1]), s.copy_items(items) is not items)[-1]",
                "Return a different list",
            ),
        ],
    ),
    "Construct a new list instead of appending to the caller's list.",
    (
        "What does the first call return?",
        ['["a", "b"]', "None", '["a"]'],
        2,
        "Each omitted input gets a fresh list, then a new list is returned.",
    ),
    [
        "Call the function twice and compare identities.",
        "Explain why list.copy does not deeply clone nested dictionaries.",
    ],
)

f(
    "keyword-only-apis",
    "Make call sites clear",
    "Use keyword-only parameters for options whose meaning would be ambiguous by position.",
    "def price(amount, *, discount=0):\n    return amount - discount\n\nprint(price(100, discount=15))\nassert price(100) == 100",
    [
        "Arguments before * may be positional or named. Parameters after a bare * are keyword-only: callers must write their names. This makes an option such as discount=15 readable at the call site.",
        "Default values make options optional; they do not change whether the argument is positional or keyword-only. Unexpected keywords and missing required arguments produce TypeError before the body starts.",
        "A small explicit signature is usually easier to understand than accepting arbitrary **kwargs. Validate a public API's shape as well as its numeric results.",
    ],
    [
        ("keyword-only", "An argument that callers must pass by name."),
        ("signature", "The names, order and calling rules of parameters."),
        (
            "TypeError",
            "An exception for an unsupported operation or invalid call shape.",
        ),
    ],
    spec(
        "greet",
        "name, *, excited=False",
        'suffix = "!" if excited else "."\nreturn f"Hello, {name}{suffix}"',
        'return "Hello, " + name + ("!" if excited else ".")',
        'return f"Hello, {name}!"',
        'Implement greet(name, *, excited=False). Return "Hello, Ada." by default, or "Hello, Ada!" when excited=True. excited must be keyword-only.',
        [
            ('s.greet("Ada") == "Hello, Ada."', "Default punctuation"),
            ('s.greet("Lin", excited=True) == "Hello, Lin!"', "Explicit option"),
            (
                '__import__("inspect").signature(s.greet).parameters["excited"].kind.name == "KEYWORD_ONLY"',
                "Require a named option",
            ),
        ],
    ),
    spec(
        "scale",
        "value, *, factor=2",
        "return value * factor",
        "result = factor * value\nreturn result",
        "return value * 2",
        "Return value multiplied by a keyword-only factor that defaults to 2.",
        [
            ("s.scale(3) == 6", "Use default"),
            ("s.scale(3, factor=4) == 12", "Use supplied factor"),
            (
                '__import__("inspect").signature(s.scale).parameters["factor"].kind.name == "KEYWORD_ONLY"',
                "Keyword-only parameter",
            ),
        ],
    ),
    "Place a bare * before the option in the signature.",
    (
        "What does price(100, discount=15) return?",
        ["85", "100", "TypeError"],
        0,
        "The named option is accepted and subtracted from the amount.",
    ),
    [
        "Try passing excited positionally and read the error.",
        "Name a real API option that should be keyword-only.",
    ],
)

f(
    "missing-is-not-falsy",
    "Separate absence from falsy values",
    "Preserve zero, False and empty text when only None means missing.",
    'def fallback(value):\n    return "unknown" if value is None else value\n\nprint(fallback(0))\nassert fallback(0) == 0',
    [
        "None is a singleton commonly used to represent absence. Test it with value is None. Zero, False and empty text are different values that may be perfectly valid input.",
        "value or fallback replaces every falsy value, not just None. That shorthand is appropriate only when the contract intentionally treats all falsy values as missing.",
        "Write a table of present, missing and explicit-null cases before choosing a fallback rule. A dictionary's get method and a None check answer different questions.",
    ],
    [
        ("None", "The singleton representing absence in many Python APIs."),
        ("truthiness", "How a value behaves in a condition."),
        ("explicit null", "A present field whose value is None."),
    ],
    spec(
        "default_if_none",
        "value, fallback",
        "return fallback if value is None else value",
        "if value is not None:\n    return value\nreturn fallback",
        "return value or fallback",
        "Return fallback only when value is None. Preserve all other values, including 0, False and empty text.",
        [
            ('s.default_if_none(None, "x") == "x"', "Replace None"),
            ("s.default_if_none(0, 9) == 0", "Keep zero"),
            ("s.default_if_none(False, True) is False", "Keep False"),
            ('s.default_if_none("", "x") == ""', "Keep empty text"),
        ],
    ),
    spec(
        "display_name",
        "name",
        'return "Anonymous" if name is None else name',
        'if name is None:\n    return "Anonymous"\nreturn name',
        'return name or "Anonymous"',
        'Return "Anonymous" only for None; preserve empty strings.',
        [
            ('s.display_name(None) == "Anonymous"', "Missing name"),
            ('s.display_name("") == ""', "Empty is present"),
            ('s.display_name("Ada") == "Ada"', "Ordinary name"),
        ],
    ),
    "Use an identity comparison with None, not or.",
    (
        "What does fallback(0) return?",
        ['"unknown"', "0", "None"],
        1,
        "Zero is a present value; only None triggers the fallback.",
    ),
    [
        "Compare dict.get with an absent key and a present None.",
        "Document an API where an empty string means a deliberate user choice.",
    ],
)

f(
    "grouping-records",
    "Group records by a key",
    "Build dictionary buckets without losing records or sharing the same list between groups.",
    'def group_words(words):\n    groups = {}\n    for word in words:\n        groups.setdefault(len(word), []).append(word)\n    return groups\n\nprint(group_words(["a", "to", "b"]))\nassert group_words([]) == {}',
    [
        "Grouping maps a key to a list of records with that key. Start with an empty dictionary and create a fresh list the first time each key appears. Append every record to its group in encounter order.",
        "setdefault(key, default) retrieves an existing value or inserts the default and returns it. defaultdict(list) is another option; calling list creates a separate list for each missing key.",
        "Do not initialize several groups with the same mutable list. Otherwise adding one record can change multiple groups at once. Preserve records unless the task explicitly asks for aggregation.",
    ],
    [
        ("bucket", "The list of records belonging to one grouping key."),
        ("setdefault", "Get a value or insert and return a default."),
        ("aggregation", "Combining several records into a summary."),
    ],
    spec(
        "group_by_team",
        "members",
        'groups = {}\nfor member in members:\n    groups.setdefault(member["team"], []).append(member["name"])\nreturn groups',
        'from collections import defaultdict\ngroups = defaultdict(list)\nfor member in members:\n    groups[member["team"]].append(member["name"])\nreturn dict(groups)',
        'return {m["team"]: [m["name"]] for m in members}',
        "Group member dictionaries by team, returning team -> list of names in input order. Each record has team and name.",
        [
            ("s.group_by_team([]) == {}", "Empty groups"),
            (
                's.group_by_team([{"team":"a","name":"Lin"},{"team":"b","name":"Mo"},{"team":"a","name":"Ada"}]) == {"a":["Lin","Ada"],"b":["Mo"]}',
                "Accumulate, do not overwrite",
            ),
            (
                's.group_by_team([{"team":"a","name":"X"},{"team":"a","name":"X"}]) == {"a":["X","X"]}',
                "Preserve duplicate names",
            ),
        ],
    ),
    spec(
        "count_words",
        "words",
        "counts = {}\nfor word in words:\n    counts[word] = counts.get(word, 0) + 1\nreturn counts",
        "from collections import Counter\nreturn dict(Counter(words))",
        "return {word: 1 for word in words}",
        "Count occurrences of each exact word.",
        [
            ('s.count_words(["a", "b", "a"]) == {"a":2,"b":1}', "Accumulate counts"),
            ("s.count_words([]) == {}", "Empty counts"),
            ('s.count_words(["A", "a"]) == {"A":1,"a":1}', "Case-sensitive keys"),
        ],
    ),
    "Create one bucket per team, then append names instead of replacing the bucket.",
    (
        "What is the bucket for length 1?",
        ['["b"]', '["a", "to", "b"]', '["a", "b"]'],
        2,
        "Both one-character words enter the same bucket in input order.",
    ),
    [
        "Try three teams and ensure their buckets are separate lists.",
        "Explain the memory cost of retaining all records versus only counts.",
    ],
)

f(
    "sorting-with-keys",
    "Sort by meaning",
    "Use a key function and preserve input when producing an ordered view.",
    'rows = [{"name": "b", "score": 2}, {"name": "a", "score": 2}]\nordered = sorted(rows, key=lambda row: (-row["score"], row["name"]))\nprint([row["name"] for row in ordered])\nassert rows[0]["name"] == "b"',
    [
        "sorted(iterable, key=...) returns a new list. list.sort mutates an existing list and returns None. Pick the operation that matches the ownership contract.",
        "A key function computes the value used for comparison. A lambda is a small anonymous function. A tuple key compares its first field, then the next field when earlier fields tie.",
        "Python sorting is stable: equal keys keep their input order. For descending numeric score and ascending name, use (-score, name); reverse=True would reverse both fields.",
    ],
    [
        ("key function", "A function that extracts the comparison value."),
        ("stable sort", "Equal keys preserve their previous order."),
        ("lambda", "A short anonymous function expression."),
    ],
    spec(
        "leaderboard",
        "rows",
        'return sorted(rows, key=lambda row: (-row["score"], row["name"]))',
        'return sorted(sorted(rows, key=lambda row: row["name"]), key=lambda row: row["score"], reverse=True)',
        'return sorted(rows, key=lambda row: row["score"])',
        "Return a new list ordered by score descending, then name ascending. Do not reorder the input list.",
        [
            ("s.leaderboard([]) == []", "Empty view"),
            (
                '[r["name"] for r in s.leaderboard([{"name":"Z","score":5},{"name":"B","score":9},{"name":"A","score":9}])] == ["A","B","Z"]',
                "Apply both sort directions",
            ),
            (
                '((rows := [{"name":"b","score":1},{"name":"a","score":2}]), s.leaderboard(rows), rows[0]["name"])[-1] == "b"',
                "Do not mutate the caller",
            ),
        ],
    ),
    spec(
        "sort_by_length",
        "words",
        "return sorted(words, key=len)",
        "return sorted(words, key=lambda word: len(word))",
        "return sorted(words)",
        "Return a new list of words ordered by length ascending; ties preserve input order.",
        [
            (
                's.sort_by_length(["bbb", "z", "aa", "x"]) == ["z","x","aa","bbb"]',
                "Stable length ordering",
            ),
            ("s.sort_by_length([]) == []", "Empty view"),
        ],
    ),
    "Use a tuple key with negative score and unchanged name.",
    (
        "What names are printed?",
        ['["a", "b"]', '["b", "a"]', "TypeError"],
        0,
        "Scores tie, so the ascending name breaks the tie.",
    ),
    [
        "Add identical keys and confirm stability.",
        "Explain why reverse=True would produce the wrong tie order.",
    ],
)

f(
    "generators-and-laziness",
    "Yield values on demand",
    "Write a generator and distinguish creating it from consuming it.",
    "def countdown(start):\n    while start > 0:\n        yield start\n        start -= 1\n\nprint(list(countdown(3)))\nassert list(countdown(0)) == []",
    [
        "A function containing yield returns a generator object when called. Its body runs as the caller requests values, rather than building the complete result immediately.",
        "yield produces one value and suspends the function, retaining local state. next(generator) resumes it; a for loop consumes values until StopIteration indicates completion.",
        "A generator is normally single-use. Converting it to a list consumes it and allocates memory for all results. Laziness helps large or infinite streams only when callers also consume incrementally.",
    ],
    [
        ("generator", "A resumable iterator produced by a function with yield."),
        ("lazy", "Compute values only when requested."),
        ("StopIteration", "The signal that an iterator has no more values."),
    ],
    spec(
        "chunks",
        "items, size",
        'if size <= 0:\n    raise ValueError("size must be positive")\nfor start in range(0, len(items), size):\n    yield items[start:start + size]',
        'if size <= 0:\n    raise ValueError("size must be positive")\nstart = 0\nwhile start < len(items):\n    yield items[start:start + size]\n    start += size',
        "yield items",
        "Yield consecutive list slices of at most size items. size must be positive or raise ValueError when consumed. Return a generator, including for empty input.",
        [
            (
                "list(s.chunks([1,2,3,4,5], 2)) == [[1,2],[3,4],[5]]",
                "Keep final partial chunk",
            ),
            ("list(s.chunks([], 2)) == []", "No empty chunk"),
            ('__import__("inspect").isgenerator(s.chunks([1], 1))', "Use a generator"),
            ("list(s.chunks([1,2], 9)) == [[1,2]]", "Larger chunk size"),
        ],
    ),
    spec(
        "countdown",
        "start",
        "while start > 0:\n    yield start\n    start -= 1",
        "yield from range(start, 0, -1)",
        "yield from range(start)",
        "Yield start, start-1, down to 1. Yield nothing for zero or negative start.",
        [
            ("list(s.countdown(3)) == [3,2,1]", "Descending order"),
            ("list(s.countdown(0)) == []", "Empty at zero"),
            ("list(s.countdown(-1)) == []", "Empty for negatives"),
            ('__import__("inspect").isgenerator(s.countdown(2))', "Return a generator"),
        ],
    ),
    "Use yield inside a loop over range(0, len(items), size). Validate size before iteration.",
    (
        "What does list(countdown(3)) produce?",
        ["[0,1,2]", "[3,2,1]", "[3,2,1,0]"],
        1,
        "The while condition stops before yielding zero.",
    ),
    [
        "Call next twice, then consume the rest.",
        "Explain why validation inside a generator happens at consumption time.",
    ],
)

f(
    "exceptions-and-validation",
    "Fail with a useful exception",
    "Validate an input and raise a specific exception instead of returning a misleading value.",
    'def positive(value):\n    if value <= 0:\n        raise ValueError("value must be positive")\n    return value\n\nprint(positive(3))\nassert positive(3) == 3',
    [
        "An exception interrupts ordinary control flow and travels to the nearest matching handler. raise ValueError(...) communicates that the input value violates this function's rule.",
        "Validate at a boundary before using invalid data. A function that returns zero for both a real zero and a failed operation forces its callers to guess what happened.",
        "Catch only exceptions you can handle meaningfully. A broad except can hide a programming defect. Tests should verify both valid outputs and the precise invalid-input policy.",
    ],
    [
        ("exception", "A signal that ordinary execution cannot continue."),
        ("raise", "Create and propagate an exception."),
        ("validation", "Check whether input meets an explicit rule."),
    ],
    spec(
        "divide",
        "numerator, denominator",
        'if denominator == 0:\n    raise ValueError("denominator must not be zero")\nreturn numerator / denominator',
        'if not denominator:\n    raise ValueError("zero denominator")\nreturn numerator / denominator',
        "return numerator / denominator if denominator else 0",
        "Return numerator / denominator; raise ValueError for a zero denominator.",
        [
            ("s.divide(9, 3) == 3", "Ordinary division"),
            ("s.divide(-5, 2) == -2.5", "Keep sign and fractions"),
            (
                "raises(ValueError, s.divide, 1, 0)",
                "Reject division by zero with ValueError",
            ),
            ("s.divide(0, 3) == 0", "Zero numerator is valid"),
        ],
    ),
    spec(
        "require_positive",
        "value",
        'if value <= 0:\n    raise ValueError("expected positive")\nreturn value',
        'if value > 0:\n    return value\nraise ValueError("expected positive")',
        "return abs(value)",
        "Return a positive value unchanged; raise ValueError for zero or negatives.",
        [
            ("s.require_positive(3) == 3", "Preserve valid input"),
            ("raises(ValueError, s.require_positive, 0)", "Reject zero"),
            ("raises(ValueError, s.require_positive, -1)", "Reject negatives"),
        ],
    ),
    "Raise ValueError before dividing when the denominator equals zero.",
    (
        "What does positive(0) do?",
        ["Returns 0", "Raises ValueError", "Returns None"],
        1,
        "The validation branch raises before the return can run.",
    ),
    [
        "Compare this public ValueError policy with Python's built-in ZeroDivisionError.",
        "Write an error message that helps a caller fix its input.",
    ],
)

f(
    "parsing-with-fallbacks",
    "Parse an integer carefully",
    "Handle expected conversion errors without swallowing unrelated problems.",
    'def parse_or_none(text):\n    try:\n        return int(text)\n    except ValueError:\n        return None\n\nprint(parse_or_none("12"))\nassert parse_or_none("no") is None',
    [
        "Parsing converts a representation into a usable value. int(text) accepts surrounding whitespace and a sign, but rejects decimal fractions and arbitrary words with ValueError.",
        "Place only the operation that may fail inside try. except ValueError handles that expected failure. Returning None is an explicit policy here, not a replacement for every exception.",
        "TypeError means a different contract problem, such as passing an unsupported object. Do not catch every exception when your API promises only to handle malformed text.",
    ],
    [
        ("parsing", "Convert a textual representation into structured data."),
        ("try/except", "Handle a specific exceptional path."),
        ("error policy", "The documented outcome for invalid input."),
    ],
    spec(
        "parse_count",
        "text",
        "try:\n    value = int(text)\nexcept ValueError:\n    return None\nreturn value if value >= 0 else None",
        "try:\n    value = int(text)\n    if value < 0:\n        return None\n    return value\nexcept ValueError:\n    return None",
        "return int(text)",
        "Parse integer text; return None for malformed text or negative counts. Preserve zero.",
        [
            ('s.parse_count(" 12 ") == 12', "Trim is accepted by int"),
            ('s.parse_count("0") == 0', "Zero count is valid"),
            ('s.parse_count("-1") is None', "Reject negative count"),
            ('s.parse_count("3.2") is None', "Reject fractional text"),
            ('s.parse_count("bad") is None', "Reject words"),
        ],
    ),
    spec(
        "parse_or",
        "text, default=0",
        "try:\n    return int(text)\nexcept ValueError:\n    return default",
        "try:\n    parsed = int(text)\nexcept ValueError:\n    parsed = default\nreturn parsed",
        "return int(text)",
        "Parse integer text; on ValueError return default, which defaults to zero.",
        [
            ('s.parse_or("3") == 3', "Valid text"),
            ('s.parse_or("x") == 0', "Default fallback"),
            ('s.parse_or("x", 7) == 7', "Explicit fallback"),
            ('s.parse_or("-2") == -2', "Negative integers are valid here"),
        ],
    ),
    "Catch ValueError from int, then validate the parsed count.",
    (
        'What is parse_or_none("no")?',
        ["0", "ValueError", "None"],
        2,
        "The matching except branch deliberately returns None.",
    ),
    [
        "Try a list as input and explain the uncaught TypeError.",
        "Explain why zero must not be mistaken for parse failure.",
    ],
)

f(
    "json-at-the-boundary",
    "Validate decoded JSON",
    "Distinguish successful JSON decoding from a valid domain record.",
    'import json\nrecord = json.loads(\'{"name":"Ada","active":true}\')\nprint(record["active"])\nassert record["active"] is True',
    [
        "json.loads turns JSON text into Python data. JSON true becomes True, null becomes None, objects become dicts, and arrays become lists. Valid JSON can also be a single number or string.",
        "Decoding proves only that the text follows JSON syntax. It does not prove that a required field exists or has the right type. Validate the shape before treating external data as a trusted domain object.",
        "In Python, bool is a subclass of int. Use type(value) is int when an exact integer is required and True must be rejected as a count.",
    ],
    [
        ("JSON", "A text format for structured data."),
        ("schema", "The required shape and rules of a record."),
        ("boundary", "Where data enters from another system or representation."),
    ],
    spec(
        "read_user",
        "text",
        'import json\nrecord = json.loads(text)\nif not isinstance(record, dict) or not isinstance(record.get("name"), str) or not record["name"].strip():\n    raise ValueError("name must be nonempty text")\nreturn {"name": record["name"].strip()}',
        'import json\nvalue = json.loads(text)\nif type(value) is not dict:\n    raise ValueError("expected object")\nname = value.get("name")\nif type(name) is not str or not name.strip():\n    raise ValueError("invalid name")\nreturn dict(name=name.strip())',
        "import json\nreturn json.loads(text)",
        'Decode an object with a nonempty string name; return only {"name": trimmed_name}. Raise ValueError for invalid JSON or shape. Ignore extra fields.',
        [
            (
                's.read_user(\'{"name":" Ada ","admin":true}\') == {"name":"Ada"}',
                "Validate and project fields",
            ),
            ('raises(ValueError, s.read_user, "[]")', "Reject arrays"),
            ("raises(ValueError, s.read_user, '{\"name\":4}')", "Reject nontext names"),
            ('raises(ValueError, s.read_user, \'{"name":" "}\')', "Reject empty names"),
            ('raises(ValueError, s.read_user, "broken")', "Reject malformed JSON"),
        ],
    ),
    spec(
        "read_names",
        "text",
        'import json\nvalue = json.loads(text)\nif not isinstance(value, list) or not all(isinstance(item, str) for item in value):\n    raise ValueError("expected list of strings")\nreturn value',
        'import json\nitems = json.loads(text)\nif type(items) is not list:\n    raise ValueError("expected list")\nfor item in items:\n    if type(item) is not str:\n        raise ValueError("expected string")\nreturn items',
        "import json\nreturn json.loads(text)",
        "Decode a JSON array of strings. Raise ValueError for other shapes or malformed JSON.",
        [
            ('s.read_names(\'["Ada","Lin"]\') == ["Ada","Lin"]', "Decode names"),
            ('s.read_names("[]") == []', "Empty array"),
            ('raises(ValueError, s.read_names, "[1]")', "Check element types"),
            ('raises(ValueError, s.read_names, "{}")', "Check container type"),
        ],
    ),
    "Decode first, validate the object and name, then construct a clean result.",
    (
        "What is the Python value of active?",
        ["True", '"true"', "1"],
        0,
        "JSON true decodes to the Python boolean True.",
    ),
    [
        "Try JSON null and a top-level string.",
        "Explain why blindly trusting a type annotation would not validate JSON.",
    ],
)

f(
    "csv-with-a-parser",
    "Read CSV without splitting commas",
    "Use DictReader to handle quoted fields and validate required headers.",
    'import csv\nimport io\nrows = list(csv.DictReader(io.StringIO(\'name,city\\n"Ada, Jr",Paris\\n\')))\nprint(rows[0]["name"])\nassert rows[0]["name"] == "Ada, Jr"',
    [
        "CSV is a format with quoting rules, not simply text separated by commas. A comma inside a quoted field belongs to the value. Newlines may also appear inside quoted fields.",
        "csv.DictReader reads the header and produces dictionaries. io.StringIO presents an in-memory string as a text stream, so the same parser can be used without touching real files.",
        "Validate headers explicitly before accessing columns. Decide whether blank fields are allowed; a syntactically readable file can still violate your domain rules.",
    ],
    [
        ("CSV", "A tabular text format with separators and quoting rules."),
        ("stream", "An object from which data can be read incrementally."),
        ("header", "The first row naming the columns."),
    ],
    spec(
        "csv_emails",
        "text",
        'import csv\nimport io\nreader = csv.DictReader(io.StringIO(text))\nif not reader.fieldnames or "email" not in reader.fieldnames:\n    raise ValueError("email header required")\nreturn [row["email"].strip().lower() for row in reader if row["email"].strip()]',
        'import csv\nfrom io import StringIO\nreader = csv.DictReader(StringIO(text))\nif "email" not in (reader.fieldnames or []):\n    raise ValueError("email header required")\nemails = []\nfor row in reader:\n    if row["email"].strip():\n        emails.append(row["email"].strip().lower())\nreturn emails',
        'return [line.split(",")[-1] for line in text.splitlines()[1:]]',
        "Read CSV with a required email header. Return nonblank emails trimmed and lowercased, in row order. Honor CSV quoting; raise ValueError if the header is missing.",
        [
            (
                's.csv_emails("name,email\nAda, A@EXAMPLE.COM \nLin,\n") == ["a@example.com"]',
                "Normalize and skip blanks",
            ),
            (
                's.csv_emails(\'name,email\n"Ada, Jr",a@x.io\n\') == ["a@x.io"]',
                "Quoted commas",
            ),
            ('s.csv_emails("email\n") == []', "Header-only file"),
            ('raises(ValueError, s.csv_emails, "name\nAda\n")', "Require header"),
        ],
    ),
    spec(
        "csv_names",
        "text",
        'import csv\nimport io\nreader = csv.DictReader(io.StringIO(text))\nif "name" not in (reader.fieldnames or []):\n    raise ValueError("name header required")\nreturn [row["name"] for row in reader]',
        'from csv import DictReader\nfrom io import StringIO\nreader = DictReader(StringIO(text))\nif not reader.fieldnames or "name" not in reader.fieldnames:\n    raise ValueError("missing name")\nreturn list(map(lambda row: row["name"], reader))',
        'return [line.split(",")[0] for line in text.splitlines()[1:]]',
        "Return the name column exactly, respecting quoted commas. Require a name header.",
        [
            (
                's.csv_names(\'name,city\n"Ada, Jr",Paris\n\') == ["Ada, Jr"]',
                "Parse quotes",
            ),
            ('s.csv_names("name\n") == []', "No data rows"),
            ('raises(ValueError, s.csv_names, "city\nParis\n")', "Require name"),
        ],
    ),
    "Use csv.DictReader over io.StringIO; never split each line on a comma.",
    (
        "What is the first name?",
        ["Ada", "Ada, Jr", '"Ada, Jr"'],
        1,
        "The parser removes CSV quoting while preserving the embedded comma.",
    ),
    [
        "Add a quoted newline inside a field.",
        "Describe how a malformed row should be reported in an import tool.",
    ],
)

f(
    "files-and-contexts",
    "Own a file lifetime",
    "Read and write UTF-8 files with a context manager in the private scratch workspace.",
    'from pathlib import Path\npath = Path("example.txt")\nwith path.open("w", encoding="utf-8") as stream:\n    stream.write("hello\\n")\nprint(path.read_text(encoding="utf-8").strip())\nassert path.read_text(encoding="utf-8") == "hello\\n"',
    [
        "A file is an external resource that must be closed even if an error occurs. with opens a context-managed lifetime and calls cleanup when the block exits, including exceptional exits.",
        'Specify encoding="utf-8" for a portable text contract. A file opened in w mode is truncated immediately. Reading and writing are side effects, so keep their location and ownership explicit.',
        "PyDojo runs each session in a new private scratch directory. Paths in these exercises refer to temporary learning files, not your Documents directory. They are removed after the session, so save reusable logic in answer.py rather than relying on persistent scratch files.",
    ],
    [
        ("context manager", "An object defining setup and cleanup for a with block."),
        ("encoding", "The mapping between text characters and bytes."),
        ("side effect", "An observable change outside a returned value."),
    ],
    spec(
        "write_lines",
        "path, lines",
        'with open(path, "w", encoding="utf-8") as stream:\n    for line in lines:\n        stream.write(line + "\\n")\nreturn len(lines)',
        'from pathlib import Path\nPath(path).write_text("".join(line + "\\n" for line in lines), encoding="utf-8")\nreturn len(lines)',
        'with open(path, "a", encoding="utf-8") as stream:\n    stream.write("\\n".join(lines))\nreturn len(lines)',
        "Write each input line followed by one newline to path, replacing prior content. Use UTF-8 and return the number of lines. Empty input creates an empty file.",
        [
            ('s.write_lines("notes.txt", ["café", "lab"]) == 2', "Return count"),
            (
                'open("notes.txt", encoding="utf-8").read() == "café\nlab\n"',
                "Write UTF-8 and final newline",
            ),
            (
                's.write_lines("notes.txt", []) == 0 and open("notes.txt").read() == ""',
                "Truncate for empty input",
            ),
        ],
    ),
    spec(
        "read_nonblank",
        "path",
        'with open(path, encoding="utf-8") as stream:\n    return [line.strip() for line in stream if line.strip()]',
        'from pathlib import Path\nreturn [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]',
        "return open(path).read().splitlines()",
        "Read UTF-8 lines, trimming each and excluding blank lines. Let FileNotFoundError propagate for a missing file.",
        [
            (
                '(open("input.txt", "w", encoding="utf-8").write(" café \n\n lab\n"), s.read_nonblank("input.txt"))[-1] == ["café","lab"]',
                "Trim and skip blanks",
            ),
            (
                'raises(FileNotFoundError, s.read_nonblank, "missing.txt")',
                "Do not hide missing files",
            ),
        ],
    ),
    "Open in w mode, specify UTF-8, and write a newline after every input line.",
    (
        "What is printed after the file is read?",
        ["hello", "hello\\n", "FileNotFoundError"],
        0,
        "The file exists within this scratch session and strip removes its final newline.",
    ),
    [
        "Raise an exception inside a with block and check stream.closed.",
        "Explain why w mode is dangerous on a real user file.",
    ],
)

f(
    "decimal-money",
    "Make rounding explicit",
    "Use Decimal from strings and an explicit rounding policy for exact decimal amounts.",
    'from decimal import Decimal, ROUND_HALF_UP\namount = Decimal("2.675")\nrounded = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)\nprint(rounded)\nassert str(rounded) == "2.68"',
    [
        "Binary floats cannot represent many decimal fractions exactly. Decimal represents decimal values according to a decimal context; construct it from a string to avoid importing a float's approximation.",
        "quantize selects a decimal scale, and rounding specifies what happens at a tie. ROUND_HALF_UP is one policy, not a universal financial rule. Different jurisdictions and products may require different rules.",
        "Keep units and boundaries explicit. This lab accepts amount text and returns fixed two-decimal text, so no caller has to guess whether a number represents dollars, cents, or a binary approximation.",
    ],
    [
        ("Decimal", "A decimal arithmetic type with explicit precision and rounding."),
        ("quantize", "Round to a specified decimal exponent."),
        (
            "rounding policy",
            "The rule used when a value lies between representable results.",
        ),
    ],
    spec(
        "money_text",
        "amount",
        'from decimal import Decimal, ROUND_HALF_UP\nreturn format(Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), ".2f")',
        'import decimal\nvalue = decimal.Decimal(amount)\nvalue = value.quantize(decimal.Decimal(".01"), rounding=decimal.ROUND_HALF_UP)\nreturn f"{value:.2f}"',
        'return f"{float(amount):.2f}"',
        "Convert valid finite decimal amount text to two-decimal text using ROUND_HALF_UP, including negative ties.",
        [
            ('s.money_text("2.675") == "2.68"', "Positive tie"),
            ('s.money_text("-1.005") == "-1.01"', "Negative tie rounds away from zero"),
            ('s.money_text("3") == "3.00"', "Keep fixed scale"),
            ('s.money_text("0") == "0.00"', "Zero amount"),
        ],
    ),
    spec(
        "decimal_sum",
        "left, right",
        "from decimal import Decimal\nreturn str(Decimal(left) + Decimal(right))",
        "import decimal\ntotal = decimal.Decimal(left)\ntotal += decimal.Decimal(right)\nreturn str(total)",
        "return str(float(left) + float(right))",
        "Add two valid decimal strings exactly and return Decimal's string representation.",
        [
            ('s.decimal_sum("0.1", "0.2") == "0.3"', "Exact decimal sum"),
            ('s.decimal_sum("1.20", "2.30") == "3.50"', "Preserve decimal scale"),
            ('s.decimal_sum("-1", "1") == "0"', "Opposite values"),
        ],
    ),
    "Build Decimal directly from text and provide ROUND_HALF_UP to quantize.",
    (
        "What is rounded?",
        ["2.67", "2.68", "2.675"],
        1,
        "An exact decimal tie is rounded according to the explicit half-up policy.",
    ),
    [
        'Compare Decimal("0.1") with Decimal(0.1).',
        "State where a real pricing system should define its rounding policy.",
    ],
)

# 24: date handling completes the reliable-data chapter.
f(
    "dates-with-timezones",
    "Treat time as a domain value",
    "Parse timezone-aware ISO timestamps and normalize an instant to UTC.",
    'from datetime import datetime, timezone\ninstant = datetime.fromisoformat("2026-01-01T09:00:00+02:00")\nprint(instant.astimezone(timezone.utc).isoformat())\nassert instant.utcoffset().total_seconds() == 7200',
    [
        "A datetime can be naive, with no usable timezone offset, or aware, identifying an instant relative to UTC. Do not silently mix the two; the same wall-clock text can refer to different instants.",
        "datetime.fromisoformat parses supported ISO forms. astimezone(timezone.utc) converts an aware instant while preserving which moment it represents. replace(tzinfo=...) assigns metadata and is not a timezone conversion.",
        "An offset such as +02:00 is not the same as a regional timezone with daylight-saving rules. This exercise accepts explicit offsets only; real scheduling needs a regional-zone policy.",
    ],
    [
        ("aware datetime", "A date-time with a usable UTC offset."),
        ("UTC", "A common reference for representing instants."),
        ("offset", "The difference between local wall-clock time and UTC."),
    ],
    spec(
        "utc_text",
        "text",
        'from datetime import datetime, timezone\nvalue = datetime.fromisoformat(text)\nif value.utcoffset() is None:\n    raise ValueError("timezone offset required")\nreturn value.astimezone(timezone.utc).isoformat()',
        'import datetime\nvalue = datetime.datetime.fromisoformat(text)\nif value.tzinfo is None or value.utcoffset() is None:\n    raise ValueError("aware timestamp required")\nreturn value.astimezone(datetime.timezone.utc).isoformat()',
        "from datetime import datetime, timezone\nreturn datetime.fromisoformat(text).replace(tzinfo=timezone.utc).isoformat()",
        "Normalize an ISO timestamp with an explicit offset to UTC ISO text. Raise ValueError for naive or malformed timestamps.",
        [
            (
                's.utc_text("2026-01-01T09:00:00+02:00") == "2026-01-01T07:00:00+00:00"',
                "Convert, do not relabel",
            ),
            (
                's.utc_text("2026-01-01T00:00:00-03:00") == "2026-01-01T03:00:00+00:00"',
                "Negative offset",
            ),
            (
                'raises(ValueError, s.utc_text, "2026-01-01T09:00:00")',
                "Reject naive time",
            ),
            ('raises(ValueError, s.utc_text, "bad")', "Reject malformed time"),
        ],
    ),
    spec(
        "iso_date",
        "text",
        "from datetime import date\nreturn date.fromisoformat(text).isoformat()",
        "import datetime\nparsed = datetime.date.fromisoformat(text)\nreturn str(parsed)",
        "return text",
        "Parse a valid ISO date and return normalized ISO date text. Invalid dates raise ValueError.",
        [
            ('s.iso_date("2024-02-29") == "2024-02-29"', "Leap day"),
            ('raises(ValueError, s.iso_date, "2025-02-29")', "Invalid leap day"),
            ('raises(ValueError, s.iso_date, "bad")', "Invalid text"),
        ],
    ),
    "Check utcoffset() before calling astimezone(timezone.utc).",
    (
        "Which UTC hour corresponds to 09:00 at +02:00?",
        ["11:00", "09:00", "07:00"],
        2,
        "Subtract the two-hour offset to represent the same instant in UTC.",
    ),
    [
        "Normalize a timestamp that crosses midnight in UTC.",
        "Explain why a recurring meeting needs more than a fixed offset.",
    ],
)

add(
    "classes-and-state",
    "Encapsulate changing state",
    "Create independent instances and update state through methods.",
    "class Counter:\n    def __init__(self):\n        self.value = 0\n\n    def increment(self):\n        self.value += 1\n        return self.value\n\ncounter = Counter()\nprint(counter.increment())\nassert Counter().value == 0",
    [
        "A class defines how instances are created and what operations they provide. __init__ initializes a new instance; self refers to the instance receiving a method call.",
        "Assign per-instance state through self. A mutable class attribute would instead be shared by instances, often causing one learner, account, or request to affect another.",
        "Methods should represent meaningful domain operations. Keep an invariant true after every public operation instead of letting callers coordinate several fragile assignments.",
    ],
    [
        ("instance", "One object created from a class."),
        ("self", "The instance passed as the first method argument."),
        ("invariant", "A rule that remains true after every valid operation."),
    ],
    raw(
        "Implement Counter(start=0) with public value and increment(step=1), returning the updated value. Instances must be independent.",
        "class Counter:\n    pass",
        """
class Counter:
    def __init__(self, start=0):
        self.value = start
    def increment(self, step=1):
        self.value += step
        return self.value
""",
        """
class Counter:
    def __init__(self, start=0):
        self.value = start
    def increment(self, step=1):
        self.value = self.value + step
        return self.value
""",
        """
class Counter:
    value = 0
    def __init__(self, start=0):
        self.value = start
    def increment(self, step=1):
        self.value += 1
        return self.value
""",
        'a = s.Counter(2)\nb = s.Counter()\nassert a.increment() == 3, "Default increment"\nassert a.increment(4) == 7, "Use the supplied step"\nassert b.value == 0, "Keep instances independent"\nassert a.increment(-2) == 5, "Support negative steps"',
    ),
    raw(
        "Implement Box(value) with a public value and replace(value) that updates and returns the new value.",
        "class Box:\n    pass",
        "class Box:\n    def __init__(self, value):\n        self.value = value\n    def replace(self, value):\n        self.value = value\n        return value",
        "class Box:\n    def __init__(self, value):\n        self.replace(value)\n    def replace(self, value):\n        self.value = value\n        return self.value",
        "class Box:\n    def __init__(self, value):\n        self.value = value\n    def replace(self, value):\n        return value",
        'box = s.Box(1)\nassert box.replace(2) == 2 and box.value == 2, "Update the instance"\nassert s.Box(9).value == 9, "Independent state"',
    ),
    "Initialize self.value in __init__ and update that same attribute in increment.",
    (
        "What does counter.increment() return?",
        ["0", "1", "None"],
        1,
        "The method updates this instance from zero to one and returns its new value.",
    ),
    [
        "Create two counters and alternate calls.",
        "Explain why a shared list declared on a class is different from an instance field.",
    ],
)

add(
    "dataclasses-and-values",
    "Model a value with a dataclass",
    "Use annotations and dataclasses to create explicit immutable records.",
    "from dataclasses import dataclass\n@dataclass(frozen=True)\nclass Point:\n    x: int\n    y: int\n\nprint(Point(1, 2) == Point(1, 2))\nassert Point(1, 2).x == 1",
    [
        "@dataclass reads annotated fields and generates methods such as __init__, __repr__, and equality. The decorator runs after the class is defined. An annotation describes intent; it does not validate a runtime value.",
        "frozen=True rejects ordinary field reassignment. It is useful for value objects, but it is not deep immutability: a list stored inside a frozen record can still change.",
        "Choose a mutable object for a lifecycle with controlled changes, and a value record for a fact that should be replaced as a whole. Domain validation still belongs at an explicit boundary.",
    ],
    [
        (
            "dataclass",
            "A class decorator generating record-oriented methods from fields.",
        ),
        ("annotation", "Metadata expressing the intended type of a name."),
        ("value object", "A record compared by its contents rather than its identity."),
    ],
    raw(
        "Create a frozen dataclass Product with fields sku: str and price_cents: int. Add subtotal(quantity) returning price_cents * quantity.",
        "class Product:\n    pass",
        "from dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass Product:\n    sku: str\n    price_cents: int\n    def subtotal(self, quantity):\n        return self.price_cents * quantity",
        "import dataclasses\n\n@dataclasses.dataclass(frozen=True)\nclass Product:\n    sku: str\n    price_cents: int\n    def subtotal(self, quantity):\n        return quantity * self.price_cents",
        "from dataclasses import dataclass\n\n@dataclass\nclass Product:\n    sku: str\n    price_cents: int\n    def subtotal(self, quantity):\n        return self.price_cents * quantity",
        'import dataclasses\np = s.Product("book", 1250)\nassert dataclasses.is_dataclass(p), "Use a dataclass"\nassert p.subtotal(3) == 3750 and p.subtotal(0) == 0, "Multiply quantity"\nassert p == s.Product("book", 1250), "Value equality"\nassert raises(dataclasses.FrozenInstanceError, setattr, p, "price_cents", 1), "Freeze reassignment"',
    ),
    raw(
        "Create a frozen dataclass Point with integer-annotated x and y fields.",
        "class Point:\n    pass",
        "from dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass Point:\n    x: int\n    y: int",
        "import dataclasses\n\n@dataclasses.dataclass(frozen=True)\nclass Point:\n    x: int\n    y: int",
        "from dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: int\n    y: int",
        'import dataclasses\np = s.Point(1, 2)\nassert dataclasses.is_dataclass(p) and p == s.Point(1, 2), "Record equality"\nassert raises(dataclasses.FrozenInstanceError, setattr, p, "x", 3), "Frozen field"',
    ),
    "Use @dataclass(frozen=True) and annotate both fields before defining the method.",
    (
        "Why are the two Point values equal?",
        [
            "They are the same object",
            "Python ignores the fields",
            "The dataclass compares field values",
        ],
        2,
        "Generated dataclass equality compares corresponding fields of the same class.",
    ),
    [
        "Put a list in a frozen dataclass and test its mutability.",
        "Explain why annotations alone do not reject a string price.",
    ],
)

f(
    "explicit-state-transitions",
    "Define valid state transitions",
    "Express a finite workflow and reject transitions outside the contract.",
    'def next_state(state, action):\n    transitions = {("draft", "submit"): "review", ("review", "approve"): "published"}\n    if (state, action) not in transitions:\n        raise ValueError("invalid transition")\n    return transitions[state, action]\n\nprint(next_state("draft", "submit"))',
    [
        "A workflow has named states and events that may move it between them. A transition table makes allowed combinations visible instead of spreading rules across unrelated boolean flags.",
        "A tuple is a suitable dictionary key for a pair of immutable strings. Looking up (state, action) expresses one rule directly. A missing transition is a domain error, not permission to keep going.",
        "Validate the current state and event together. Without this boundary, a duplicate event or a stale client can skip required review steps. Persistence and concurrency would need additional guarantees in a real service.",
    ],
    [
        ("state machine", "A set of states and allowed transitions."),
        ("transition", "A permitted change caused by an event."),
        ("domain error", "A failure defined by the rules of the problem."),
    ],
    spec(
        "transition",
        "state, event",
        'rules = {("pending", "start"): "running", ("running", "finish"): "done", ("running", "fail"): "failed"}\nif (state, event) not in rules:\n    raise ValueError("invalid transition")\nreturn rules[state, event]',
        'if state == "pending" and event == "start":\n    return "running"\nif state == "running" and event in ("finish", "fail"):\n    return "done" if event == "finish" else "failed"\nraise ValueError("invalid transition")',
        'return "done" if event == "finish" else "running"',
        "Allow pending/start -> running, running/finish -> done, running/fail -> failed. Raise ValueError for every other pair.",
        [
            ('s.transition("pending", "start") == "running"', "Start pending work"),
            ('s.transition("running", "finish") == "done"', "Finish running work"),
            ('s.transition("running", "fail") == "failed"', "Record failure"),
            (
                'raises(ValueError, s.transition, "done", "start")',
                "Terminal states cannot restart",
            ),
            (
                'raises(ValueError, s.transition, "pending", "finish")',
                "Do not skip running",
            ),
        ],
    ),
    spec(
        "can_publish",
        "state",
        'return state == "approved"',
        'if state == "approved":\n    return True\nreturn False',
        'return state != "draft"',
        'Return True only for the exact state "approved".',
        [
            ('s.can_publish("approved") is True', "Approved can publish"),
            ('s.can_publish("draft") is False', "Draft cannot"),
            ('s.can_publish("unknown") is False', "Unknown cannot"),
        ],
    ),
    "Map each allowed pair explicitly and raise ValueError for missing pairs.",
    (
        "What follows draft + submit?",
        ["review", "published", "draft"],
        0,
        "The table explicitly maps that pair to review.",
    ),
    [
        "Draw the state graph and identify terminal states.",
        "Explain why two concurrent transitions require more than this pure function.",
    ],
)

add(
    "properties-and-invariants",
    "Protect a domain invariant",
    "Expose readable state while keeping updates behind a validating operation.",
    'class Wallet:\n    def __init__(self):\n        self._balance = 0\n    @property\n    def balance(self):\n        return self._balance\n    def deposit(self, cents):\n        if cents <= 0:\n            raise ValueError("positive cents required")\n        self._balance += cents\n\nwallet = Wallet()\nwallet.deposit(100)\nprint(wallet.balance)',
    [
        "A property presents a method as attribute access. A read-only property without a setter prevents ordinary assignment to that public attribute. The underscore in _balance signals internal ownership by convention; it is not secrecy.",
        "Validate before changing state. If a withdrawal would overdraw an account, reject it while keeping the previous balance intact. Partial state changes followed by an exception break trust in the object.",
        "An object with money-like state should use explicit units and well-defined operations. This exercise models integer cents in memory; production financial systems require durable transactions and audit records as well.",
    ],
    [
        ("property", "A descriptor exposing controlled attribute access."),
        ("encapsulation", "Keep state changes behind meaningful operations."),
        ("atomic failure", "A rejected operation leaves prior state unchanged."),
    ],
    raw(
        "Implement Wallet(balance=0) with read-only balance and withdraw(cents). Reject nonpositive amounts or overdrafts with ValueError. Successful withdrawal returns the remaining balance; rejection preserves state.",
        "class Wallet:\n    pass",
        'class Wallet:\n    def __init__(self, balance=0):\n        self._balance = balance\n    @property\n    def balance(self):\n        return self._balance\n    def withdraw(self, cents):\n        if cents <= 0 or cents > self._balance:\n            raise ValueError("invalid withdrawal")\n        self._balance -= cents\n        return self._balance',
        'class Wallet:\n    def __init__(self, balance=0):\n        self._balance = balance\n    balance = property(lambda self: self._balance)\n    def withdraw(self, cents):\n        if not 0 < cents <= self.balance:\n            raise ValueError("invalid withdrawal")\n        self._balance = self.balance - cents\n        return self.balance',
        "class Wallet:\n    def __init__(self, balance=0):\n        self.balance = balance\n    def withdraw(self, cents):\n        self.balance -= cents\n        return self.balance",
        'w = s.Wallet(100)\nassert w.withdraw(40) == 60, "Subtract cents"\nassert raises(ValueError, w.withdraw, 70) and w.balance == 60, "Reject overdraft atomically"\nassert raises(ValueError, w.withdraw, 0) and w.balance == 60, "Reject zero"\nassert raises(ValueError, w.withdraw, -1), "Reject negative amounts"\nassert raises(AttributeError, setattr, w, "balance", 99), "Expose read-only balance"\nassert w.withdraw(60) == 0, "Allow exact balance"',
    ),
    raw(
        "Create Celsius(value) with a read-only value property; reject values below -273.15 in the constructor.",
        "class Celsius:\n    pass",
        'class Celsius:\n    def __init__(self, value):\n        if value < -273.15:\n            raise ValueError("below absolute zero")\n        self._value = value\n    @property\n    def value(self):\n        return self._value',
        'class Celsius:\n    def __init__(self, value):\n        if not value >= -273.15:\n            raise ValueError("invalid temperature")\n        self._value = value\n    value = property(lambda self: self._value)',
        "class Celsius:\n    def __init__(self, value):\n        self.value = value",
        'assert s.Celsius(-273.15).value == -273.15, "Boundary is valid"\nassert raises(ValueError, s.Celsius, -274), "Reject below boundary"\nassert raises(AttributeError, setattr, s.Celsius(20), "value", 30), "Read-only property"',
    ),
    "Validate cents before changing _balance, and expose balance through @property.",
    (
        "After deposit(100), what is wallet.balance?",
        ["None", "100", "0"],
        1,
        "The validated operation updated the internal balance, and the property returns it.",
    ),
    [
        "Test that every rejected operation preserves the balance.",
        "Discuss where a database transaction would be required.",
    ],
)

f(
    "inject-dependencies",
    "Separate policy from delivery",
    "Accept a collaborator from the caller and test behavior with an in-memory fake.",
    'def notify(message, send):\n    send(message)\n    return "sent"\n\nmessages = []\nprint(notify("ready", messages.append))\nassert messages == ["ready"]',
    [
        "A dependency is something a function needs to do its work, such as sending a message or reading a repository. Passing it as an argument makes the boundary visible and avoids hardcoding a global service.",
        "An in-memory fake can implement the same small operation and record calls. This tests your policy without network requests, credentials or a live provider. It does not prove the real provider integration works.",
        "Keep validation ahead of delivery so invalid work produces no side effects. Let unexpected delivery failures propagate unless your API has a documented retry or compensation policy.",
    ],
    [
        (
            "dependency injection",
            "Supply a collaborator instead of constructing it internally.",
        ),
        ("fake", "A simple working substitute used for a test."),
        ("port", "A small interface describing a needed external operation."),
    ],
    spec(
        "send_receipt",
        "email, total_cents, send",
        'if "@" not in email or total_cents < 0:\n    raise ValueError("invalid receipt")\nmessage = f"Receipt: {total_cents} cents"\nsend(email, message)\nreturn message',
        'if total_cents < 0 or "@" not in email:\n    raise ValueError("invalid receipt")\ntext = "Receipt: " + str(total_cents) + " cents"\nsend(email, text)\nreturn text',
        "send(email, str(total_cents))\nreturn str(total_cents)",
        'Validate that email contains @ and total_cents is nonnegative. Call send(email, "Receipt: N cents") exactly once and return that message. Invalid inputs raise ValueError without calling send.',
        [
            (
                '((calls := []), s.send_receipt("a@x.io", 120, lambda *args: calls.append(args)), calls)[-1] == [("a@x.io", "Receipt: 120 cents")]',
                "Send exactly once",
            ),
            (
                's.send_receipt("a@x.io", 0, lambda *args: None) == "Receipt: 0 cents"',
                "Zero receipt",
            ),
            (
                '((calls := []), raises(ValueError, s.send_receipt, "bad", 1, lambda *args: calls.append(args)), calls)[1:] == (True, [])',
                "Invalid email has no side effect",
            ),
            (
                'raises(ValueError, s.send_receipt, "a@x", -1, lambda *args: None)',
                "Reject negative amount",
            ),
        ],
    ),
    spec(
        "publish",
        "message, sink",
        'if not message:\n    raise ValueError("message required")\nsink(message)\nreturn True',
        'if message == "":\n    raise ValueError("empty message")\nsink(message)\nreturn True',
        "sink(message)\nreturn True",
        "For nonempty text call sink(message) once and return True. Empty text raises ValueError without delivery.",
        [
            (
                '((calls := []), s.publish("ready", calls.append), calls)[1:] == (True, ["ready"])',
                "One delivery",
            ),
            (
                '((calls := []), raises(ValueError, s.publish, "", calls.append), calls)[1:] == (True, [])',
                "Validate before delivery",
            ),
        ],
    ),
    "Validate both inputs, build one message, then call the injected send function.",
    (
        "What is printed by notify?",
        ["sent", "ready", "None"],
        0,
        "The fake records ready while the policy returns sent.",
    ),
    [
        "Inject a collaborator that raises and observe propagation.",
        "Explain what a separate provider contract test would verify.",
    ],
)

f(
    "copying-nested-data",
    "Copy the structure you own",
    "Avoid mutating nested caller data and understand shallow versus deep copies.",
    'import copy\noriginal = {"tags": ["a"]}\nclone = copy.deepcopy(original)\nclone["tags"].append("b")\nprint(original["tags"])\nassert original["tags"] == ["a"]',
    [
        "A dictionary copy duplicates the outer mapping but keeps references to nested values. Mutating a nested list in that shallow copy still changes the original list.",
        "copy.deepcopy recursively copies ordinary nested structures while tracking already-seen objects. It is not a general transaction or a safe way to clone arbitrary resources such as open sockets.",
        "Often the clearest solution is to explicitly reconstruct the small part of a structure you own. Document which values may be shared and which must be independent.",
    ],
    [
        ("shallow copy", "A new outer container referencing the same nested values."),
        ("deep copy", "Recursively copy nested objects when supported."),
        ("ownership", "Responsibility for deciding whether a value may change."),
    ],
    spec(
        "with_tag",
        "record, tag",
        'import copy\nresult = copy.deepcopy(record)\nresult.setdefault("tags", []).append(tag)\nreturn result',
        'result = {key: value for key, value in record.items()}\nresult["tags"] = [*record.get("tags", []), tag]\nreturn result',
        'result = record.copy()\nresult.setdefault("tags", []).append(tag)\nreturn result',
        "Return a new record with tag appended to a new tags list. Preserve other fields and never mutate the input or its tags. Other nested fields may be shared.",
        [
            (
                's.with_tag({"name":"a"}, "x") == {"name":"a","tags":["x"]}',
                "Create missing tags",
            ),
            (
                '((record := {"name":"a","tags":["x"]}), s.with_tag(record, "y"), record)[-1] == {"name":"a","tags":["x"]}',
                "Preserve nested input",
            ),
            ('s.with_tag({"tags":[]}, "x") == {"tags":["x"]}', "Empty tags"),
        ],
    ),
    spec(
        "copy_rows",
        "rows",
        "return [dict(row) for row in rows]",
        "from copy import deepcopy\nreturn deepcopy(rows)",
        "return list(rows)",
        "Copy a list of flat dictionaries so later changes to a copied row do not change the original.",
        [
            ('s.copy_rows([{"x":1}]) == [{"x":1}]', "Same contents"),
            (
                '((rows := [{"x":1}]), (copied := s.copy_rows(rows)), copied[0] is not rows[0])[-1]',
                "Independent row",
            ),
            ("s.copy_rows([]) == []", "Empty rows"),
        ],
    ),
    "Copy the tags list explicitly; copying only the dictionary is insufficient.",
    (
        'What is original["tags"] after modifying clone?',
        ['["a", "b"]', '["b"]', '["a"]'],
        2,
        "deepcopy created an independent nested list.",
    ),
    [
        "Replace deepcopy with copy and observe aliasing.",
        "Explain why copying an object cannot roll back an external side effect.",
    ],
)

f(
    "closures-and-state",
    "Capture a local environment",
    "Return a function that retains controlled state with nonlocal.",
    "def multiplier(factor):\n    def apply(value):\n        return value * factor\n    return apply\n\ntriple = multiplier(3)\nprint(triple(4))\nassert triple(2) == 6",
    [
        "A closure is a function that retains references to names from an enclosing function scope. multiplier returns apply, and each call to multiplier creates a separate environment.",
        "Reading a captured variable needs no special keyword. Rebinding a captured local name requires nonlocal; otherwise assignment creates a new local binding in the inner function.",
        "Closures are useful for small configurable behaviors, but hidden mutable state can complicate concurrency. Use an explicit object when the lifecycle or operations become substantial.",
    ],
    [
        ("closure", "A function retaining its enclosing lexical environment."),
        ("lexical scope", "Name lookup based on where code is defined."),
        ("nonlocal", "Rebind a name in an enclosing function scope."),
    ],
    spec(
        "make_counter",
        "start=0",
        "value = start\ndef next_value():\n    nonlocal value\n    value += 1\n    return value\nreturn next_value",
        "state = [start]\ndef next_value():\n    state[0] += 1\n    return state[0]\nreturn next_value",
        "return lambda: start + 1",
        "Return a zero-argument function that increments and returns a private counter. The first call returns start + 1; counters must be independent.",
        [
            (
                "((counter := s.make_counter(4)), counter(), counter())[1:] == (5, 6)",
                "Retain state across calls",
            ),
            (
                "((a := s.make_counter()), (b := s.make_counter()), a(), a(), b())[2:] == (1,2,1)",
                "Independent closures",
            ),
        ],
    ),
    spec(
        "make_prefixer",
        "prefix",
        "def apply(text):\n    return prefix + text\nreturn apply",
        'return lambda text: f"{prefix}{text}"',
        "return lambda text: text",
        "Return a function that prepends prefix to its text argument.",
        [
            ('s.make_prefixer("lab:")("one") == "lab:one"', "Capture prefix"),
            ('s.make_prefixer("")("x") == "x"', "Empty prefix"),
            ('s.make_prefixer("a")("b") == "ab"', "Apply supplied text"),
        ],
    ),
    "Keep value in the enclosing function and declare nonlocal before rebinding it.",
    (
        "What does triple(4) return?",
        ["7", "12", "4"],
        1,
        "The returned apply function retains factor = 3.",
    ),
    [
        "Create two different multiplier functions.",
        "Explain why nonlocal is unnecessary when only reading factor.",
    ],
)

add(
    "decorators-and-metadata",
    "Wrap behavior transparently",
    "Write a decorator that forwards arguments and preserves function metadata.",
    'from functools import wraps\ndef traced(function):\n    @wraps(function)\n    def wrapper(*args, **kwargs):\n        return function(*args, **kwargs)\n    return wrapper\n\n@traced\ndef add(a, b):\n    return a + b\n\nprint(add(2, 3))\nassert add.__name__ == "add"',
    [
        "A decorator receives a function and returns a replacement. @traced above a definition is equivalent to assigning add = traced(add) after defining add.",
        "*args collects positional arguments into a tuple; **kwargs collects named arguments into a dictionary. Forward both when a wrapper should support the original calling interface.",
        "functools.wraps copies useful metadata and sets __wrapped__ for inspection. A decorator should state whether it changes return values, exceptions, timing, or side effects; transparent wrappers should not silently change these.",
    ],
    [
        ("decorator", "A callable transforming a function or class definition."),
        ("wrapper", "A replacement function that delegates to an underlying function."),
        ("metadata", "Descriptive information such as name and documentation."),
    ],
    raw(
        "Implement logged(sink), a decorator factory. Before each call, send the original function name to sink, then forward arguments and return its result. Preserve metadata with wraps; propagate failures.",
        "def logged(sink):\n    return None",
        "from functools import wraps\n\ndef logged(sink):\n    def decorate(function):\n        @wraps(function)\n        def wrapper(*args, **kwargs):\n            sink(function.__name__)\n            return function(*args, **kwargs)\n        return wrapper\n    return decorate",
        "import functools\n\ndef logged(sink):\n    def decorate(function):\n        def wrapper(*args, **kwargs):\n            sink(function.__name__)\n            return function(*args, **kwargs)\n        return functools.wraps(function)(wrapper)\n    return decorate",
        "def logged(sink):\n    def decorate(function):\n        def wrapper(*args, **kwargs):\n            sink(function.__name__)\n            return function(*args, **kwargs)\n        return wrapper\n    return decorate",
        'calls = []\n@s.logged(calls.append)\ndef combine(a, *, b=2):\n    "Combine two values."\n    return a + b\nassert combine(3, b=4) == 7, "Forward keyword arguments"\nassert calls == ["combine"], "Log once before call"\nassert combine.__name__ == "combine" and combine.__doc__ == "Combine two values.", "Preserve metadata"\n@s.logged(calls.append)\ndef broken():\n    raise ValueError("expected")\nassert raises(ValueError, broken), "Propagate failures"',
    ),
    raw(
        "Implement identity_decorator(function), forwarding all arguments and returning the original result while preserving metadata.",
        "def identity_decorator(function):\n    return None",
        "from functools import wraps\ndef identity_decorator(function):\n    @wraps(function)\n    def wrapper(*args, **kwargs):\n        return function(*args, **kwargs)\n    return wrapper",
        "import functools\ndef identity_decorator(function):\n    def wrapper(*args, **kwargs):\n        return function(*args, **kwargs)\n    return functools.wraps(function)(wrapper)",
        "def identity_decorator(function):\n    def wrapper(*args):\n        return function(*args)\n    return wrapper",
        '@s.identity_decorator\ndef add(a, *, b=1):\n    return a + b\nassert add(2, b=3) == 5, "Forward keywords"\nassert add.__name__ == "add", "Preserve name"',
    ),
    "Use a factory, an inner decorator, and an @wraps wrapper that accepts *args and **kwargs.",
    (
        "What is add.__name__ after wrapping?",
        ["wrapper", "traced", "add"],
        2,
        "wraps preserves the original function metadata.",
    ),
    [
        "Inspect __wrapped__ and the function signature.",
        "Decide whether logging before a failing call is part of your contract.",
    ],
)

add(
    "custom-context-managers",
    "Guarantee cleanup",
    "Use contextmanager and finally so cleanup runs on success and failure.",
    'from contextlib import contextmanager\n@contextmanager\ndef session(events):\n    events.append("open")\n    try:\n        yield "resource"\n    finally:\n        events.append("close")\n\nevents = []\nwith session(events) as value:\n    events.append(value)\nprint(events)\nassert events == ["open", "resource", "close"]',
    [
        "@contextmanager adapts a generator into a context manager. Code before yield performs setup, the yielded value becomes the as target, and code after yield handles exit.",
        "Put cleanup in finally so it runs when the body raises. Without finally, an exception injected at yield can skip the code that releases your resource.",
        "A context manager may deliberately handle an exception, but this lab must propagate it. Silently swallowing failures makes cleanup appear successful while the actual work was lost.",
    ],
    [
        ("finally", "A block that runs when control leaves try, including on failure."),
        (
            "resource lifetime",
            "The interval between acquiring and releasing a resource.",
        ),
        ("propagation", "Allow a failure to continue to the caller."),
    ],
    raw(
        'Implement managed(events) as a context manager: append "enter", yield "ready", and always append "exit". Preserve exceptions raised by the with body.',
        "def managed(events):\n    return None",
        'from contextlib import contextmanager\n\n@contextmanager\ndef managed(events):\n    events.append("enter")\n    try:\n        yield "ready"\n    finally:\n        events.append("exit")',
        'class managed:\n    def __init__(self, events):\n        self.events = events\n    def __enter__(self):\n        self.events.append("enter")\n        return "ready"\n    def __exit__(self, kind, error, traceback):\n        self.events.append("exit")\n        return False',
        'from contextlib import contextmanager\n@contextmanager\ndef managed(events):\n    events.append("enter")\n    yield "ready"\n    events.append("exit")',
        'events = []\nwith s.managed(events) as value:\n    assert value == "ready", "Yield the resource"\nassert events == ["enter", "exit"], "Normal cleanup"\nevents = []\ntry:\n    with s.managed(events):\n        raise ValueError("expected")\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError("Propagate the body failure")\nassert events == ["enter", "exit"], "Cleanup after failure"',
    ),
    raw(
        'Implement bracket(events) as a context manager appending "open" on entry and "close" on every exit.',
        "def bracket(events):\n    return None",
        'from contextlib import contextmanager\n@contextmanager\ndef bracket(events):\n    events.append("open")\n    try:\n        yield\n    finally:\n        events.append("close")',
        'class bracket:\n    def __init__(self, events):\n        self.events = events\n    def __enter__(self):\n        self.events.append("open")\n    def __exit__(self, *args):\n        self.events.append("close")\n        return False',
        'from contextlib import contextmanager\n@contextmanager\ndef bracket(events):\n    events.append("open")\n    yield\n    events.append("close")',
        'events=[]\ntry:\n    with s.bracket(events):\n        raise ValueError("expected")\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError("Do not suppress exceptions")\nassert events == ["open", "close"], "Always release"',
    ),
    "Place yield inside try and cleanup inside finally.",
    (
        "What is events after the successful with block?",
        ['["open", "resource", "close"]', '["open", "close"]', '["resource"]'],
        0,
        "Setup runs first, then the body, then finally performs cleanup.",
    ),
    [
        "Raise inside the body and inspect the events.",
        "Explain how returning True from __exit__ changes exception handling.",
    ],
)

add(
    "iterator-protocol",
    "Implement an iterator protocol",
    "Connect iter, next and StopIteration to the behavior of a for loop.",
    "class Countdown:\n    def __init__(self, start):\n        self.current = start\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.current <= 0:\n            raise StopIteration\n        result = self.current\n        self.current -= 1\n        return result\n\nprint(list(Countdown(3)))",
    [
        "An iterable can produce an iterator through iter(value). An iterator provides __next__ and returns itself from __iter__. for repeatedly calls next until StopIteration signals completion.",
        "A single-use iterator owns traversal state. Once exhausted, it should remain exhausted. A reusable collection usually returns a new iterator for each traversal instead of storing one shared cursor.",
        "Generators implement this protocol for you and are usually shorter. Implementing it explicitly helps when an object needs a specialized stateful interface.",
    ],
    [
        ("iterable", "An object from which an iterator can be requested."),
        ("iterator", "An object yielding values through next()."),
        ("exhaustion", "The permanent end of a particular traversal."),
    ],
    raw(
        "Implement Countdown(start) as an iterator yielding start down to 1. Zero and negatives yield nothing. iter(instance) returns the same instance; exhausted instances stay exhausted.",
        "class Countdown:\n    pass",
        "class Countdown:\n    def __init__(self, start):\n        self.current = start\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.current <= 0:\n            raise StopIteration\n        value = self.current\n        self.current -= 1\n        return value",
        "class Countdown:\n    def __init__(self, start):\n        self.values = iter(range(start, 0, -1))\n    def __iter__(self):\n        return self\n    def __next__(self):\n        return next(self.values)",
        "class Countdown:\n    def __init__(self, start):\n        self.current = start\n    def __iter__(self):\n        return iter(range(self.current))",
        'counter=s.Countdown(3)\nassert iter(counter) is counter, "Implement an iterator"\nassert next(counter) == 3, "Start at supplied value"\nassert list(counter) == [2,1], "Resume traversal"\nassert list(counter) == [], "Remain exhausted"\nassert list(s.Countdown(0)) == [] and list(s.Countdown(-2)) == [], "Empty nonpositive ranges"',
    ),
    raw(
        "Implement One(value) as an iterator yielding exactly one value, then remaining exhausted.",
        "class One:\n    pass",
        "class One:\n    def __init__(self, value):\n        self.value = value\n        self.done = False\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.done:\n            raise StopIteration\n        self.done = True\n        return self.value",
        "class One:\n    def __init__(self, value):\n        self.iterator = iter([value])\n    def __iter__(self):\n        return self\n    def __next__(self):\n        return next(self.iterator)",
        "class One:\n    def __init__(self, value):\n        self.value = value\n    def __iter__(self):\n        return iter([self.value])",
        'item=s.One(None)\nassert iter(item) is item, "Iterator returns itself"\nassert next(item) is None, "None is a real value"\nassert raises(StopIteration, next, item), "Stop after one"\nassert raises(StopIteration, next, item), "Stay exhausted"',
    ),
    "Implement __iter__ returning self and __next__ raising StopIteration when no values remain.",
    (
        "What does list(Countdown(3)) produce?",
        ["[0,1,2]", "[3,2,1]", "[3,2,1,0]"],
        1,
        "Each next call decrements state; the zero state raises StopIteration.",
    ),
    [
        "Compare an iterator with a reusable range object.",
        "Implement the same sequence as a generator and compare readability.",
    ],
)

# Async contracts use a real event loop and in-memory coroutines; no network requests.
f(
    "async-and-await",
    "Compose asynchronous work",
    "Await coroutines and gather their results in a real event loop.",
    "import asyncio\nasync def double(value):\n    await asyncio.sleep(0)\n    return value * 2\n\nasync def main():\n    return await asyncio.gather(double(2), double(3))\n\nprint(asyncio.run(main()))",
    [
        "async def defines a coroutine function. Calling it creates a coroutine object; its body runs when it is awaited or scheduled by an event loop. await allows another task to run while this one waits.",
        "asyncio.gather schedules awaitables together and returns results in input order, even if tasks finish in another order. asyncio.run creates and closes an event loop around a top-level coroutine.",
        "Concurrency is not automatic CPU parallelism. Blocking synchronous work blocks the event loop; real I/O integrations need nonblocking clients and cancellation policies. These exercises use in-memory coroutines and do not contact the network.",
    ],
    [
        ("coroutine", "A computation that can suspend at await points."),
        ("event loop", "The scheduler advancing ready asynchronous tasks."),
        (
            "concurrency",
            "Overlapping progress of multiple tasks, not necessarily parallel CPU execution.",
        ),
    ],
    spec(
        "collect",
        "values, transform",
        "import asyncio\nreturn list(await asyncio.gather(*(transform(value) for value in values)))",
        "tasks = [transform(value) for value in values]\nfrom asyncio import gather\nresults = await gather(*tasks)\nreturn list(results)",
        "return [transform(value) for value in values]",
        "Define async collect(values, transform). Await the supplied asynchronous transform for every value using gather, preserving input order; return [] for empty input.",
        [
            ('__import__("inspect").iscoroutinefunction(s.collect)', "Use async def"),
            (
                "async_collect_case(s.collect)",
                "Await results and schedule all transforms together",
            ),
            ("async_empty_case(s.collect)", "Handle empty input"),
        ],
    ),
    spec(
        "double_async",
        "value",
        "import asyncio\nawait asyncio.sleep(0)\nreturn value * 2",
        "return value + value",
        "return value",
        "Define async double_async(value), returning twice the input when awaited.",
        [
            (
                '__import__("inspect").iscoroutinefunction(s.double_async)',
                "Define coroutine function",
            ),
            (
                '__import__("asyncio").run(s.double_async(3)) == 6',
                "Await computed result",
            ),
            ('__import__("asyncio").run(s.double_async(0)) == 0', "Zero result"),
        ],
    ),
    "Use async def and await asyncio.gather over the transform calls.",
    (
        "In what order are results returned?",
        ["[6,4]", "Completion order only", "[4,6]"],
        2,
        "gather preserves the order of the input awaitables.",
    ),
    [
        "Explain why replacing async I/O with a blocking call stalls other tasks.",
        "Discuss how to cancel unfinished work if one operation fails.",
    ],
)
# Add async syntax to helper-generated definitions; ordinary functions must not contain await.
for exercise in (LESSONS[-1], GUIDES[-1]["practice"]):
    for field in ("starter", "solution", "alternative", "negative"):
        exercise[field] = (
            exercise[field]
            .replace("def collect(", "async def collect(")
            .replace("def double_async(", "async def double_async(")
        )

f(
    "type-hints-and-contracts",
    "Use hints without trusting them blindly",
    "Annotate a small API while validating the runtime boundary explicitly.",
    'def add(left: int, right: int) -> int:\n    return left + right\n\nprint(add(2, 3))\nassert add("a", "b") == "ab"',
    [
        "Type annotations describe an intended contract for readers, editors and static analyzers. CPython does not generally enforce them when a function is called; the worked example still concatenates two strings.",
        "Use runtime validation at untrusted boundaries and static analysis during development. They solve different problems. PyDojo executes behavioral checks. Its checks validate actual results and failure policies.",
        "A public API should say which values it accepts, what it returns, and what happens on failure. Reject bool explicitly when the contract requires exact integer counts, because bool inherits from int.",
    ],
    [
        ("type hint", "Metadata describing an intended type contract."),
        ("static analysis", "Inspect code without executing its ordinary behavior."),
        ("runtime validation", "Check actual incoming values during execution."),
    ],
    spec(
        "validated_count",
        "value: object",
        'if type(value) is not int or value < 0:\n    raise ValueError("nonnegative integer required")\nreturn value',
        'if isinstance(value, bool) or not isinstance(value, int) or value < 0:\n    raise ValueError("invalid count")\nreturn value',
        "return int(value)",
        "Annotate value as object and the return as int. Return exact nonnegative ints unchanged; raise ValueError for bools, floats, strings or negative ints.",
        [
            ("s.validated_count(0) == 0 and s.validated_count(4) == 4", "Valid counts"),
            (
                'all(raises(ValueError, s.validated_count, value) for value in [True, False, 2.0, "2", -1])',
                "Validate exact integer boundary",
            ),
            (
                '__import__("typing").get_type_hints(s.validated_count) == {"value":object,"return":int}',
                "Document hints",
            ),
        ],
    ),
    spec(
        "is_count",
        "value: object",
        "return type(value) is int and value >= 0",
        "if type(value) is not int:\n    return False\nreturn value >= 0",
        "return isinstance(value, int) and value >= 0",
        "Annotate value: object and return: bool. Return whether a value is an exact nonnegative int, excluding bool.",
        [
            ("s.is_count(0) is True and s.is_count(2) is True", "Valid counts"),
            (
                'all(s.is_count(value) is False for value in [True, "2", -1, 2.0])',
                "Reject other types",
            ),
            (
                '__import__("typing").get_type_hints(s.is_count)["return"] is bool',
                "Annotate the result",
            ),
        ],
    ),
    "Check type(value) is int, validate the sign, and add -> int to the signature.",
    (
        "What happens when the annotated add receives two strings?",
        [
            "It concatenates them",
            "Python rejects them before the call",
            "The annotations are deleted",
        ],
        0,
        "Annotations alone do not change the runtime + operation.",
    ),
    [
        "Explain which errors a static checker could find before execution.",
        "Discuss validation for nested external records.",
    ],
)
for exercise, name, result in (
    (LESSONS[-1], "validated_count", "int"),
    (GUIDES[-1]["practice"], "is_count", "bool"),
):
    for field in ("starter", "solution", "alternative", "negative"):
        exercise[field] = exercise[field].replace(
            f"def {name}(value: object):", f"def {name}(value: object) -> {result}:"
        )

f(
    "project-log-report",
    "Project · A log report",
    "Combine parsing, filtering, aggregation and deterministic output in a small report.",
    'def summarize(lines):\n    counts = {}\n    for line in lines:\n        level, separator, message = line.partition(":")\n        if separator and level in {"INFO", "ERROR"}:\n            counts[level] = counts.get(level, 0) + 1\n    return counts\n\nprint(summarize(["INFO:ready", "bad", "ERROR:failed"]))',
    [
        "A useful report starts with a precise input contract. Here a record is LEVEL:message, the first colon separates fields, and only INFO, WARN and ERROR are recognized. The message itself may contain colons.",
        "Separate parsing from aggregation mentally: decide whether a line is valid, normalize the level, then increment its count. Malformed lines are intentionally ignored in this project, while a real operational tool may need a rejected-row count.",
        "Deterministic output makes reports easier to test and compare. Always return all three known levels with zero counts when absent. This project tests behavior, not whether you used one particular implementation.",
    ],
    [
        ("deterministic", "The same input produces the same observable result."),
        ("partition", "Split text once, preserving whether a separator existed."),
        ("observability", "Evidence that helps explain a system's behavior."),
    ],
    spec(
        "log_report",
        "lines",
        'counts = {"INFO": 0, "WARN": 0, "ERROR": 0}\nfor line in lines:\n    level, separator, message = line.partition(":")\n    level = level.strip().upper()\n    if separator and level in counts and message.strip():\n        counts[level] += 1\nreturn counts',
        'from collections import Counter\nlevels = []\nfor line in lines:\n    parts = line.split(":", 1)\n    if len(parts) == 2 and parts[1].strip() and parts[0].strip().upper() in {"INFO","WARN","ERROR"}:\n        levels.append(parts[0].strip().upper())\ncounts = Counter(levels)\nreturn {level: counts[level] for level in ("INFO","WARN","ERROR")}',
        'return {"INFO": len(lines), "WARN": 0, "ERROR": 0}',
        "Count INFO, WARN and ERROR records. Normalize surrounding whitespace and level case. Require a colon and a nonblank message; ignore unknown levels and malformed lines. Return all three keys.",
        [
            (
                's.log_report([]) == {"INFO":0,"WARN":0,"ERROR":0}',
                "Stable empty schema",
            ),
            (
                's.log_report(["info: ready", " WARN : slow", "ERROR: a:b", "bad", "DEBUG:x", "INFO: "]) == {"INFO":1,"WARN":1,"ERROR":1}',
                "Normalize and validate records",
            ),
            (
                's.log_report(["ERROR:a", "ERROR:b"]) == {"INFO":0,"WARN":0,"ERROR":2}',
                "Aggregate repeated levels",
            ),
        ],
    ),
    spec(
        "split_record",
        "line",
        'level, separator, message = line.partition(":")\nif not separator or not message.strip():\n    return None\nreturn level.strip().upper(), message.strip()',
        'parts = line.split(":", 1)\nif len(parts) != 2 or not parts[1].strip():\n    return None\nreturn parts[0].strip().upper(), parts[1].strip()',
        'return tuple(line.split(":"))',
        "Return (normalized_level, trimmed_message) using the first colon, or None if colon or message is absent.",
        [
            ('s.split_record(" info : a:b ") == ("INFO","a:b")', "Split only once"),
            ('s.split_record("bad") is None', "Require separator"),
            ('s.split_record("INFO: ") is None', "Require message"),
        ],
    ),
    "Initialize all known counters, split only once, then validate before incrementing.",
    (
        "Why does ERROR:network:timeout stay one record?",
        [
            "Every colon starts a record",
            "partition splits only at the first colon",
            "The extra text is discarded",
        ],
        1,
        "partition preserves the rest of the message after the first separator.",
    ),
    [
        "Add a rejected-record count without changing valid counts.",
        "Discuss how a streaming report would avoid retaining every log line.",
    ],
)

f(
    "project-stock-reservation",
    "Project · Reserve stock safely",
    "Plan a batch update and reject it without partially mutating caller state.",
    'def decrement_copy(stock, sku):\n    if stock.get(sku, 0) < 1:\n        raise ValueError("out of stock")\n    result = dict(stock)\n    result[sku] -= 1\n    return result\n\nstock = {"book": 2}\nprint(decrement_copy(stock, "book"))\nassert stock == {"book": 2}',
    [
        "A multi-item reservation is one business operation. If the second item is unavailable, consuming the first item and then raising leaves a partial result that violates the operation's promise.",
        "Work on a private copy and validate every requested quantity. Returning the new stock only after all operations succeed provides atomic failure for this pure in-memory interface.",
        "This is not a concurrency-safe inventory service. Two workers reading the same database snapshot still need a transaction, conditional update or other coordination. Name that limitation when explaining the design.",
    ],
    [
        (
            "atomicity",
            "The operation succeeds as a whole or has no observable partial effect.",
        ),
        ("reservation", "A request to set aside available quantity."),
        ("concurrency control", "Coordinate overlapping operations on shared state."),
    ],
    spec(
        "reserve",
        "stock, request",
        'updated = dict(stock)\nfor sku, quantity in request.items():\n    if type(quantity) is not int or quantity <= 0 or sku not in updated or updated[sku] < quantity:\n        raise ValueError("invalid or unavailable reservation")\n    updated[sku] -= quantity\nreturn updated',
        'if any(type(q) is not int or q <= 0 or sku not in stock or stock[sku] < q for sku, q in request.items()):\n    raise ValueError("cannot reserve")\nreturn {sku: count - request.get(sku, 0) for sku, count in stock.items()}',
        "for sku, quantity in request.items():\n    stock[sku] -= quantity\nreturn stock",
        "Return new stock after reserving requested quantities. Require exact positive integer quantities and existing sufficient stock. Raise ValueError for invalid requests. Never mutate stock or request, even on failure.",
        [
            (
                's.reserve({"a":3,"b":2}, {"a":2}) == {"a":1,"b":2}',
                "Subtract requested quantity",
            ),
            (
                '((stock := {"a":3,"b":0}), raises(ValueError, s.reserve, stock, {"a":1,"b":1}), stock)[1:] == (True, {"a":3,"b":0})',
                "Reject whole batch without mutation",
            ),
            ('raises(ValueError, s.reserve, {"a":3}, {"x":1})', "Unknown SKU"),
            (
                'all(raises(ValueError, s.reserve, {"a":3}, {"a":q}) for q in [0,-1,True,1.5])',
                "Validate exact positive quantities",
            ),
            (
                '((stock := {"a":1}), s.reserve(stock, {}) is not stock)[-1]',
                "Return a fresh mapping",
            ),
        ],
    ),
    spec(
        "can_reserve",
        "available, requested",
        "return type(requested) is int and requested > 0 and available >= requested",
        "if type(requested) is not int or requested <= 0:\n    return False\nreturn requested <= available",
        "return available >= requested",
        "Return whether requested is an exact positive int and no greater than available.",
        [
            ("s.can_reserve(3, 3) is True", "Exact stock is enough"),
            ("s.can_reserve(2, 3) is False", "Insufficient stock"),
            (
                "all(s.can_reserve(3, q) is False for q in [0,-1,True,1.2])",
                "Invalid quantities",
            ),
        ],
    ),
    "Change only a fresh copy and reject every invalid quantity before returning it.",
    (
        "What happens to stock after decrement_copy?",
        ["It becomes zero", "It loses book", "It remains unchanged"],
        2,
        "The function returns a changed copy and leaves the input mapping intact.",
    ),
    [
        "Explain a race between two simultaneous reservations.",
        "Describe a database condition that prevents overselling.",
    ],
)

f(
    "project-cart-pricing",
    "Project · Price a shopping cart",
    "Combine exact integer units, validation and an explicit per-order discount.",
    "def line_total(price_cents, quantity):\n    return price_cents * quantity\n\nprint(line_total(1250, 3))\nassert line_total(1250, 0) == 0",
    [
        "A price contract must define units. Here all amounts are integer cents, quantities are positive integers, and the discount applies once to the subtotal. The total never becomes negative.",
        "Validate every line before producing a result. An empty cart has subtotal zero. A boolean is not a valid quantity even though Python allows arithmetic with True and False.",
        "Keep this calculation pure so it can be tested independently from checkout, payment and inventory. This exercise does not model taxes, currency conversion or jurisdiction-specific rounding.",
    ],
    [
        ("pure calculation", "Compute from inputs without external side effects."),
        ("unit", "The scale and meaning of a number, such as cents."),
        ("line item", "A price-and-quantity record within an order."),
    ],
    spec(
        "price_cart",
        "lines, discount_cents=0",
        'if type(discount_cents) is not int or discount_cents < 0:\n    raise ValueError("invalid discount")\nsubtotal = 0\nfor line in lines:\n    price, quantity = line["price_cents"], line["quantity"]\n    if type(price) is not int or price < 0 or type(quantity) is not int or quantity <= 0:\n        raise ValueError("invalid line")\n    subtotal += price * quantity\nreturn {"subtotal_cents": subtotal, "total_cents": max(0, subtotal - discount_cents)}',
        'if type(discount_cents) is not int or discount_cents < 0:\n    raise ValueError("invalid discount")\nfor line in lines:\n    if type(line["price_cents"]) is not int or line["price_cents"] < 0 or type(line["quantity"]) is not int or line["quantity"] < 1:\n        raise ValueError("invalid line")\nsubtotal = sum(line["price_cents"] * line["quantity"] for line in lines)\nreturn dict(subtotal_cents=subtotal, total_cents=max(subtotal - discount_cents, 0))',
        'subtotal = sum(line["price_cents"] * line["quantity"] for line in lines)\nreturn {"subtotal_cents":subtotal,"total_cents":subtotal-discount_cents}',
        "Return subtotal_cents and total_cents after one nonnegative integer discount, clamped to zero. Validate exact nonnegative integer prices and exact positive integer quantities; invalid inputs raise ValueError.",
        [
            (
                's.price_cart([{"price_cents":1250,"quantity":2},{"price_cents":500,"quantity":1}], 250) == {"subtotal_cents":3000,"total_cents":2750}',
                "Price every line and discount once",
            ),
            (
                's.price_cart([], 200) == {"subtotal_cents":0,"total_cents":0}',
                "Clamp empty cart",
            ),
            (
                'raises(ValueError, s.price_cart, [{"price_cents":2,"quantity":True}])',
                "Reject bool quantity",
            ),
            (
                'raises(ValueError, s.price_cart, [{"price_cents":-1,"quantity":1}])',
                "Reject negative price",
            ),
            ("raises(ValueError, s.price_cart, [], -1)", "Reject negative discount"),
        ],
    ),
    spec(
        "discounted",
        "subtotal, discount",
        'if subtotal < 0 or discount < 0:\n    raise ValueError("amounts must be nonnegative")\nreturn max(0, subtotal - discount)',
        'if min(subtotal, discount) < 0:\n    raise ValueError("negative amount")\nreturn subtotal - min(subtotal, discount)',
        "return subtotal - discount",
        "Return max(0, subtotal - discount). Negative inputs raise ValueError.",
        [
            ("s.discounted(100, 30) == 70", "Apply discount"),
            ("s.discounted(10, 20) == 0", "Clamp total"),
            ("raises(ValueError, s.discounted, -1, 0)", "Validate inputs"),
        ],
    ),
    "Validate units and exact types, sum line totals, then clamp the discounted total.",
    (
        "What is 1250 cents times 3?",
        ["3750 cents", "37.5 cents", "1253 cents"],
        0,
        "Multiplication preserves the explicit cents unit.",
    ),
    [
        "Add a currency field and prevent mixing currencies.",
        "Explain why payment success must not be inferred from a correct price calculation.",
    ],
)

f(
    "project-idempotent-handler",
    "Project · Handle duplicate requests",
    "Cache a completed result and reject reuse of a key for a different request.",
    'def once(cache, key, operation):\n    if key not in cache:\n        cache[key] = operation()\n    return cache[key]\n\ncache = {}\nprint(once(cache, "r1", lambda: 42))\nassert once(cache, "r1", lambda: 99) == 42',
    [
        "An idempotency key lets a caller retry the same operation without repeating its successful side effect. A response cache should retain both a request fingerprint and the completed result.",
        "A matching key with a different payload is a conflict, not a cache hit. If the operation raises, do not store a success entry; a later retry must still have a chance to run.",
        "This in-memory exercise handles sequential calls only. A production handler must atomically claim a key and coordinate concurrent requests, expiry, durable results and crash recovery. It does not create exactly-once delivery by itself.",
    ],
    [
        (
            "idempotency key",
            "An identifier used to recognize retries of the same operation.",
        ),
        ("fingerprint", "A representation identifying the relevant request content."),
        ("conflict", "A reused key paired with a different request."),
    ],
    spec(
        "handle_once",
        "cache, key, payload, operation",
        'if key in cache:\n    previous_payload, result = cache[key]\n    if previous_payload != payload:\n        raise ValueError("idempotency conflict")\n    return result\nresult = operation(payload)\ncache[key] = (payload, result)\nreturn result',
        'entry = cache.get(key)\nif entry is not None:\n    if entry[0] != payload:\n        raise ValueError("conflicting payload")\n    return entry[1]\nvalue = operation(payload)\ncache[key] = (payload, value)\nreturn value',
        "result = operation(payload)\ncache[key] = (payload, result)\nreturn result",
        "For sequential calls, cache key -> (payload, result). Matching retries return cached results without calling operation; conflicting payloads raise ValueError. Cache only successful calls. payload is immutable text.",
        [
            (
                "idempotency_case(s.handle_once)",
                "Duplicates, conflicts, falsy results and failure retry are covered",
            )
        ],
    ),
    spec(
        "cached",
        "cache, key, compute",
        "if key not in cache:\n    cache[key] = compute()\nreturn cache[key]",
        "if key in cache:\n    return cache[key]\nvalue = compute()\ncache[key] = value\nreturn value",
        "return cache.get(key) or compute()",
        "Compute once per missing key and cache the result, including zero or None. Existing entries must not recompute.",
        [
            (
                "cache_case(s.cached)",
                "Cache falsy values and avoid duplicate computation",
            )
        ],
    ),
    "Check key membership, compare payloads, then store only after operation returns.",
    (
        "Why does the second once call still return 42?",
        [
            "The lambda is ignored by Python",
            "The key already has a cached result",
            "99 is converted to 42",
        ],
        1,
        "A cache hit returns the previous result without invoking the new operation.",
    ),
    [
        "Describe a crash after delivery but before recording success.",
        "Design a durable concurrent claim for the same key.",
    ],
)

f(
    "project-retry-policy",
    "Project · Retry a transient failure",
    "Make attempts, retryable errors and backoff visible through injected collaborators.",
    'def attempt(operation):\n    try:\n        return operation()\n    except TimeoutError:\n        return "retry later"\n\nprint(attempt(lambda: "ok"))',
    [
        "A retry policy should identify which failures are transient and safe to repeat. Retrying every exception can amplify bugs or duplicate a non-idempotent side effect.",
        "max_attempts includes the initial call. Backoff happens only between failed attempts, never after the last one. Injecting sleep makes timing testable without real delays.",
        "Exponential backoff with jitter, cancellation and a total deadline are useful production additions. This exercise deliberately uses deterministic delays 1, 2, 4 and retries only TimeoutError.",
    ],
    [
        (
            "transient failure",
            "A failure that may disappear without changing the request.",
        ),
        ("backoff", "A delay between repeated attempts."),
        ("retry budget", "A bound on how much work retries may perform."),
    ],
    spec(
        "retry",
        "operation, max_attempts, sleep",
        'if type(max_attempts) is not int or max_attempts < 1:\n    raise ValueError("positive attempt count required")\nfor attempt in range(max_attempts):\n    try:\n        return operation()\n    except TimeoutError:\n        if attempt == max_attempts - 1:\n            raise\n        sleep(2 ** attempt)',
        'if type(max_attempts) is not int or max_attempts <= 0:\n    raise ValueError("invalid attempts")\nattempt = 0\nwhile True:\n    try:\n        return operation()\n    except TimeoutError:\n        attempt += 1\n        if attempt >= max_attempts:\n            raise\n        sleep(2 ** (attempt - 1))',
        "for attempt in range(max_attempts):\n    try:\n        return operation()\n    except Exception:\n        sleep(1)\nreturn None",
        "Retry only TimeoutError, at most max_attempts total calls. Between failed attempts call sleep with 1, 2, 4...; propagate the final timeout or any other error. Reject nonpositive or non-int attempt counts.",
        [
            (
                "retry_case(s.retry)",
                "Success, backoff, exhaustion, validation and nonretryable failure",
            )
        ],
    ),
    spec(
        "try_twice",
        "operation",
        "try:\n    return operation()\nexcept TimeoutError:\n    return operation()",
        "for attempt in range(2):\n    try:\n        return operation()\n    except TimeoutError:\n        if attempt == 1:\n            raise",
        "try:\n    return operation()\nexcept Exception:\n    return operation()",
        "Try operation once and retry once only after TimeoutError. Propagate other failures and a second timeout.",
        [("twice_case(s.try_twice)", "Only a timeout permits the second attempt")],
    ),
    "Count total attempts explicitly and sleep only when another retry remains.",
    (
        "What happens on an immediate successful operation?",
        ["No retries or delay", "Always sleeps once", "Runs twice"],
        0,
        "The first returned result leaves the function before the exception branch.",
    ),
    [
        "Add a maximum total delay without making real calls.",
        "Explain why idempotency and retries must be designed together.",
    ],
)

f(
    "project-import-pipeline",
    "Project · Build an import pipeline",
    "Compose CSV parsing, row validation and deterministic summaries while reporting invalid rows.",
    'import csv\nimport io\nrows = list(csv.DictReader(io.StringIO("team,points\\na,2\\na,3\\n")))\nprint(sum(int(row["points"]) for row in rows))\nassert len(rows) == 2',
    [
        "An import pipeline has several boundaries: bytes become text, text becomes rows, rows become validated domain values, and values become a summary. Each step can fail for a different reason.",
        "This project requires team and points headers. A row with blank team, invalid integer points, or negative points is rejected. Good rows still contribute. The result reports accepted and rejected counts rather than hiding data loss.",
        "Normalize team whitespace, aggregate exact integer points and sort the summary by team name. Keep parsing and policy independently understandable. The exercise is a local batch; large production imports also need streaming limits, idempotency and operational evidence.",
    ],
    [
        ("pipeline", "A sequence of transformations with explicit boundaries."),
        ("rejected row", "A record excluded because it violates a documented rule."),
        (
            "reconciliation",
            "Account for input records through accepted and rejected outcomes.",
        ),
    ],
    spec(
        "import_points",
        "text",
        'import csv\nimport io\nreader = csv.DictReader(io.StringIO(text))\nif not {"team", "points"}.issubset(reader.fieldnames or []):\n    raise ValueError("team and points headers required")\ntotals = {}\naccepted = rejected = 0\nfor row in reader:\n    team = (row.get("team") or "").strip()\n    try:\n        points = int(row.get("points") or "")\n    except ValueError:\n        rejected += 1\n        continue\n    if not team or points < 0:\n        rejected += 1\n        continue\n    totals[team] = totals.get(team, 0) + points\n    accepted += 1\nreturn {"accepted": accepted, "rejected": rejected, "totals": dict(sorted(totals.items()))}',
        'from csv import DictReader\nfrom io import StringIO\nreader = DictReader(StringIO(text))\nif any(key not in (reader.fieldnames or []) for key in ("team", "points")):\n    raise ValueError("missing headers")\nvalid = []\ninvalid = 0\nfor row in reader:\n    try:\n        name = (row.get("team") or "").strip()\n        count = int(row.get("points") or "")\n        if not name or count < 0:\n            raise ValueError("bad row")\n    except ValueError:\n        invalid += 1\n    else:\n        valid.append((name, count))\nresult = {}\nfor name, count in valid:\n    result[name] = result.get(name, 0) + count\nreturn dict(accepted=len(valid), rejected=invalid, totals={key:result[key] for key in sorted(result)})',
        'return {"accepted":0,"rejected":0,"totals":{}}',
        "Read CSV with team and points headers, raising ValueError if either is absent. Count valid rows, reject blank teams or malformed/negative integer points, and aggregate valid points by trimmed team. Return accepted, rejected and alphabetically ordered totals.",
        [
            (
                's.import_points("team,points\nb,2\na,3\nb,4\n,1\nc,no\na,-1\n") == {"accepted":3,"rejected":3,"totals":{"a":3,"b":6}}',
                "Reconcile good and invalid rows",
            ),
            (
                's.import_points("team,points\n") == {"accepted":0,"rejected":0,"totals":{}}',
                "Header-only batch",
            ),
            (
                'list(s.import_points("team,points\nz,0\na,1\n")["totals"]) == ["a","z"]',
                "Deterministic key order",
            ),
            (
                's.import_points(\'team,points\n"a,b",2\n\')["totals"] == {"a,b":2}',
                "Honor CSV quoting",
            ),
            (
                'raises(ValueError, s.import_points, "team\na\n")',
                "Reject missing schema",
            ),
        ],
    ),
    spec(
        "sum_valid",
        "texts",
        'total = 0\nrejected = 0\nfor text in texts:\n    try:\n        total += int(text)\n    except ValueError:\n        rejected += 1\nreturn {"total":total,"rejected":rejected}',
        "values = []\nrejected = 0\nfor text in texts:\n    try:\n        values.append(int(text))\n    except ValueError:\n        rejected += 1\nreturn dict(total=sum(values), rejected=rejected)",
        'return {"total":sum(map(int,texts)),"rejected":0}',
        "Parse integer strings, sum valid values and count malformed entries. Return total and rejected; negative integers are valid.",
        [
            (
                's.sum_valid(["2","bad","-1"]) == {"total":1,"rejected":1}',
                "Aggregate and account for bad input",
            ),
            ('s.sum_valid([]) == {"total":0,"rejected":0}', "Empty batch"),
            (
                's.sum_valid(["0"," 4 ","2.5"]) == {"total":4,"rejected":1}',
                "Whitespace and invalid decimal",
            ),
        ],
    ),
    "Use DictReader, validate headers once, then handle row failures without losing the accepted-row count.",
    (
        "What does the worked example print?",
        ["2", "23", "5"],
        2,
        "Each points field is parsed as an integer before summation.",
    ),
    [
        "Reconcile accepted + rejected against the number of parsed data rows.",
        "Explain where to add size limits, durable job status and a rejected-row download in a production importer.",
    ],
)


def build():
    from playgrounds import make

    assert len(LESSONS) == 43
    for lesson, guide in zip(LESSONS, GUIDES):
        lesson["playground"] = make(lesson["id"], lesson, False)
        guide["practice"]["playground"] = make(lesson["id"], guide["practice"], True)
    for name, data in (("course.json", LESSONS), ("learning.json", GUIDES)):
        (ROOT / "content" / name).write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        )
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, str(ROOT / "tools/format_content.py"), "--write"], check=True
    )
    print(f"Authored {len(LESSONS)} labs and {len(GUIDES)} distinct guided practices.")


if __name__ == "__main__":
    build()
