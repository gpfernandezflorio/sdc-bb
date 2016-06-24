#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, math, random, pygame, datetime
from pygame.locals import *

# VERSION
version = "v1.1"

# DEFAULT
difficulty = 10

# MOUSE and KEYS
key_quit = -1#pygame.K_ESCAPE
mouse_quit = 3
key_rst = pygame.K_ESCAPE
key_rst_str = u"Esc"
key_diff_up = -1#pygame.K_KP_PLUS
key_diff_dw = -1#pygame.K_KP_MINUS
mouse_diff_up = 4
mouse_diff_dw = 5
key_clue = pygame.K_LCTRL
mouse_clue = 1
key_clue_str = u"Ctrl Izq."

# STRINGS
title = u"Búsqueda Binaria: El Juego!"
question = u"¿Dónde está el conejo?"
question_d = u"¿Dónde está Dory?"
positives = [u"Vas por buen camino",u"Eso! seguí así",u"A este paso vas a terminar en seguida",u"Muy buena eleccción",u"Como un campeón",u"Vos sí que sabés",u"Eso es ser inteligente",u"Ya casi, un poco más"]
negatives = [u"Vas directo a una trampa",u"Lo veo difícil",u"Estás dando vueltas en círculos",u"Estás desperdiciando tus vidas",u"No creo que lo hayas pensado mucho",u"¿En qué estabas pensando?",u"Chau, chau adiós",u"Se te va a escapar",u"Ay, qué lástima!"]
err_no_number = u"No se ha ingresado ningún número"
err_bigger = u" es mayor a "
err_smaller = u" es menor a "
over = u"  Por arriba de "
below = u"  Por abajo de "
it_was = u"  Era "
instructions = [u"Ingrese un número entre ", u" y ", u", inclusive"]
end_message = u"Exactas - Departamento de Computación  "
reset_message = u"  " + key_rst_str + u": Reiniciar"
clue_message = u"  " + key_clue_str + u": Pista"
clue = u"Pista: El medio es "
copy = u"Semana de la Computación "
start_message = u"Presione Enter para empezar"

# FILES
background_file = "bg.jpg"
background_file_d = "bg_d.png"
win_file = "win.png"
lost_files = ["go1.jpg","go2.jpg","go3.png","go4.jpg","go5.jpg","go6.png","go7.jpg","go8.jpg"]
life_file = "life.png"
life_empty_file = "life-empty.png"
hand_file = "hand.png"
sign_file = "sign.png"
jumping_file = "jumping.png"
swiming_file = "swiming.png"
win_back_file = "win_back.jpg"
win_back_file_d = "win_back_d.jpg"

def update_view():
	if scene == "BUNNY":
		screen.blit(background, background.get_rect())
	else:
		screen.blit(background_d, background.get_rect())
	if anim <= anim_limit:
		screen.blit(start_label, (w/2 - start_label.get_rect().w/2, h/5+math.pow(anim-anim_limit/2,2)))
		if scene == "BUNNY":
			x = anim
			if fliped:
				x = -anim
			screen.blit(jumping, (jumping_pos + 2*x*w/2/anim_limit/2,h/3+2*math.pow(anim-anim_limit/2,2)))
		else:
			pos = anim*(w+jumping.get_rect().w)/anim_limit
			if fliped:
				pos = w-pos+jumping.get_rect().w
			screen.blit(jumping, (pos-jumping.get_rect().w,h/6 + jumping_pos + 10000*math.sin(pos/100.0)/w))
	else:
		r = life.get_rect()
		for i in range(difficulty - lifes):
			screen.blit(life_empty, (w-(i+lifes+1)*(r.w+10),10))
		for i in range(lifes):
			screen.blit(life, (w-(i+1)*(r.w+10),10))
		r = rhand.get_rect()
		screen.blit(rhand, (w*0.08 + w*0.84*max_val/top,h/2+r.h))
		screen.blit(lhand, (w*0.08 + w*0.84*min_val/top - r.w,h/2+r.h))
		screen.blit(min_label, (w*0.08 + w*0.84*min_val/top - min_label.get_rect().w, h/2+2*r.h))
		screen.blit(max_label, (w*0.08 + w*0.84*max_val/top, h/2+2*r.h))
		if scene == "BUNNY":
			screen.blit(quest_label, (w/2-quest_label.get_rect().w/2, h/3))
		else:
			screen.blit(quest_label_d, (w/2-quest_label.get_rect().w/2, h/3))
		screen.blit(input_label, (w/2-input_label.get_rect().w/2, h/2))
		r = rsign.get_rect()
		r2 = top_label.get_rect()
		screen.blit(rsign, (w-r.w, h/2))
		screen.blit(lsign, (0, h/2))
		screen.blit(top_label, (w-r.w+(r.w-r2.w)/2, h/2+(r.h-r2.h)/2))
		r2 = bottom_label.get_rect()
		screen.blit(bottom_label, ((r.w-r2.w)/2, h/2+(r.h-r2.h)/2))
		screen.blit(message_label, (w/2-message_label.get_rect().w/2, 8*h/10))
		screen.blit(message_2_label, (w/2-message_2_label.get_rect().w/2, 8*h/10+message_label.get_rect().h+5))
		screen.blit(instructions_label, (w/2-instructions_label.get_rect().w/2, 4*h/10))
		screen.blit(reset_label, (0, h-(reset_label.get_rect().h+5)))
		screen.blit(clue_label, (0, h-2*(clue_label.get_rect().h+5)))
		screen.blit(end_label, (w-end_label.get_rect().w-5, h-end_label.get_rect().h-5))
		screen.blit(sdc_label, (w-sdc_label.get_rect().w-5, h-2*(end_label.get_rect().h+5)))
	screen.blit(title_label, (w/50, h/10))
	screen.blit(version_label, (w/50 + title_label.get_rect().w + 10, h/10 + title_label.get_rect().h - 1.5*version_label.get_rect().h))
	pygame.display.update()

