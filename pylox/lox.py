"""Entry point — Chapter 4.1, "The Interpreter Framework".

Three modes:
    pylox            -> REPL
    pylox script.lox -> run that file
    pylox a b c      -> usage error
"""

import sys

from pylox.error_reporter import ErrorReporter
from pylox.scanner import Scanner

# Exit codes from UNIX's sysexits.h. Arbitrary, but conventional, and the book's own
# test suite checks for them.
EX_USAGE = 64  # bad command line
EX_DATAERR = 65  # the source code was bad (scan or parse error)
EX_SOFTWARE = 70  # runtime error — not used until ch. 7


def main(argv: list[str] | None = None) -> int:
    """Dispatch on argument count. Returns the process exit code."""
    args = sys.argv[1:] if argv is None else argv
    # TODO(ch4.1): >1 arg  -> print "Usage: pylox [script]" to stderr, return EX_USAGE
    #              ==1 arg -> run_file(args[0])
    #              ==0     -> run_prompt()
    raise NotImplementedError


def run_file(path: str) -> int:
    """Read a whole file and run it."""
    # TODO(ch4.1): read the file as text with an explicit encoding, run it, and
    # return EX_DATAERR if the reporter saw an error — otherwise 0.
    #
    # A bad path should print a clean message rather than dumping a traceback.
    raise NotImplementedError


def run_prompt() -> int:
    """Read-eval-print loop."""
    # TODO(ch4.1): loop forever: print the "> " prompt, read a line, run it.
    #
    # Two things the book's Java version gets for free that Python does not:
    #   - Java's readLine() returns null at end of input; Python's input() raises
    #     EOFError. Catch it to exit cleanly on Ctrl-Z (Windows) or Ctrl-D (Unix).
    #     Catching KeyboardInterrupt is worth doing too.
    #   - Reset the reporter after each line, or one typo poisons the whole session.
    raise NotImplementedError


def run(source: str, reporter: ErrorReporter) -> None:
    """Scan `source` and, for now, just print the tokens.

    This is the seam every later chapter widens: ch. 6 adds a parser here, ch. 7 an
    interpreter. For chapter 4 it stops at the token dump.
    """
    # TODO(ch4.1): build a Scanner, scan_tokens(), print each token.
    #
    # Then bail if reporter.had_error — never go on to execute a program that had a
    # static error. Right now there is nothing to bail out of, but wiring the check
    # in now means ch. 6 onward is already correct.
    raise NotImplementedError
