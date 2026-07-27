# Chapter 7 — Evaluating Expressions

The interpreter finally runs something. Short chapter, and **by far the most
Python-specific traps of any chapter in Part II** — Python's own semantics for truthiness,
equality and division all differ from Lox's in ways that silently produce wrong answers.

**Milestone:** type `1 + 2 * 3` at the REPL and get `7`. Then `"a" + "b"` gives `ab`, and
`1 + "a"` gives a clean runtime error with a line number instead of a traceback.

## Representing values

Lox values are represented directly as host-language values:

| Lox | Python |
| --- | --- |
| `nil` | `None` |
| Boolean | `bool` |
| number | `float` — always, there is no int |
| string | `str` |

Later chapters add function and instance objects. A Lox value is typed `object` in
signatures, which is unavoidable in a dynamically typed interpreter.

## What to implement

### 1. The Interpreter visitor

One visitor over `Expr`, returning a value for each node:

- **Literal** — return the stored value. Already converted by the scanner.
- **Grouping** — evaluate the inner expression.
- **Unary** — `-` negates (operand must be a number), `!` returns the inverse truthiness.
- **Binary** — arithmetic, comparison, equality.

**Post-order traversal:** every node evaluates its children first, then combines. Recursion
does this for free.

### 2. Truthiness

Lox's rule: **only `false` and `nil` are falsey.** `0`, `""`, and empty everything else are
truthy. Write an `is_truthy` helper and use it everywhere.

### 3. Equality

`nil` equals only `nil`. Values of different types are never equal — there are no implicit
conversions, so `1 == "1"` is `false`.

### 4. `+` is overloaded

Two numbers → addition. Two strings → concatenation. Anything else → runtime error. It's
the one operator that inspects operand types before deciding what it means.

### 5. Runtime errors

A `LoxRuntimeError` carrying **both** a message and the token where it happened — that
token is the only reason chapter 5 stored operator tokens in the AST rather than characters.

Helpers `check_number_operand` / `check_number_operands` keep the type checks from drowning
the arithmetic. The top-level `interpret()` catches `LoxRuntimeError`, prints
`<message>\n[line N]`, and sets a `had_runtime_error` flag → exit code **70**.

Crucially, a runtime error unwinds to the top and abandons the statement, but in the REPL it
must **not** kill the session.

### 6. Stringify

Converting a Lox value back to display text. Three special cases, all of which Python gets
wrong by default — see below.

## Python translation notes — read this section twice

This is the trap-dense chapter. Five real bugs waiting:

**1. Equality: `1.0 == True` is `True` in Python.** This is the big one. `bool` subclasses
`int`, so a naive `a == b` makes Lox's `1 == true` evaluate to `true`, which is wrong.
Compare types before values — if exactly one operand is a `bool`, they're unequal. Same
issue makes `0.0 == False` true.

**2. Truthiness: never call `bool(value)`.** Python says `0`, `""`, `[]` are falsey; Lox
says they're truthy. Only `None` and `False` are falsey. This one is easy to get right and
easy to forget in an `if` somewhere.

**3. Type checks: use `isinstance(x, float)`, not `(int, float)`.** All Lox numbers are
floats, and the wider check would let `True` through, since `bool` is an `int` subclass.

**4. Stringify has three cases Python botches:**
   - `None` → `"nil"`, not `"None"`.
   - `True`/`False` → `"true"`/`"false"`, not `"True"`/`"False"` — Python capitalizes.
   - Floats → trim a trailing `.0`, so `2.0` prints as `2`. The book does exactly this,
     chopping the last two characters when the text ends in `.0`.

   Get this into one function now. Ch. 8's `print` statement, ch. 5's AST printer, and
   ch. 12's instance printing all route through it.

**5. Division by zero.** Python raises `ZeroDivisionError`; Java produces `Infinity`, so
jlox's `1/0` evaluates to `Infinity` and does *not* error. Pick deliberately: match the book
by catching `ZeroDivisionError` and returning `float("inf")` / `float("nan")`, or make it a
`LoxRuntimeError`. Matching the book keeps the official test suite green. Either way, don't
leave a bare Python traceback escaping.

Also: Python's `<` works on strings, and `+` on `str + str` works — but Lox only permits
comparison on numbers, so check operand types explicitly rather than letting Python's
semantics leak through. And `str + float` raises `TypeError`; catch the case before Python
does, so the error carries a Lox token.

## Gotchas

- [ ] `1 == true` is `false`. Test this explicitly.
- [ ] `!0` is `false` — `0` is truthy in Lox.
- [ ] `!nil` is `true`.
- [ ] `print 2.0` shows `2`.
- [ ] `print true` shows `true`, lowercase.
- [ ] `"a" + 1` is a runtime error naming the line, not a Python `TypeError`.
- [ ] `-"a"` is a runtime error.
- [ ] `1 < "a"` is a runtime error, even though Python would happily... actually refuse
      this one too. `"a" < "b"` must *also* error — Lox restricts comparison to numbers.
- [ ] A runtime error in the REPL prints and returns to the prompt.

`examples/07-expressions.lox` covers most of these, though it needs ch. 8's `print`
statement to run as a file — until then, paste lines into the REPL.
