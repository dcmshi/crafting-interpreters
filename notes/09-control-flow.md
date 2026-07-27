# Chapter 9 — Control Flow

Short, and the payoff is enormous: at the end of this chapter Lox is **Turing complete**.
Three statement forms and two operators.

**Milestone:** `examples/09-control-flow.lox` runs, including the Fibonacci loop.

## What to implement

### 1. `if` / `else`

```
statement → exprStmt | ifStmt | printStmt | block ;
ifStmt    → "if" "(" expression ")" statement ( "else" statement )? ;
```

The interpreter side is three lines — evaluate the condition, check truthiness, execute one
branch. Note that Lox's control flow uses *Lox* truthiness, so `if (0)` takes the then-branch.

**The dangling else problem.** In `if (a) if (b) x(); else y();` the grammar is genuinely
ambiguous about which `if` the `else` belongs to. Every C-family language resolves it the
same way: **the `else` binds to the nearest preceding `if`.** Recursive descent gives you
this for free — the innermost `if` call is the one executing when the `else` is consumed,
so it grabs it. Worth knowing you got it right by accident rather than by design.

### 2. Logical operators

```
expression → assignment ;
assignment → IDENTIFIER "=" assignment | logic_or ;
logic_or   → logic_and ( "or" logic_and )* ;
logic_and  → equality ( "and" equality )* ;
```

`and` binds tighter than `or`; both sit between assignment and equality.

**A new `Expr.Logical` node, separate from `Binary`.** They look identical structurally,
and that's exactly the trap — the *evaluation* differs. A `Binary` node evaluates both
operands then combines. A `Logical` node evaluates the left operand, and **short-circuits**:
if that's enough to determine the result, the right operand is never evaluated at all. That
makes them control flow, not operators. Different behavior, different node.

**They return an operand, not a boolean.** `nil or "hi"` evaluates to `"hi"`. `1 and 2`
evaluates to `2`. The rule: `or` returns the left operand if it's truthy, otherwise the
right; `and` is the mirror image. This is the JavaScript/Python behavior, not the Java one.

### 3. `while`

```
statement → ... | whileStmt ;
whileStmt → "while" "(" expression ")" statement ;
```

The one place a Python `while` loop appears in your interpreter.

### 4. `for` — and desugaring

```
forStmt → "for" "(" ( varDecl | exprStmt | ";" )
                    expression? ";"
                    expression? ")" statement ;
```

The chapter's big idea: **`for` gets no AST node at all.** The parser reads the three
clauses and the body, then builds a tree out of nodes that already exist:

```
for (init; cond; incr) body
```
becomes
```
{ init; while (cond) { body; incr; } }
```

That's **desugaring** — a surface feature expressed entirely in terms of existing ones. The
interpreter never learns what a `for` loop is. Every language does this extensively; it's
how you add ergonomics without adding semantics.

Assemble it back to front: wrap the body with the increment, build the while with the
condition (a `Literal(True)` if the condition was omitted), then wrap it all in a block with
the initializer. Watch the ordering — the increment runs *after* the body, and the
initializer's scope must enclose the loop, not repeat inside it.

## Python translation notes

- **Return the operand, not `True`/`False`,** from `visit_logical_expr`. Easy to get wrong,
  and `examples/09-control-flow.lox` tests it directly with `print nil or "hi";`.
- **Short-circuiting is observable.** The example file checks that `false and (ran = "yes")`
  leaves `ran` untouched. If you evaluate both sides eagerly, that test fails and nothing
  else does — it's the only way to catch the bug.
- **Desugaring happens in the parser**, so you're constructing `Stmt` objects by hand there
  rather than parsing them. It feels odd the first time; it's correct.
- **The interpreter's `while`** calls `is_truthy` on the re-evaluated condition each pass,
  not Python's own truth test.
- **Infinite loops are now writable**, and Ctrl-C in the REPL should ideally not kill the
  whole session. Handling `KeyboardInterrupt` around `execute` is a nicety worth two lines.

## Gotchas

- [ ] `if (0)` takes the then-branch — Lox truthiness, not Python's.
- [ ] `else` binds to the nearest `if`.
- [ ] `print nil or "hi";` prints `hi`, not `true`.
- [ ] `print true and false;` prints `false` — a real boolean here, because that's the
      operand.
- [ ] The right operand of a short-circuited `and`/`or` never evaluates.
- [ ] `for (;;)` with all three clauses omitted parses and loops forever.
- [ ] `for` produces no new AST node type.
- [ ] The loop variable in `for (var i = ...)` is scoped to the loop, not leaked outward.

## Challenges

`break` is the interesting one, and the technique previews ch. 10: you implement it by
raising an exception that the `while` handler catches. It also needs a parse-time check
that `break` only appears inside a loop. Skippable if you're racing to ch. 11, but it's
about twenty minutes and the exception-as-control-flow idea is exactly what `return` uses.
