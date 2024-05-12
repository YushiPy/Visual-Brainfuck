
DEFAULT_SIZE: int = 30_000

class Tape(list[int]):

	def __init__(self, size: int = DEFAULT_SIZE) -> None:
		super().__init__([0] * size)

		self.__pointer: int = 0


	@property
	def pointer(self) -> int:
		return self.__pointer


	@pointer.setter
	def pointer(self, value: int) -> None:
		
		if value < 0:
			raise ValueError(f"New pointer value is negative; {value} < 0.")

		self.__pointer = value


	@property
	def byte(self) -> int:
		return self[self.pointer]
	

	@byte.setter
	def byte(self, value: int) -> None:
		self[self.pointer] = value & 0xff


	def shift_by(self, ammount: int) -> None:
		self.pointer += ammount
	

	def shift_right(self) -> None:
		self.shift_by(1)
	

	def shift_left(self) -> None:
		self.shift_by(-1)
	

	def increase_by(self, ammount: int) -> None:
		self.byte += ammount
	

	def increase(self) -> None:
		self.increase_by(1)
	

	def decrease(self) -> None:
		self.increase_by(-1)


	def reset(self) -> None:
		
		self.pointer = 0

		for i in range(len(self)):
			self[i] = 0
