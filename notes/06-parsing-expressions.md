# Chapter 6 — Parsing Expressions

Tokens in, AST out. This is where the ambiguous grammar from chapter 5 gets rewritten into
something you can actually parse, and where error handling gets serious.

**Milestone:** type an expression at the REPL and see the AST printer's output. `1 + 2 * 3`
must print as `(+ 1 (* 2 3))`, not `(* (+ 1 2) 3)`.

## Ambiguity, precedence, associativity

Two rules resolve the ambiguity:

- **Precedence** — which operator binds tighter when they're different. `*` beats `+`.
- **Associativity** — which side binds tighter when they're the same. `-` is
  **left**-associative, so `5 - 3 - 1` is `(5 - 3) - 1`. Assignment (ch. 8) is
  **right**-associative.

Lox's precedence, lowest to highest: equality → comparison → term → factor → unary.

The trick that makes this parseable: **give each precedence level its own grammar rule**,
where each rule matches operators at its level *or any higher level*. Precedence stops
being something the parser remembers and becomes structure in the grammar.

```
expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" ;
```

Read the shape of each binary rule: *one operand of the next-higher level, then zero or
more (operator, operand) pairs.* That `( ... )*` is where associativity comes from.

## Recursive descent

**Every grammar rule becomes a function.** That's the whole technique. It's top-down —
you start at the lowest-precedence rule and descend — and it's what GCC, V8, and most
production parsers actually use, despite being the simplest thing in the book.

The translation is mechanical:

| Grammar | Code |
| --- | --- |
| `a \| b` | if/elif on the lookahead |
| `a b` | sequential calls |
| `a*` | a `while` loop |
| `a?` | an `if` |
| a nonterminal | a call to that rule's function |

**Left-associativity comes from the loop, not the recursion.** Each iteration wraps the
tree built so far as the *left* child of a new Binary node. If you wrote it as recursion
you'd get right-associativity and `5 - 3 - 1` would be wrong. Unary is right-associative,
which is exactly why `unary` recurses into itself instead of looping.

## What to implement

### 1. The Parser

State: the token list and a `current` index. Helpers, all one-liners:

| Helper | Job |
| --- | --- |
| `peek` | current token, unconsumed |
| `previous` | most recently consumed token |
| `is_at_end` | is `peek` the EOF token |
| `advance` | consume and return |
| `check` | does the current token have this type (no consume) |
| `match` | consume if the current token is any of these types |
| `consume` | require a specific type, or raise a parse error |

Note how closely these mirror the scanner's helpers — same idea, one level up. `match` is
the parser's conditional advance, just as it was in the scanner.

### 2. One method per grammar rule

`expression`, `equality`, `comparison`, `term`, `factor`, `unary`, `primary`. The four
binary rules are near-identical; the book writes them out longhand and so should you the
first time, then decide whether to factor out a helper.

### 3. Syntax error handling

A parser has two jobs: build a tree for valid input, **and** detect and report invalid input
without crashing, hanging, or reporting one real error as fifty cascading ones.

- **Report at a token**, not a line — you can say `Error at ')': Expect expression.` The
  reporter needs a second entry point that takes a token, formatting the location as
  ` at end` for EOF and ` at '<lexeme>'` otherwise.
- **Panic mode.** On an error, raise a `ParseError` to unwind out of however many nested
  rule calls you're inside.
- **Synchronize.** Discard tokens until you're plausibly at the start of a new statement —
  just past a `;`, or just before one of `class fun var for if while print return`. This
  keeps one syntax error from generating a cascade of bogus follow-on errors.
- The book has `error()` **return** the exception rather than raise it, so the caller
  decides whether this error is worth unwinding for. Subtle, and it matters in ch. 8.

Synchronization is barely exercised in this chapter — there's only one expression to parse.
Build it anyway; ch. 8 introduces statements and it starts earning its keep immediately.

## Python translation notes

- **`ParseError`** — a plain `Exception` subclass. It carries no data; it exists purely to
  unwind the stack.
- **`match` as a method name** is fine. It's a *soft* keyword in Python, only special in
  statement position, so `self.match(...)` never conflicts.
- **`*types: TokenType`** for `match`'s varargs reads well.
- **Returning `None` on error** — `parse()` should return `None` when it fails, and the
  caller checks the reporter's flag before touching the result. Type it `Expr | None`.
- **Recursion depth** — deeply nested parentheses recurse deeply. Not a problem at this
  scale, but it's the first hint of the recursion-limit issue that bites in ch. 10.

## Gotchas

- [ ] `1 + 2 * 3` parses as `(+ 1 (* 2 3))`. Check this first; it's the whole point.
- [ ] `5 - 3 - 1` is `(- (- 5 3) 1)`. If it's right-associative, you recursed where you
      should have looped.
- [ ] `!!true` works — `unary` recurses into itself.
- [ ] An unclosed `(` reports `Expect ')' after expression.` rather than hanging.
- [ ] A stray `)` alone reports `Expect expression.` and doesn't loop forever.
- [ ] Never execute when the reporter has an error flagged.

## Challenges

The interesting one is adding the **comma operator** and the **ternary `?:`** — the latter
forces you to think about how a right-associative, three-operand rule slots into the
precedence chain. Also worth skimming: error productions for a binary operator appearing
with no left operand, which is how real compilers produce "did you mean" messages.
