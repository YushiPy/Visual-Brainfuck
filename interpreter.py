
from typing import Callable
from tape import Tape

TOKEN_MAP: dict[str, int] = {a : i for i, a in enumerate("><+-.,[]")}

class Interpreter:

	def __init__(self, code: str) -> None:
		
		self.tape: Tape = Tape()

		self.code: str = code
		self.filtered: list[int] = [TOKEN_MAP[i] for i in self.code if i in TOKEN_MAP]

		self.converter: list[Callable[[], None]] = [
			self.tape.shift_right,
			self.tape.shift_left,
			self.tape.increase,
			self.tape.decrease,
			self.output,
			self.read,
		]

		self.__output: str = ""
		self.__input: list[int] = []


	def __get_map(self) -> dict[int, int]:

		queue: list[int] = []
		result: dict[int, int] = {}

		__open_brace: int = TOKEN_MAP['[']
		__close_brace: int = TOKEN_MAP[']']

		for i, a in enumerate(self.filtered):
			
			if a == __open_brace:
				queue.append(i)
			
			elif a == __close_brace:
				result[i] = queue.pop()
				
		return result


	def output(self) -> None:
		self.__output += chr(self.tape.byte)
	

	def read(self) -> None:
		self.tape.byte = self.__input.pop()
	


