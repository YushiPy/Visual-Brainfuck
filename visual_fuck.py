
from pygame import Surface
from game import Game

class Gameplay(Game):

	def __init__(self, __tps: int | float = 125, __flags: int = 0) -> None:
		super().__init__(__tps, __flags)


	def draw(self, surface: Surface) -> Surface | None:
		return surface
	

	def fixed_update(self) -> None | bool:
		return None
	

	def update(self) -> None | bool:
		return None

	def start(self) -> None:
		pass

	def end(self) -> None:
		pass

	def set_base_surface(self, surface: Surface) -> Surface | None:
		pass


def main() -> None:
	print(Gameplay().run().get_info())


if __name__ == "__main__":
	main()