def error(s):
	message(s,(255,0,0))

def message(s,c=(255,255,255)):
	messages("  " + s + "  ","",(255,255,255),c)

def messages(s1,s2,c2=(255,255,255),c1=(255,255,255)):
	global message_label, message_2_label
	message_label = font3.render(s1, True, c1, (50,50,50))
	message_2_label = font3.render(s2, True, c2, (50,50,50))
	update_view()

def enter():
	global _input, input_label, medio, lifes, message_label, message_2_label
	message_label = font3.render("", False, (0,0,0))
	message_2_label = font3.render("", False, (0,0,0))
	if _input == "":
		error(err_no_number)
	else:
		x = int(_input)
		_input = ""
		input_label = font2.render("?", True, (0,0,0))
		if x > max_val:
			error(str(x) + err_bigger + str(max_val))
		elif x < min_val:
			error(str(x) + err_smaller + str(min_val))
		else:
			if (max_val == min_val):
				if (x == min_val):
					won()
				else:
					error("FATAL ERROR! 0x01")
			else:
				m = random.choice([True,False])
				if lifes == 1:
					if m and x < max_val:
						lost(random.randint(x+1, max_val))
					elif x > min_val:
						lost(random.randint(min_val, x-1))
					elif x < max_val:
						lost(random.randint(x+1, max_val))
					else:
						error("FATAL ERROR! 0x02")
				else:
					lifes = lifes-1
					if x == medio:
						if m:
							por_abajo(x, random.choice(positives),(0,255,0))
						else:
							por_arriba(x, random.choice(positives),(0,255,0))
					elif x > medio:
						por_abajo(x, random.choice(negatives))
					elif x < medio:
						por_arriba(x, random.choice(negatives))
					else:
						error("FATAL ERROR! 0x03")
					medio = min_val + int((max_val - min_val)/2)

def por_arriba(x,s,c=(255,0,0)):
	global min_val, min_label, instructions_label
	min_val = x+1
	min_label = font2.render(str(min_val), True, (0,0,0))
	instructions_label = font3.render(instructions[0] + str(min_val) + instructions[1] + str(max_val) + instructions[2], True, (0,0,0))
	update_view()
	messages(over + str(x) + "  ","  " + s + "  ",c)

def por_abajo(x,s,c=(255,0,0)):
	global max_val, max_label, instructions_label
	max_val = x-1
	max_label = font2.render(str(max_val), True, (0,0,0))
	instructions_label = font3.render(instructions[0] + str(min_val) + instructions[1] + str(max_val) + instructions[2], True, (0,0,0))
	update_view()
	messages(below + str(x) + "  ","  " + s + "  ",c)

def won():
	global end
	end = True
	r = win.get_rect()
	if scene == "BUNNY":
		screen.blit(win_back, win_back.get_rect())
	else:
		screen.blit(win_back_d, win_back_d.get_rect())
	screen.blit(win, (w/3-r.w/2, h/2-r.h/2))
	screen.blit(reset_label, (0, h-(reset_label.get_rect().h+5)))
	pygame.display.update()

