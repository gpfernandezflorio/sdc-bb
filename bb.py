#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, math, random, pygame, datetime
from pygame.locals import *

title = u"Búsqueda Binaria: El Juego!"
question = u"¿Dónde está el conejo?"
background_file = "bg.jpg"
win_file = "win.jpg"
lost_files = ["go1.jpg","go2.jpg","go3.png","go4.jpg","go5.jpg","go6.png","go7.jpg","go8.jpg"]
life_file = "life.png"
life_empty_file = "life-empty.png"
positives = [u"Vas por buen camino",u"Eso! seguí así",u"A este paso lo vas a encontrar en seguida",u"Muy buena eleccción"]
negatives = [u"Vas directo a una trampa",u"Lo veo difícil",u"Estás dando vueltas en círculos",u"Estás desperdiciando tus vidas"]
difficulty = 10

err_no_number = u"No se ha ingresado ningún número"
err_bigger = u" es mayor a "
err_smaller = u" es menor a "
over = u"  Por arriba de "
below = u"  Por abajo de "
it_was = u"  Era "
instructions = [u"Ingrese un número entre ", u" y ", u", inclusive"]
end_message = u"Exactas - Departamento de Computación  "
quit_message = u"  Esc: Salir"
reset_message = u"  Supr: Reiniciar"
diff_message = u"  +/-: Cambiar dificultad"
clue_message = u"  Intro: Pista"
clue = u"Pista: El medio es "
copy = u"Semana de la Computación "


def update_view():
	screen.blit(background, background.get_rect())
	screen.blit(title_label, (w/50, h/10))
	screen.blit(quest_label, (w/2-quest_label.get_rect().w/2, h/3))
	screen.blit(input_label, (w/2-input_label.get_rect().w/2, h/2))
	screen.blit(min_label, (w/50, h/2))
	screen.blit(max_label, (w-w/50-max_label.get_rect().w, h/2))
	screen.blit(message_label, (w/2-message_label.get_rect().w/2, 8*h/10))
	screen.blit(message_2_label, (w/2-message_2_label.get_rect().w/2, 8*h/10+message_label.get_rect().h+5))
	screen.blit(instructions_label, (w/2-instructions_label.get_rect().w/2, 4*h/10))
	screen.blit(quit_label, (0, h-quit_label.get_rect().h-5))
	screen.blit(reset_label, (0, h-2*(reset_label.get_rect().h+5)))
	screen.blit(diff_label, (0, h-3*(diff_label.get_rect().h+5)))
	screen.blit(clue_label, (0, h-4*(clue_label.get_rect().h+5)))
	screen.blit(copy_label, (w-copy_label.get_rect().w-5, h-copy_label.get_rect().h-5))
	screen.blit(end_label, (w-end_label.get_rect().w-5, h-2*(end_label.get_rect().h+5)))
	screen.blit(sdc_label, (w-sdc_label.get_rect().w-5, h-3*(sdc_label.get_rect().h+5)))
	r = life.get_rect()
	for i in range(difficulty - lifes):
		screen.blit(life_empty, (w-(i+lifes+1)*(r.w+10),10))
	for i in range(lifes):
		screen.blit(life, (w-(i+1)*(r.w+10),10))
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
	message_label = font3.render("", False, (0,0,0))
	message_2_label = font3.render("", False, (0,0,0))

def enter():
	global _input, input_label, medio, lifes
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
#			_input = ""
#			input_label = font2.render("?", True, (0,0,0))
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
	min_label = font2.render(str(min_val-1) + " -", True, (0,0,0))
	instructions_label = font3.render(instructions[0] + str(min_val) + instructions[1] + str(max_val) + instructions[2], True, (0,0,0))
	update_view()
	messages(over + str(x) + "  ","  " + s + "  ",c)

def por_abajo(x,s,c=(255,0,0)):
	global max_val, max_label, instructions_label
	max_val = x-1
	max_label = font2.render("- " + str(max_val+1), True, (0,0,0))
	instructions_label = font3.render(instructions[0] + str(min_val) + instructions[1] + str(max_val) + instructions[2], True, (0,0,0))
	update_view()
	messages(below + str(x) + "  ","  " + s + "  ",c)

def won():
	global end
	end = True
	r = win.get_rect()
	screen.fill((255,255,255))
	screen.blit(win, (w/2-r.w/2, h/2-r.h/2))
	screen.blit(quit_label_w, (0, h-quit_label.get_rect().h-5))
	screen.blit(reset_label_w, (0, h-2*(quit_label.get_rect().h+5)))
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
	screen.blit(quit_label, (0, h-quit_label.get_rect().h-5))
	screen.blit(reset_label, (0, h-2*(quit_label.get_rect().h+5)))
	pygame.display.update()
	message_label = font3.render("", False, (0,0,0))

