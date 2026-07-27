# Chapter 4 — Scanning

First code. This chapter builds the project skeleton *and* the lexer, so it's front-loaded
with plumbing that every later chapter reuses.

**Milestone:** run a `.lox` file or drop into a REPL and print the token stream. An
unterminated string reports a line number instead of crashing.

## The idea

Scanning turns a flat stream of characters into a list of **tokens**. `var x = 1;` becomes
six tokens. Whitespace and comments are discarded — the parser never sees them.

Two terms the book keeps distinct:

- **Lexeme** — the raw substring from the source: `var`, `x`, `=`, `1`, `;`.
- **Token** — a lexeme plus everything the scanner figured out about it: its type, its
  literal value (if any), and its line number.

The scanner's whole structure is one loop: mark the start of a lexeme, consume characters
until you know what it is, emit a token, repeat.

The lexical grammar of Lox is a **regular language**, so this could be done with regexes
or a generator like lex/flex. Hand-writing it is more code but no black boxes, and it makes
error reporting much better.

## What to implement

### 1. The interpreter framework

The entry point, with three modes:

- **No arguments** → REPL. Read a line, run it, loop. Reset the error flag after each line
  so one typo doesn't kill the session.
- **One argument** → read that file and run it.
- **More** → print a usage message and exit.

A `run(source)` function ties it together: construct a scanner, scan tokens, and for now
just print them.

### 2. Error reporting

An `error(line, message)` function and a `report(line, where, message)` helper that writes
to **stderr** in the form `[line N] Error<where>: message`, plus a `had_error` flag.

Two behaviors that matter more than they look:

- **Keep scanning after an error.** You want to report *every* bad character in one run,
  not just the first. The `had_error` flag is what stops you from executing the result.
- **Never execute code with `had_error` set.** Report, then bail before running.

Exit codes come from UNIX's `sysexits.h`: **64** for a usage error, **65** for a data
(source) error, and later **70** for a runtime error. Arbitrary, but conventional.

Nystrom flags in an aside that better engineering would put error reporting behind a
separate reporter object passed into the scanner and parser, rather than a static on the
main class. He does the simple thing for the book. **We should do the good thing** — a
small reporter object, because in Python a module-level global creates a circular import
between the scanner and the entry-point module. Doing it now costs nothing; retrofitting
it in Chapter 6 is annoying.

### 3. Token types

An enum covering:

- **Single-character:** `( ) { } , . - + ; * /`
- **One-or-two-character:** `! !=`, `= ==`, `> >=`, `< <=`
- **Literals:** identifier, string, number
- **Keywords:** `and class else false fun for if nil or print return super this true var while`
- **EOF**

The EOF token matters — the parser leans on it as a sentinel so it never has to bounds-check.

### 4. Token

Four fields: type, lexeme, literal, line. The literal is the *converted* value — the scanner
turns the characters `123` into the number 123.0 and strips the quotes off a string, using
the host language's own value types. Everything downstream gets real values, not text.

Only the line number is stored for location. An aside notes you could store offset and
length for much better error messages; the book keeps it simple.

### 5. The scanner

State: the source text, the token list, and three cursors — `start` (first character of the
lexeme being scanned), `current` (the character being looked at), and `line`.

The main loop runs until the end of input: set `start` to `current`, scan one token, repeat.
Then append the EOF token.

Helpers you'll want, roughly in the order you need them:

| Helper      | Job                                                                     |
| ----------- | ----------------------------------------------------------------------- |
| `is_at_end` | has `current` run off the end                                           |
| `advance`   | consume and return the current character                                |
| `add_token` | emit a token spanning `start`..`current`                                |
| `match`     | conditional advance — consume only if the next char is the expected one |
| `peek`      | look at the current character without consuming                         |
| `peek_next` | look one further ahead                                                  |

`match` is the two-character-operator trick; `peek` is one character of lookahead; `peek_next`
is the second character of lookahead, needed only by numbers.