def lost(x):
	global end, message_label
	end = True
	lost_file = random.choice(lost_files)
	lost_image = pygame.image.load(lost_file).convert()
	screen.fill((0,0,0))
	r = lost_image.get_rect()
	if r.w > w or r.h > h:
		lost_image = pygame.transform.scale(lost_image, (w, h))
		screen.blit(lost_image, (0,0))
	else:
		screen.blit(lost_image, (w/2-r.w/2, h/2-r.h/2))
	message_label = font3.render(it_was + str(x) + "  ", True, (255,0,0), (50,50,50))
	screen.blit(message_label, (w/2-message_label.get_rect().w/2, 8*h/10))
	screen.blit(reset_label, (0, h-(reset_label.get_rect().h+5)))
	pygame.display.update()
	message_label = font3.render("", False, (0,0,0))

def restart():
	global scene, end, lifes, _input, input_label, medio, min_val, max_val, min_label, max_label, instructions_label, top_label, bottom_label, anim, jumping
	if scene == "BUNNY":
		jumping = pygame.transform.rotate(jumping_idle,0)
	else:
		jumping = pygame.transform.rotate(swiming_idle,0)
	lifes = difficulty
	top = int(math.pow(2, difficulty))-1
	min_val = 1
	max_val = top
	medio = min_val + int((max_val - min_val)/2)
	min_label = font2.render(str(min_val), True, (0,0,0))
	max_label = font2.render(str(max_val), True, (0,0,0))
	bottom_label = font2.render(str(min_val-1), True, (0,0,0))
	top_label = font2.render(str(max_val+1), True, (0,0,0))
	instructions_label = font3.render(instructions[0] + str(min_val) + instructions[1] + str(max_val) + instructions[2], True, (0,0,0))
	_input = ""
	input_label = font2.render("?", True, (0,0,0))
	anim = 1
	end = False

def back():
	global _input, input_label
	if len(_input) > 0:
		_input = _input[:len(_input)-1]
		if len(_input) == 0:
			input_label = font2.render("?", True, (0,0,0))
		else:
			input_label = font2.render(_input, True, (0,0,0))
		update_view()

def update_input(c):
	global _input, input_label
	_input = _input + c
	input_label = font2.render(_input, True, (0,0,0))
	update_view()

