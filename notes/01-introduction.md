# Chapter 1 — Introduction

Framing chapter. No code, but it sets expectations for the next 29 chapters.

## The pitch

Language implementation has a reputation for being the deep end of computer science — dragon books, compiler theory, PhD territory. Nystrom's argument is that the reputation is mostly folklore. The core techniques are approachable, and the payoff is practical: "little languages" are everywhere. Config formats, template engines, markup, query DSLs, build files, save-game serialization. Most of them start as an ad-hoc string parser and grow into an accidental, badly-specified language. Knowing the real techniques means you recognize that moment and reach for the right tool.

The other payoff is less tangible but more real: after this, no language is a black box. You stop treating the runtime as magic.

## Two interpreters, on purpose

The book implements Lox twice. This is the central structural decision:

|               | **jlox** (Part II, ch. 4–13)                         | **clox** (Part III, ch. 14–30)      |
| ------------- | ---------------------------------------------------- | ----------------------------------- |
| Host language | Java                                                 | C                                   |
| Strategy      | Tree-walk interpreter                                | Bytecode virtual machine            |
| Optimizes for | Concepts, clarity                                    | Performance, control                |
| Teaches       | Semantics — scoping, closures, dispatch, inheritance | Memory, GC, encoding, dispatch cost |
| Speed         | Slow, and that's fine                                | Genuinely fast                      |

The first pass gets a *correct* language into your hands quickly so you understand what the semantics actually are. The second pass rebuilds the same language caring about how it runs. The insight is that these are separable concerns, and conflating them is what makes compilers feel hard.

**Our deviation:** Part II in Python rather than Java. Same architecture, less ceremony. Part III would still need C (the whole point is manual memory management), so it stays a stretch goal.

## Lox, briefly

Dynamically typed, garbage collected, C-family syntax, with first-class functions, closures, classes, and single inheritance. Small enough to finish, big enough that nothing important is dodged. Notably it includes closures and OOP — the two features people usually assume are the hard part.

## How the book is structured

- **Every line of code is in the book.** No "the rest is left as an exercise for the reader," no elided helper functions. If it runs, it's on the page.
- **Each chapter ends with a working program.** You are never stranded mid-refactor across a chapter boundary. This is worth respecting — resist the urge to skip ahead and build three chapters at once.
- **Challenges** at the end of each chapter are optional and often explore design alternatives the book rejected. Solutions live in a separate repo. Good for depth, safe to skip on a first pass.
- **Design Notes** are asides about language *design* rather than implementation — why a feature is shaped the way it is. Easy to skim past, usually the most interesting writing in the book.

## Takeaways to carry forward

1. Correctness first, speed second — and they're separable.
2. Keep it runnable at every step. A working slow interpreter beats a half-built fast one.
3. The pipeline stages are independent enough to learn one at a time.
