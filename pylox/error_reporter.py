"""Error reporting — Chapter 4.1.1, "Error handling".

The book hangs `error()` and a `hadError` flag off the main Lox class as statics, and
Nystrom notes in an aside that a separate reporter passed into each phase would be
better engineering. We take the aside's advice, for a Python-specific reason: a
module-level global here would mean scanner.py imports lox.py while lox.py imports
scanner.py. An object threaded through as a constructor argument sidesteps that
entirely, and chapters 6, 7 and 11 all want to report errors too.
"""


class ErrorReporter:
    """Collects and prints errors, and remembers whether any occurred."""

    def __init__(self) -> None:
        # TODO(ch4.1.1): a `had_error` flag, initially False.
        raise NotImplementedError

    def error(self, line: int, message: str) -> None:
        """Report an error at a line. Called by the scanner (and later the parser)."""
        # TODO(ch4.1.1): delegate to report() with an empty `where`.
        raise NotImplementedError

    def report(self, line: int, where: str, message: str) -> None:
        """Print `[line N] Error<where>: message` and set the error flag.

        Write to **stderr**, not stdout — a token dump or a program's own output
        should stay separable from diagnostics when piping.
        """
        # TODO(ch4.1.1): print to sys.stderr, then set had_error = True.
        raise NotImplementedError

    def reset(self) -> None:
        """Clear the flag. The REPL calls this after each line.

        Without it, one typo would poison every later line of the session: the flag
        would stay set and nothing would ever run again.
        """
        # TODO(ch4.1.1)
        raise NotImplementedError
