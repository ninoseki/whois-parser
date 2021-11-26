from pyparsing import Regex, White

SPACE_OR_TAB = White(" \t\r")
ANY_CHARACTERS = Regex(".+")
DEILIMITER: str = ":"
