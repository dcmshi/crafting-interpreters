"""pylox — a tree-walk interpreter for Lox, following Crafting Interpreters Part II.

Module map (chapters that introduce each piece):

    token_type.py      ch. 4  — the TokenType enum
    token.py           ch. 4  — the Token record
    error_reporter.py  ch. 4  — error reporting, shared by every phase
    scanner.py         ch. 4  — characters -> tokens
    lox.py             ch. 4  — entry point: run a file, or a REPL

    ast.py             ch. 5  — expression nodes
    parser.py          ch. 6  — tokens -> AST
    interpreter.py     ch. 7  — walk the AST and evaluate
    environment.py     ch. 8  — variable storage and scope
    resolver.py        ch. 11 — static resolution pass
"""
