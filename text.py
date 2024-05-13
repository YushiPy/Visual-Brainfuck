
import pygame as pg

pg.init()

FontInfo = tuple[str, int, bool, bool]

DEFAULT_FONT: FontInfo = "ヒラキノ角コシックw0", 30, False, False

__saved_fonts: dict[FontInfo, pg.font.Font] = {}

def get_font(name: str | None = None, size: int | None = None, 
			bold: bool | None = None, italic: bool | None = None) -> pg.font.Font:

	info: FontInfo = (
		name if name is not None else DEFAULT_FONT[0], 
		size if size is not None else DEFAULT_FONT[1], 
		bold if bold is not None else DEFAULT_FONT[2], 
		italic if italic is not None else DEFAULT_FONT[3]
		)

	if info in __saved_fonts:
		return __saved_fonts[info]

	__saved_fonts[info] = pg.font.SysFont(*info)

	return __saved_fonts[info]

class Text:

	string: str
	font: pg.font.Font
	color: tuple[int, int, int]

	surface: pg.Surface
	rect: pg.Rect
	
	def __init__(self, 
			  string: str, 
			  font: FontInfo | pg.font.Font, 
			  color: tuple[int, int, int] = (255, 255, 255)) -> None:
		
		self.string = string
		self.color = color
		
		self.font = font if isinstance(font, pg.font.Font) else get_font(*font)

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
