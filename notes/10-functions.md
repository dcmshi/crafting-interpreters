# Chapter 10 — Functions

The largest chapter in Part II, and the one that makes Lox a real language. Calls,
declarations, returns, and closures.

**Milestone:** `examples/10-functions.lox` runs, including `makeCounter()`. Recursive
`fib(20)` computes.

**Heads up:** at the end of this chapter closures *mostly* work — and the bug that remains
is the entire reason chapter 11 exists. `examples/11-scope-resolution.lox` will still be
wrong here. That's expected.

## What to implement

### 1. Call expressions

```
unary     → ( "!" | "-" ) unary | call ;
call      → primary ( "(" arguments? ")" )* ;
arguments → expression ( "," expression )* ;
```

Think of `(` as an **infix operator with very high precedence** whose left operand is the
callee. The `*` in the rule is what makes `f(1)(2)` work — currying falls out for free,
and `examples/10-functions.lox` exercises it with `identity(returnSum)(1, 2)`.

An `Expr.Call` node holds the callee, the **closing paren token** (kept purely so runtime
errors have a line number), and the argument list.

The book caps arguments at **255**, for forward-compatibility with clox's bytecode operand
size. Report the error but *don't* raise — the parser isn't confused, so there's nothing to
synchronize from. That distinction is why ch. 6's `error()` returns the exception rather
than raising it.

### 2. Callables

A `LoxCallable` interface with `arity()` and `call(interpreter, arguments)`.

Interpreting a call: evaluate the callee, evaluate each argument **left to right** (order is
observable, so the book fixes it deliberately), then check two things —

- the callee is actually callable (`"not a function"();` must error, not crash),
- the argument count matches the arity exactly.

Both are runtime errors carrying the paren token.

### 3. Native functions

`clock()`, returning seconds as a float. It's the only thing in the standard library, and it
exists so ch. 11's benchmark and the book's tests can measure anything at all. Define it in
the **globals** environment at interpreter construction, not in the current scope.

### 4. Function declarations

```
declaration → funDecl | varDecl | statement ;
funDecl     → "fun" function ;
function    → IDENTIFIER "(" parameters? ")" block ;
parameters  → IDENTIFIER ( "," IDENTIFIER )* ;
```

The `function` rule is factored out separately because ch. 12 reuses it verbatim for
methods, which are declared the same way minus the `fun` keyword.

### 5. Function objects

`LoxFunction` wraps the declaration and implements the callable interface. Calling it:

1. Create a **new environment** whose parent is the function's closure.
2. Bind each parameter to its argument in that environment.
3. Execute the body block in it.

A fresh environment **per call**, not per declaration — that's what makes recursion work,
since each invocation needs its own parameters.

### 6. Return

```
returnStmt → "return" expression? ";" ;
```

Implemented by **raising an exception** carrying the value, caught in `LoxFunction.call`.
This looks like a hack and isn't: `return` has to unwind an arbitrary number of nested
statement executions — out of loops, out of blocks, out of `if`s — and exceptions are
exactly the mechanism for that. Omitting the value returns `nil`; so does falling off the
end.

### 7. Closures

`LoxFunction` stores the environment **in effect where the function was declared**, and uses
it as the parent when called — not the environment active at the call site. That one choice
is what makes `makeCounter()` work.

## Python translation notes

- **`sys.setrecursionlimit`.** The one Python-specific problem the book can't warn you
  about. Python's default limit is 1000 frames, and each *Lox* call burns several Python
  frames (`call` → `execute_block` → `execute` → `visit_*` → `evaluate` → …). Recursive Lox
  code hits `RecursionError` far sooner than you'd expect — `fib(25)` is at risk. Raise the
  limit early in `main`, and consider catching `RecursionError` and reporting it as a Lox
  "stack overflow" runtime error rather than leaking a Python traceback.
- **`Return` as an `Exception` subclass**, not `BaseException`, carrying a `value`. Don't
  let it inherit from `LoxRuntimeError` — it isn't an error and must not be caught by the
  top-level error handler.
- **`LoxCallable`** — an `abc.ABC` with abstract `arity` and `call`, or a `typing.Protocol`
  if you'd rather structurally type it. The ABC gives better errors.
- **The `finally` in `execute_block`** now earns its keep: a `Return` raised deep inside a
  function body unwinds straight through it, and without `finally` the interpreter is left
  pointing at the callee's dead scope. If you skipped it in ch. 8, fix it before testing
  `return`.
- **`__str__` on `LoxFunction`** → `<fn name>`, which the book's tests check.
- **Native functions** — a small class implementing the same interface. A lambda won't do;
  it needs `arity()`.
- **`time.time()`** for `clock()`.

## Gotchas

- [ ] A fresh environment per **call**, not per declaration — otherwise recursion corrupts
      its own parameters.
- [ ] The closure environment is the **declaration** site, not the call site.
- [ ] Arguments evaluate left to right.
- [ ] Arity mismatch is a runtime error: "Expected 2 arguments but got 3."
- [ ] Calling a non-callable errors cleanly.
- [ ] `return;` with no value yields `nil`, as does falling off the end.
- [ ] `Return` isn't caught by the runtime-error handler.
- [ ] `f(1)(2)` parses — the `*` in the `call` rule.
- [ ] Recursion works: write `fib` and run it.
- [ ] `examples/11-scope-resolution.lox` still prints `global` then `block`. **This is the
      correct state at the end of ch. 10** — it's the bug ch. 11 fixes, and seeing it fail
      here is the best possible motivation for the resolver.
