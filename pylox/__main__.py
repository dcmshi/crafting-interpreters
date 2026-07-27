"""Makes `python -m pylox` work.

    python -m pylox                       # REPL
    python -m pylox examples/07-expressions.lox
"""

import sys

from pylox.lox import main

if __name__ == "__main__":
    sys.exit(main())
