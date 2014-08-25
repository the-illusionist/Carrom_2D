import pygame, sys, time
from pygame.locals import *
import math
from numpy import *

friction = 0.16
wid = 700
hitstrength=0.45

RED=(255,0,0)
BLUE=(0,0,255)
WOODEN = (192, 64, 0)#used nowhere
YELLOW=(245,190,154)#Center Circle
BLACK = (0,0,0)
PINK = (242,4,105)
CREAM = (238,199,154)#Background color, peg's color
GREEN = (0,170,0)# Valid region of dragging mouse
GREY=(40,40,40)

strikerrad = (wid*3/100 - 1)
Pegrad=(wid/50)
border = Pegrad*9/5
pi=3.14
clock = pygame.time.Clock()
mod = lambda v: math.sqrt(v[0] * v[0] + v[1] * v[1])


class Peg(pygame.sprite.Sprite):
	def __init__(self,color,radius,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([2*radius, 2*radius])
		self.image.fill(YELLOW)
		self.image.set_colorkey(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.x = x-radius
		self.rect.y = y-radius		
		if color==BLACK:
			self.isWhite = False
			self.isQueen = False
			self.isBLACK = True
			for i in range(radius):
				pygame.draw.ellipse(self.image, (5*i, 5*i, 5*i), [i, i, 2*radius-2*i, 2*radius-2*i])
		elif color==CREAM:
			self.isWhite = True
			self.isQueen = False
			self.isBLACK = False
			for i in range(radius):
				pygame.draw.ellipse(self.image, (245-radius*5+5*i, 245-radius*5+5*i, 245-radius*5+5*i), [i, i, 2*radius-2*i, 2*radius-2*i])
		elif color==PINK:
			self.isWhite = False
			self.isQueen = True
			self.isBLACK = False
			for i in range(radius):
				pygame.draw.ellipse(self.image, (250-i, 2*i, 85+i), [i, i, 2*radius-2*i, 2*radius-2*i])
			pygame.draw.circle(self.image, BLUE,(radius,radius),radius,2)	
		self.velx=0
		self.vely=0
		self.radius=Pegrad
		self.color=color
		self.collided = False
		self.inhole=False

	def sound(self):
		if self.isWhite or self.isQueen or self.isBLACK :
			pygame.mixer.music.load("inpocket.ogg")
			pygame.mixer.music.play(1, 0.0)
			time.sleep(.12)
			pygame.mixer.music.stop()

	def update(self):
		self.rect.centerx+=self.velx
		self.rect.centery+=self.vely
		if self.rect.y > wid-border-2*Pegrad  :
			self.rect.y = wid-border-2*Pegrad
			self.vely = -1*self.vely
		elif self.rect.y<border:
			self.rect.y=border
			self.vely = -1*self.vely
		if self.rect.x > wid-border-2*Pegrad :
			self.velx = -1*self.velx
		elif self.rect.x<border:
			self.rect.x=border
			self.velx = -1*self.velx
		if mod([self.velx, self.vely])==0:
			self.velx=0
			self.vely=0
		else:
			self.velx = self.velx - friction * self.velx / mod([self.velx, self.vely])
			self.vely = self.vely - friction * self.vely / mod([self.velx, self.vely])
			if abs(self.velx)<friction:
				self.velx=0
			if abs(self.vely)<friction:
				self.vely=0 

class Striker(pygame.sprite.Sprite):
	def __init__(self,color,radius,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([2*radius, 2*radius])
		self.image.fill(YELLOW)
		self.image.set_colorkey(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.x = x-radius
		self.rect.y = y-radius
		pygame.draw.circle(self.image, color,(radius,radius),radius-1)
		self.velx=5
		self.vely=15
		self.radius=strikerrad
		self.state=0
		self.player=1	
		self.player1score=0
		self.player2score=0
	
	def sound(self):
		pygame.mixer.music.load("strikerfoul.mp3")
		pygame.mixer.music.play(1, 0.0)
		time.sleep(.50)
		pygame.mixer.music.stop()

	def update(self):
		pos = pygame.mouse.get_pos()

		if(self.state==1):			
			self.velx=(pos[0]-self.rect.centerx)*-1*hitstrength
			self.vely=(pos[1]-self.rect.centery)*-1*hitstrength
			if self.velx > 20 and self.velx>=abs(self.vely) :
				self.velx=20
				self.vely=(20*self.vely)/self.velx
			elif self.velx < -20 and abs(self.velx)>=abs(self.vely) :
				self.velx=-20
				self.vely=(20*self.vely)/abs(self.velx)
			if self.vely > 20 and self.vely>=abs(self.velx) :
				self.vely=20
				self.velx=(20*self.velx)/self.vely
			elif self.vely < -20 and abs(self.vely)>=abs(self.velx) :
				self.vely=-20
				self.velx=(20*self.velx)/abs(self.vely)

		elif(self.state==2):			
				self.rect.centerx+=self.velx
				self.rect.centery+=self.vely
				if self.rect.y > wid-border-2*strikerrad  :
					self.rect.y = wid-border-2*strikerrad
					self.vely = -1*self.vely
				elif self.rect.y<border:
					self.rect.y=border
					self.vely = -1*self.vely
				if self.rect.x > wid-border-2*strikerrad :
					self.velx = -1*self.velx
				elif self.rect.x<border:
					self.rect.x=border
					self.velx = -1*self.velx
				if mod([self.velx, self.vely])==0:
					self.velx=0
					self.vely=0					
				else:
					self.velx = self.velx - friction * self.velx / mod([self.velx, self.vely])
					self.vely = self.vely - friction * self.vely / mod([self.velx, self.vely])
					if abs(self.velx)<friction:
						self.velx=0
					if abs(self.vely)<friction:
						self.vely=0 


def collideBalls(ball1,ball2):
	c2 = [ball2.rect.centerx, ball2.rect.centery]
	c1 = [ball1.rect.centerx, ball1.rect.centery]
	temp = [(c1[0]-c2[0]),(c1[1]-c2[1])]	
	dist = (ball1.radius+ball2.radius - mod(temp))/2+2
	normal = [(c1[0]-c2[0])/(mod(temp)+.001),(c1[1]-c2[1])/(mod(temp)+.001)]
	tangent = [-normal[1],normal[0]]
	dist_normal = [dist*normal[0], dist*normal[1]]
	ball1.rect.centerx+=dist_normal[0]
	ball1.rect.centery+=dist_normal[1]
	ball2.rect.centerx-=dist_normal[0]
	ball2.rect.centery-dist_normal[1]
	c1 = [ball1.rect.centerx, ball1.rect.centery]
	c2 = [ball2.rect.centerx, ball2.rect.centery]
	ball1vel = [ball1.velx,ball1.vely]
	ball2vel = [ball2.velx,ball2.vely]
	ball1vel_normal = normal[0]*ball1vel[0]+normal[1]*ball1vel[1]
	ball1vel_tangent = tangent[0]*ball1vel[0]+tangent[1]*ball1vel[1]
	ball2vel_normal = normal[0]*ball2vel[0]+normal[1]*ball2vel[1]
	ball2vel_tangent = tangent[0]*ball2vel[0]+tangent[1]*ball2vel[1]
	ball2vel_normal, ball1vel_normal = ball1vel_normal, ball2vel_normal
	normal1 = [ball1vel_normal*normal[0],ball1vel_normal*normal[1]] 
	normal2 = [ball2vel_normal*normal[0],ball2vel_normal*normal[1]]
	tangent1 = [ball1vel_tangent*tangent[0],ball1vel_tangent*tangent[1]] 
	tangent2 = [ball2vel_tangent*tangent[0],ball2vel_tangent*tangent[1]]
	ball1.velx = normal1[0]+tangent1[0]
	ball1.vely = normal1[1]+tangent1[1]
	ball2.velx = normal2[0]+tangent2[0]
	ball2.vely = normal2[1]+tangent2[1]


class CarromBoard():
	def __init__(self, width=wid*4/3, height=wid, caption="Carrom Board"):
		pygame.init()
		self.width, self.height, self.caption = width, height, caption
		self.screen=pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(self.caption)
		self.peg_list=pygame.sprite.Group()
		self.peg_list.add(Peg(PINK, Pegrad-1,25*Pegrad,25*Pegrad))
		self.peg_list.add(Peg(BLACK,Pegrad-1,25*Pegrad,27*Pegrad))
		self.peg_list.add(Peg(CREAM,Pegrad-1,268*Pegrad/10,26*Pegrad))
		self.peg_list.add(Peg(BLACK,Pegrad-1,268*Pegrad/10,24*Pegrad))
		self.peg_list.add(Peg(BLACK,Pegrad-1,232*Pegrad/10,24*Pegrad))
		self.peg_list.add(Peg(CREAM,Pegrad-1,232*Pegrad/10,26*Pegrad))
		self.peg_list.add(Peg(BLACK,Pegrad-1,268*Pegrad/10,28*Pegrad))
		self.peg_list.add(Peg(CREAM,Pegrad-1,25*Pegrad,29*Pegrad))
		self.peg_list.add(Peg(BLACK,Pegrad-1,232*Pegrad/10,28*Pegrad))
		self.peg_list.add(Peg(BLACK,Pegrad-1,268*Pegrad/10,22*Pegrad))
		self.peg_list.add(Peg(CREAM,Pegrad-1,286*Pegrad/10,27*Pegrad))
		self.peg_list.add(Peg(BLACK,Pegrad-1,232*Pegrad/10,22*Pegrad))
		self.peg_list.add(Peg(BLACK,Pegrad-1,286*Pegrad/10,25*Pegrad))
		self.peg_list.add(Peg(BLACK,Pegrad-1,214*Pegrad/10,25*Pegrad))
		self.peg_list.add(Peg(CREAM,Pegrad-1,25*Pegrad,23*Pegrad))
		self.peg_list.add(Peg(CREAM,Pegrad-1,25*Pegrad,21*Pegrad))
		self.peg_list.add(Peg(CREAM,Pegrad-1,214*Pegrad/10,27*Pegrad))		
		self.peg_list.add(Peg(CREAM,Pegrad-1,214*Pegrad/10,23*Pegrad))
		self.peg_list.add(Peg(CREAM,Pegrad-1,286*Pegrad/10,23*Pegrad))
		
		self.striker_list = pygame.sprite.Group()
		self.striker = Striker(BLUE,strikerrad,wid/2,wid-(4*strikerrad))
		self.striker_list.add(self.striker)

		self.draw()

	def draw(self):
		'''
		texture=pygame.image.load('texture.png')
	 	DISPLAYSURF = pygame.display.set_mode((wid,wid), 0, 32)
		DISPLAYSURF.blit(texture, (0,0))
		'''
		self.screen.fill(CREAM)
		pygame.draw.lines(self.screen, BLACK, False, [(8*Pegrad,5*Pegrad),(42*Pegrad,5*Pegrad)],2*Pegrad/10)
		pygame.draw.lines(self.screen, BLACK, False, [(8*Pegrad,7*Pegrad),(42*Pegrad,7*Pegrad)],2*Pegrad/10)
		pygame.draw.lines(self.screen, BLACK, False, [(8*Pegrad,43*Pegrad),(42*Pegrad,43*Pegrad)],2*Pegrad/10)
		pygame.draw.lines(self.screen, BLACK, False, [(8*Pegrad,45*Pegrad),(42*Pegrad,45*Pegrad)],2*Pegrad/10)
		
		pygame.draw.circle(self.screen, BLACK, (8*Pegrad,6*Pegrad), 11*Pegrad/10+2)
		pygame.draw.circle(self.screen, BLACK, (8*Pegrad,44*Pegrad), 11*Pegrad/10+2)
		pygame.draw.circle(self.screen, BLACK, (42*Pegrad,6*Pegrad), 11*Pegrad/10+2)
		pygame.draw.circle(self.screen, BLACK, (42*Pegrad,44*Pegrad), 11*Pegrad/10+2)

		pygame.draw.circle(self.screen, RED, (8*Pegrad,6*Pegrad), 11*Pegrad/10)
		pygame.draw.circle(self.screen, RED, (8*Pegrad,44*Pegrad), 11*Pegrad/10)
		pygame.draw.circle(self.screen, RED, (42*Pegrad,6*Pegrad), 11*Pegrad/10)
		pygame.draw.circle(self.screen, RED, (42*Pegrad,44*Pegrad), 11*Pegrad/10)
		
		pygame.draw.lines(self.screen, BLACK, False, [(5*Pegrad,8*Pegrad),(5*Pegrad,42*Pegrad)],2*Pegrad/10)
		pygame.draw.lines(self.screen, BLACK, False, [(7*Pegrad,8*Pegrad),(7*Pegrad, 42*Pegrad)],2*Pegrad/10)
		pygame.draw.lines(self.screen, BLACK, False, [(45*Pegrad,8*Pegrad),(45*Pegrad,42*Pegrad)],2*Pegrad/10)
		pygame.draw.lines(self.screen, BLACK, False, [(43*Pegrad,8*Pegrad),(43*Pegrad,42*Pegrad)],2*Pegrad/10)

		pygame.draw.circle(self.screen, BLACK, (6*Pegrad,8*Pegrad), 11*Pegrad/10+2)
		pygame.draw.circle(self.screen, BLACK, (6*Pegrad,42*Pegrad), 11*Pegrad/10+2)
		pygame.draw.circle(self.screen, BLACK, (44*Pegrad,8*Pegrad), 11*Pegrad/10+2)
		pygame.draw.circle(self.screen, BLACK, (44*Pegrad,42*Pegrad), 11*Pegrad/10+2)

		pygame.draw.circle(self.screen, RED, (6*Pegrad,8*Pegrad), 11*Pegrad/10)
		pygame.draw.circle(self.screen, RED, (6*Pegrad,42*Pegrad), 11*Pegrad/10)
		pygame.draw.circle(self.screen, RED, (44*Pegrad,8*Pegrad), 11*Pegrad/10)
		pygame.draw.circle(self.screen, RED, (44*Pegrad,42*Pegrad), 11*Pegrad/10)
		#CENTRE CIRCLES
		pygame.draw.circle(self.screen, BLACK, (wid/2,wid/2), 55*Pegrad/10)
		pygame.draw.circle(self.screen, YELLOW, (wid/2,wid/2), 54*Pegrad/10)
		pygame.draw.circle(self.screen, BLACK, (wid/2,wid/2), 48*Pegrad/10)
		pygame.draw.circle(self.screen, YELLOW, (wid/2,wid/2), 47*Pegrad/10)
		pygame.draw.circle(self.screen, BLACK, (wid/2,wid/2), Pegrad)
		pygame.draw.circle(self.screen, YELLOW, (wid/2,wid/2), Pegrad-2)
		
		#POCKETS
		pygame.draw.circle(self.screen, GREEN, (27*Pegrad/10,27*Pegrad/10), 25*Pegrad/10+2)
		pygame.draw.circle(self.screen, GREEN, (473*Pegrad/10,27*Pegrad/10), 25*Pegrad/10+2)
		pygame.draw.circle(self.screen, GREEN, (27*Pegrad/10,473*Pegrad/10), 25*Pegrad/10+2)
		pygame.draw.circle(self.screen, GREEN, (473*Pegrad/10,473*Pegrad/10), 25*Pegrad/10+2)

		pygame.draw.circle(self.screen, GREY, (27*Pegrad/10,27*Pegrad/10), 25*Pegrad/10-2)
		pygame.draw.circle(self.screen, GREY, (473*Pegrad/10,27*Pegrad/10), 25*Pegrad/10-2)
		pygame.draw.circle(self.screen, GREY, (27*Pegrad/10,473*Pegrad/10), 25*Pegrad/10-2)
		pygame.draw.circle(self.screen, GREY, (473*Pegrad/10,473*Pegrad/10), 25*Pegrad/10-2)


		rad=wid/24
		pygame.draw.line(self.screen, BLACK,(2*rad/(2**0.5)+wid/16,2*rad/(2**0.5)+wid/16),(2.75*wid/8,2.75*wid/8),3)
		pygame.draw.line(self.screen, BLACK,(wid-(2*rad/(2**0.5)+wid/16),2*rad/(2**0.5)+wid/16),(wid-2.75*wid/8,2.75*wid/8),3)
		pygame.draw.line(self.screen, BLACK,(2*rad/(2**0.5)+wid/16,wid-(2*rad/(2**0.5)+wid/16)),(2.75*wid/8,wid-2.75*wid/8),3)
		pygame.draw.line(self.screen, BLACK,(wid-(2*rad/(2**0.5)+wid/16),wid-(2*rad/(2**0.5)+wid/16)),(wid-2.75*wid/8,wid-2.75*wid/8),3)

		secant=wid/9
		pygame.draw.arc(self.screen, BLACK,[wid/4,wid/4, secant, secant], -5*pi/4+0.8, 3*pi/4-0.8, 2)
		pygame.draw.arc(self.screen, BLACK,[wid-2.87*wid/8,wid/4, secant, secant], -7*pi/4+0.8, pi/4-0.8, 2)
		pygame.draw.arc(self.screen, BLACK,[wid/4,wid-2.87*wid/8, secant, secant], -3*pi/4+0.8, 5*pi/4-0.8, 2)
		pygame.draw.arc(self.screen, BLACK,[wid-2.87*wid/8,wid-2.87*wid/8, secant, secant], -1*pi/4+0.8, 7*pi/4-0.8, 2)

		for i in range(0, wid/35, 5):
			pygame.draw.rect(self.screen, (65+2*i, 65+i, 100), [i, i,wid- 2*i, wid- 2*i],1*Pegrad)
		#pygame.draw.rect(self.screen,WOODEN,(0,0,self.width,self.height),3*Pegrad)
		self.peg_list.draw(self.screen)
		self.striker_list.draw(self.screen)

		myfont = pygame.font.SysFont("Times New Roman", 30)
		myfont1 = pygame.font.SysFont("Times New Roman", 20)
		label = myfont.render("Score", 1, BLACK)
		player1 = myfont.render("Player 1: "+str(self.striker.player1score), 1, BLACK)
		player2 = myfont.render("Player 2: "+str(self.striker.player2score), 1, BLACK)
		dev1 = myfont1.render("Developed by:", 1, BLACK)
		dev2 = myfont1.render("Abhishek Kumar", 1, BLACK)
		dev3 = myfont1.render("Gaurav Shastri", 1, BLACK)
		dev4 = myfont1.render("Under the guidance of:", 1, BLACK)
		dev5 = myfont1.render("Dr. Gaurav Harit", 1, BLACK)
		self.screen.blit(label, (wid+2*strikerrad, 4*strikerrad))
		self.screen.blit(player1, (wid+2*strikerrad, 6*strikerrad))
		self.screen.blit(player2, (wid+2*strikerrad, 8*strikerrad))
		self.screen.blit(dev1, (wid+strikerrad, 22*strikerrad))
		self.screen.blit(dev2, (wid+strikerrad, 23*strikerrad))
		self.screen.blit(dev3, (wid+strikerrad, 24*strikerrad))
		self.screen.blit(dev4, (wid+strikerrad, 30*strikerrad))
		self.screen.blit(dev5, (wid+strikerrad, 31*strikerrad))

	
	def run(self):
		GAME_INIT=0
		self.state=0
		flag=0
		queen_capt=0
		whcount=9
		blcount=9
		while True:
			for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				if whcount==0:
					if queen_capt==8:
						player1score+=50
					myfont = pygame.font.SysFont("Times New Roman", 50)					
					dev1 = myfont1.render("Player1 wins", 1, BLACK)	
					self.screen.blit(dev1, (wid/5,wid/2))
					self.draw()
				elif blcount==0:
					if queen_capt==9:
						player2score+=50
					myfont = pygame.font.SysFont("Times New Roman", 50)					
					dev1 = myfont1.render("Player2 wins", 1, BLACK)	
					self.screen.blit(dev1, (wid/5,wid/2))
					self.draw()
				elif event.type==MOUSEBUTTONDOWN and event.button == 1:
					pos = pygame.mouse.get_pos()
					if self.striker.state==0:
						self.striker.state=1
					elif self.striker.state==1 and pos[1]>wid-4.65*strikerrad and self.striker.player==1:
						self.striker.state=2
						flag=0
						if(queen_capt==1):
							queen_capt=3
						if(queen_capt==4):
							queen_capt=0
							self.peg_list.add(Peg(PINK, Pegrad-1,25*Pegrad,25*Pegrad))
							self.draw()
					elif self.striker.state==1 and pos[1]<4.65*strikerrad and self.striker.player==2:
						self.striker.state=2
						flag=0
						if(queen_capt==2):
							queen_capt=4
						if(queen_capt==3):
							queen_capt=0
							self.peg_list.add(Peg(PINK, Pegrad-1,25*Pegrad,25*Pegrad))
							self.draw()
				elif event.type==MOUSEBUTTONDOWN and event.button == 3 and self.striker.rect.centery==wid-6*Pegrad and self.striker.player==1:
	 				self.striker.state=0
	 			elif event.type==MOUSEBUTTONDOWN and event.button == 3 and self.striker.rect.centery==6*Pegrad and self.striker.player==2:
	 				self.striker.state=0

			self.striker.update()
			pygame.display.update()
			self.draw()	
			pos = pygame.mouse.get_pos()

			#collision of striker with peg on the line
			if (self.striker.state==0):
				CollidedWithPeg=False
				for peg in self.peg_list:
					if pygame.sprite.collide_circle(peg, self.striker):
						CollidedWithPeg=True
						break
				if not CollidedWithPeg:
					if self.striker.player==1:			
						if pos[1]>wid-(4*strikerrad)-strikerrad and pos[1]<wid-(4*strikerrad)+strikerrad:
							if(pos[0]<5.5*strikerrad):
								self.striker.rect.centerx = 5.5*strikerrad
							elif(pos[0]>wid-5.5*strikerrad):
								self.striker.rect.centerx = wid-5.5*strikerrad
							else:
								self.striker.rect.centerx = pos[0]
					elif self.striker.player==2:							
						if pos[1]>3*strikerrad and pos[1]<5*strikerrad:
							if(pos[0]<5.5*strikerrad):
								self.striker.rect.centerx = 5.5*strikerrad
							elif(pos[0]>wid-5.5*strikerrad):
								self.striker.rect.centerx = wid-5.5*strikerrad
							else:
								self.striker.rect.centerx = pos[0]
					
				else:
						if self.striker.rect.centerx != wid/2 : 
							self.striker.rect.centerx = wid/2 
						elif pos[0]> wid/2:
							self.striker.rect.centerx = wid-5.5*strikerrad
						else:
							self.striker.rect.centerx = 5.5*strikerrad

			for peg1 in self.peg_list:
				for peg2 in self.peg_list:
					if peg1 is not peg2 and pygame.sprite.collide_circle(peg1, peg2) and not peg1.collided and not peg2.collided and GAME_INIT==1:
						collideBalls(peg1, peg2)
						peg1.collided, peg2.collided = True, True

			for peg in self.peg_list:
				peg.collided = False
				peg.update()
				if queen_capt==3 or queen_capt==4:
					if( (peg.rect.x<27*Pegrad/10+Pegrad/2 and peg.rect.y<27*Pegrad/10+Pegrad/2 ) or (peg.rect.x<27*Pegrad/10+Pegrad/2 and peg.rect.y+(5*Pegrad/2)>wid-27*Pegrad/10) or (peg.rect.x+(5*Pegrad/2)>wid-27*Pegrad/10 and peg.rect.y<27*Pegrad/10+Pegrad/2) or (peg.rect.x+(5*Pegrad/2)>wid-27*Pegrad/10 and peg.rect.y+(5*Pegrad/2)>wid-27*Pegrad/10)) :
						if not peg.inhole:
							peg.sound()
							peg.velx=0
							peg.vely=0
							peg.rect.x=wid*2
							peg.rect.y=wid*2	
							peg.inhole=True
							if(peg.isWhite and self.striker.player==1):
								self.striker.player1score+=10
								flag=1
								queen_capt=8
								whcount-=1
							elif(peg.isWhite and self.striker.player==2):
								self.striker.player1score+=10
								whcount-=1
				
							elif(peg.isBLACK and self.striker.player==2):
								self.striker.player2score+=10
								flag=2
								queen_capt=9
								blcount-=1
							elif(peg.isBLACK and self.striker.player==1):
								self.striker.player2score+=10
								blcount-=1
									
				
				else:
					if( (peg.rect.x<27*Pegrad/10+Pegrad/2 and peg.rect.y<27*Pegrad/10+Pegrad/2 ) or (peg.rect.x<27*Pegrad/10+Pegrad/2 and peg.rect.y+(5*Pegrad/2)>wid-27*Pegrad/10) or (peg.rect.x+(5*Pegrad/2)>wid-27*Pegrad/10 and peg.rect.y<27*Pegrad/10+Pegrad/2) or (peg.rect.x+(5*Pegrad/2)>wid-27*Pegrad/10 and peg.rect.y+(5*Pegrad/2)>wid-27*Pegrad/10)) :
						if not peg.inhole:
							peg.sound()
							peg.velx=0
							peg.vely=0
							peg.rect.x=wid*2
							peg.rect.y=wid*2	
							peg.inhole=True
							if(peg.isWhite ):
								self.striker.player1score+=10
								flag=1
								whcount-=1
							elif(peg.isBLACK ):
								self.striker.player2score+=10
								flag=2
								blcount-=1
							elif(peg.isQueen and self.striker.player==1 ):
								queen_capt=1
								
							elif(peg.isQueen and self.striker.player==2 ):
								queen_capt=2
								

			if( (self.striker.rect.x<27*strikerrad/10+strikerrad/2 and self.striker.rect.y<27*strikerrad/10+strikerrad/2 ) or (self.striker.rect.x<27*strikerrad/10+strikerrad/2 and self.striker.rect.y+(5*strikerrad/2)>wid-27*strikerrad/10) or (self.striker.rect.x+(5*strikerrad/2)>wid-27*strikerrad/10 and self.striker.rect.y<27*strikerrad/10+strikerrad/2) or (self.striker.rect.x+(5*strikerrad/2)>wid-27*strikerrad/10 and self.striker.rect.y+(5*strikerrad/2)>wid-27*strikerrad/10)) :
				self.striker.sound()
				self.striker.rect.x=wid/2
				self.striker.velx=0
				self.striker.vely=0
				if self.striker.player==1:
					self.striker.rect.y=wid-6*Pegrad
					if(self.striker.player1score>0):
						self.striker.player1score-=10
						whcount+=1
						self.peg_list.add(Peg(CREAM, Pegrad-1,25*Pegrad,25*Pegrad))
						self.draw()
				elif self.striker.player==2:
					self.striker.rect.y=6*Pegrad
					if(self.striker.player2score>0):
						self.striker.player2score-=10
						blcount+=1
						self.peg_list.add(Peg(BLACK, Pegrad-1,25*Pegrad,25*Pegrad))
						self.draw()

			if self.striker.state==2:
				for peg in self.peg_list:
					if pygame.sprite.collide_circle(peg, self.striker):
						collideBalls(peg,self.striker)
						if GAME_INIT == 0:
							GAME_INIT=1
			stopped = True
			for peg in self.peg_list:
				if peg.velx!=0 or peg.vely!=0 or self.striker.velx!=0 or self.striker.vely!=0:
					stopped = False
					break			

			if self.striker.state==1 and self.striker.player==1:
					pos = pygame.mouse.get_pos()
					if(pos[1]>wid-4.65*strikerrad and pos[1]<wid-3*Pegrad/2 and pos[0]>3*Pegrad/2 and pos[0]<wid-3*Pegrad/2):
						pygame.draw.lines(self.screen,GREEN, False,[(self.striker.rect.centerx,self.striker.rect.centery),(pos[0],pos[1])],5)
					elif(pos[1]>3*Pegrad/2 and pos[1]<wid-4.65*strikerrad and pos[0]>3*Pegrad/2 and pos[0]<wid-3*Pegrad/2):
						pygame.draw.lines(self.screen,RED, False,[(self.striker.rect.centerx,self.striker.rect.centery),(pos[0],pos[1])],5)	
			elif self.striker.state==1 and self.striker.player==2:
					pos = pygame.mouse.get_pos()
					if(pos[1]>3*Pegrad/2 and pos[1]<4.65*strikerrad and pos[0]>3*Pegrad/2 and pos[0]<wid-3*Pegrad/2):
						pygame.draw.lines(self.screen,GREEN, False,[(self.striker.rect.centerx,self.striker.rect.centery),(pos[0],pos[1])],5)
					elif(pos[1]>4.65*strikerrad and pos[1]<wid-3*Pegrad/2 and pos[0]>3*Pegrad/2 and pos[0]<wid-3*Pegrad/2):
						pygame.draw.lines(self.screen,RED, False,[(self.striker.rect.centerx,self.striker.rect.centery),(pos[0],pos[1])],5)	

			if stopped and self.striker.state==2 and self.striker.player==1:
				self.striker.state = 0

				if flag==1 :
					self.striker.rect.centery=44*Pegrad
					pos = pygame.mouse.get_pos()
					if pos[0]>5.5*strikerrad and pos[0]<wid-5.5*strikerrad:
						self.striker.rect.centerx=pos[0]
					else:
						if pos[0]>wid-5.5*strikerrad:
							self.striker.rect.centerx=wid-5.5*strikerrad
						else:
							self.striker.rect.centerx=5.5*strikerrad
					self.striker.player=1
				elif queen_capt==1:
					self.striker.rect.centery=44*Pegrad
					pos = pygame.mouse.get_pos()
					if pos[0]>5.5*strikerrad and pos[0]<wid-5.5*strikerrad:
						self.striker.rect.centerx=pos[0]
					else:
						if pos[0]>wid-5.5*strikerrad:
							self.striker.rect.centerx=wid-5.5*strikerrad
						else:
							self.striker.rect.centerx=5.5*strikerrad
					self.striker.player=1
				else:
					self.striker.rect.centery=6*Pegrad
					pos = pygame.mouse.get_pos()
					if pos[0]>5.5*strikerrad and pos[0]<wid-5.5*strikerrad:
						self.striker.rect.centerx=pos[0]
					else:
						if pos[0]>wid-5.5*strikerrad:
							self.striker.rect.centerx=wid-5.5*strikerrad
						else:
							self.striker.rect.centerx=5.5*strikerrad
					self.striker.player=2
				print "Player1:- "+ str(self.striker.player1score)
				print "Player2:- "+ str(self.striker.player2score)
			elif stopped and self.striker.state==2 and self.striker.player==2:
				self.striker.state = 0
				if flag==2:
					self.striker.rect.centery=6*Pegrad
					pos = pygame.mouse.get_pos()
					if pos[0]>5.5*strikerrad and pos[0]<wid-5.5*strikerrad:
						self.striker.rect.centerx=pos[0]
					else:
						if pos[0]>wid-5.5*strikerrad:
							self.striker.rect.centerx=wid-5.5*strikerrad
						else:
							self.striker.rect.centerx=5.5*strikerrad
					self.striker.player=2
				if queen_capt==2:
					self.striker.rect.centery=6*Pegrad
					pos = pygame.mouse.get_pos()
					if pos[0]>5.5*strikerrad and pos[0]<wid-5.5*strikerrad:
						self.striker.rect.centerx=pos[0]
					else:
						if pos[0]>wid-5.5*strikerrad:
							self.striker.rect.centerx=wid-5.5*strikerrad
						else:
							self.striker.rect.centerx=5.5*strikerrad
					self.striker.player=2
				else:
					self.striker.rect.centery=44*Pegrad
					pos = pygame.mouse.get_pos()
					if pos[0]>5.5*strikerrad and pos[0]<wid-5.5*strikerrad:
						self.striker.rect.centerx=pos[0]
					else:
						if pos[0]>wid-5.5*strikerrad:
							self.striker.rect.centerx=wid-5.5*strikerrad
						else:
							self.striker.rect.centerx=5.5*strikerrad
					self.striker.player=1
				print "Player1:- "+ str(self.striker.player1score)
				print "Player2:- "+ str(self.striker.player2score)

			clock.tick(50)


def main():
	game = CarromBoard()
	WhiteCount=9
	BLACKCount=9
	while game.run():
			pass


if __name__ == '__main__':
	main()