### 6. The cases, in the order the chapter adds them

1. **Single characters** — a straight dispatch on the consumed character.
2. **Two-character operators** — `!`, `=`, `<`, `>` each check whether `=` follows.
3. **`/` vs. comments** — the interesting one. Same first character, two meanings. If a
   second `/` follows, consume to end of line and emit *nothing*; comments are discarded.
4. **Whitespace** — space, carriage return, and tab are ignored; newline increments the line
   counter and is otherwise ignored.
5. **Unexpected characters** — report an error, but keep going.
6. **Strings** — consume until the closing quote. Lox strings **may span lines** (so bump the
   line counter inside the loop) and have **no escape sequences**. Hitting the end of input
   first is an unterminated-string error. Strip the surrounding quotes for the literal value.
7. **Numbers** — consume digits; then, only if a `.` is followed by another digit, consume the
   `.` and the remaining digits. Convert to a float.
8. **Identifiers and keywords** — consume the full identifier, *then* look the text up in a
   keyword table. Not found means it's a plain identifier.

## Two ideas worth more than the code

**Maximal munch.** When two lexical rules both match, the one consuming more characters wins.
`orchid` is an identifier, not the keyword `or` followed by `chid`. This is exactly why you
scan the whole identifier before consulting the keyword table rather than trying to match
keywords as you go.

**Lookahead.** How far ahead a scanner must peek to decide what it's looking at is a real
design property. Lox needs one character almost everywhere, and two in exactly one place:
deciding whether a `.` is a decimal point requires seeing a digit after it. The same question
— how much lookahead — comes back for the parser in Chapter 6.

## Python translation notes

- **Enum** — `enum.Enum` with `auto()`. Plain strings work but you lose typo-checking.
- **Token** — a `dataclass` is the natural fit. Give it a `__str__` that prints
  type / lexeme / literal, since dumping tokens is this chapter's only output.
- **Static `hadError`** → the reporter object described above, not a module global.
- **`char`** → Python has no char type; a one-character string from indexing the source is
  the equivalent. `peek` at end of input should return a sentinel (`"\0"` matches the book).
- **`switch`** → an if/elif chain, or `match` on 3.10+.
- **`Double.parseDouble`** → `float()`.
- **Don't use `str.isdigit()` / `str.isalpha()`.** This is the real trap in this chapter.
  Python's versions are Unicode-aware: `"²".isdigit()` and `"٣".isdigit()` are both true, and
  `isalpha()` accepts every accented and non-Latin letter. Lox is ASCII-only, so hand-roll the
  range checks. Remember `_` counts as an identifier character but not as a letter.
- **Reading the file** — read as text with an explicit encoding.
- **REPL** — Java's `readLine()` returns null at end of input; Python's `input()` raises
  `EOFError`. Catch it to exit cleanly on Ctrl-D (Ctrl-Z on Windows), and consider catching
  `KeyboardInterrupt` too.
- **Keyword table** — a plain dict.
- Suggested module split: entry point, error reporter, token type, token, scanner. Keeps the
  circular-import problem from ever appearing.

## Gotchas checklist

- [ ] EOF token appended after the loop.
- [ ] Quotes stripped from the string literal's value.
- [ ] Unterminated string reports an error rather than running off the end.
- [ ] Multi-line strings still increment the line counter.
- [ ] `.5` and `5.` are **not** valid number literals — no leading or trailing dot. (The book's
      reason: it keeps the door open for method calls on numbers later, like `123.sqrt()`.)
- [ ] Comments produce no token at all.
- [ ] Scanning continues after an unexpected character; `had_error` prevents execution.
- [ ] `orchid` scans as one identifier.

## Challenges

The end-of-chapter challenges are worth skimming even if you skip them. The genuinely useful
one is **adding C-style `/* ... */` block comments, with nesting** — nesting is what makes it
interesting, since it can't be done with a regular expression.
