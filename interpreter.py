
from typing import Callable
from tape import Tape

TOKEN_MAP: dict[str, int] = {a : i for i, a in enumerate("><+-.,[]")}

class Interpreter:

	def __init__(self, code: str) -> None:
		
		self.tape: Tape = Tape()

		self.code: str = code
		self.__filtered: list[int] = [TOKEN_MAP[i] for i in self.code if i in TOKEN_MAP]

		self.index: int = 0

		self.converter: list[Callable[[], None]] = [
			self.tape.shift_right,
			self.tape.shift_left,
			self.tape.increase,
			self.tape.decrease,
			self.output,
			self.read,
			lambda: None, # Does nothing on open brace
			self.go_back
		]

		self.__output: str = ""
		self.__input: list[int] = []

		self.__brace_map: dict[int, int] = self.__get_map()


	def __get_map(self) -> dict[int, int]:

		queue: list[int] = []
		result: dict[int, int] = {}

		__open_brace: int = TOKEN_MAP['[']
		__close_brace: int = TOKEN_MAP[']']

		for i, a in enumerate(self.__filtered):
			
			if a == __open_brace:
				queue.append(i)
			
			elif a == __close_brace:
				result[i] = queue.pop()
				
		return result


	def output(self) -> None:
		self.__output += chr(self.tape.byte)
	

	def read(self) -> None:
		self.tape.byte = self.__input.pop()
	

	def go_back(self) -> None:
	
		open_index: int = self.__brace_map[self.index]

		if not self.tape.byte:
			return

		self.index = open_index


	def run(self, _input: str = "") -> str:

		self.tape.reset()
		self.index = 0

		self.__output = ""
		self.__input = [ord(i) for i in _input]

		max_index: int = len(self.__filtered)

		while self.index < max_index:
			self.run_command()

		return self.__output


	def run_command(self) -> None:
		
		self.converter[self.__filtered[self.index]]()

		self.index += 1
