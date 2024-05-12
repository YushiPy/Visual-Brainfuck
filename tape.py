
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
