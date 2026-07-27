# Examples

Lox programs harvested from Chapter 3 (the language spec), organized as a progress bar.

Each file is named for **the chapter that makes it run**. Before that chapter it will
fail to parse or fail at runtime; after it, it should produce exactly the output in its
`Expected output:` header comment.

| File | Runs after | Exercises |
| --- | --- | --- |
| `07-expressions.lox` | Ch. 7 — Evaluating Expressions | literals, arithmetic, comparison, equality, truthiness, string concat |
| `08-statements-and-state.lox` | Ch. 8 — Statements and State | `print`, `var`, assignment, blocks, shadowing |
| `09-control-flow.lox` | Ch. 9 — Control Flow | `if`/`else`, `while`, `for`, short-circuit `and`/`or` |
| `10-functions.lox` | Ch. 10 — Functions | declaration, calls, `return`, first-class functions, basic closure |
| `11-scope-resolution.lox` | Ch. 11 — Resolving and Binding | the closure/scope bug the resolver fixes |
| `12-classes.lox` | Ch. 12 — Classes | `class`, instantiation, fields, methods, `this`, `init` |
| `13-inheritance.lox` | Ch. 13 — Inheritance | `<`, inherited methods, `super` |

Note `07-expressions.lox` uses `print`, which technically arrives in Chapter 8. At the end
of Chapter 7 the interpreter evaluates a single bare expression, so check that chapter's
work by pasting individual expressions into the REPL; this file becomes runnable at Ch. 8.

## Running them all

Once there's an interpreter, running the whole folder and diffing against the expected
output in each header is the fastest regression check available.

For something far more thorough, clone [munificent/craftinginterpreters](https://github.com/munificent/craftinginterpreters)
outside this repo — its `test/` directory has several hundred Lox files with expected
output and error messages, and a runner that can be pointed at any implementation.
