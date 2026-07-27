# Chapter 3 — The Lox Language

This chapter is the **requirements document**. Everything in chapters 4–13 exists to make something on this page work. Keep it open while implementing.

Lox is a high-level, dynamically typed, garbage-collected scripting language. Syntax borrows from the C family (curly braces, semicolons, parenthesized conditions); semantics are much closer to Scheme and JavaScript — everything is an expression-oriented value, functions are first class, and there's no static type system.

## Data types — there are exactly four

| Type | Notes |
|---|---|
| **Boolean** | `true`, `false`. Dedicated type, not integers. |
| **Number** | Double-precision floating point **only**. No integer type. `1` and `1.0` are the same value. |
| **String** | Double-quoted. Distinct from numbers, no implicit conversion. |
| **Nil** | The "no value" value. Nystrom notes he'd omit it in a statically typed language, but a dynamic language needs it. |

Four types is a deliberate minimum. Everything else in the language is built from these plus functions and class instances.

**Consequence to remember:** numbers being doubles means naive printing gives you `2.0` where a user expects `2`. You'll need a stringify step that trims the trailing `.0` for integral values. This bites in Chapter 7.

## Expressions

**Arithmetic** — binary `+ - * /`, unary `-` for negation. Standard C precedence and associativity.

**`+` is overloaded** — numeric addition on two numbers, string concatenation on two strings. It's the one operator that inspects its operand types. Mixed operands are a runtime error, not a coercion.

**Comparison and equality** — `< <= > >=` on numbers only. `==` and `!=` on any pair of values.

**No implicit conversions, ever.** `1 == "1"` is `false`. This is a stated design position: Lox refuses the JavaScript-style coercion lattice. Values of different types are never equal.

**Logical operators** — `!` for not; `and` and `or` as keywords rather than `&&`/`||`. Both **short-circuit**, which means they are *control flow*, not ordinary binary operators — they can't be implemented by evaluating both sides. This matters in Chapter 9.

**Grouping** — parentheses, as expected.

**Truthiness rule:** only `false` and `nil` are falsey. Everything else — including `0` and the empty string — is truthy. Do not let the host language's own truthiness leak into your implementation; Python would call `0` and `""` falsey, and that would be wrong.

## Statements

- **Expression statements** — an expression followed by `;`, evaluated for its side effect.
- **`print`** — a *statement built into the grammar*, not a library function. This is a pragmatic hack Nystrom is upfront about: it lets the language produce output long before functions or a standard library exist, so every chapter can demonstrate something. In a real language it'd be a library call.
- **Blocks** — `{ }` group statements and introduce a new scope.

## Variables

`var` declares. An omitted initializer implicitly means `nil`. Scoping is **lexical** — an inner block shadows an outer name, and which declaration a name refers to is determined by where it appears in the source, not by the call stack.

Chapter 8 introduces the environment; Chapter 11 exists almost entirely because getting lexical scope *correct* in the presence of closures is subtler than it looks.

## Control flow

`if`/`else`, `while`, and C-style three-clause `for`. That's the whole set.

No `do`/`while`, no `switch`, no `break`/`continue` (the latter show up as end-of-chapter challenges). The justification is that `if` plus `while` is the minimum for Turing completeness, and `for` earns its place on ergonomics alone. Everything else is sugar that costs implementation effort without teaching anything new.

## Functions

Declared with `fun`. Called with parens. `return` returns a value; falling off the end returns `nil` implicitly.

Terminology the book is careful about, and it's worth adopting: **arguments** are the actual values at the call site; **parameters** are the named variables in the declaration.

Functions are **first class** — real values you can store in variables, pass around, and return. And they can be **declared inside other functions**.

Those two facts together force **closures**: an inner function referring to an outer function's local variable must keep working after the outer function has returned. That means environments can outlive the call frame that created them, which kills the simple "locals live on the stack" model. This single feature is why Chapter 11 exists, and it's the hardest idea in Part II.

## Classes

Nystrom addresses "why OOP at all" head-on: most languages in wide use have some form of it, and the implementation techniques — dynamic dispatch, method lookup, inheritance chains, `this` binding — are genuinely interesting work that a language without objects would skip entirely.

**Classes over prototypes.** Prototypal inheritance (JavaScript, Self) is *simpler to implement* — that's the honest tradeoff — but it pushes complexity onto every user of the language, who then tend to reinvent classes on top of it anyway. Lox takes the complexity into the implementation.

Details:

- `class` declares. Methods are written **without** the `fun` keyword.
- **Classes are first-class values** — you can pass a class around and store it in a variable.
- Instantiate by **calling the class itself**: `Bagel()`. No `new` keyword.
- **Fields are open** — assign any field on any instance at any time, like Python or JavaScript. There are no declared fields.
- `this` inside a method refers to the receiving instance.
- `init()` is the constructor, called automatically on instantiation.

**Inheritance** — single, no interfaces or mixins. Declared with `<`. Subclasses inherit **methods**, not fields (there are no declared fields to inherit). `super` calls the superclass's version of a method.

Chapter 12 is classes; Chapter 13 is inheritance.

## The standard library

Almost nonexistent. `print` (a statement) and `clock()` (added in Chapter 10 as a native function, used for benchmarking). Nystrom openly calls this the weakest part of Lox — a real language lives or dies on its library, but writing one teaches you nothing new about implementation.

## Decisions that will bite later — flag these now

1. **Numbers are doubles** → custom stringify to avoid printing `2.0`.
2. **Truthiness is only false/nil** → never delegate to the host language's truth test.
3. **No implicit conversion** → equality must compare types first. In Python, watch out for `1 == True` being true.
4. **`print` is a statement** → it lives in the grammar, so it's in the parser (Chapter 8), not a builtin.
5. **`and`/`or` short-circuit** → they're control flow, handled separately from binary operators (Chapter 9).
6. **Closures** → the reason Chapter 11 exists; don't be surprised when the naive environment model breaks.
7. **Fields and methods share a namespace on instances** → lookup order matters (Chapter 12): fields shadow methods.
