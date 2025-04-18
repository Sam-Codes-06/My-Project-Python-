import pygame, sys
pygame.init()
class Button:
	def __init__(self,text,width,height,pos):
		#Core attributes
		self.text = text
		self.pressed = False
		self.original_y_pos = pos[1]
		self.status = None
		self.elevation = 3
		# top rectangle
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = (244, 120, 20)

		# bottom rectangle
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'
		#text
		self.text_surf = gui_font.render(text,True,'#000000')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self, screen):
		self.surf = screen

		if self.text == 'PLAY':
			pygame.draw.rect(screen, self.top_color, self.top_rect)
			screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))
		if self.text == 'EXIT':
			self.top_color = (20, 120, 220)
			pygame.draw.rect(screen, self.top_color, self.top_rect)
			screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))
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
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				if self.pressed == True:
					self.pressed = False
gui_font = pygame.font.Font(None, 78)