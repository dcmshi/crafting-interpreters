"""The Token record — Chapter 4.2, "Lexemes and Tokens".

Note: this module is named `token`, which is also a stdlib module name. That is safe
here because Python 3 uses absolute imports, so `pylox.token` and the stdlib `token`
never collide — but don't `import token` from inside this package expecting either one.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    """A lexeme plus everything the scanner worked out about it.

    The distinction worth holding onto:
      - `lexeme` is the raw substring of source text, exactly as written.
      - `literal` is the *converted runtime value*, and only literals have one.
        The characters `123` become the float 123.0; the characters `"hi"` become
        the string hi, with the quotes stripped. Everything downstream gets real
        Python values, never text it has to re-parse.
    """

    # TODO(ch4.2): four fields.
    #   type    — a TokenType
    #   lexeme  — the raw source substring (str)
    #   literal — the converted value for STRING/NUMBER, otherwise None.
    #             Type it as `object | None`; Lox literals can be str or float.
    #   line    — the line it appeared on (int)
    #
    # The book stores only a line number for location. An aside notes you could
    # store a source offset and length instead for much better error messages.
    # Staying with the book here keeps the error-reporting code simple.

    def __str__(self) -> str:
        # TODO(ch4.2): "<type> <lexeme> <literal>".
        # Dumping tokens is this chapter's only visible output, so make it readable.
        raise NotImplementedError
