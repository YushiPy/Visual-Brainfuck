
import pygame as pg

FontInfo = tuple[str, int, bool, bool]

__saved_fonts: dict[FontInfo, pg.font.Font]

class Text:

	string: str
	font: pg.font.Font

	surface: pg.Surface
	rect: pg.Rect

	@staticmethod
	def get_font(name: str = "ヒラキノ角コシックw0", size: int = 30, 
			  bold: bool = False, italic: bool = False) -> pg.font.Font:

		info: FontInfo = (name, size, bold, italic)

		if info in __saved_fonts:
			return __saved_fonts[info]

		__saved_fonts[info] = pg.font.SysFont(name, size, bold, italic)

		return __saved_fonts[info]

	
	def __init__(self, 
			  string: str, 
			  font: FontInfo | pg.font.Font, 
			  color: tuple[int, int, int] = (255, 255, 255)) -> None:
		
		self.string = string
		self.font = font if isinstance(font, pg.font.Font) else Text.get_font(*font)
		self.color = color

		self.surface = self.font.render(self.string, False, self.color)
		self.rect = self.surface.get_rect()

	def draw(self, surface: pg.Surface) -> None:
		surface.blit(self.surface, self.rect)
