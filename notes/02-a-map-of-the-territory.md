# Chapter 2 — A Map of the Territory

The most important conceptual chapter in the book. Everything after this is filling in one box on this map. Worth re-reading when you get lost later.

## The mountain

Nystrom's metaphor: you start at the bottom-left with raw source text, climb *up* the analysis side gaining higher-level understanding of the program, cross a summit, then descend the synthesis side toward the target representation. Every language implementation walks some path over this mountain — the differences are how high it climbs before turning around, and where it comes back down.

```
                    IR / optimization
                       /        \
          static analysis        code generation
                 /                        \
            parsing                    bytecode / native
               /                              \
         scanning                          (runtime)
            /                                    \
      source code                            running program
```

## Climbing up: the front end

### 1. Scanning (lexing)

Characters → **tokens**. `var x = 1;` becomes `var`, `x`, `=`, `1`, `;`. Whitespace and comments get discarded here. The scanner's whole job is chunking a flat character stream into meaningful words. Conceptually the easiest stage, and it's where Chapter 4 starts.

### 2. Parsing

Tokens → a tree — the **AST** (abstract syntax tree) or parse tree. This is where *grammar* enters: rules describing which token sequences are valid, and how they nest. The parser is also where syntax errors get reported.

The tree structure matters because it encodes precedence and associativity. Once `1 + 2 * 3` is a tree, the fact that `*` binds tighter is a structural property, not something the evaluator has to remember.

### 3. Static analysis

The first stage that is genuinely *language-specific*. Everything before this is mostly mechanical; this is where your language's rules live.

- **Binding / resolution** — for each identifier, figure out which declaration it refers to. This requires implementing **scope**.
- **Type checking** — only if the language is statically typed. Lox isn't, so we mostly skip this. This is where type errors get reported in languages that have them.

Where do the results go? Three options, all used in practice:
- as extra attributes stored on the AST nodes,
- in a **symbol table** off to the side keyed by identifier,
- or by transforming the tree into an entirely new representation.

Everything up to and including this point is the **front end**. Everything after is the **back end**.

## The summit: intermediate representations

The middle of the pipeline is where the code stops resembling the source language and doesn't yet resemble the target machine. An **IR** is a representation tied to neither.

The motivating problem is combinatorial: supporting M source languages on N target architectures naively costs M×N implementations. With a shared IR it's M front ends plus N back ends — M+N. This is exactly why GCC and LLVM exist in the shape they do, and why a new language can get twenty architectures for free by emitting LLVM IR.

Named IR styles worth recognizing (you won't implement these): control flow graph, static single-assignment (SSA), continuation-passing style (CPS), three-address code.

## Optimization

Once you understand what the program *means*, you can swap it for a different program with identical semantics but better performance.

The teaching example is **constant folding**: `3 + 4` in the source becomes the literal `7` at compile time. Real optimizers go much further — constant propagation, common subexpression elimination, loop unrolling, escape analysis, inlining.

Important calibration, and Nystrom is blunt about it: this is a deep rabbit hole and **many successful languages barely do it**. Lua and CPython invest almost nothing in compile-time optimization and put the effort into a fast runtime instead. We do essentially none of this.

## Descending: the back end

### Code generation

Emit instructions the machine can run. The fork in the road:

- **Native machine code** — fast, but you're writing an architecture-specific backend, and you need to learn that architecture's instruction set. Non-portable by construction.
- **Bytecode** — a synthetic instruction set for an idealized machine you invent. Portable, far simpler to generate. But no chip runs it.

### Virtual machine

If you emitted bytecode, something has to execute it: a VM that simulates the hypothetical machine. You pay a real speed penalty (you're emulating in software) in exchange for portability — write the VM once in C, run your language anywhere C compiles. This is Part III.

### Runtime

Services the program needs *while executing*: garbage collection, tracking object types for `instance of`-style checks. In Java or Python this lives inside the VM. In a fully-compiled language like Go, it's linked into every produced executable.

## Shortcuts and alternate routes

Not every implementation makes the full climb.

**Single-pass compilers** interleave parsing, analysis, and code generation — emitting output directly in the parser, with no AST and no IR. That means no going back to revisit earlier parts of the program, which *restricts the language design*. This is the actual reason C requires you to declare things before using them, and why forward declarations exist. Pascal and C were both shaped by 1970s memory constraints.

**Tree-walk interpreters** skip the back end entirely: build the AST, then execute it by traversing the tree directly. Simple, slow. Rare in production — early Ruby (MRI) was one. **This is jlox, and it's what we're building in Part II.**

**Transpilers (source-to-source)** write a front end, then emit *another high-level language* as the target and let its toolchain do the rest. Historically people emitted C; today everything emits JavaScript. Cheap way to get a huge platform for free.

**Just-in-time compilation** compiles to native code at load time, on the user's actual machine. Sophisticated JITs profile at runtime, find hot spots, and recompile them with better optimization. HotSpot, V8, and the CLR all do this. Hardest option, fastest result.

## Vocabulary: compiler vs. interpreter

The distinction people argue about is mostly confused. The precise version:

- **Compiling** is translating source code into some other form. That's it — it doesn't mean "produces a native binary."
- A **compiler** translates and stops; it doesn't run the result.
- An **interpreter** takes source and executes it immediately — it runs programs "from source."

These overlap. Draw it as a Venn diagram: GCC is a pure compiler. Old Ruby MRI was a pure interpreter. **CPython is both** — it compiles your source to bytecode, then interprets that bytecode. So is our Lox implementation eventually.

The related error: **a language is not interpreted or compiled — an implementation is.** "Is Python interpreted?" is a category mistake. Python is a language; CPython, PyPy, and Jython make different choices.

## What this means for us

Our path over the mountain, Part II: **scanning → parsing → static analysis (resolution only) → walk the tree.** No IR, no optimization, no code generation, no VM. We climb the front end properly and then jump straight to execution.

That's chapters 4–13. Chapter 11 (Resolving and Binding) is the static analysis box; everything else is scanner, parser, and evaluator.