def restart():
	global end, lifes, _input, input_label, medio, min_val, max_val, min_label, max_label, instructions_label
	lifes = difficulty
	min_val = 1
	max_val = int(math.pow(2, difficulty))-1
	medio = min_val + int((max_val - min_val)/2)
	min_label = font2.render(str(min_val-1) + " -", True, (0,0,0))
	max_label = font2.render("- " + str(max_val+1), True, (0,0,0))
	instructions_label = font3.render(instructions[0] + str(min_val) + instructions[1] + str(max_val) + instructions[2], True, (0,0,0))
	_input = ""
	input_label = font2.render("?", True, (0,0,0))
	update_view()
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
	max_val = int(math.pow(2, difficulty))-1

	screen = pygame.display.set_mode((w,h), FULLSCREEN)
	win = pygame.image.load(win_file).convert()
	r = win.get_rect()
	if r.w > w or r.h > h:
		win = pygame.transform.scale(win, (w, h))
	life_image = pygame.image.load(life_file).convert_alpha()
	life = pygame.transform.scale(life_image, (w/20, w/25))
	life_empty_image = pygame.image.load(life_empty_file).convert_alpha()
	life_empty = pygame.transform.scale(life_empty_image, (w/20, w/25))
	background_image = pygame.image.load(background_file).convert()
	background = pygame.transform.scale(background_image, (w, h))

	font1 = pygame.font.SysFont("monospace", w/25, True)
	title_label = font1.render(title, True, (0,0,0))

	font2 = pygame.font.SysFont("monospace", w/40, True)
	quest_label = font2.render(question, True, (0,0,0))
	input_label = font2.render("?", True, (0,0,0))
	min_label = font2.render(str(min_val-1) + " -", True, (0,0,0))
	max_label = font2.render("- " + str(max_val+1), True, (0,0,0))

	font3 = pygame.font.SysFont("monospace", w/50, True)
	message_label = font3.render("", True, (255,0,0), (50,50,50))
	message_2_label = font3.render("", True, (255,0,0), (50,50,50))
	instructions_label = font3.render(instructions[0] + str(min_val) + instructions[1] + str(max_val) + instructions[2], True, (0,0,0))

	font4 = pygame.font.SysFont("monospace", w/60, True)
	end_label = font4.render(end_message, True, (255,255,255))
	sdc_label = font4.render(copy + str(datetime.datetime.now().year) + "  ", True, (255,255,255))
	copy_label = font4.render(u"(c) ALL RIGHTS RESERVED  ", True, (255,255,255))
	quit_label = font4.render(quit_message, True, (255,255,255))
	reset_label = font4.render(reset_message, True, (255,255,255))
	quit_label_w = font4.render(quit_message, True, (0,0,0))
	reset_label_w = font4.render(reset_message, True, (0,0,0))
	diff_label = font4.render(diff_message, True, (255,255,255))
	clue_label = font4.render(clue_message, True, (255,255,255))

	_input = ""
	medio = min_val + int((max_val - min_val)/2)
	lifes = difficulty
	end = False
	update_view()


	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
				elif event.key == pygame.K_DELETE:
					restart()
				elif (not end):
					if event.key == pygame.K_1:
						update_input("1")
					elif event.key == pygame.K_2:
						update_input("2")
					elif event.key == pygame.K_3:
						update_input("3")
					elif event.key == pygame.K_4:
						update_input("4")
					elif event.key == pygame.K_5:
						update_input("5")
					elif event.key == pygame.K_6:
						update_input("6")
					elif event.key == pygame.K_7:
						update_input("7")
					elif event.key == pygame.K_8:
						update_input("8")
					elif event.key == pygame.K_9:
						update_input("9")
					elif event.key == pygame.K_0:
						update_input("0")
					elif event.key == pygame.K_RETURN:
						enter()
					elif event.key == pygame.K_BACKSPACE:
						back()
					elif event.key == pygame.K_KP_PLUS:
						difficulty = difficulty +1
						restart()
					elif event.key == pygame.K_KP_MINUS:
						if (difficulty > 1):
							difficulty = difficulty -1
							restart()
					elif event.key == pygame.K_KP_ENTER:
						message(clue + str(medio),(255,255,255))
