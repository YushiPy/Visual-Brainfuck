
import pygame as pg

pg.init()

FontInfo = tuple[str, int, bool, bool]

class Text:

	string: str
	font: pg.font.Font
	color: tuple[int, int, int]

	surface: pg.Surface
	rect: pg.Rect
	
	__saved_fonts: dict[FontInfo, pg.font.Font] = {}

	@staticmethod
	def get_font(name: str = "ヒラキノ角コシックw0", size: int = 30, 
			  bold: bool = False, italic: bool = False) -> pg.font.Font:

		info: FontInfo = (name, size, bold, italic)

		if info in Text.__saved_fonts:
			return Text.__saved_fonts[info]

		Text.__saved_fonts[info] = pg.font.SysFont(name, size, bold, italic)

		return Text.__saved_fonts[info]

	
	def __init__(self, 
			  string: str, 
			  font: FontInfo | pg.font.Font, 
			  color: tuple[int, int, int] = (255, 255, 255)) -> None:
		
		self.string = string
		self.color = color
		
		self.font = font if isinstance(font, pg.font.Font) else Text.get_font(*font)

		self.surface = self.font.render(self.string, False, self.color)
		self.rect = self.surface.get_rect()


	def center_by_index(self, index: int, position: tuple[int, int]) -> None:

		left: int = self.font.size(self.string[:index])[0]
		char: int = self.font.size(self.string[index])[0]

		self.rect.x = position[0]
		self.rect.centery = position[1]

		self.rect.x -= left + char // 2


	def draw(self, surface: pg.Surface) -> None:
		surface.blit(self.surface, self.rect)


	def __str__(self) -> str:
		return f"<Text: '{self.string}'; {self.rect}>"