if __name__ == '__main__':

	pygame.init()
	pygame.mouse.set_visible(0)

	infoObject = pygame.display.Info()
	w = infoObject.current_w
	h = infoObject.current_h

	min_val = 1
	top = int(math.pow(2, difficulty))-1
	max_val = top

	screen = pygame.display.set_mode((w,h), FULLSCREEN)
	win = pygame.image.load(win_file).convert_alpha()
	r = win.get_rect()
	if r.w > w or r.h > h:
		win = pygame.transform.scale(win, (w, h))
	win_back = pygame.image.load(win_back_file).convert()
	win_back = pygame.transform.scale(win_back, (w, h))
	win_back_d = pygame.image.load(win_back_file_d).convert()
	win_back_d = pygame.transform.scale(win_back_d, (w, h))
	life_image = pygame.image.load(life_file).convert_alpha()
	life = pygame.transform.scale(life_image, (w/20, w/25))
	life_empty_image = pygame.image.load(life_empty_file).convert_alpha()
	life_empty = pygame.transform.scale(life_empty_image, (w/20, w/25))
	rsign = pygame.image.load(sign_file).convert_alpha()
	rsign = pygame.transform.scale(rsign, (w/9, h/9))
	lsign = pygame.transform.flip(rsign, True, False)
	rhand = pygame.image.load(hand_file).convert_alpha()
	rhand = pygame.transform.scale(rhand, (w/9, h/9))
	lhand = pygame.transform.flip(rhand, True, False)
	background = pygame.image.load(background_file).convert()
	background = pygame.transform.scale(background, (w, h))
	background_d = pygame.image.load(background_file_d).convert()
	background_d = pygame.transform.scale(background_d, (w, h))

	font1 = pygame.font.SysFont("monospace", w/25, True)
	title_label = font1.render(title, True, (0,0,0))

	font2 = pygame.font.SysFont("monospace", w/40, True)
	quest_label = font2.render(question, True, (0,0,0))
	quest_label_d = font2.render(question_d, True, (0,0,0))
	input_label = font2.render("?", True, (0,0,0))
	min_label = font2.render(str(min_val), True, (0,0,0))
	max_label = font2.render(str(max_val), True, (0,0,0))
	bottom_label = font2.render(str(min_val-1), True, (0,0,0))
	top_label = font2.render(str(max_val+1), True, (0,0,0))

	font3 = pygame.font.SysFont("monospace", w/50, True)
	message_label = font3.render("", True, (255,0,0), (50,50,50))
	message_2_label = font3.render("", True, (255,0,0), (50,50,50))
	instructions_label = font3.render(instructions[0] + str(min_val) + instructions[1] + str(max_val) + instructions[2], True, (0,0,0))
	start_label = font1.render(start_message, True, (200,10,40))

	font4 = pygame.font.SysFont("monospace", w/60, True)
	end_label = font4.render(end_message, True, (255,255,255))
	sdc_label = font4.render(copy + str(datetime.datetime.now().year) + "  ", True, (255,255,255))
	reset_label = font4.render(reset_message, True, (255,255,255))
	clue_label = font4.render(clue_message, True, (255,255,255))
	version_label = font4.render(version, True, (0,0,0))

	_input = ""
	medio = min_val + int((max_val - min_val)/2)
	lifes = difficulty
	dead_limit = 15
	anim_limit = 40
	jumping_pos = random.randint(-w/3,w/3)
	anim = 1
	dead = dead_limit
	end = False
	fliped = False

	jumping_idle = pygame.image.load(jumping_file).convert_alpha()
	jumping_idle = pygame.transform.scale(jumping_idle, (w/4,h/3))
	swiming_idle = pygame.image.load(swiming_file).convert_alpha()
	swiming_idle = pygame.transform.scale(swiming_idle, (w/4,h/3))

	scene = random.choice(["BUNNY","DORY"])
	random_scene = True
	if scene == "BUNNY":
		jumping = pygame.transform.rotate(jumping_idle,0)
	else:
		jumping = pygame.transform.rotate(swiming_idle,0)

	while 1:
		if not end:
			if anim < anim_limit:
				anim = anim+1
				if anim == anim_limit:
					dead = 0
				pygame.time.wait(100)
				if scene == "BUNNY":
					if fliped:
						jumping = pygame.transform.rotate(jumping_idle,6*anim-120)
					else:
						jumping = pygame.transform.rotate(jumping_idle,100-5*anim)
				else:
					if fliped:
						jumping = pygame.transform.rotate(swiming_idle,15+30*math.sin(anim/2.0))
					else:
						jumping = pygame.transform.rotate(swiming_idle,30*math.sin(anim/2.0))
				update_view()
			else:
				pygame.time.wait(10)
				dead = dead + 1
				if dead == dead_limit:
					jumping_pos = random.randrange(0,int(w/3))
					if scene == "BUNNY":
						if random.choice([True,False]):
							fliped = not fliped
							jumping_idle = pygame.transform.flip(jumping_idle,True,False)
							swiming_idle = pygame.transform.flip(swiming_idle,True,False)
					else:
						fliped = not fliped
						jumping_idle = pygame.transform.flip(jumping_idle,True,False)
						swiming_idle = pygame.transform.flip(swiming_idle,True,False)
					anim = 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == mouse_diff_up:
					if anim > anim_limit:
						difficulty = difficulty +1
						top = int(math.pow(2, difficulty))-1
						restart()
						anim = anim_limit + 1
						update_view()
				elif event.button == mouse_diff_dw:
					if anim > anim_limit:
						if (difficulty > 1):
							difficulty = difficulty -1
							top = int(math.pow(2, difficulty))-1
							restart()
							anim = anim_limit + 1
							update_view()
				elif event.button == mouse_quit:
					sys.exit()
				elif event.button == mouse_clue:
					message(clue + str(medio),(255,255,255))
			elif event.type == pygame.KEYDOWN:
				if event.key == key_quit:
					sys.exit()
				elif event.key == key_rst:
					if (random_scene):
						scene = random.choice(["BUNNY","DORY"])
					restart()
					update_view()
				elif (not end):
					if event.key == pygame.K_r:
						random_scene = not random_scene
					elif event.key == pygame.K_d:
						scene = "DORY"
						update_view()
					elif event.key == pygame.K_c:
						scene = "BUNNY"
						update_view()
					elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
						update_input("1")
					elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
						update_input("2")
					elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
						update_input("3")
					elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
						update_input("4")
					elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
						update_input("5")
					elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
						update_input("6")
					elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
						update_input("7")
					elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
						update_input("8")
					elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
						update_input("9")
					elif event.key == pygame.K_0 or event.key == pygame.K_KP0:
						update_input("0")
					elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
						if anim <= anim_limit:
							restart()
							anim = anim_limit + 1
							message_label = font3.render("", False, (0,0,0))
							message_2_label = font3.render("", False, (0,0,0))
							update_view()
						else:
							enter()
					elif event.key == pygame.K_BACKSPACE:
						back()
					elif event.key == key_diff_up:
						if anim > anim_limit:
							difficulty = difficulty +1
							top = int(math.pow(2, difficulty))-1
							restart()
							anim = anim_limit + 1
							update_view()
					elif event.key == key_diff_dw:
						if anim > anim_limit:
							if (difficulty > 1):
								difficulty = difficulty -1
								top = int(math.pow(2, difficulty))-1
								restart()
								anim = anim_limit + 1
								update_view()
					elif event.key == key_clue:
						message(clue + str(medio),(255,255,255))
