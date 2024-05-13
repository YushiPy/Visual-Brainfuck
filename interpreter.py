
from typing import Callable
from tape import Tape

TOKEN_MAP: dict[str, int] = {a : i for i, a in enumerate("><+-.,[]")}

class Interpreter:

	tape: Tape
	code: str

	__filtered: list[int]
	__reverse_map: dict[int, int]

	__filtered_index: int

	__converter: list[Callable[[], None]]

	__output: str
	__input: list[int]

	__close_map: dict[int, int]
	__open_map: dict[int, int]

	def __init__(self, code: str) -> None:
		
		self.tape = Tape()
		self.code = code
		
		self.__filtered, self.__reverse_map = self.__get_filtered()

		self.__filtered_index = 0


		self.__converter = [
			self.tape.shift_right,
			self.tape.shift_left,
			self.tape.increase,
			self.tape.decrease,
			self.output,
			self.read,
			self.go_foward,
			self.go_back
		]


		self.__output = ""
		self.__input = []

		self.__close_map = self.__get_map()
		self.__open_map = {b : a for a, b in self.__close_map.items()}


	@property
	def can_run(self) -> bool:
		return self.__filtered_index < len(self.__filtered)


	@property
	def code_index(self) -> int:
		return self.__reverse_map[self.__filtered_index]


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


	def __get_filtered(self) -> tuple[list[int], dict[int, int]]:

		reverse: dict[int, int] = {}
		filtered: list[int] = []

		for i, a in enumerate(self.code):
			
			if a not in TOKEN_MAP:
				continue

			token: int = TOKEN_MAP[a]

			filtered.append(token)
			reverse[token] = i

		return filtered, reverse


	def output(self) -> None:
		self.__output += chr(self.tape.byte)
	

	def read(self) -> None:
		self.tape.byte = self.__input.pop()
	

	def go_foward(self) -> None:

		if not self.tape.byte:
			self.__filtered_index = self.__open_map[self.__filtered_index]


	def go_back(self) -> None:
	
		open_index: int = self.__close_map[self.__filtered_index]

		if not self.tape.byte:
			return

		self.__filtered_index = open_index


	def set_input(self, _input: str) -> None:

		self.__input = list(map(ord, reversed(_input)))

		if self.__input[0] != 0:
			self.__input = [0] + self.__input


	def run(self, _input: str = "") -> str:

		self.reset()
		self.set_input(_input)

		while self.can_run:
			self.run_command()

		return self.__output


	def run_command(self) -> None:
		
		if not self.can_run:
			return

		self.__converter[self.__filtered[self.__filtered_index]]()

		self.__filtered_index += 1


	def reset(self) -> None:

		self.tape.reset()
		self.__filtered_index = 0

		self.__output = ""
		self.__input = []
