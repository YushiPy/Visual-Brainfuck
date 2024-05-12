
from enum import Enum

class Tokens:

	RIGHT: int = 0
	LEFT: int = 1
	INCREASE: int = 2
	DECREASE: int = 3
	OUTPUT: int = 4
	READ: int = 5
	OPEN_WHILE: int = 6
	CLOSE_WHILE: int = 7

	TOKEN_MAP: dict[str, int] = {
		'>': RIGHT,
		'<': LEFT,
		'+': INCREASE,
		'-': DECREASE,
		'.': OUTPUT,
		',': READ,
		'[': OPEN_WHILE,
		']': CLOSE_WHILE
	}


class Interpreter:

	def __init__(self, code: str) -> None:
		
		self.code: str = code
		self.filtered: list[int] = []
