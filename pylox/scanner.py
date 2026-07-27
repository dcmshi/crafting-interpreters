"""The Scanner — Chapter 4.4 through 4.7.

Turns a flat string of characters into a list of Tokens. Whitespace and comments are
consumed and discarded; the parser never sees them.

The whole structure is one loop: point `start` at the beginning of a lexeme, consume
characters until you know what it is, emit a token, repeat.
"""

from pylox.error_reporter import ErrorReporter
from pylox.token import Token
from pylox.token_type import TokenType

# TODO(ch4.7): the keyword table — a dict mapping the sixteen reserved words to their
# TokenType. This is the other half of "maximal munch": the scanner consumes a whole
# identifier first, *then* looks the finished text up here. That is why `orchid` scans
# as one IDENTIFIER rather than the keyword `or` followed by `chid`.
KEYWORDS: dict[str, TokenType] = {}


class Scanner:
    def __init__(self, source: str, reporter: ErrorReporter) -> None:
        self.source = source
        self.reporter = reporter
        self.tokens: list[Token] = []

        # Three cursors:
        #   start   — index of the first character of the lexeme being scanned
        #   current — index of the character currently being looked at
        #   line    — which source line `current` is on, for error messages
        self.start = 0
        self.current = 0
        self.line = 1

    # ------------------------------------------------------------------
    # Main loop — ch. 4.4
    # ------------------------------------------------------------------

    def scan_tokens(self) -> list[Token]:
        """Scan the whole source and return the token list."""
        # TODO(ch4.4): loop until at end — each pass sets self.start = self.current,
        # then calls scan_token(). Afterwards append the EOF token (lexeme "", literal
        # None, current line) and return self.tokens.
        raise NotImplementedError

    def scan_token(self) -> None:
        """Scan exactly one token, starting at self.start."""
        # Consume one character and dispatch on it. A `match` statement reads closest
        # to the book's `switch`; an if/elif chain is equally fine.
        #
        # TODO(ch4.5): single-character tokens — ( ) { } , . - + ; *
        #
        # TODO(ch4.5): one-or-two-character operators — ! = < >
        #   Each checks whether '=' follows. That check is self.match('=').
        #
        # TODO(ch4.5): '/' — the interesting case, since '/' and '//' share a first
        #   character. If a second '/' follows it is a comment: consume to end of line
        #   and emit NO token. Otherwise emit SLASH.
        #   Careful: consume *up to* the newline, not through it, so the newline case
        #   below still gets to bump the line counter.
        #
        # TODO(ch4.5): whitespace — ' ', '\r', '\t' are skipped entirely.
        #   '\n' increments self.line and is otherwise skipped.
        #
        # TODO(ch4.6): '"' starts a string literal -> self.string()
        #
        # TODO(ch4.6): a digit starts a number literal -> self.number()
        #   Numbers are checked here rather than listing ten cases.
        #
        # TODO(ch4.7): a letter or '_' starts an identifier -> self.identifier()
        #
        # TODO(ch4.5): anything else — report an error via self.reporter, but KEEP
        #   SCANNING. Reporting every bad character in one pass is much friendlier
        #   than stopping at the first. The reporter's had_error flag is what
        #   actually prevents the bad program from running.
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Longer lexemes — ch. 4.6 and 4.7
    # ------------------------------------------------------------------

    def string(self) -> None:
        """Scan a string literal. The opening quote is already consumed."""
        # TODO(ch4.6): consume until the closing '"' or end of input.
        #   - Lox strings MAY span multiple lines, so bump self.line when you pass a
        #     '\n' inside the loop, or your later error messages will be off.
        #   - Lox has NO escape sequences. \n in source is a backslash and an n.
        #   - Running out of input first is an "Unterminated string." error — report
        #     it and return, don't fall through.
        #   - Consume the closing quote, then strip BOTH quotes for the literal value.
        raise NotImplementedError

    def number(self) -> None:
        """Scan a number literal. Lox numbers are all floats — there is no int type."""
        # TODO(ch4.6): consume digits; then accept a fractional part ONLY if the '.'
        # is followed by another digit — that check is what needs peek_next(), and it
        # is the only place in the whole scanner needing two characters of lookahead.
        #
        # So `.5` and `5.` are deliberately NOT valid literals. The book's reason: it
        # leaves room to later add method calls on numbers, like `123.sqrt()`.
        #
        # Convert the lexeme with float().
        raise NotImplementedError

    def identifier(self) -> None:
        """Scan an identifier, which may turn out to be a keyword."""
        # TODO(ch4.7): consume while alphanumeric, then look the finished text up in
        # KEYWORDS. A hit means that keyword's TokenType; a miss means IDENTIFIER.
        #
        # Scanning the whole thing before looking it up is the point — see the note
        # on maximal munch above KEYWORDS.
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Character helpers
    # ------------------------------------------------------------------

    def is_at_end(self) -> bool:
        """Has `current` run past the end of the source?"""
        # TODO(ch4.4)
        raise NotImplementedError

    def advance(self) -> str:
        """Consume the current character and return it."""
        # TODO(ch4.5): return source[current], then increment current.
        raise NotImplementedError

    def match(self, expected: str) -> bool:
        """Consume the current character only if it is `expected`.

        This is the two-character-operator trick: a conditional advance.
        """
        # TODO(ch4.5): False at end of input, False on mismatch (consuming nothing),
        # True and consume on a match.
        raise NotImplementedError

    def peek(self) -> str:
        """Look at the current character WITHOUT consuming it. One char of lookahead."""
        # TODO(ch4.5): return "\0" at end of input so callers never index out of range.
        raise NotImplementedError

    def peek_next(self) -> str:
        """Look one character past `current`. The second char of lookahead."""
        # TODO(ch4.6): same sentinel rule. Only number() needs this.
        raise NotImplementedError

    def add_token(self, type: TokenType, literal: object | None = None) -> None:
        """Emit a token for the lexeme spanning start..current."""
        # TODO(ch4.5): slice source[start:current] for the lexeme, build a Token,
        # append it. The default literal of None covers every non-literal token, which
        # is most of them.
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Character classification
    # ------------------------------------------------------------------
    #
    # Write these by hand. Do NOT use str.isdigit() / str.isalpha() / str.isalnum():
    # they are Unicode-aware, so "²".isdigit() and "٣".isdigit() are both True, and
    # isalpha() accepts every accented and non-Latin letter. Lox is ASCII-only, and
    # matching the book exactly here saves confusing divergence later.

    @staticmethod
    def is_digit(c: str) -> bool:
        # TODO(ch4.6): '0' through '9' only.
        raise NotImplementedError

    @staticmethod
    def is_alpha(c: str) -> bool:
        # TODO(ch4.7): a-z, A-Z, and '_'. Underscore counts as a letter for
        # identifiers even though it obviously isn't one.
        raise NotImplementedError

    @staticmethod
    def is_alpha_numeric(c: str) -> bool:
        # TODO(ch4.7)
        raise NotImplementedError
