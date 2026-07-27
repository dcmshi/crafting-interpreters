# Chapter 8 — Statements and State

The language becomes usable: multiple statements, variables, and scope. This is the biggest
structural chapter since 5 — it adds a whole second AST hierarchy.

**Milestone:** `examples/08-statements-and-state.lox` runs end to end.

## What to implement

### 1. Statements

A program stops being one expression:

```
program   → statement* EOF ;
statement → exprStmt | printStmt ;
```

**A parallel `Stmt` hierarchy with its own visitor.** Statements and expressions are
genuinely different — an expression produces a value, a statement produces an effect — and
keeping them as separate types means the type system stops you from writing `1 + 2;` where
a statement belongs, or using a `print` as a subexpression.

Start with two: `Expression` (an expression evaluated for its side effect) and `Print`.

The interpreter gets an `execute(stmt)` alongside `evaluate(expr)`, and `interpret()` now
takes a list of statements.

### 2. Global variables

```
program     → declaration* EOF ;
declaration → varDecl | statement ;
varDecl     → "var" IDENTIFIER ( "=" expression )? ";" ;
primary     → ... | IDENTIFIER ;
```

The new `declaration` level exists because declarations aren't allowed everywhere a
statement is — `if (x) var y = 1;` is nonsense, since nothing could ever reference `y`.
Splitting the rule enforces that for free.

Two new nodes: `Stmt.Var` (name token, optional initializer) and `Expr.Variable` (name
token). Omitting the initializer means `nil`.

This is where `synchronize()` from ch. 6 finally matters — the declaration loop is the
natural recovery point.

### 3. Environments

The `Environment` class: a dict from name to value, with

- **`define`** — always creates a binding in *this* environment. Redefining an existing
  global is deliberately allowed, because it makes the REPL bearable.
- **`get`** — look up, error if not found.

**Undefined variables are a *runtime* error, not a static one.** This is a real design
decision the book explains: making it static would break mutual recursion, since the first
function would reference the second before it's declared. Deferring to runtime is what lets
recursive and mutually recursive functions work in ch. 10.

### 4. Assignment

```
expression → assignment ;
assignment → IDENTIFIER "=" assignment | equality ;
```

Assignment is an **expression**, and it's **right-associative** — `a = b = c` works.

The parsing trick is worth understanding, because it recurs: you don't know you're looking
at an assignment until you hit the `=`, which could be arbitrarily far ahead. Rather than
unbounded lookahead, **parse the left side as a normal expression, then if you see `=`,
check whether what you parsed is a valid assignment target and convert it.** A `Variable`
node becomes an `Assign` node. Anything else is an "Invalid assignment target." error.

This is the **l-value / r-value** distinction: `a` on the left of `=` means the storage
location, on the right it means the value.

`Environment.assign` differs from `define`: it walks the enclosing chain looking for an
existing binding and errors if there isn't one. **Assignment never creates a variable.**

### 5. Scope

`Stmt.Block` and `{ }` in the grammar. Each block gets a fresh `Environment` whose
`enclosing` field points at the one it's nested in — a linked list, walked outward on
lookup. That chain *is* lexical scope.

`execute_block` swaps in the new environment, runs the statements, and restores the
previous one.

## Python translation notes

- **Two visitor hierarchies** — this is where the `visit_binary_expr` / `visit_print_stmt`
  naming stops looking redundant.
- **`Environment.values`** is a `dict[str, object]`. Nothing fancier is needed.
- **Restore the environment in a `finally`.** Not optional. In ch. 10 `return` is
  implemented as a raised exception that unwinds straight through `execute_block`, and
  without `finally` the interpreter would be left pointing at a dead scope. Costs one line
  now, causes a baffling bug in two chapters if you skip it.
- **`Stmt` visitor methods return `None`.** Fine, but be deliberate — don't accidentally
  rely on a statement's return value.
- **Chained assignment** — `a = b = c` should work as soon as `assignment` recurses into
  itself. `examples/08-statements-and-state.lox` tests it.
- **`get` and `assign` raise `LoxRuntimeError`** with the name token, so the error reports
  a line.

## Gotchas

- [ ] `var a;` then `print a;` gives `nil`, not an error.
- [ ] `a = 1;` with no prior `var a` is a runtime error — assignment doesn't declare.
- [ ] Reading an undefined variable is a **runtime** error, not a parse error.
- [ ] Inner blocks shadow outer names, and the outer value is intact after the block ends.
- [ ] An inner block can read *and assign* an outer variable — `assign` walks the chain,
      `define` doesn't.
- [ ] `a = b = c` parses right-associatively.
- [ ] `1 = 2;` reports "Invalid assignment target."
- [ ] The environment is restored even when a statement inside the block errors.

## Challenges

The REPL challenge is worth doing for your own comfort: make a bare expression typed at the
prompt print its value, so you can type `1 + 2` instead of `print 1 + 2;`. The other one —
making it an error to reference a variable that's declared but not yet *initialized* —
is a preview of ch. 11.
