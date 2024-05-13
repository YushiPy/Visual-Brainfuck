
from abc import ABC, abstractmethod
from typing import Self

import pygame

pygame.init()

PORT_WIDTH: int = 1512
PORT_HEIGHT: int = 945

PORT_CENTERX: int = PORT_WIDTH // 2
PORT_CENTERY: int = PORT_HEIGHT // 2

PORT_SIZE: tuple[int, int] = PORT_WIDTH, PORT_HEIGHT
PORT_CENTER: tuple[int, int] = PORT_CENTERX, PORT_CENTERY

clock = pygame.time.Clock()

# Flags

EVENTS_IN_FIXED: int = 1 << 0
SAVE_SURFACE: int = 1 << 1
USE_GLOBAL_DISPLAY: int = 1 << 2
START_DISPLAY: int = 1 << 3

class Game(ABC):
	
	surface: pygame.Surface

	down_keys: "EventHolder" # Keys pressed down at frame
	up_keys: "EventHolder" # Keys released on frame
	events: "EventHolder" # Events on frame
	held_keys: "EventHolder" # Keys held at frame

	time_step: int | float # Time between each fixed update (ms)

	fps_tracker: int # Render Loops ran
	game_loop_tracker: int # Game Loops ran

	start_time: int # Global start time (ms)
	end_time: int # Global end time (ms)
	render_delta_time: int # Time since last render call (ms)

	__global_display: pygame.Surface | None = None

	def __init__(self, __tps: int | float = 125, __flags: int = 0) -> None:

		self.__set_flags(__flags)

		if self.__START_DISPLAY: 
			Game.start_display()

		self.down_keys = EventHolder()
		self.up_keys = EventHolder()
		self.events = EventHolder()
		self.held_keys = EventHolder()

		self.__base_surface: pygame.Surface | None = None
		
		self.surface = self.__display if self.__USE_GLOBAL_DISPLAY else pygame.Surface((PORT_WIDTH, PORT_HEIGHT))

		self.time_step = 1000 / __tps if 1000 % __tps else 1000 // __tps

		self.__accumulator: int | float = 0

		self.fps_tracker = 0
		self.game_loop_tracker = 0

		self.__tick_times: list[int] = []

		self.__run_game: bool = True

	@property
	def __display(self) -> pygame.Surface:
		
		if Game.__global_display is not None: 
			return Game.__global_display
		
		Game.__global_display = pygame.display.set_mode((PORT_WIDTH, PORT_HEIGHT), pygame.FULLSCREEN)
		
		return Game.__global_display
	
	
	@property
	def base_surface(self) -> pygame.Surface | None:
		
		if self.__base_surface is not None: 
			return self.__base_surface
		
		self.__base_surface = self.set_base_surface(pygame.Surface((PORT_WIDTH, PORT_HEIGHT)))

		return self.__base_surface
	

	def __set_flags(self, flags: int) -> None:

		self.__EVENTS_IN_FIXED: bool = bool(flags & EVENTS_IN_FIXED)
		self.__SAVE_SURFACE: bool = bool(flags & SAVE_SURFACE)
		self.__USE_GLOBAL_DISPLAY: bool = bool(flags & USE_GLOBAL_DISPLAY)
		self.__START_DISPLAY: bool = bool(flags & START_DISPLAY)


	@abstractmethod
	def set_base_surface(self, surface: pygame.Surface) -> pygame.Surface | None: ...

	@abstractmethod
	def draw(self, surface: pygame.Surface) -> pygame.Surface | None: ...

	@abstractmethod
	def fixed_update(self) -> None | bool: ...

	@abstractmethod
	def update(self) -> None | bool: ...

	def __rendering_update(self) -> None:

		if not self.__SAVE_SURFACE:

			base: pygame.Surface

			if self.base_surface is None:
				base = pygame.Surface((PORT_WIDTH, PORT_HEIGHT))
			else:
				base = self.base_surface.copy()

			if self.__USE_GLOBAL_DISPLAY:
				self.__display.blit(base, (0, 0))
			else:
				self.surface.blit(base, (0, 0))
			
		self.draw(self.__display if self.__USE_GLOBAL_DISPLAY else self.surface)

		if not self.__USE_GLOBAL_DISPLAY: 
			self.__display.blit(self.surface, (0, 0))
		
		pygame.display.flip()

	@abstractmethod
	def start(self) -> None: ...

	@abstractmethod
	def end(self) -> None: ...


	def run(self) -> Self:

		self.start()
		   
		if self.__SAVE_SURFACE and self.base_surface:
			self.surface.blit(self.base_surface, (0, 0))
		
		
		self.start_time = pygame.time.get_ticks()

		__start: int = self.start_time

		while self.__run_game:

			self.render_delta_time = pygame.time.get_ticks() - self.start_time
			
			self.__tick_times.append(__start)
			__start = self.__loop(__start)
			
			
		self.end_time = __start

		self.end()

		return self
	

	def __loop(self, __start: int) -> int:
		
		if not self.__EVENTS_IN_FIXED: 
			self.__manage_events()

		while self.__accumulator >= self.time_step:
		
			self.game_loop_tracker += 1
			self.__accumulator -= self.time_step
		
			if self.__EVENTS_IN_FIXED: 
				self.__manage_events()
			
			if self.fixed_update() is not None: 
				self.__run_game = False


		if self.update() is not None: 
			self.__run_game = False

		self.fps_tracker += 1
		self.__rendering_update()

		__end: int = pygame.time.get_ticks()

		self.render_delta_time = __end - __start
		self.__accumulator += self.render_delta_time

		return __end


	def __manage_events(self) -> tuple['EventHolder', 'EventHolder', 'EventHolder', 'EventHolder']:

		game_events: list[pygame.event.Event] = pygame.event.get()

		self.down_keys.clear()
		self.up_keys.clear()
		self.events.clear()

		for i in game_events:
			
			if i.type == pygame.KEYDOWN: 
				self.down_keys.add(i.key)
			
			elif i.type == pygame.KEYUP: 
				self.up_keys.add(i.key)
			
			else: 
				self.events.add(i.type)

		if pygame.QUIT in self.events: 
			self.__run_game = False

		if pygame.K_ESCAPE in self.down_keys: 
			self.__run_game = False

		self.held_keys.update(self.down_keys)
		self.held_keys.difference_update(self.up_keys)

		return self.down_keys, self.up_keys, self.held_keys, self.events


	def get_info(self, precision: int = 3, stringify: bool = True) -> str | tuple[float, float]:

		if not self.fps_tracker or not self.game_loop_tracker:

			if not stringify: 
				return 0, 0

			return f"The game apparently hasn't been ran yet, " + \
					"rendering it impossible to determine any information about its behavior"

		fps: float = 1000 * self.fps_tracker / (self.end_time - self.start_time)
		game_fps: float = 1000 * self.game_loop_tracker / (self.end_time - self.start_time)

		if not stringify: 
			return fps, game_fps

		fps, game_fps = round(fps, precision), round(game_fps, precision)

		expected_fps: float = round(1000 / self.time_step, precision)

		message_1: str = f'The game ran, on average, at {fps} fps'
		message_2: str = f'The game loop was called {game_fps} times per seconds'
		message_3: str = f'Expected: {expected_fps}, Difference: {round(game_fps - expected_fps, 3)}'

		return f'{message_1}\n{message_2}\n{message_3}'
	
	
	@staticmethod
	def start_display() -> None:
		Game.__global_display = pygame.display.set_mode((PORT_WIDTH, PORT_HEIGHT), pygame.FULLSCREEN)
	

class EventHolder(set[int]):
	def __getitem__(self, key: int) -> bool:
		return key in self