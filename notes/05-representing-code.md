# Chapter 5 — Representing Code

No interpreter behavior in this chapter. It defines the **data structure** every later
chapter operates on, and introduces the notation the book uses to specify grammar.

**Milestone:** hand-build a small tree and print it. The chapter's own example prints
`(* (- 123) (group 45.67))`.

## Context-free grammars

Chapter 4 used a *lexical* grammar: characters in, tokens out, and it was **regular** —
expressible as a regular expression. That's not enough for expressions, because expressions
nest arbitrarily deep and regular languages can't count nesting. So the *syntactic* grammar
— tokens in, expressions out — is **context-free**.

The notation, which the book uses for the rest of Part II:

- **Terminals** — literal tokens, written in quotes or CAPS: `"("`, `NUMBER`.
- **Nonterminals** — named references to other rules, lowercase: `expression`.
- A rule is `name → body ;` with `|` for alternatives, `( )` for grouping, `*` for
  zero-or-more, `+` for one-or-more, `?` for optional.

The first Lox expression grammar:

```
expression     → literal | unary | binary | grouping ;
literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">=" | "+" | "-" | "*" | "/" ;
```

**This grammar is ambiguous on purpose.** It says nothing about precedence or
associativity, so `1 + 2 * 3` has two valid parses. Don't try to write a parser against it.
Chapter 6 rewrites it into an unambiguous form. Right now it exists only to tell you which
tree node types to define.

## What to implement

### 1. The expression nodes

Four classes, all of them **dumb data** — no behavior, no methods that do work:

| Node | Fields |
| --- | --- |
| `Binary` | left, operator token, right |
| `Grouping` | the inner expression |
| `Literal` | the value |
| `Unary` | operator token, right |

Plus an `Expr` base type they all share, so the parser has something to return.

The book generates these with a metaprogramming script (`GenerateAst`) because writing
them in Java is 200 lines of boilerplate. **Skip that entirely.** In Python these are four
frozen dataclasses and about twenty lines. Write them by hand; the generator solves a
problem we don't have. Note the book keeps adding node types through ch. 12, so leave the
file easy to extend.

### 2. A tree-walking mechanism

This is the real content of the chapter.

**The Expression Problem.** Picture a table: rows are types (Binary, Grouping, …), columns
are operations (interpret, resolve, print). Object-oriented languages make it easy to add a
*row* — define a new class with all its methods — and painful to add a *column*, since you'd
have to touch every class. Functional languages are the reverse.

We need to add columns: interpret (ch. 7), resolve (ch. 11), print. So we want the
functional shape, in an OO language.

**The visitor pattern** is how you get it. Each node gets an `accept(visitor)` that calls
back into `visitor.visit_binary_expr(self)` — the node knows its own type, so it picks the
right method. That's **double dispatch**: one dispatch on the node, one on the visitor.
Each new operation is then one new visitor class, with every node type handled in one file.

### 3. The AST printer

Your first visitor, and a genuinely useful debugging tool for chapter 6. Produces Lisp-style
parenthesized output: `(* (- 123) (group 45.67))`.

## Python translation notes

- **Nodes** — `@dataclass(frozen=True)`, one per node type, all subclassing `Expr`. Type the
  literal value as `object | None`.
- **Visitor** — Python gives you three options:
  1. **`accept()` plus `visit_*` methods**, mirroring the book.
  2. **`match` with class patterns.** Dataclasses generate `__match_args__` for free, so
     `case Binary(left, op, right):` just works. Genuinely more elegant Python.
  3. `functools.singledispatchmethod`.

  **Recommendation: option 1.** Not because it's prettier — it isn't — but because
  chapters 7, 8, 11 and 12 are all written as visitor classes, and keeping a 1:1 mapping
  to the book means you're translating rather than redesigning while reading. You're
  aiming at chapter 11 fast; fidelity is worth more than elegance here. If you want
  option 2, do it as a refactor *after* ch. 11 works.

- **Don't build the AST generator.** It solves a Java verbosity problem.
- **Naming** — the book uses `visitBinaryExpr`; `visit_binary_expr` is the Python spelling.
  The `Expr` suffix looks redundant until ch. 8 adds a parallel `Stmt` hierarchy with its
  own visitor — then `visit_expression_stmt` vs. `visit_variable_expr` earns its keep.
- **`Literal(None)`** is how `nil` is represented. That's a real literal value, not "no
  value", so don't let a default-argument `None` blur the two.

## Gotchas

- [ ] The grammar in this chapter is ambiguous — it defines node *types*, not parsing.
- [ ] Nodes hold the operator **token**, not just the character. Ch. 7 needs `token.line`
      to report runtime errors, and by then the source text is long gone.
- [ ] Freeze the dataclasses. Nothing should mutate a tree after parsing, and it makes the
      ch. 11 resolver easier to reason about.
- [ ] Printing `123` not `123.0` shows up here for the first time — same stringify problem
      as ch. 7. Worth solving once, in one place.
