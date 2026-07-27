# crafting-interpreters

Working through [Crafting Interpreters](https://craftinginterpreters.com/) by Bob Nystrom,
building the Lox language from scratch — in Python instead of Java.

## Goal

**Reach Chapter 11 — Resolving and Binding.**

That's the point where Lox stops being a toy. Chapters 4–10 get you a language that
runs, but its lexical scoping is subtly wrong: a closure resolves variables by walking
the environment chain at *call* time, so a variable declared after the closure was
created can hijack a name the closure had already captured. Chapter 11 adds a static
resolution pass that binds each variable reference to a specific declaration once, up
front — and that's what makes closures behave.

`examples/11-scope-resolution.lox` is the failing case, and it's the acceptance test
for this goal: it must print `global` twice, not `global` then `block`.

Chapters 12–13 (classes and inheritance) come after, and finish jlox.

## Progress

### Part I — Welcome

- [x] 1. Introduction — [notes](notes/01-introduction.md)
- [x] 2. A Map of the Territory — [notes](notes/02-a-map-of-the-territory.md)
- [x] 3. The Lox Language — [notes](notes/03-the-lox-language.md)

### Part II — A Tree-Walk Interpreter (pylox)

- [ ] 4. Scanning — [notes](notes/04-scanning.md)
- [ ] 5. Representing Code — [notes](notes/05-representing-code.md)
- [ ] 6. Parsing Expressions — [notes](notes/06-parsing-expressions.md)
- [ ] 7. Evaluating Expressions — [notes](notes/07-evaluating-expressions.md)
- [ ] 8. Statements and State — [notes](notes/08-statements-and-state.md)
- [ ] 9. Control Flow — [notes](notes/09-control-flow.md)
- [ ] 10. Functions — [notes](notes/10-functions.md)
- [ ] 11. Resolving and Binding **← goal**
- [ ] 12. Classes
- [ ] 13. Inheritance

### Part III — A Bytecode Virtual Machine (clox)

- [ ] 14–30 (stretch goal)

## Layout

- `pylox/` — the interpreter itself.
- `notes/` — one write-up per chapter.
- `examples/` — Lox programs used as smoke tests. Each file is named for the chapter
  that makes it run; see [examples/README.md](examples/README.md).

## Running it

Requires Python 3.10+ (developed on 3.14). No dependencies.

```
python -m pylox                 # REPL
python -m pylox script.lox      # run a file
```

### pylox modules

| Module | Chapter | Role |
| --- | --- | --- |
| `token_type.py` | 4 | the `TokenType` enum |
| `token.py` | 4 | the `Token` record |
| `error_reporter.py` | 4 | error reporting, shared by every phase |
| `scanner.py` | 4 | characters → tokens |
| `lox.py` | 4 | entry point: run a file, or a REPL |

## Resources

- **[craftinginterpreters.com](https://craftinginterpreters.com/)** — the book, free to
  read online.
- **[munificent/craftinginterpreters](https://github.com/munificent/craftinginterpreters)**
  — the book's official repository. Contains the book's own source text, the complete
  reference implementations of jlox and clox, and most usefully:
  - **[`test/`](https://github.com/munificent/craftinginterpreters/tree/master/test)** —
    several hundred `.lox` files with expected output and expected error messages,
    organized by feature, plus a runner that can be pointed at any implementation. Far
    more thorough than our `examples/`. Clone it *outside* this repo.
  - **[`note/answers/`](https://github.com/munificent/craftinginterpreters/tree/master/note/answers)**
    — worked solutions to the end-of-chapter challenges.
