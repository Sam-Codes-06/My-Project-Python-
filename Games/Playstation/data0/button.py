import pygame, sys
pygame.init()
settings = pygame.image.load('data0/settings.png')
play = pygame.image.load('data0/play.png')
exit = pygame.image.load('data0/exit.png')
class Button:
	def __init__(self,text,width,height,pos,elevation):
		#Core attributes
		self.text = text
		self.pressed = False
		self.original_y_pos = pos[1]
		self.status = None
		self.elevation = 3
		# top rectangle
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#475F77'

		# bottom rectangle
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'
		#text
		self.text_surf = gui_font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self, screen):
		self.surf = screen

		if self.text == 'PLAY':
			pygame.draw.rect(screen, self.top_color, self.top_rect)
			screen.blit(play, (self.top_rect.x + 193, self.top_rect.y +6))
			screen.blit(self.text_surf, (self.text_rect.x + 30, self.text_rect.y))
		if self.text == 'EXIT':
			pygame.draw.rect(screen, self.top_color, self.top_rect)
			screen.blit(exit, (self.top_rect.x + 18, self.top_rect.y + 14))
			screen.blit(self.text_surf, (self.text_rect.x + 14, self.text_rect.y))
		if self.text == '':
			pygame.draw.rect(screen, self.top_color, self.top_rect)
			screen.blit(settings, (self.top_rect.x + 10, self.top_rect.y + 10))
		if self.text == ' ':
			self.top_color = (74, 196, 251)
			pygame.draw.rect(screen, self.top_color, self.top_rect)
			self.top_color = '#5b7bf9'
		if self.text == 'Exit to Desktop':
			self.top_color = (255, 255, 255)
			screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))
			pygame.draw.rect(screen, self.top_color, self.top_rect, self.elevation)
		if self.text == 'Exit to Main-Menu':
			self.top_color = (255, 255, 255)
			screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))
			pygame.draw.rect(screen, self.top_color, self.top_rect, self.elevation)
		if self.text == 'Cancel':
			self.top_color = (255, 255, 255)
			screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))
			pygame.draw.rect(screen, self.top_color, self.top_rect, self.elevation)

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.elevation = 1
			self.top_color = '#7494da'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				if self.pressed == True:
					self.pressed = False
					if self.text == 'PLAY':
						self.status = 'play'
					elif self.text == 'EXIT':
						self.status = 'exit'
					elif self.text == '':
						self.status = 'settings'
					elif self.text == 'Cancel':
						self.status = 'cancel'
					elif self.text == 'Exit to Desktop':
						self.status = 'exit_whole'
					elif self.text == 'Exit to Main-Menu':
						self.status = 'exit_snake_game'

		else:
			self.elevation = 3
			self.top_color = '#5b7bf9'

gui_font = pygame.font.Font(None,48)