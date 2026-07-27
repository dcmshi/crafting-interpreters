"""The TokenType enum — Chapter 4.2, "Lexemes and Tokens"."""

from enum import Enum, auto


class TokenType(Enum):
    """Every kind of token the scanner can produce.

    Using `auto()` for the values: nothing downstream cares what the numbers are,
    only that members compare equal to themselves.
    """

    # TODO(ch4.2): Single-character tokens.
    #   ( ) { } , . - + ; / *
    #   Eleven of them. Note SLASH lives here even though scanning it needs a
    #   lookahead to rule out a `//` comment.

    # TODO(ch4.2): One- or two-character tokens.
    #   ! and !=, = and ==, > and >=, < and <=
    #   Eight members: each of the four characters gets a bare form and an
    #   ..._EQUAL form.

    # TODO(ch4.2): Literals.
    #   IDENTIFIER, STRING, NUMBER

    # TODO(ch4.2): Keywords.
    #   and class else false fun for if nil or print return super this true var while
    #   Sixteen of them. These are also the values of the keyword table in
    #   scanner.py — keep the two in sync.

    # TODO(ch4.2): EOF
    #   Appended once at the end of the token list. The parser relies on it as a
    #   sentinel so it never has to bounds-check while looking ahead.

    pass  # remove once the first member is added
