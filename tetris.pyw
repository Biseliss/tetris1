# -*- coding: cp1251 -*-
#1
#TETRIS 2
"""
Код писал Мартин Вернер с ~9.12.2020
Спасибо всем, кто внёс хоть и малый, но вклад в создание этой игры <3
"""
python2=False
import pygame
import sys
from random import randint
import time
import copy
import json
import os
from threading import Thread
import subprocess
try:from urllib.request import urlopen
except:
    from six.moves.urllib.request import urlopen
    python2=True
import io
import shutil
import zipfile
import socket
import pickle
import requests
pygame.init()
pygame.font.init()

def exit(in_game_call=False):
    global running
    if (in_game_call):
        dr=tf_dialog("Выйти из игры", "Сохранить игру перед выходом?", byellow, bpyellow, "Да", bgreen, bpgreen, "Нет", baqua, bpaqua, "Назад", 2)
        if (dr==1):
            save_game()
        elif (dr==2):
            pass
        elif (dr==3):
            return
    running=False
    pygame.quit()
    sys.exit()
"""
bred=(222, 37, 37)
bpred=(255, 74, 74)
borange=(238, 89, 7)
bporange=(255, 178, 14)
byellow=(255, 174, 0)
bpyellow=(255, 255, 0)
bgreen=(6, 164, 11)
bpgreen=(12, 255, 22)
baqua=(41, 154, 255)
bpaqua=(90, 255, 255)
bblue=(43, 83, 173)
bpblue=(89, 151, 250)
bpurple=(124, 87, 180)
bppurple=(248, 174, 155)

bblack=(0,0,0)
bpblack=(50,50,50)

bdred=(111,18,18)
bdgreen=(3,82,5)
"""
site="vmartin.codead.dev"
def cfc():
    global connection
    try:
        requests.get("http://"+site,timeout=2)
        connection=True
    except:
        connection=False
Thread(target=cfc).start()

if (python2):
    try:
        data=open('settings.tse2', "r").read()
        settings=json.loads(data)
    except:
        f=open("settings.tse2", "w")
        f.write("{}")
        f.close()
else:
    try:
        with open('settings.tse2', "r", encoding="utf-8") as settings:
            settings=json.load(settings)
    except:
        f=open("settings.tse2", "w")
        f.write("{}")
        f.close()
        #data=requests.get("http://"+site+"/TETRIS/settings.tse2",allow_redirects=True)
        #open("settings.tse2","wb").write(data.content)
        with open('settings.tse2', "r", encoding="utf-8") as settings:
            settings=json.load(settings)

def save_settings():
    if (python2):
        with io.open('settings.tse2', 'w', encoding='utf-8') as write_file:
            write_file.write(json.dumps(settings, ensure_ascii=False, indent=4))
    else:
        with open("settings.tse2", "w", encoding="utf-8") as write_file:
            json.dump(settings, write_file, ensure_ascii=False, indent=4)

def settings_integrity_check():
    global settings
    mass=list(settings.keys())
    #print(settings)
    if ("resize" not in mass or type(settings["resize"])!=int):
        settings["resize"]=1
    if ("piece_cd_move_time" not in mass or type(settings["piece_cd_move_time"])!=float):
        settings["piece_cd_move_time"]=0.06
    if ("toggleaf" not in mass or type(settings["toggleaf"])!=bool):
        settings["toggleaf"]=False
    if ("togglefall" not in mass or type(settings["togglefall"])!=bool):
        settings["togglefall"]=False
    if ("togglecleara" not in mass or type(settings["togglecleara"])!=bool):
        settings["togglecleara"]=False
    if ("toggleproection" not in mass or type(settings["toggleproection"])!=bool):
        settings["toggleproection"]=False
    if ("theme" not in mass or type(settings["theme"])!=str):
        settings["theme"]="Default"
    if ("music" not in mass or type(settings["music"])!=str):
        settings["music"]="Default.ogg"
    if ("music_volume" not in mass or type(settings["music_volume"])!=float):
        settings["music_volume"]=1.0
    if ("effect_volume" not in mass or type(settings["effect_volume"])!=float):
        settings["effect_volume"]=1.0
    if ("rtol" not in mass or type(settings["rtol"])!=list):
        settings["rtol"]=[]
    save_settings()

settings_integrity_check()

resize=settings["resize"]

screen_size=440*resize

fps=pygame.time.Clock()

#кнопки
#сюда писать значения при разрешении 440х440п
#0 - размер; 1 - координаты
marathon_button=((360,60), (40,360))
settings_button=((40,40), (0,0))
scores_button=((40,40), (120,0))
themes_button=((40,40),(80,0))
music_button=((40,40),(40,0))
mat_button=((40,40), (0,400))
info_button=((40,40), (400,0))
back_button=((40,40), (0,0))
select_mat_button=((400,40), (20,40)) #Кнопка больше не используется!

resume_button=((400,40), (20,20))
restart_button=((400,40), (20,80))
select_mat_button=((400,40), (20,140))
p_settings_button=((400,40), (20,200))
to_menu_button=((400,40), (20,260))
quit_game_button=((400,40), (20,320))

up_button=((40,40), (370,60))
down_button=((40,40), (370,140))
up_button2=((40,40), (370,300))
down_button2=((40,40), (370,380))

musicpp=((20,20),(220,200))
musicp=((20,20),(245,200))
musicm=((20,20),(345,200))
musicmm=((20,20),(370,200))

effectpp=((20,20),(220,250))
effectp=((20,20),(245,250))
effectm=((20,20),(345,250))
effectmm=((20,20),(370,250))

proekcon=((60,30),(300,56))
proekcoff=((60,30),(360,56))
azfon=((60,30),(300,96))
azfoff=((60,30),(360,96))
aolon=((60,30),(300,136))
aoloff=((60,30),(360,136))
apon=((60,30),(300,176))
apoff=((60,30),(360,176))

button_resize_plus=((30,30),(300,236))
button_resize_minus=((30,30),(390,236))
button_pcdmt_plus=((30,30),(300,276))
button_pcdmt_minus=((30,30),(390,276))

info_screen_button=((400,40), (20,120))

dialog_true_button=((400,40), (20,120))
dialog_false_button=((400,40), (20,180))
dialog_cancel_button=((400,40), (20,240))

tetriscom=((360,40), (40,360))

catalog_button=((360,40),(40,380))

explorer_music_button=((360,40),(40,380))

catalog_up=((40,40),(400,0))
catalog_down=((40,40),(400,400))

catalog_theme_download=((400,40),(20,380))
catalog_theme_update=((190,40),(20,380))
catalog_theme_remove=((190,40),(230,380))

pers_music_menu_button=((400,40),(20,160))
pers_themes_menu_button=((400,40),(20,220))

loading_screen_to_show=""

def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((255, 255, 255, 255), None, pygame.BLEND_RGBA_MULT)
    #screen.blit(image, (0,0))
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    return image

def s_text(text, ttx, place, color, mode, font, alpha=0):
    #1 - нормальный режим; 2 - режим с отстопом от правого края; 3 - режим с отступом от левого края; 4 - по центру (y); 5 - по центру (х, у)
    if (mode==1):
        screen.blit(font.render(text, ttx, color),(place[0]*resize,place[1]*resize))
    elif (mode==2):
        texti=font.render(text, ttx, color)
        if (alpha!=0):
            texti.set_alpha(alpha)
        screen.blit(texti,(screen_size-texti.get_rect()[2]-otstup_ot_kraja,place[1]*resize))
    elif (mode==3):
        texti=font.render(text, ttx, color)
        if (alpha!=0):
            texti.set_alpha(alpha)
        screen.blit(texti,(0+otstup_ot_kraja,place[1]*resize))
    elif (mode==4):
        texti=font.render(text, ttx, color)
        if (alpha!=0):
            texti.set_alpha(alpha)
        screen.blit(texti,((screen_size-texti.get_rect()[2])//2+place[0]*resize,place[1]*resize))
    elif (mode==5):
        texti=font.render(text, ttx, color)
        if (alpha!=0):
            texti.set_alpha(alpha)
        screen.blit(texti, ((place[0]*resize)-(texti.get_rect()[2]//2), (place[1]*resize)-(texti.get_rect()[3]//2)))
        #screen.blit(texti,((screen_size-texti.get_rect()[2])//2+place[0]*resize,(screen_size-texti.get_rect()[3])//2+place[1]*resize))
    
starting=True

lfont12=pygame.font.Font('resources/Themes/Default/resources/font.ttf', 12*resize)

def loading_screen():
    global display
    logo=pygame.image.load("resources/Themes/Default/resources/logo.png").convert_alpha().convert_alpha()
    logo=pygame.transform.scale(logo, (logo.get_rect()[2]*resize,logo.get_rect()[3]*resize))
    loading_circle=pygame.image.load("resources/Themes/Default/resources/loading_circle.png").convert_alpha()
    loading_circle=pygame.transform.scale(loading_circle,(50*resize,50*resize))
    ugol=0
    while (starting):
        screen.fill((0,0,0))
        screen.blit(logo, (40*resize, 0*resize))
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit()
        ugol+=3
        if (ugol==360):
            ugol=0
        rotated=pygame.transform.rotozoom(loading_circle,-ugol,1)
        screen.blit(rotated,rotated.get_rect(center=(220*resize,380*resize)))
        s_text(loading_screen_to_show, True, (0,420), (255,255,255), 4, lfont12)
        pygame.display.flip()
        fps.tick(60)
screen=pygame.display.set_mode((screen_size, screen_size))
Thread(target=loading_screen).start()
pygame.display.set_icon(pygame.image.load("resources/Themes/Default/resources/logo.png").convert_alpha())
pygame.display.set_caption('Tetris')
#
#cbg, marathon_button10im, matarhon_button11im, settings_button10im, settings_button11im, scores_button10im, scores_button11im, logo, icon, back_button10im, back_button11im, font=0,0,0,0,0,0,0,0,0,0,0,0
if (os.path.isdir('tuol')):
    loading_screen_to_show="Обновление тем при запуске..."
    for i in os.listdir("tuol"):
        try:
            shutil.rmtree("resources/Themes/"+i)
        except:
            pass
        shutil.move("tuol/"+i, "resources/Themes/")
    shutil.rmtree("tuol")
if (len(settings["rtol"])>0):
    loading_screen_to_show="Запланированное удаление тем при запуске..."
    for i in settings["rtol"]:
        try:
            shutil.rmtree("resources/Themes/"+i)
        except:
            pass
settings["rtol"]=[]
save_settings()

def reload_resources(directory):
    global loading_screen_to_show
    global bg, cbg, marathon_button10im, marathon_button11im, settings_button10im, settings_button11im, scores_button10im, scores_button11im, back_button10im, back_button11im, up_button10im, up_button11im, down_button10im, down_button11im, mat_button10im, mat_button11im, info_button10im, info_button11im, themes_button10im, themes_button11im, music_button10im, music_button11im, screen
    global logo, icon, font, bigfont, font18, font12, font20, font22, hugefont, aqua, blue, green, orange, purple, yellow, red, grey, projection, clear_animation_0, clear_animation_1, clear_animation_2, clear_animation_3, clear_animation_4, clear_animation_5, clear_animation_6, clear_animation_7, clear_animation_8, clear_animation_9, fall_effect, pause_bg, selection, loading_circle, noprev, tbg, ibtu, disc
    global red_disc, orange_disc, yellow_disc, green_disc, aqua_disc, blue_disc, purple_disc
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/bg.png"
    try:bg=pygame.image.load("resources/Themes/"+directory+"/resources/bg.png").convert_alpha()
    except:bg=pygame.image.load("resources/Themes/Default/resources/bg.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/pause_bg.png"
    try:pause_bg=pygame.image.load("resources/Themes/"+directory+"/resources/pause_bg.png").convert_alpha()
    except:pause_bg=pygame.image.load("resources/Themes/Default/resources/pause_bg.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/cbg.png"
    try:cbg=pygame.image.load("resources/Themes/"+directory+"/resources/cbg.png").convert_alpha()
    except:cbg=pygame.image.load("resources/Themes/Default/resources/cbg.png").convert_alpha()
    
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/marathon_button10im.png"
    try:marathon_button10im=pygame.image.load("resources/Themes/"+directory+"/resources/marathon_button10im.png").convert_alpha()
    except:marathon_button10im=pygame.image.load("resources/Themes/Default/resources/marathon_button10im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/marathon_button11im.png"
    try:marathon_button11im=pygame.image.load("resources/Themes/"+directory+"/resources/marathon_button11im.png").convert_alpha()
    except:marathon_button11im=pygame.image.load("resources/Themes/Default/resources/marathon_button11im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/settings_button10im.png"
    try:settings_button10im=pygame.image.load("resources/Themes/"+directory+"/resources/settings_button10im.png").convert_alpha()
    except:settings_button10im=pygame.image.load("resources/Themes/Default/resources/settings_button10im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/settings_button11im.png"
    try:settings_button11im=pygame.image.load("resources/Themes/"+directory+"/resources/settings_button11im.png").convert_alpha()
    except:settings_button11im=pygame.image.load("resources/Themes/Default/resources/settings_button11im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/scores_button10im.png"
    try:scores_button10im=pygame.image.load("resources/Themes/"+directory+"/resources/scores_button10im.png").convert_alpha()
    except:scores_button10im=pygame.image.load("resources/Themes/Default/resources/scores_button10im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/scores_button11im.png"
    try:scores_button11im=pygame.image.load("resources/Themes/"+directory+"/resources/scores_button11im.png").convert_alpha()
    except:scores_button11im=pygame.image.load("resources/Themes/Default/resources/scores_button11im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/back_button10im.png"
    try:back_button10im=pygame.image.load("resources/Themes/"+directory+"/resources/back_button10im.png").convert_alpha()
    except:back_button10im=pygame.image.load("resources/Themes/Default/resources/back_button10im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/back_button11im.png"
    try:back_button11im=pygame.image.load("resources/Themes/"+directory+"/resources/back_button11im.png").convert_alpha()
    except:back_button11im=pygame.image.load("resources/Themes/Default/resources/back_button11im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/up_button10im.png"
    try:up_button10im=pygame.image.load("resources/Themes/"+directory+"/resources/up_button10im.png").convert_alpha()
    except:up_button10im=pygame.image.load("resources/Themes/Default/resources/up_button10im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/up_button11im.png"
    try:up_button11im=pygame.image.load("resources/Themes/"+directory+"/resources/up_button11im.png").convert_alpha()
    except:up_button11im=pygame.image.load("resources/Themes/Default/resources/up_button11im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/down_button10im.png"
    try:down_button10im=pygame.image.load("resources/Themes/"+directory+"/resources/down_button10im.png").convert_alpha()
    except:down_button10im=pygame.image.load("resources/Themes/Default/resources/down_button10im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/down_button11im.png"
    try:down_button11im=pygame.image.load("resources/Themes/"+directory+"/resources/down_button11im.png").convert_alpha()
    except:down_button11im=pygame.image.load("resources/Themes/Default/resources/down_button11im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/mat_button10im.png"
    try:mat_button10im=pygame.image.load("resources/Themes/"+directory+"/resources/mat_button10im.png").convert_alpha()
    except:mat_button10im=pygame.image.load("resources/Themes/Default/resources/mat_button10im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/mat_button11im.png"
    try:mat_button11im=pygame.image.load("resources/Themes/"+directory+"/resources/mat_button11im.png").convert_alpha()
    except:mat_button11im=pygame.image.load("resources/Themes/Default/resources/mat_button11im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/info_button10im.png"
    try:info_button10im=pygame.image.load("resources/Themes/"+directory+"/resources/info_button10im.png").convert_alpha()
    except:info_button10im=pygame.image.load("resources/Themes/Default/resources/info_button10im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/info_button11im.png"
    try:info_button11im=pygame.image.load("resources/Themes/"+directory+"/resources/info_button11im.png").convert_alpha()
    except:info_button11im=pygame.image.load("resources/Themes/Default/resources/info_button11im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/themes_button10im.png"
    try:themes_button10im=pygame.image.load("resources/Themes/"+directory+"/resources/themes_button10im.png").convert_alpha()
    except:themes_button10im=pygame.image.load("resources/Themes/Default/resources/themes_button10im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/themes_button11im.png"
    try:themes_button11im=pygame.image.load("resources/Themes/"+directory+"/resources/themes_button11im.png").convert_alpha()
    except:themes_button11im=pygame.image.load("resources/Themes/Default/resources/themes_button11im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/music_button10im.png"
    try:music_button10im=pygame.image.load("resources/Themes/"+directory+"/resources/music_button10im.png").convert_alpha()
    except:music_button10im=pygame.image.load("resources/Themes/Default/resources/music_button10im.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/music_button11im.png"
    try:music_button11im=pygame.image.load("resources/Themes/"+directory+"/resources/music_button11im.png").convert_alpha()
    except:music_button11im=pygame.image.load("resources/Themes/Default/resources/music_button11im.png").convert_alpha()
    
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/logo.png"
    try:logo=pygame.image.load("resources/Themes/"+directory+"/resources/logo.png").convert_alpha()
    except:logo=pygame.image.load("resources/Themes/Default/resources/logo.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/logo.png"
    try:icon=pygame.image.load("resources/Themes/"+directory+"/resources/logo.png").convert_alpha()
    except:icon=pygame.image.load("resources/Themes/Default/resources/logo.png").convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Tetris')
    
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/selection.png"
    try:selection=pygame.image.load("resources/Themes/"+directory+"/resources/selection.png").convert_alpha()
    except:selection=pygame.image.load("resources/Themes/Default/resources/selection.png").convert_alpha()

    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/aqua.png"
    try:aqua=pygame.image.load("resources/Themes/"+directory+"/resources/aqua.png").convert_alpha()
    except:aqua=pygame.image.load("resources/Themes/Default/resources/aqua.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/blue.png"
    try:blue=pygame.image.load("resources/Themes/"+directory+"/resources/blue.png").convert_alpha()
    except:blue=pygame.image.load("resources/Themes/Default/resources/blue.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/green.png"
    try:green=pygame.image.load("resources/Themes/"+directory+"/resources/green.png").convert_alpha()
    except:green=pygame.image.load("resources/Themes/Default/resources/green.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/orange.png"
    try:orange=pygame.image.load("resources/Themes/"+directory+"/resources/orange.png").convert_alpha()
    except:orange=pygame.image.load("resources/Themes/Default/resources/orange.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/purple.png"
    try:purple=pygame.image.load("resources/Themes/"+directory+"/resources/purple.png").convert_alpha()
    except:purple=pygame.image.load("resources/Themes/Default/resources/purple.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/yellow.png"
    try:yellow=pygame.image.load("resources/Themes/"+directory+"/resources/yellow.png").convert_alpha()
    except:yellow=pygame.image.load("resources/Themes/Default/resources/yellow.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/red.png"
    try:red=pygame.image.load("resources/Themes/"+directory+"/resources/red.png").convert_alpha()
    except:red=pygame.image.load("resources/Themes/Default/resources/red.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/grey.png"
    try:grey=pygame.image.load("resources/Themes/"+directory+"/resources/grey.png").convert_alpha()
    except:grey=pygame.image.load("resources/Themes/Default/resources/grey.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/projection.png"
    try:projection=pygame.image.load("resources/Themes/"+directory+"/resources/projection.png").convert_alpha()
    except:projection=pygame.image.load("resources/Themes/Default/resources/projection.png").convert_alpha()
    
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/font.ttf"
    try:font=pygame.font.Font('resources/Themes/'+directory+'/resources/font.ttf', 24*resize)
    except:font=pygame.font.Font('resources/Themes/Default/resources/font.ttf', 24*resize)
    try:bigfont=pygame.font.Font('resources/Themes/'+directory+'/resources/font.ttf', 30*resize)
    except:bigfont=pygame.font.Font('resources/Themes/Default/resources/font.ttf', 30*resize)
    try:font22=pygame.font.Font('resources/Themes/'+directory+'/resources/font.ttf', 22*resize)
    except:font22=pygame.font.Font('resources/Themes/Default/resources/font.ttf', 22*resize)
    try:font12=pygame.font.Font('resources/Themes/'+directory+'/resources/font.ttf', 12*resize)
    except:font12=pygame.font.Font('resources/Themes/Default/resources/font.ttf', 12*resize)
    try:font20=pygame.font.Font('resources/Themes/'+directory+'/resources/font.ttf', 20*resize)
    except:font20=pygame.font.Font('resources/Themes/Default/resources/font.ttf', 20*resize)
    try:font18=pygame.font.Font('resources/Themes/'+directory+'/resources/font.ttf', 18*resize)
    except:font18=pygame.font.Font('resources/Themes/Default/resources/font.ttf', 18*resize)
    try:hugefont=pygame.font.Font('resources/Themes/'+directory+'/resources/font.ttf', 144*resize)
    except:hugefont=pygame.font.Font('resources/Themes/Default/resources/font.ttf', 144*resize)
    
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/clear_animation/0.png"
    try:clear_animation_0=pygame.image.load("resources/Themes/"+directory+"/resources/clear_animation/0.png").convert_alpha()
    except:clear_animation_0=pygame.image.load("resources/Themes/Default/resources/clear_animation/0.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/clear_animation/1.png"
    try:clear_animation_1=pygame.image.load("resources/Themes/"+directory+"/resources/clear_animation/1.png").convert_alpha()
    except:clear_animation_1=pygame.image.load("resources/Themes/Default/resources/clear_animation/1.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/clear_animation/2.png"
    try:clear_animation_2=pygame.image.load("resources/Themes/"+directory+"/resources/clear_animation/2.png").convert_alpha()
    except:clear_animation_2=pygame.image.load("resources/Themes/Default/resources/clear_animation/2.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/clear_animation/3.png"
    try:clear_animation_3=pygame.image.load("resources/Themes/"+directory+"/resources/clear_animation/3.png").convert_alpha()
    except:clear_animation_3=pygame.image.load("resources/Themes/Default/resources/clear_animation/3.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/clear_animation/4.png"
    try:clear_animation_4=pygame.image.load("resources/Themes/"+directory+"/resources/clear_animation/4.png").convert_alpha()
    except:clear_animation_4=pygame.image.load("resources/Themes/Default/resources/clear_animation/4.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/clear_animation/5.png"
    try:clear_animation_5=pygame.image.load("resources/Themes/"+directory+"/resources/clear_animation/5.png").convert_alpha()
    except:clear_animation_5=pygame.image.load("resources/Themes/Default/resources/clear_animation/5.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/clear_animation/6.png"
    try:clear_animation_6=pygame.image.load("resources/Themes/"+directory+"/resources/clear_animation/6.png").convert_alpha()
    except:clear_animation_6=pygame.image.load("resources/Themes/Default/resources/clear_animation/6.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/clear_animation/7.png"
    try:clear_animation_7=pygame.image.load("resources/Themes/"+directory+"/resources/clear_animation/7.png").convert_alpha()
    except:clear_animation_7=pygame.image.load("resources/Themes/Default/resources/clear_animation/7.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/clear_animation/8.png"
    try:clear_animation_8=pygame.image.load("resources/Themes/"+directory+"/resources/clear_animation/8.png").convert_alpha()
    except:clear_animation_8=pygame.image.load("resources/Themes/Default/resources/clear_animation/8.png").convert_alpha()
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/clear_animation/9.png"
    try:clear_animation_9=pygame.image.load("resources/Themes/"+directory+"/resources/clear_animation/9.png").convert_alpha()
    except:clear_animation_9=pygame.image.load("resources/Themes/Default/resources/clear_animation/9.png").convert_alpha()
    
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/fall_effect.png"
    try:fall_effect=pygame.image.load("resources/Themes/"+directory+"/resources/fall_effect.png").convert_alpha()
    except:fall_effect=pygame.image.load("resources/Themes/Default/resources/fall_effect.png").convert_alpha()

    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/noprev.png"
    try:noprev=pygame.image.load("resources/Themes/"+directory+"/resources/noprev.png").convert_alpha()
    except:noprev=pygame.image.load("resources/Themes/Default/resources/noprev.png").convert_alpha()

    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/tbg.png"
    try:tbg=pygame.image.load("resources/Themes/"+directory+"/resources/tbg.png").convert_alpha()
    except:tbg=pygame.image.load("resources/Themes/Default/resources/tbg.png").convert_alpha()

    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/ibtu.png"
    try:ibtu=pygame.image.load("resources/Themes/"+directory+"/resources/ibtu.png").convert_alpha()
    except:ibtu=pygame.image.load("resources/Themes/Default/resources/ibtu.png").convert_alpha()

    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/resources/disc.png"
    try:disc=pygame.image.load("resources/Themes/"+directory+"/resources/disc.png").convert_alpha()
    except:disc=pygame.image.load("resources/Themes/Default/resources/disc.png").convert_alpha()

    loading_screen_to_show="Изменение размеров ресурсов..."
    bg=pygame.transform.scale(bg, (screen_size, screen_size))
    pause_bg=pygame.transform.scale(pause_bg, (screen_size, screen_size))
    cbg=pygame.transform.scale(cbg, (screen_size, screen_size))
    logo=pygame.transform.scale(logo, (360*resize, 360*resize))#logo.get_rect()[2]*resize,logo.get_rect()[3]*resize))
    marathon_button10im=pygame.transform.scale(marathon_button10im, (marathon_button[0][0]*resize, marathon_button[0][1]*resize))
    marathon_button11im=pygame.transform.scale(marathon_button11im, (marathon_button[0][0]*resize, marathon_button[0][1]*resize))
    settings_button10im=pygame.transform.scale(settings_button10im, (settings_button[0][0]*resize, settings_button[0][1]*resize))
    settings_button11im=pygame.transform.scale(settings_button11im, (settings_button[0][0]*resize, settings_button[0][1]*resize))
    scores_button10im=pygame.transform.scale(scores_button10im, (scores_button[0][0]*resize, scores_button[0][1]*resize))
    scores_button11im=pygame.transform.scale(scores_button11im, (scores_button[0][0]*resize, scores_button[0][1]*resize))
    back_button10im=pygame.transform.scale(back_button10im, (back_button[0][0]*resize, back_button[0][1]*resize))
    back_button11im=pygame.transform.scale(back_button11im, (back_button[0][0]*resize, back_button[0][1]*resize))
    up_button10im=pygame.transform.scale(up_button10im, (up_button[0][0]*resize, up_button[0][1]*resize))
    up_button11im=pygame.transform.scale(up_button11im, (up_button[0][0]*resize, up_button[0][1]*resize))
    down_button10im=pygame.transform.scale(down_button10im, (down_button[0][0]*resize, down_button[0][1]*resize))
    down_button11im=pygame.transform.scale(down_button11im, (down_button[0][0]*resize, down_button[0][1]*resize))
    mat_button10im=pygame.transform.scale(mat_button10im, (mat_button[0][0]*resize, mat_button[0][1]*resize))
    mat_button11im=pygame.transform.scale(mat_button11im, (mat_button[0][0]*resize, mat_button[0][1]*resize))
    info_button10im=pygame.transform.scale(info_button10im, (info_button[0][0]*resize, info_button[0][1]*resize))
    info_button11im=pygame.transform.scale(info_button11im, (info_button[0][0]*resize, info_button[0][1]*resize))
    themes_button10im=pygame.transform.scale(themes_button10im, (themes_button[0][0]*resize, themes_button[0][1]*resize))
    themes_button11im=pygame.transform.scale(themes_button11im, (themes_button[0][0]*resize, themes_button[0][1]*resize))
    music_button10im=pygame.transform.scale(music_button10im, (music_button[0][0]*resize, music_button[0][1]*resize))
    music_button11im=pygame.transform.scale(music_button11im, (music_button[0][0]*resize, music_button[0][1]*resize))
    
    aqua=pygame.transform.scale(aqua, (piece_part_size, piece_part_size))
    blue=pygame.transform.scale(blue, (piece_part_size, piece_part_size))
    green=pygame.transform.scale(green, (piece_part_size, piece_part_size))
    orange=pygame.transform.scale(orange, (piece_part_size, piece_part_size))
    purple=pygame.transform.scale(purple, (piece_part_size, piece_part_size))
    yellow=pygame.transform.scale(yellow, (piece_part_size, piece_part_size))
    red=pygame.transform.scale(red, (piece_part_size, piece_part_size))
    grey=pygame.transform.scale(grey, (piece_part_size, piece_part_size))
    projection=pygame.transform.scale(projection, (piece_part_size, piece_part_size))

    clear_animation_0=pygame.transform.scale(clear_animation_0, (240*resize, 40*resize))
    clear_animation_1=pygame.transform.scale(clear_animation_1, (240*resize, 40*resize))
    clear_animation_2=pygame.transform.scale(clear_animation_2, (240*resize, 40*resize))
    clear_animation_3=pygame.transform.scale(clear_animation_3, (240*resize, 40*resize))
    clear_animation_4=pygame.transform.scale(clear_animation_4, (240*resize, 40*resize))
    clear_animation_5=pygame.transform.scale(clear_animation_5, (240*resize, 40*resize))
    clear_animation_6=pygame.transform.scale(clear_animation_6, (240*resize, 40*resize))
    clear_animation_7=pygame.transform.scale(clear_animation_7, (240*resize, 40*resize))
    clear_animation_8=pygame.transform.scale(clear_animation_8, (240*resize, 40*resize))
    clear_animation_9=pygame.transform.scale(clear_animation_9, (240*resize, 40*resize))

    fall_effect=pygame.transform.scale(fall_effect, (piece_part_size, piece_part_size))
    selection=pygame.transform.scale(selection, (340*resize, 120*resize))
    noprev=pygame.transform.scale(noprev, (100*resize, 100*resize))
    tbg=pygame.transform.scale(tbg, (360*resize, 100*resize))
    ibtu=pygame.transform.scale(ibtu, (360*resize, 40*resize))
    disc=pygame.transform.scale(disc, (150*resize, 150*resize))

    global row_1, row_2, row_3, row_4, e_move_right, e_move_left, e_move_error, pause_music, menu_music, nav, nav_back, e_drop, e_hard_drop, e_rotation_right, e_rotation_left, e_tm_p, e_tm_p_error, start_sound, game_over_sound, e_perfect_clear
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/pause_music.ogg"
    try:pause_music=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/pause_music.ogg")
    except:pause_music=pygame.mixer.Sound("resources/Themes/Default/mf/pause_music.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/perfect_clear.ogg"
    try:e_perfect_clear=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/perfect_clear.ogg")
    except:e_perfect_clear=pygame.mixer.Sound("resources/Themes/Default/mf/perfect_clear.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/1_row.ogg"
    try:row_1=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/1_row.ogg")
    except:row_1=pygame.mixer.Sound("resources/Themes/Default/mf/1_row.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/2_row.ogg"
    try:row_2=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/2_row.ogg")
    except:row_2=pygame.mixer.Sound("resources/Themes/Default/mf/2_row.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/3_row.ogg"
    try:row_3=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/3_row.ogg")
    except:row_3=pygame.mixer.Sound("resources/Themes/Default/mf/3_row.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/4_row.ogg"
    try:row_4=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/4_row.ogg")
    except:row_4=pygame.mixer.Sound("resources/Themes/Default/mf/4_row.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/e_move_right.ogg"
    try:e_move_right=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/e_move_right.ogg")
    except:e_move_right=pygame.mixer.Sound("resources/Themes/Default/mf/e_move_right.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/e_move_left.ogg"
    try:e_move_left=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/e_move_left.ogg")
    except:e_move_left=pygame.mixer.Sound("resources/Themes/Default/mf/e_move_left.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/e_move_error.ogg"
    try:e_move_error=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/e_move_error.ogg")
    except:e_move_error=pygame.mixer.Sound("resources/Themes/Default/mf/e_move_error.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/menu.ogg"
    try:menu_music=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/menu.ogg")
    except:menu_music=pygame.mixer.Sound("resources/Themes/Default/mf/menu.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/nav.ogg"
    try:nav=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/nav.ogg")
    except:nav=pygame.mixer.Sound("resources/Themes/Default/mf/nav.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/nav_back.ogg"
    try:nav_back=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/nav_back.ogg")
    except:nav_back=pygame.mixer.Sound("resources/Themes/Default/mf/nav_back.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/e_drop.ogg"
    try:e_drop=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/e_drop.ogg")
    except:e_drop=pygame.mixer.Sound("resources/Themes/Default/mf/e_drop.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/e_hard_drop.ogg"
    try:e_hard_drop=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/e_hard_drop.ogg")
    except:e_hard_drop=pygame.mixer.Sound("resources/Themes/Default/mf/e_hard_drop.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/e_rotation_right.ogg"
    try:e_rotation_right=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/e_rotation_right.ogg")
    except:e_rotation_right=pygame.mixer.Sound("resources/Themes/Default/mf/e_rotation_right.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/e_rotation_left.ogg"
    try:e_rotation_left=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/e_rotation_left.ogg")
    except:e_rotation_left=pygame.mixer.Sound("resources/Themes/Default/mf/e_rotation_left.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/e_tm_p.ogg"
    try:e_tm_p=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/e_tm_p.ogg")
    except:e_tm_p=pygame.mixer.Sound("resources/Themes/Default/mf/e_tm_p.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/e_tm_p_error.ogg"
    try:e_tm_p_error=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/e_tm_p_error.ogg")
    except:e_tm_p_error=pygame.mixer.Sound("resources/Themes/Default/mf/e_tm_p_error.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/start.ogg"
    try:start_sound=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/start.ogg")
    except:start_sound=pygame.mixer.Sound("resources/Themes/Default/mf/start.ogg")
    loading_screen_to_show="Загрузка ресурса resources/Themes/"+directory+"/mf/game_over.ogg"
    try:game_over_sound=pygame.mixer.Sound("resources/Themes/"+directory+"/mf/game_over.ogg")
    except:game_over_sound=pygame.mixer.Sound("resources/Themes/Default/mf/game_over.ogg")

    global bred, bpred, borange, bporange, byellow, bpyellow, bgreen, bpgreen, baqua, bpaqua, bblue, bpblue, bpurple, bppurple, bblack, bpblack, bdred, bdgreen
    
    loading_screen_to_show="Получение информации из resources/Themes/"+directory+"/theme.json"
    bred=(222, 37, 37)
    bpred=(255, 74, 74)
    borange=(238, 89, 7)
    bporange=(255, 178, 14)
    byellow=(255, 174, 0)
    bpyellow=(255, 255, 0)
    bgreen=(6, 164, 11)
    bpgreen=(12, 255, 22)
    baqua=(41, 154, 255)
    bpaqua=(90, 255, 255)
    bblue=(43, 83, 173)
    bpblue=(89, 151, 250)
    bpurple=(124, 87, 180)
    bppurple=(248, 174, 155)

    bblack=(0,0,0)
    bpblack=(50,50,50)

    bdred=(111,18,18)
    bdgreen=(3,82,5)
    try:
        with open("resources/Themes/"+directory+"/theme.json") as file:
            theme_data=json.load(file)
        try:
            bred=theme_data["colors"]["bred"]
            bpred=theme_data["colors"]["bpred"]
            borange=theme_data["colors"]["borange"]
            bporange=theme_data["colors"]["bporange"]
            byellow=theme_data["colors"]["byellow"]
            bpyellow=theme_data["colors"]["bpyellow"]
            bgreen=theme_data["colors"]["bgreen"]
            bpgreen=theme_data["colors"]["bpgreen"]
            baqua=theme_data["colors"]["baqua"]
            bpaqua=theme_data["colors"]["bpaqua"]
            bblue=theme_data["colors"]["bblue"]
            bpblue=theme_data["colors"]["bpblue"]
            bpurple=theme_data["colors"]["bpurple"]
            bppurple=theme_data["colors"]["bppurple"]

            bblack=theme_data["colors"]["bblack"]
            bpblack=theme_data["colors"]["bpblack"]

            bdred=theme_data["colors"]["bdred"]
            bdgreen=theme_data["colors"]["bdgreen"]
        except:
            pass
    except:
        pass
    loading_screen_to_show="Крашу диски..."
    
    red_disc=colorize(disc, bred)
    orange_disc=colorize(disc, borange)
    yellow_disc=colorize(disc, byellow)
    green_disc=colorize(disc, bgreen)
    aqua_disc=colorize(disc, baqua)
    blue_disc=colorize(disc, bblue)
    purple_disc=colorize(disc, bpurple)
    
    loading_screen_to_show=""
    
def load_music(name):
    global music
    try:
        music=pygame.mixer.Sound("resources/Music/"+name)
    except:
        music=pygame.mixer.Sound("resources/Music/Default.ogg")
        
def change_volume(new=True):
    global row_1, row_2, row_3, row_4, e_move_right, e_move_left, e_move_error, pause_music, menu_music, nav, nav_back, e_drop, e_hard_drop, e_rotation_right, e_rotation_left, e_tm_p, e_tm_p_error, start_sound, game_over_sound, e_perfect_clear
    global pause_music_channel, music_channel, effect_channel
    e_perfect_clear.set_volume(settings["effect_volume"])
    row_1.set_volume(settings["effect_volume"])
    row_2.set_volume(settings["effect_volume"])
    row_3.set_volume(settings["effect_volume"])
    row_4.set_volume(settings["effect_volume"])
    e_move_right.set_volume(settings["effect_volume"])
    e_move_left.set_volume(settings["effect_volume"])
    e_move_error.set_volume(settings["effect_volume"])
    #pause_music.set_volume(settings["effect_volume"])
    #menu_music.set_volume(settings["effect_volume"])
    nav.set_volume(settings["effect_volume"])
    nav_back.set_volume(settings["effect_volume"])
    e_drop.set_volume(settings["effect_volume"])
    e_hard_drop.set_volume(settings["effect_volume"])
    e_rotation_left.set_volume(settings["effect_volume"])
    e_rotation_right.set_volume(settings["effect_volume"])
    e_tm_p.set_volume(settings["effect_volume"])
    e_tm_p_error.set_volume(settings["effect_volume"])
    start_sound.set_volume(settings["effect_volume"])
    game_over_sound.set_volume(settings["effect_volume"])
    if (new):
        pause_music_channel.set_volume(polzunok_music_volume[1]/100)
        music_channel.set_volume(polzunok_music_volume[1]/100)
        effect_channel.set_volume(polzunok_sound_volume[1]/100)
    else:
        pause_music_channel.set_volume(polzunok_music[1]/100)
        music_channel.set_volume(polzunok_music[1]/100)
        effect_channel.set_volume(polzunok_sound[1]/100)
    
#значения
piece_cd_move_time=settings["piece_cd_move_time"]
piece_cd_moveD_time=0.5
piece_part_size=20*resize
otstup_ot_kraja=20*resize
g_overed=False
show_ib=False
toggleaf=settings["toggleaf"]
togglefall=settings["togglefall"]
togglecleara=settings["togglecleara"]
toggleproection=settings["toggleproection"]

reload_resources(settings["theme"])
launch_theme=settings["theme"]

music_channel=pygame.mixer.Channel(1)
effect_channel=pygame.mixer.Channel(2)
pause_music_channel=pygame.mixer.Channel(3)
music_channel.set_volume(settings["music_volume"])
effect_channel.set_volume(settings["effect_volume"])
pause_music_channel.set_volume(settings["music_volume"])

load_music(settings["music"])

#speed_levels_frames=[52,48,44,40,36,32,27,21,16,10,9,8,7,6,5,4,3,2,2]
#speed_levels_frames=[60,50,40,30,20,10,8,6,4,2,1]
#                   0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22    23    24    25    26    27    28    29    30    31    32    33    34    35    36
change_time_sec=[0.50, 0.50, 0.49, 0.48, 0.47, 0.46, 0.45, 0.44, 0.43, 0.42, 0.41, 0.40, 0.39, 0.38, 0.37, 0.36, 0.35, 0.34, 0.33, 0.32, 0.31, 0.30, 0.28, 0.26, 0.24, 0.22, 0.20, 0.17, 0.18, 0.16, 0.15, 0.14, 0.13, 0.12, 0.11, 0.10, 0.08, 0.07, 0.06, 0.05]
speed_levels_frames=[60,52,44,36,28,24,20,16,12,8,7,6,5,4,3,2,1]
speed_levels=[]
for i in speed_levels_frames:
    speed_levels.append(1*i/60)
    #speed_levels.append(round(1*i/60,1))
#print(speed_levels)

#button data     size (x,y), position (x,y), color (r,g,b) или переменная с картинкой, color_preshed(r,g,b) или переменная с картинкой
#
#
#
polzunok_music=[[230,210],int(settings["music_volume"]*100)]
polzunok_sound=[[230,240],int(settings["effect_volume"]*100)]
polzunok_music_volume=[[230,310],int(settings["music_volume"]*100)]
polzunok_sound_volume=[[230,340],int(settings["effect_volume"]*100)]
#polzunok_pcdmt=[[120,330],int(settings["piece_cd_move_time"]*100)]
#
def polzunok_sp_check(name, start_pos):
    if ((name[0][0]-20)*resize<=start_pos[0]<=(name[0][0]+200+10)*resize and (name[0][1]-10)*resize<=start_pos[1]<=(name[0][1]+10)*resize):
        return True
    return False
def polzunok(name, start_pos):
    if (not polzunok_sp_check(name, start_pos)):
        return name[1]
    mouse_pos=pygame.mouse.get_pos()
    if (name[0][0]*resize>mouse_pos[0]):
        return 0
    elif (mouse_pos[0]>(name[0][0]+200)*resize):
        return 100
    elif (name[0][0]*resize<=mouse_pos[0]<=(name[0][0]+200)*resize):# and name[0][1]-5<=mouse_pos[1]<=name[0][1]+5):
        return ((mouse_pos[0]-name[0][0]*resize)//(2*resize))
    return name[1]
def polzunok_ris(name):
    pygame.draw.rect(screen, (200,200,200), (name[0][0]*resize, (name[0][1]-2)*resize, (name[1]*2)*resize, 4*resize))
    pygame.draw.rect(screen, (125,125,125), ((name[0][0]+name[1]*2)*resize, (name[0][1]-2)*resize, (100-name[1])*2*resize, 4*resize))
    pygame.draw.rect(screen, (255,255,255), ((name[1]*2+name[0][0]-8)*resize, (name[0][1]-10)*resize, 16*resize, 20*resize))
#40-19//2+20
def draw_button(button_data, color, text, tfont=font):
    pygame.draw.rect(screen, color, (button_data[1][0]*resize, button_data[1][1]*resize, button_data[0][0]*resize, button_data[0][1]*resize))
    texti=tfont.render(text, True, (255,255,255))
    screen.blit(texti,((button_data[0][0]*resize-texti.get_rect()[2])//2+button_data[1][0]*resize,(button_data[0][1]*resize-texti.get_rect()[3])//2+button_data[1][1]*resize))
    
def press_check(button_data, mouse_pos):
    if (button_data[1][0]*resize<=mouse_pos[0]<button_data[1][0]*resize+button_data[0][0]*resize and button_data[1][1]*resize<=mouse_pos[1]<button_data[1][1]*resize+button_data[0][1]*resize):
        return True
    else:
        return False
    
def get_statistic():
    rewrite=False
    try:
        file=open("stats.dat","r")
        file_r=file.read()
        file.close()
        file_r=file_r.split()
        for i in file_r:
            int(i)
    except:
        rewrite=True
    if (rewrite):
        file=open("stats.dat","w")
        #           0        1        2        3        4        5        6        7        8        9        10       11       12       13       14       15       16       17       18       19       20       21       22       23       24       25       26       27       28       29       30       31       32       33       34       35       36       37       38       39
        file.write("0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0"+"\n"+"0")
        file.close()
        file=open("stats.dat","r")
        file_r=file.read()
        file.close()
        file_r=file_r.split()
    return file_r

def proekcija():
    global proekc
    proekc=copy.copy(padenie)
    while (True):
        #print("proekcija")
        piece_locations=get_piece_locations(proekc)
        if (len(piece_locations)!=4):
            return
        for i in piece_locations:
            if (i[0]+1>=bordery or positions[i[0]+1][i[1]]!=0):
                return
        for i in range(0,bordery):
            i=bordery-i-1
            proekc[i]=proekc[i-1]
        proekc[0]=[0,0,0,0,0,0,0,0,0,0]

def ris():
    global padenie, positions, resize
    screen.blit(bg, (0, 0))
    if (not toggleproection):
        proekcija()
        for i in range(0,borderx): #i - x
            for j in range(3,bordery): # j - y
                if (proekc[j][i]!=0):
                    screen.blit(projection, ((i*20+120)*resize, (j*20-40)*resize))
    i=0
    j=0
    for i in range(0,borderx): #i - x
        for j in range(3,bordery): # j - y
            if (positions[j][i]==1):
                screen.blit(orange, ((i*20+120)*resize, (j*20-40)*resize))
            if (positions[j][i]==2):
                screen.blit(blue, ((i*20+120)*resize, (j*20-40)*resize))
            if (positions[j][i]==3):
                screen.blit(red, ((i*20+120)*resize, (j*20-40)*resize))
            if (positions[j][i]==4):
                screen.blit(green, ((i*20+120)*resize, (j*20-40)*resize))
            if (positions[j][i]==5):
                screen.blit(yellow, ((i*20+120)*resize, (j*20-40)*resize))
            if (positions[j][i]==6):
                screen.blit(aqua, ((i*20+120)*resize, (j*20-40)*resize))
            if (positions[j][i]==7):
                screen.blit(purple, ((i*20+120)*resize, (j*20-40)*resize))
    i=0
    j=0
    for i in range(0,borderx): #i - x
        for j in range(3,bordery): # j - y
            if (padenie[j][i]==1):
                screen.blit(orange, ((i*20+120)*resize, (j*20-40)*resize))
            if (padenie[j][i]==2):
                screen.blit(blue, ((i*20+120)*resize, (j*20-40)*resize))
            if (padenie[j][i]==3):
                screen.blit(red, ((i*20+120)*resize, (j*20-40)*resize))
            if (padenie[j][i]==4):
                screen.blit(green, ((i*20+120)*resize, (j*20-40)*resize))
            if (padenie[j][i]==5):
                screen.blit(yellow, ((i*20+120)*resize, (j*20-40)*resize))
            if (padenie[j][i]==6):
                screen.blit(aqua, ((i*20+120)*resize, (j*20-40)*resize))
            if (padenie[j][i]==7):
                screen.blit(purple, ((i*20+120)*resize, (j*20-40)*resize))
    npsllris()
def npsllris():
    #s_text(str(score), True, (60, 332), (255, 255, 255), 5, font)
    #s_text(str(level), True, (60, 372), (255, 255, 255), 5, font)
    #s_text(str(linii), True, (60, 412), (255, 255, 255), 5, font)
    texti=font.render(str(score), True, (255,255,255))
    if (texti.get_rect()[2]<=80*resize):
        screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (332*resize)-(texti.get_rect()[3]//2)))
    else:
        texti=font22.render(str(score), True, (255,255,255))
        if (texti.get_rect()[2]<=80*resize):
            screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (332*resize)-(texti.get_rect()[3]//2)))
        else:
            texti=font20.render(str(score), True, (255,255,255))
            if (texti.get_rect()[2]<=80*resize):
                screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (332*resize)-(texti.get_rect()[3]//2)))
            else:
                texti=font18.render(str(score), True, (255,255,255))
                #if (texti.get_rect()[2]<=80*resize):
                screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (332*resize)-(texti.get_rect()[3]//2)))
        
    texti=font.render(str(level), True, (255,255,255))        
    if (texti.get_rect()[2]<=80*resize):
        screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (372*resize)-(texti.get_rect()[3]//2)))
    else:
        texti=font22.render(str(level), True, (255,255,255))
        if (texti.get_rect()[2]<=80*resize):
            screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (372*resize)-(texti.get_rect()[3]//2)))
        else:
            texti=font20.render(str(level), True, (255,255,255))
            if (texti.get_rect()[2]<=80*resize):
                screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (372*resize)-(texti.get_rect()[3]//2)))
            else:
                texti=font18.render(str(level), True, (255,255,255))
                #if (texti.get_rect()[2]<=80*resize):
                screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (372*resize)-(texti.get_rect()[3]//2)))

    texti=font.render(str(linii), True, (255,255,255))
    if (texti.get_rect()[2]<=80*resize):
        screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (412*resize)-(texti.get_rect()[3]//2)))
    else:
        texti=font22.render(str(linii), True, (255,255,255))
        if (texti.get_rect()[2]<=80*resize):
            screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (412*resize)-(texti.get_rect()[3]//2)))
        else:
            texti=font20.render(str(linii), True, (255,255,255))
            if (texti.get_rect()[2]<=80*resize):
                screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (412*resize)-(texti.get_rect()[3]//2)))
            else:
                texti=font18.render(str(linii), True, (255,255,255))
                #if (texti.get_rect()[2]<=80*resize):
                screen.blit(texti, ((60*resize)-(texti.get_rect()[2]//2), (412*resize)-(texti.get_rect()[3]//2)))
    #sb_score=font.render(str(score), True, (255, 255, 255))
    #screen.blit(sb_score,(20*resize,320*resize))
    #sb_level=font.render(str(level), True, (255, 255, 255))
    #screen.blit(sb_level,(20*resize,360*resize))
    #sb_linii=font.render(str(linii), True, (255, 255, 255))
    #screen.blit(sb_linii,(20*resize,400*resize))
    if (stat_tablo_to_show=="Back-To-Back TETRIS"):
        s_text("Back-To-Back", True, (160,352), (255,255,255), 4, font18)
        s_text("TETRIS", True, (160,370), (255,255,255), 4, font18)
    else:
        s_text(stat_tablo_to_show, True, (159,361), (255,255,255), 4, font18)
    if (next1==1):
        screen.blit(orange, (350*resize, 40*resize))
        screen.blit(orange, (370*resize, 40*resize))
        screen.blit(orange, (390*resize, 40*resize))
        screen.blit(orange, (390*resize, 20*resize))
    elif (next1==2):
        screen.blit(blue, (350*resize, 40*resize))
        screen.blit(blue, (370*resize, 40*resize))
        screen.blit(blue, (390*resize, 40*resize))
        screen.blit(blue, (350*resize, 20*resize))
    elif (next1==3):
        screen.blit(red, (350*resize, 20*resize))
        screen.blit(red, (370*resize, 20*resize))
        screen.blit(red, (370*resize, 40*resize))
        screen.blit(red, (390*resize, 40*resize))
    elif (next1==4):
        screen.blit(green, (350*resize, 40*resize))
        screen.blit(green, (370*resize, 40*resize))
        screen.blit(green, (370*resize, 20*resize))
        screen.blit(green, (390*resize, 20*resize))
    elif (next1==5):
        screen.blit(yellow, (360*resize, 40*resize))
        screen.blit(yellow, (360*resize, 20*resize))
        screen.blit(yellow, (380*resize, 40*resize))
        screen.blit(yellow, (380*resize, 20*resize))
    elif (next1==6):
        screen.blit(aqua, (340*resize, 40*resize))
        screen.blit(aqua, (360*resize, 40*resize))
        screen.blit(aqua, (380*resize, 40*resize))
        screen.blit(aqua, (400*resize, 40*resize))
    elif (next1==7):
        screen.blit(purple, (350*resize, 40*resize))
        screen.blit(purple, (370*resize, 40*resize))
        screen.blit(purple, (390*resize, 40*resize))
        screen.blit(purple, (370*resize, 20*resize))
    if (next2==1):
        screen.blit(orange, (350*resize, 100*resize))
        screen.blit(orange, (370*resize, 100*resize))
        screen.blit(orange, (390*resize, 100*resize))
        screen.blit(orange, (390*resize, 80*resize))
    elif (next2==2):
        screen.blit(blue, (350*resize, 100*resize))
        screen.blit(blue, (370*resize, 100*resize))
        screen.blit(blue, (390*resize, 100*resize))
        screen.blit(blue, (350*resize, 80*resize))
    elif (next2==3):
        screen.blit(red, (350*resize, 80*resize))
        screen.blit(red, (370*resize, 80*resize))
        screen.blit(red, (370*resize, 100*resize))
        screen.blit(red, (390*resize, 100*resize))
    elif (next2==4):
        screen.blit(green, (350*resize, 100*resize))
        screen.blit(green, (370*resize, 100*resize))
        screen.blit(green, (370*resize, 80*resize))
        screen.blit(green, (390*resize, 80*resize))
    elif (next2==5):
        screen.blit(yellow, (360*resize, 100*resize))
        screen.blit(yellow, (360*resize, 80*resize))
        screen.blit(yellow, (380*resize, 100*resize))
        screen.blit(yellow, (380*resize, 80*resize))
    elif (next2==6):
        screen.blit(aqua, (340*resize, 100*resize))
        screen.blit(aqua, (360*resize, 100*resize))
        screen.blit(aqua, (380*resize, 100*resize))
        screen.blit(aqua, (400*resize, 100*resize))
    elif (next2==7):
        screen.blit(purple, (350*resize, 100*resize))
        screen.blit(purple, (370*resize, 100*resize))
        screen.blit(purple, (390*resize, 100*resize))
        screen.blit(purple, (370*resize, 80*resize))
    if (next3==1):
        screen.blit(orange, (350*resize, 160*resize))
        screen.blit(orange, (370*resize, 160*resize))
        screen.blit(orange, (390*resize, 160*resize))
        screen.blit(orange, (390*resize, 140*resize))
    elif (next3==2):
        screen.blit(blue, (350*resize, 160*resize))
        screen.blit(blue, (370*resize, 160*resize))
        screen.blit(blue, (390*resize, 160*resize))
        screen.blit(blue, (350*resize, 140*resize))
    elif (next3==3):
        screen.blit(red, (350*resize, 140*resize))
        screen.blit(red, (370*resize, 140*resize))
        screen.blit(red, (370*resize, 160*resize))
        screen.blit(red, (390*resize, 160*resize))
    elif (next3==4):
        screen.blit(green, (350*resize, 160*resize))
        screen.blit(green, (370*resize, 160*resize))
        screen.blit(green, (370*resize, 140*resize))
        screen.blit(green, (390*resize, 140*resize))
    elif (next3==5):
        screen.blit(yellow, (360*resize, 160*resize))
        screen.blit(yellow, (360*resize, 140*resize))
        screen.blit(yellow, (380*resize, 160*resize))
        screen.blit(yellow, (380*resize, 140*resize))
    elif (next3==6):
        screen.blit(aqua, (340*resize, 160*resize))
        screen.blit(aqua, (360*resize, 160*resize))
        screen.blit(aqua, (380*resize, 160*resize))
        screen.blit(aqua, (400*resize, 160*resize))
    elif (next3==7):
        screen.blit(purple, (350*resize, 160*resize))
        screen.blit(purple, (370*resize, 160*resize))
        screen.blit(purple, (390*resize, 160*resize))
        screen.blit(purple, (370*resize, 140*resize))
    if (paused==1):
        screen.blit(orange, (30*resize, 40*resize))
        screen.blit(orange, (50*resize, 40*resize))
        screen.blit(orange, (70*resize, 40*resize))
        screen.blit(orange, (70*resize, 20*resize))
    elif (paused==2):
        screen.blit(blue, (30*resize, 40*resize))
        screen.blit(blue, (50*resize, 40*resize))
        screen.blit(blue, (70*resize, 40*resize))
        screen.blit(blue, (30*resize, 20*resize))
    elif (paused==3):
        screen.blit(red, (30*resize, 20*resize))
        screen.blit(red, (50*resize, 20*resize))
        screen.blit(red, (50*resize, 40*resize))
        screen.blit(red, (70*resize, 40*resize))
    elif (paused==4):
        screen.blit(green, (30*resize, 40*resize))
        screen.blit(green, (50*resize, 40*resize))
        screen.blit(green, (50*resize, 20*resize))
        screen.blit(green, (70*resize, 20*resize))
    elif (paused==5):
        screen.blit(yellow, (40*resize, 40*resize))
        screen.blit(yellow, (40*resize, 20*resize))
        screen.blit(yellow, (60*resize, 40*resize))
        screen.blit(yellow, (60*resize, 20*resize))
    elif (paused==6):
        screen.blit(aqua, (20*resize, 40*resize))
        screen.blit(aqua, (40*resize, 40*resize))
        screen.blit(aqua, (60*resize, 40*resize))
        screen.blit(aqua, (80*resize, 40*resize))
    elif (paused==7):
        screen.blit(purple, (30*resize, 40*resize))
        screen.blit(purple, (50*resize, 40*resize))
        screen.blit(purple, (70*resize, 40*resize))
        screen.blit(purple, (50*resize, 20*resize))

def menu_ris(menu_type):
    #а теперь эту функцию можно слить с menu()
    screen.blit(cbg,(0,0))
    if (menu_type==1):
        screen.blit(logo, (40*resize, 40*resize))
        screen.blit(marathon_button10im, (marathon_button[1][0]*resize,marathon_button[1][1]*resize))
        screen.blit(settings_button10im, (settings_button[1][0]*resize,settings_button[1][1]*resize))
        screen.blit(scores_button10im, (scores_button[1][0]*resize,scores_button[1][1]*resize))
        #screen.blit(mat_button10im, (mat_button[1][0]*resize,mat_button[1][1]*resize))
        screen.blit(info_button10im, (info_button[1][0]*resize,info_button[1][1]*resize))
        screen.blit(themes_button10im, (themes_button[1][0]*resize,themes_button[1][1]*resize))
        screen.blit(music_button10im, (music_button[1][0]*resize,music_button[1][1]*resize))
    elif (menu_type==2):
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
        draw_button(select_mat_button, bgreen, "Выбор темы")
    elif (menu_type==3):
        s_text("Статистика", True, (0,20), (255,255,255), 4, bigfont)
        
        stats=get_statistic()
        
        s_text(str(stats[0]), True, (0,60), (255,255,255), 2, font)
        s_text(str(stats[1]), True, (0,90), (255,255,255), 2, font)
        s_text(str(stats[2]), True, (0,120), (255,255,255), 2, font)
        s_text(str(stats[3]), True, (0,150), (255,255,255), 2, font)
        s_text(str(stats[4]), True, (0,180), (255,255,255), 2, font)
        s_text(str(stats[5]), True, (0,210), (255,255,255), 2, font)
        s_text(str(stats[6]), True, (0,240), (255,255,255), 2, font)
        s_text(str(stats[7]), True, (0,270), (255,255,255), 2, font)
        s_text(str(stats[8]), True, (0,300), (255,255,255), 2, font)
        s_text(str(stats[9]), True, (0,330), (255,255,255), 2, font)

        s_text("Рекорд Marathon:", True, (0,60), (255,255,255), 3, font)
        s_text("Рекорд Endless:", True, (0,90), (255,255,255), 3, font)
        s_text("Рекордный уровень:", True, (0,120), (255,255,255), 3, font)
        s_text("Рекорд по убранным линиям:", True, (0,150), (255,255,255), 3, font)
        s_text("Кол-во убранных линий:", True, (0,180), (255,255,255), 3, font)
        s_text("Одинарная расчистка линий:", True, (0,210), (255, 255, 255), 3, font)
        s_text("Двойная расчистка линий:", True, (0,240), (255, 255, 255), 3, font)
        s_text("Тройная расчистка линий:", True, (0,270), (255, 255, 255), 3, font)
        s_text("Расчистка линий \"TETRIS\":", True, (0,300), (255, 255, 255), 3, font)
        s_text("Кол-во комбо:", True, (0,330), (255, 255, 255), 3, font)
        
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
    elif (menu_type==4):
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
#
#

#переменные игры
bordery=23
borderx=10
#создание функций игры
def n_level():
    global level
    level=linii//10+1

def clear_ris(removed):
    screen.fill((0,0,0))
    screen.blit(bg, (0, 0))
    for j in range(3,bordery): #i - x
        if (j not in removed):
            for i in range(0,borderx): # j - y
                if (positions[j][i]==1):
                    screen.blit(orange, ((i*20+120)*resize, (j*20-40)*resize))
                if (positions[j][i]==2):
                    screen.blit(blue, ((i*20+120)*resize, (j*20-40)*resize))
                if (positions[j][i]==3):
                    screen.blit(red, ((i*20+120)*resize, (j*20-40)*resize))
                if (positions[j][i]==4):
                    screen.blit(green, ((i*20+120)*resize, (j*20-40)*resize))
                if (positions[j][i]==5):
                    screen.blit(yellow, ((i*20+120)*resize, (j*20-40)*resize))
                if (positions[j][i]==6):
                    screen.blit(aqua, ((i*20+120)*resize, (j*20-40)*resize))
                if (positions[j][i]==7):
                    screen.blit(purple, ((i*20+120)*resize, (j*20-40)*resize))
    npsllris()

def fall_animation(first_position_part, second_position_part, cleared):
    if (togglefall):
        return
    #times=[0.00,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.20,0.21]
    #times=[0.000,0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.010,0.011,0.012,0.013,0.014,0.015,0.016,0.017,0.018,0.019,0.020,0.021]
    times=[0.000,0.005,0.010,0.015,0.020,0.025,0.030,0.035,0.040,0.045,0.050,0.055,0.060,0.065,0.070,0.075,0.080,0.085,0.090,0.095,0.100,0.105]
    #print("====================")
    #print(first_position_part)
    #print("====================")
    #print(second_position_part)
    #print("====================")
    #input()
    second_position_part[0]=[0,0,0,0,0,0,0,0,0,0]
    startTime=time.time()
    k=0
    bymspp=bordery-len(second_position_part)
    while True:
        if (time.time()-startTime>times[-1]):
            break
        for k in range(1,len(times)):#while (k!=21):
            #print("fall_animation")
            #input()
            if (times[k-1]<round(time.time()-startTime,3)<=times[k]):#if (time.time()-startTime>=0.1/20*k):
                #print(k)
                screen.blit(bg,(0,0))
                for j in range(3,len(first_position_part)): # j - y
                    if (0 in positions[j]):
                        for i in range(0,len(first_position_part[j])): #i - x
                            #print(j*20-40+k)
                            if (first_position_part[j][i]==1):
                                screen.blit(orange, ((i*20+120)*resize, (j*20-40+k)*resize))
                            if (first_position_part[j][i]==2):
                                screen.blit(blue, ((i*20+120)*resize, (j*20-40+k)*resize))
                            if (first_position_part[j][i]==3):
                                screen.blit(red, ((i*20+120)*resize, (j*20-40+k)*resize))
                            if (first_position_part[j][i]==4):
                                screen.blit(green, ((i*20+120)*resize, (j*20-40+k)*resize))
                            if (first_position_part[j][i]==5):
                                screen.blit(yellow, ((i*20+120)*resize, (j*20-40+k)*resize))
                            if (first_position_part[j][i]==6):
                                screen.blit(aqua, ((i*20+120)*resize, (j*20-40+k)*resize))
                            if (first_position_part[j][i]==7):
                                screen.blit(purple, ((i*20+120)*resize, (j*20-40+k)*resize))
                for j in range(0,len(second_position_part)): # j - y
                    for i in range(0,len(second_position_part[j])): #i - x
                        if (second_position_part[j][i]==1):
                            screen.blit(orange, ((i*20+120)*resize, ((j+bymspp)*20-40)*resize))
                        if (second_position_part[j][i]==2):
                            screen.blit(blue, ((i*20+120)*resize, ((j+bymspp)*20-40)*resize))
                        if (second_position_part[j][i]==3):
                            screen.blit(red, ((i*20+120)*resize, ((j+bymspp)*20-40)*resize))
                        if (second_position_part[j][i]==4):
                            screen.blit(green, ((i*20+120)*resize, ((j+bymspp)*20-40)*resize))
                        if (second_position_part[j][i]==5):
                            screen.blit(yellow, ((i*20+120)*resize, ((j+bymspp)*20-40)*resize))
                        if (second_position_part[j][i]==6):
                            screen.blit(aqua, ((i*20+120)*resize, ((j+bymspp)*20-40)*resize))
                        if (second_position_part[j][i]==7):
                            screen.blit(purple, ((i*20+120)*resize, ((j+bymspp)*20-40)*resize))
                npsllris()
                pygame.display.flip()
                if (k==21):
                    return#k=k+1
    #print(time.time()-startTime)
    #input()
def clear():
    global positions, todown, toleft, toright, linii, score, count1row, count2row, count3row, count4row, stat_tablo_mass, toleft, todown, toright, count_combo, combo
    cleared=[]
    cleared_massive=copy.copy(positions)
    #second_part_massive=[]
    for i in range(0,bordery):
        i=bordery-1-i
        if (0 not in positions[i]):
            cleared.append(i)
    if (len(cleared)==1):
        score=score+100*level
        linii=linii+1
        count1row+=1
        row_1.play()
        #stat_tablo_mass.append("1 линия")
    elif (len(cleared)==2):
        score=score+300*level
        linii=linii+2
        count2row+=1
        row_2.play()
        #stat_tablo_mass.append("2 линии")
    elif (len(cleared)==3):
        score=score+500*level
        linii=linii+3
        count3row+=1
        row_3.play()
        #stat_tablo_mass.append("3 линии")
    elif (len(cleared)==4):
        linii=linii+4
        count4row+=1
        row_4.play()
        if (l_cleared==6):
            stat_tablo_mass.append("Back-To-Back TETRIS")
            score+=1200*level
        else:
            score=score+800*level
            stat_tablo_mass.append("TETRIS")
    perfect_clear=copy.copy(positions)
    for i in range(0,len(cleared)):
        perfect_clear.remove(perfect_clear[cleared[i]])
        perfect_clear.append([0,0,0,0,0,0,0,0,0,0])
        for j in range(0,bordery):
            j=bordery-j-1
    if (len(cleared)>0):
        combo+=1
        perfect=True
        for i in perfect_clear:
            if (not 1 in i and not 2 in i and not 3 in i and not 4 in i and not 5 in i and not 6 in i and not 7 in i):
                pass
            else:
                perfect=False
                break
        if (perfect):
            e_perfect_clear.play()
            stat_tablo_mass.append("Пылесос")
            if (len(cleared)==1):
                score+=800*level
            elif (len(cleared)==2):
                score+=1200*level
            elif (len(cleared)==3):
                score+=1800*level
            elif (len(cleared)==4 and l_cleared==6):
                score+=3200*level
            elif (len(cleared)==4):
                score+=2000*level
        if (combo>1):
            stat_tablo_mass.append("Комбо +"+str(combo-1))
            score+=50*combo-1*level
            count_combo+=1
    else:
        combo=0
    #first_part_massive=copy.copy(cleared_massive)
    if (len(cleared)>0 and not togglecleara):
        startTime=time.time()
        while True:
            #print("clear")
            if (round(time.time()-startTime,2)==0.03):
                clear_ris(cleared)
                for i in range(0,len(cleared)):
                    screen.blit(clear_animation_0, (100*resize, (cleared[i]-2)*20*resize-10*resize))
                pygame.display.flip()
            elif (round(time.time()-startTime,2)==0.06):
                clear_ris(cleared)
                for i in range(0,len(cleared)):
                    screen.blit(clear_animation_1, (100*resize, (cleared[i]-2)*20*resize-10*resize))
                pygame.display.flip()
            elif (round(time.time()-startTime,2)==0.09):
                clear_ris(cleared)
                for i in range(0,len(cleared)):
                    screen.blit(clear_animation_2, (100*resize, (cleared[i]-2)*20*resize-10*resize))
                pygame.display.flip()
            elif (round(time.time()-startTime,2)==0.12):
                clear_ris(cleared)
                for i in range(0,len(cleared)):
                    screen.blit(clear_animation_3, (100*resize, (cleared[i]-2)*20*resize-10*resize))
                pygame.display.flip()
            elif (round(time.time()-startTime,2)==0.15):
                clear_ris(cleared)
                for i in range(0,len(cleared)):
                    screen.blit(clear_animation_4, (100*resize, (cleared[i]-2)*20*resize-10*resize))
                pygame.display.flip()
            elif (round(time.time()-startTime,2)==0.18):
                clear_ris(cleared)
                for i in range(0,len(cleared)):
                    screen.blit(clear_animation_5, (100*resize, (cleared[i]-2)*20*resize-10*resize))
                pygame.display.flip()
            elif (round(time.time()-startTime,2)==0.21):
                clear_ris(cleared)
                for i in range(0,len(cleared)):
                    screen.blit(clear_animation_6, (100*resize, (cleared[i]-2)*20*resize-10*resize))
                pygame.display.flip()
            elif (round(time.time()-startTime,2)==0.24):
                clear_ris(cleared)
                for i in range(0,len(cleared)):
                    screen.blit(clear_animation_7, (100*resize, (cleared[i]-2)*20*resize-10*resize))
                pygame.display.flip()
            elif (round(time.time()-startTime,2)==0.27):
                clear_ris(cleared)
                for i in range(0,len(cleared)):
                    screen.blit(clear_animation_8, (100*resize, (cleared[i]-2)*20*resize-10*resize))
                pygame.display.flip()
            elif (round(time.time()-startTime,2)>=0.30):
                clear_ris(cleared)
                for i in range(0,len(cleared)):
                    screen.blit(clear_animation_9, (100*resize, (cleared[i]-2)*20*resize-10*resize))
                pygame.display.flip()
                break
    old_cleared=copy.copy(cleared)
    if (1<len(cleared)):
        cleared[1]=cleared[1]+1
    if (2<len(cleared)):
        cleared[2]=cleared[2]+2
    if (3<len(cleared)):
        cleared[3]=cleared[3]+3
    for i in range(0,len(cleared)):
        first_part_massive=cleared_massive[:cleared[i]:]
        second_part_massive=cleared_massive[cleared[i]::]
        fall_animation(first_part_massive, second_part_massive, old_cleared)
        positions.remove(positions[cleared[i]])
        positions.append([0,0,0,0,0,0,0,0,0,0])
        for j in range(0,bordery):
            j=bordery-j-1
            positions[j]=positions[j-1]
        positions[0]=[0,0,0,0,0,0,0,0,0,0]
        cleared_massive.remove(cleared_massive[cleared[i]])
        cleared_massive.append([0,0,0,0,0,0,0,0,0,0])
        for j in range(0,bordery):
            j=bordery-j-1
            cleared_massive[j]=cleared_massive[j-1]
        cleared_massive[0]=[0,0,0,0,0,0,0,0,0,0]
    for event in pygame.event.get():
        if (event.type==pygame.QUIT):
            exit(True)
        elif (event.type==pygame.KEYDOWN):
            if (event.key==pygame.K_LEFT):
                toleft=True
            elif (event.key==pygame.K_RIGHT):
                toright=True
            elif (event.key==pygame.K_DOWN):
                todown=True
        elif (event.type==pygame.KEYUP):
            if (event.key==pygame.K_LEFT):
                toleft=False
            elif (event.key==pygame.K_RIGHT):
                toright=False
            elif (event.key==pygame.K_DOWN):
                todown=False
    if (len(cleared)>0):
        """
        perfect=True
        for i in positions:
            if (not 1 in i and not 2 in i and not 3 in i and not 4 in i and not 5 in i and not 6 in i and not 7 in i):
                pass
            else:
                perfect=False
                break
        if (perfect):
            stat_tablo_mass.append("Пылесос")
            if (len(cleared)==1):
                score+=800*level
            elif (len(cleared)==2):
                score+=1200*level
            elif (len(cleared)==3):
                score+=1800*level
            elif (len(cleared)==4 and l_cleared==6):
                score+=3200*level
            elif (len(cleared)==4):
                score+=2000*level
        """
        n_level()
        return True
    else:
        return False
    #toleft,todown,toright=False,False,False
    #while (round(time.time()-startTime,1)<4.0):
        
            
def pause():
    global paused, figure, p_s, rotation
    if (p_s==1):
        rotation=0
        #e_tm_p.play()
        cont=1
        if (paused==0):
            paused=figure
            cont=0
            p_clear()
            figura()
        if(cont==1):
            p_clear()
            tmp=paused
            paused=figure
            figure=tmp
        spawn_new_figure(figure)
        p_s=0
        return True
    else:
        #e_tm_p_error.play()
        return False
        
def restart():
    global positions, padenie, proekc, figure, next1, next2, next3, paused, score, linii, level, p_s, r_marathon, r_endless, rotation, count1row, count2row, count3row, count4row, count_combo, combo, stat_tablo_mass, p_figure, stat_tablo_to_show, l_cleared
    r_marathon,r_endless=0,0
    stat_tablo_mass=[]
    stat_tablo_to_show=""
    positions=[[0,0,0,0,0,0,0,0,0,0], #0 линия, которая не отображается в игре, но здесь может находиться фигура
               [0,0,0,0,0,0,0,0,0,0], #1 линия, которая не отображается в игре, но здесь может находиться фигура
               [0,0,0,0,0,0,0,0,0,0], #2 линия, которая не отображается в игре, но здесь может находиться фигура
               [0,0,0,0,0,0,0,0,0,0], #3
               [0,0,0,0,0,0,0,0,0,0], #4
               [0,0,0,0,0,0,0,0,0,0], #5
               [0,0,0,0,0,0,0,0,0,0], #6
               [0,0,0,0,0,0,0,0,0,0], #7
               [0,0,0,0,0,0,0,0,0,0], #8
               [0,0,0,0,0,0,0,0,0,0], #9
               [0,0,0,0,0,0,0,0,0,0], #10
               [0,0,0,0,0,0,0,0,0,0], #11
               [0,0,0,0,0,0,0,0,0,0], #12
               [0,0,0,0,0,0,0,0,0,0], #13
               [0,0,0,0,0,0,0,0,0,0], #14
               [0,0,0,0,0,0,0,0,0,0], #15
               [0,0,0,0,0,0,0,0,0,0], #16
               [0,0,0,0,0,0,0,0,0,0], #17
               [0,0,0,0,0,0,0,0,0,0], #18
               [0,0,0,0,0,0,0,0,0,0], #19
               [0,0,0,0,0,0,0,0,0,0], #20
               [0,0,0,0,0,0,0,0,0,0], #21
               [0,0,0,0,0,0,0,0,0,0]] #22
    #           0 1 2 3 4 5 6 7 8 9
    padenie=[[0,0,0,0,0,0,0,0,0,0], #0 линия, которая не отображается в игре, но здесь может находиться фигура
             [0,0,0,0,0,0,0,0,0,0], #1 линия, которая не отображается в игре, но здесь может находиться фигура
             [0,0,0,0,0,0,0,0,0,0], #2 линия, которая не отображается в игре, но здесь может находиться фигура
             [0,0,0,0,0,0,0,0,0,0], #3
             [0,0,0,0,0,0,0,0,0,0], #4
             [0,0,0,0,0,0,0,0,0,0], #5
             [0,0,0,0,0,0,0,0,0,0], #6
             [0,0,0,0,0,0,0,0,0,0], #7
             [0,0,0,0,0,0,0,0,0,0], #8
             [0,0,0,0,0,0,0,0,0,0], #9
             [0,0,0,0,0,0,0,0,0,0], #10
             [0,0,0,0,0,0,0,0,0,0], #11
             [0,0,0,0,0,0,0,0,0,0], #12
             [0,0,0,0,0,0,0,0,0,0], #13
             [0,0,0,0,0,0,0,0,0,0], #14
             [0,0,0,0,0,0,0,0,0,0], #15
             [0,0,0,0,0,0,0,0,0,0], #16
             [0,0,0,0,0,0,0,0,0,0], #17
             [0,0,0,0,0,0,0,0,0,0], #18
             [0,0,0,0,0,0,0,0,0,0], #19
             [0,0,0,0,0,0,0,0,0,0], #20
             [0,0,0,0,0,0,0,0,0,0], #21
             [0,0,0,0,0,0,0,0,0,0]] #22
    try:
        file=open("save.gst","r")
        file.close()
        dr=tf_dialog("Обнаружено сохранение", "Продолжить ранее начатую игру?", bpurple, bppurple, "Продолжить", baqua, bpaqua, "Начать заново", bblue, bpblue, "Назад", 2)
        if (dr==1):
            g_resume=open("save.gst", "r")
            grs=g_resume.read()
            g_rsm=[int(x) for x in grs.split(",")]
            g_resume.close()
            os.remove("save.gst")
            rplc=0
            for i in range (0,23):
                for j in range (0,10):
                    positions[i][j]=g_rsm[rplc]
                    rplc=rplc+1
            rplc=230
            for i in range (0,23):
                for j in range (0,10):
                    padenie[i][j]=g_rsm[rplc]
                    rplc=rplc+1
            level=g_rsm[460]
            score=g_rsm[461]
            linii=g_rsm[462]
            rotation=g_rsm[463]
            #next0=g_rsm[464]
            next1=g_rsm[465]
            next2=g_rsm[466]
            next3=g_rsm[467]
            paused=g_rsm[468]
            figure=g_rsm[469]
            p_s=g_rsm[470]
            r_marathon=g_rsm[471]
            count1row=g_rsm[472]
            count2row=g_rsm[473]
            count3row=g_rsm[474]
            count4row=g_rsm[475]
            combo=g_rsm[476]
            p_figure=g_rsm[477]
            l_cleared=g_rsm[478]
            count_combo=g_rsm[479]
            return True
        elif (dr==2):
            pass
        elif (dr==3):
            return False
    except:# Exception as error:
        pass#print(error)
    try:os.remove("save.gst")
    except:pass
    positions=[[0,0,0,0,0,0,0,0,0,0], #0 линия, которая не отображается в игре, но здесь может находиться фигура
               [0,0,0,0,0,0,0,0,0,0], #1 линия, которая не отображается в игре, но здесь может находиться фигура
               [0,0,0,0,0,0,0,0,0,0], #2 линия, которая не отображается в игре, но здесь может находиться фигура
               [0,0,0,0,0,0,0,0,0,0], #3
               [0,0,0,0,0,0,0,0,0,0], #4
               [0,0,0,0,0,0,0,0,0,0], #5
               [0,0,0,0,0,0,0,0,0,0], #6
               [0,0,0,0,0,0,0,0,0,0], #7
               [0,0,0,0,0,0,0,0,0,0], #8
               [0,0,0,0,0,0,0,0,0,0], #9
               [0,0,0,0,0,0,0,0,0,0], #10
               [0,0,0,0,0,0,0,0,0,0], #11
               [0,0,0,0,0,0,0,0,0,0], #12
               [0,0,0,0,0,0,0,0,0,0], #13
               [0,0,0,0,0,0,0,0,0,0], #14
               [0,0,0,0,0,0,0,0,0,0], #15
               [0,0,0,0,0,0,0,0,0,0], #16
               [0,0,0,0,0,0,0,0,0,0], #17
               [0,0,0,0,0,0,0,0,0,0], #18
               [0,0,0,0,0,0,0,0,0,0], #19
               [0,0,0,0,0,0,0,0,0,0], #20
               [0,0,0,0,0,0,0,0,0,0], #21
               [0,0,0,0,0,0,0,0,0,0]] #22
    #           0 1 2 3 4 5 6 7 8 9
    padenie=[[0,0,0,0,0,0,0,0,0,0], #0 линия, которая не отображается в игре, но здесь может находиться фигура
             [0,0,0,0,0,0,0,0,0,0], #1 линия, которая не отображается в игре, но здесь может находиться фигура
             [0,0,0,0,0,0,0,0,0,0], #2 линия, которая не отображается в игре, но здесь может находиться фигура
             [0,0,0,0,0,0,0,0,0,0], #3
             [0,0,0,0,0,0,0,0,0,0], #4
             [0,0,0,0,0,0,0,0,0,0], #5
             [0,0,0,0,0,0,0,0,0,0], #6
             [0,0,0,0,0,0,0,0,0,0], #7
             [0,0,0,0,0,0,0,0,0,0], #8
             [0,0,0,0,0,0,0,0,0,0], #9
             [0,0,0,0,0,0,0,0,0,0], #10
             [0,0,0,0,0,0,0,0,0,0], #11
             [0,0,0,0,0,0,0,0,0,0], #12
             [0,0,0,0,0,0,0,0,0,0], #13
             [0,0,0,0,0,0,0,0,0,0], #14
             [0,0,0,0,0,0,0,0,0,0], #15
             [0,0,0,0,0,0,0,0,0,0], #16
             [0,0,0,0,0,0,0,0,0,0], #17
             [0,0,0,0,0,0,0,0,0,0], #18
             [0,0,0,0,0,0,0,0,0,0], #19
             [0,0,0,0,0,0,0,0,0,0], #20
             [0,0,0,0,0,0,0,0,0,0], #21
             [0,0,0,0,0,0,0,0,0,0]] #22
    #        0 1 2 3 4 5 6 7 8 9
    proekc=[[0,0,0,0,0,0,0,0,0,0], #0 линия, которая не отображается в игре, но здесь может находиться фигура
            [0,0,0,0,0,0,0,0,0,0], #1 линия, которая не отображается в игре, но здесь может находиться фигура
            [0,0,0,0,0,0,0,0,0,0], #2 линия, которая не отображается в игре, но здесь может находиться фигура
            [0,0,0,0,0,0,0,0,0,0], #3
            [0,0,0,0,0,0,0,0,0,0], #4
            [0,0,0,0,0,0,0,0,0,0], #5
            [0,0,0,0,0,0,0,0,0,0], #6
            [0,0,0,0,0,0,0,0,0,0], #7
            [0,0,0,0,0,0,0,0,0,0], #8
            [0,0,0,0,0,0,0,0,0,0], #9
            [0,0,0,0,0,0,0,0,0,0], #10
            [0,0,0,0,0,0,0,0,0,0], #11
            [0,0,0,0,0,0,0,0,0,0], #12
            [0,0,0,0,0,0,0,0,0,0], #13
            [0,0,0,0,0,0,0,0,0,0], #14
            [0,0,0,0,0,0,0,0,0,0], #15
            [0,0,0,0,0,0,0,0,0,0], #16
            [0,0,0,0,0,0,0,0,0,0], #17
            [0,0,0,0,0,0,0,0,0,0], #18
            [0,0,0,0,0,0,0,0,0,0], #19
            [0,0,0,0,0,0,0,0,0,0], #20
            [0,0,0,0,0,0,0,0,0,0], #21
            [0,0,0,0,0,0,0,0,0,0]] #22
    figure=0
    next1=randint(1,7)
    next2=randint(1,7)
    next3=randint(1,7)
    paused=0
    p_s=1
    score,linii,level=0,0,1
    count1row,count2row,count3row,count4row,count_combo=0,0,0,0,0
    combo=0
    p_figure=0
    l_cleared=0
    figura()
    return True

def p_clear():
    global padenie
    padenie=[[0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0]]

def af_effect(old_padenie):
    global toleft, todown, toright
    if (toggleaf):
        return
    pos=get_piece_locations(padenie)
    if (len(pos)==0): return
    animation_time=0.4
    startTime=time.time()#print(pos)
    while (time.time()-startTime<=animation_time/2):
        ris()
        proc=procras(startTime, startTime+animation_time/2)
        alpha=round(0+(255-0)*proc)
        fall_effect.set_alpha(alpha)
        if (pos[0][0]>=3):
            screen.blit(fall_effect,((pos[0][1]*20+120)*resize,(pos[0][0]*20-40)*resize))
        if (pos[1][0]>=3):
            screen.blit(fall_effect,((pos[1][1]*20+120)*resize,(pos[1][0]*20-40)*resize))
        if (pos[2][0]>=3):
            screen.blit(fall_effect,((pos[2][1]*20+120)*resize,(pos[2][0]*20-40)*resize))
        if (pos[3][0]>=3):
            screen.blit(fall_effect,((pos[3][1]*20+120)*resize,(pos[3][0]*20-40)*resize))
        pygame.display.flip()
        fps.tick(60)
    while (time.time()-startTime<=animation_time):
        ris()
        proc=procras(startTime+animation_time/2, startTime+animation_time)
        alpha=round(255+(0-255)*proc)
        fall_effect.set_alpha(alpha)
        if (pos[0][0]>=3):
            screen.blit(fall_effect,((pos[0][1]*20+120)*resize,(pos[0][0]*20-40)*resize))
        if (pos[1][0]>=3):
            screen.blit(fall_effect,((pos[1][1]*20+120)*resize,(pos[1][0]*20-40)*resize))
        if (pos[2][0]>=3):
            screen.blit(fall_effect,((pos[2][1]*20+120)*resize,(pos[2][0]*20-40)*resize))
        if (pos[3][0]>=3):
            screen.blit(fall_effect,((pos[3][1]*20+120)*resize,(pos[3][0]*20-40)*resize))
        pygame.display.flip()
        fps.tick(60)
        
    for event in pygame.event.get():
        if (event.type==pygame.QUIT):
            exit(True)
        elif (event.type==pygame.KEYDOWN):
            if (event.key==pygame.K_LEFT):
                toleft=True
            elif (event.key==pygame.K_RIGHT):
                toright=True
            elif (event.key==pygame.K_DOWN):
                todown=True
        elif (event.type==pygame.KEYUP):
            if (event.key==pygame.K_LEFT):
                toleft=False
            elif (event.key==pygame.K_RIGHT):
                toright=False
            elif (event.key==pygame.K_DOWN):
                todown=False
    
def figura():
    global padenie, positions, figure, next1, next2, next3, rotation, p_s, running, p_figure, l_cleared#, score, count_combo, combo, stat_tablo_mass
    rotation=0
    p_s=1
    old_padenie=copy.copy(padenie)
    for i in range(bordery):
        for j in range(borderx):
            if (padenie[i][j]!=0):
                positions[i][j]=padenie[i][j]
    if (clear()):
        l_cleared=figure
    #    combo+=1
    else:
    #    combo=0
        af_effect(old_padenie)
    p_figure=figure
    figure=next1
    next1=next2
    next2=next3
    next3=randint(1,7)
    p_clear()
    spawn_new_figure(figure)
    #if (combo>1):
    #    stat_tablo_mass.append("Комбо +"+str(combo))
    #    score+=50*combo-1*level
    #    count_combo+=1

def spawn_new_figure(figure):
    global padenie, running
    if (figure==1):
        if (positions[2][5]==0 and positions[3][3]==0 and positions[3][4]==0 and positions[3][5]==0):
            padenie[2][5]=1
            padenie[3][3]=1
            padenie[3][4]=1
            padenie[3][5]=1
        else:
            running=False
            #game_overed()
    elif (figure==2):
        if (positions[2][3]==0 and positions[3][3]==0 and positions[3][4]==0 and positions[3][5]==0):
            padenie[2][3]=2
            padenie[3][3]=2
            padenie[3][4]=2
            padenie[3][5]=2
        else:
            running=False
            #game_overed()
    elif (figure==3):
        if (positions[2][3]==0 and positions[2][4]==0 and positions[3][4]==0 and positions[3][5]==0):
            padenie[2][3]=3
            padenie[2][4]=3
            padenie[3][4]=3
            padenie[3][5]=3
        else:
            running=False
            #game_overed()
    elif (figure==4):
        if (positions[2][4]==0 and positions[2][5]==0 and positions[3][4]==0 and positions[3][3]==0):
            padenie[2][4]=4
            padenie[2][5]=4
            padenie[3][4]=4
            padenie[3][3]=4
        else:
            running=False
            #game_overed()
    elif (figure==5):
        if (positions[2][5]==0 and positions[2][4]==0 and positions[3][4]==0 and positions[3][5]==0):
            padenie[2][5]=5
            padenie[2][4]=5
            padenie[3][4]=5
            padenie[3][5]=5
        else:
            running=False
            #game_overed()
    elif (figure==6):
        if (positions[3][3]==0 and positions[3][4]==0 and positions[3][5]==0 and positions[3][6]==0):
            padenie[3][3]=6
            padenie[3][4]=6
            padenie[3][5]=6
            padenie[3][6]=6
        else:
            running=False
            #game_overed()
    else:
        if (positions[2][4]==0 and positions[3][3]==0 and positions[3][4]==0 and positions[3][5]==0):
            padenie[2][4]=7
            padenie[3][3]=7
            padenie[3][4]=7
            padenie[3][5]=7
        else:
            running=False
            #game_overed()

#передвижение фигур
def get_piece_locations(massive):
    result=[]
    for i in range(0,bordery):
        for j in range(0,borderx):
            if (massive[i][j]!=0):
                result.append([i,j])
    return result
            
def left():
    global padenie
    for i in get_piece_locations(padenie):
        if (i[1]-1<0 or positions[i[0]][i[1]-1]!=0):
            return False
    for j in range(0,bordery):
        for i in range(0,borderx-1):
            padenie[j][i]=padenie[j][i+1]
        padenie[j][borderx-1]=0
    e_move_left.play()
    return True

def right():
    global padenie
    for i in get_piece_locations(padenie):
        if (i[1]+1>9 or positions[i[0]][i[1]+1]!=0):
            return False
    for j in range(0,bordery):
        for i in range(0,borderx-1):
            i=borderx-i-1
            #print(i)
            padenie[j][i]=padenie[j][i-1]
        padenie[j][0]=0
    e_move_right.play()
    return True

def down_check():
    for i in get_piece_locations(padenie):
        if (i[0]+1>=bordery or positions[i[0]+1][i[1]]!=0):
            return True
    return False

def down(user_call):
    global padenie, score
    for i in get_piece_locations(padenie):
        if (i[0]+1>=bordery or positions[i[0]+1][i[1]]!=0):
            return False
    for i in range(0,bordery):
        i=bordery-i-1
        padenie[i]=padenie[i-1]
    padenie[0]=[0,0,0,0,0,0,0,0,0,0]
    if (user_call):
        score=score+1
    return True

def hard_drop():
    global score
    attempts=0
    moved=False
    while (down(False) and attempts<=bordery+5):
        #print("down")
        score=score+2
        attempts=attempts+1
        moved=True
    return moved

#  1 оранж. 3 красный 5 желтый  7 фиолетовый
#  x    x                x  
#  x    x  xx    xx  xx  x     xxx
#  xx  xx   xx  xx   xx  x      x
#                        x
#      2 синий  4 зел.   6 голубой
#figure rotation data
frdr=[[[[2,0],[-1,1],[0,0],[1,-1]],
      [[1,1],[0,0],[-1,-1],[0,-2]],
      [[-1,1],[0,0],[1,-1],[-2,0]],
      [[0,2],[1,1],[0,0],[-1,-1]]], #1
     
     [[[0,1],[-1,2],[0,0],[1,-1]],
      [[1,1],[2,0],[0,0],[-1,-1]],
      [[1,0],[0,0],[-1,-1],[0,-1]],
      [[1,1],[0,0],[-2,0],[-1,-1]]], #2
     
     [[[0,2],[2,0],[0,0],[0,0]],
      [[1,-2],[0,0],[1,0],[0,0]],
      [[0,0],[0,0],[0,-1],[-2,-1]],
      [[0,0],[0,2],[0,0],[-2,0]]], #3
     
     [[[0,0],[1,0],[1,2],[0,0]],
      [[2,0],[0,0],[0,0],[0,-2]],
      [[0,0],[-1,-2],[-1,0],[0,0]],
      [[0,2],[0,0],[0,0],[-2,0]]], #4
     
     [[[0,0],[0,0],[0,0],[0,0]],
      [[0,0],[0,0],[0,0],[0,0]],
      [[0,0],[0,0],[0,0],[0,0]],
      [[0,0],[0,0],[0,0],[0,0]]], #5
     
     [[[-1,2],[0,1],[1,0],[2,-1]],
      [[2,1],[1,0],[0,-1],[-1,-2]],
      [[-2,1],[-1,0],[0,-1],[1,-2]],
      [[1,2],[0,1],[-1,0],[-2,-1]]], #6
     
     [[[0,0],[1,1],[0,0],[0,0]],
      [[1,-1],[0,0],[0,0],[0,0]],
      [[0,0],[0,0],[-1,-1],[0,0]],
      [[0,0],[0,0],[0,0],[-1,1]]]] #7
#
#
#
frdl=[[[[1,-1],[0,0],[-1,1],[-2,0]],
      [[1,1],[0,0],[-1,-1],[0,2]],
      [[2,0],[1,-1],[0,0],[-1,1]],
      [[0,-2],[1,1],[0,0],[-1,-1]]], #1
     
     [[[1,-1],[0,-2],[0,0],[-1,1]],
      [[1,1],[0,0],[-1,-1],[-2,0]],
      [[1,-1],[0,0],[0,2],[-1,1]],
      [[2,0],[1,1],[0,0],[-1,-1]]], #2
     
     [[[0,-2],[0,0],[-1,-1],[-1,1]],
      [[1,1],[0,0],[-1,1],[-2,0]],
      [[1,-1],[1,1],[0,0],[0,2]],
      [[2,0],[1,-1],[0,0],[-1,-1]]], #3
     
     [[[1,-1],[0,0],[-1,-1],[-2,0]],
      [[0,0],[-1,-1],[0,2],[-1,1]],
      [[2,0],[1,1],[0,0],[-1,1]],
      [[1,-1],[0,-2],[1,1],[0,0]]], #4
     
     [[[0,0],[0,0],[0,0],[0,0]],
      [[0,0],[0,0],[0,0],[0,0]],
      [[0,0],[0,0],[0,0],[0,0]],
      [[0,0],[0,0],[0,0],[0,0]]], #5
     
     [[[1,-2],[0,-1],[-1,0],[-2,1]],
      [[1,2],[0,1],[-1,0],[-2,-1]],
      [[2,-1],[1,0],[0,1],[-1,2]],
      [[2,1],[1,0],[0,-1],[-1,-2]]], #6
     
     [[[1,-1],[0,0],[-1,-1],[-1,1]],
      [[1,1],[0,0],[-1,-1],[-1,1]],
      [[1,-1],[1,1],[0,0],[-1,1]],
      [[1,-1],[1,1],[0,0],[-1,-1]]]] #7

def wall_kick(test_number, figure, rotation, piece_location, rotate):
    #J, L, S, T, Z
    #   Test1   Test2   Test3   Test4   Test5
    #12 ( 0, 0)	(-1, 0)	(-1,-1)	( 0, 2)	(-1, 2)
    #23 ( 0, 0)	( 1, 0)	( 1, 1)	( 0,-2)	( 1,-2)
    #34 ( 0, 0)	( 1, 0)	( 1,-1)	( 0, 2)	( 1, 2)
    #40 ( 0, 0)	(-1, 0)	(-1, 1)	( 0,-2)	(-1,-2)

    #I
    #12 ( 0, 0)	(-2, 0)	( 1, 0)	(-2, 1)	( 1,-2)
    #23 ( 0, 0)	(-1, 0)	( 2, 0)	(-1,-2)	( 2, 1)
    #34 ( 0, 0)	( 2, 0)	(-1, 0)	( 2,-1)	(-1, 2)
    #40 ( 0, 0)	( 1, 0)	(-2, 0)	( 1, 2)	(-2,-1)

    #(0, -1)	(-1,-1)	( 2, 0)	( 2,-1)
    #(0,  1)	( 1, 1)	(-2, 0)	(-2, 1)
    #(0,  1)	(-1, 1)	( 2, 0)	( 2, 1)
    #(0, -1)	( 1,-1)	(-2, 0)	(-2,-1)
    #
    #( 0,-2)	( 0, 1)	( 1,-2)	(-2, 1)
    #( 0,-1)	( 0, 2)	(-2,-1)	( 1, 2)
    #( 0, 2)	( 0,-1)	(-1, 2)	( 2,-1)
    #( 0, 1)	( 0,-2)	( 2, 1)	(-1,-2)
    if (rotate==1):
        if (test_number==1):
            if (rotation==1):
                if (figure!=6):test_data=[0,0]
                else:test_data=[0,0]
            elif (rotation==2):
                if (figure!=6):test_data=[0,0]
                else:test_data=[0,0]
            elif (rotation==3):
                if (figure!=6):test_data=[0,0]
                else:test_data=[0,0]
            elif (rotation==4):
                if (figure!=6):test_data=[0,0]
                else:test_data=[0,0]
        elif (test_number==2):
            if (rotation==1):
                if (figure!=6):test_data=[0,-1]
                else:test_data=[0,-2]
            elif (rotation==2):
                if (figure!=6):test_data=[0,1]
                else:test_data=[0,-1]
            elif (rotation==3):
                if (figure!=6):test_data=[0,1]
                else:test_data=[0,2]
            elif (rotation==4):
                if (figure!=6):test_data=[0,-1]
                else:test_data=[0,1]
        elif (test_number==3):
            if (rotation==1):
                if (figure!=6):test_data=[-1,-1]
                else:test_data=[0,1]
            elif (rotation==2):
                if (figure!=6):test_data=[1,1]
                else:test_data=[0,2]
            elif (rotation==3):
                if (figure!=6):test_data=[-1,1]
                else:test_data=[0,-1]
            elif (rotation==4):
                if (figure!=6):test_data=[1,-1]
                else:test_data=[0,-2]
        elif (test_number==4):
            if (rotation==1):
                if (figure!=6):test_data=[2,0]
                else:test_data=[1,-2]
            elif (rotation==2):
                if (figure!=6):test_data=[-2,0]
                else:test_data=[-2,-1]
            elif (rotation==3):
                if (figure!=6):test_data=[2,0]
                else:test_data=[-1,2]
            elif (rotation==4):
                if (figure!=6):test_data=[-2,0]
                else:test_data=[2,1]
        elif (test_number==5):
            if (rotation==1):
                if (figure!=6):test_data=[2,-1]
                else:test_data=[-2,1]
            elif (rotation==2):
                if (figure!=6):test_data=[-2,1]
                else:test_data=[1,2]
            elif (rotation==3):
                if (figure!=6):test_data=[2,1]
                else:test_data=[2,-1]
            elif (rotation==4):
                if (figure!=6):test_data=[-2,-1]
                else:test_data=[-1,-2]
    elif (rotate==2):
        #( 0, 1)	( 1, 1)	(-2, 0)	(-2, 1)
        #( 0,-1)	(-1,-1)	( 2, 0)	( 2,-1)
        #( 0,-1)	( 1,-1)	(-2, 0)	(-2,-1)
        #( 0, 1)	(-1, 1)	( 2, 0)	( 2, 1)
        #
        #( 0, 2)	( 0,-1)	(-1, 2)	( 2,-1)
        #( 0, 1)	( 0,-2)	( 2, 1)	(-1,-2)
        #( 0,-2)	( 0, 1)	( 1,-2)	(-2, 1)
        #( 0,-1)	( 0, 2)	(-2,-1)	( 1, 2)

        if (test_number==1):
            if (rotation==1):
                if (figure!=6):
                    test_data=[0,0]
                else:
                    test_data=[0,0]
            elif (rotation==2):
                if (figure!=6):
                    test_data=[0,0]
                else:
                    test_data=[0,0]
            elif (rotation==3):
                if (figure!=6):
                    test_data=[0,0]
                else:
                    test_data=[0,0]
            elif (rotation==4):
                if (figure!=6):
                    test_data=[0,0]
                else:
                    test_data=[0,0]
        elif (test_number==2):
            if (rotation==1):
                if (figure!=6):
                    test_data=[0, 1]
                else:
                    test_data=[0, 2]
            elif (rotation==2):
                if (figure!=6):
                    test_data=[0, -1]
                else:
                    test_data=[0, 1]
            elif (rotation==3):
                if (figure!=6):
                    test_data=[0, -1]
                else:
                    test_data=[0, -2]
            elif (rotation==4):
                if (figure!=6):
                    test_data=[0, 1]
                else:
                    test_data=[0, -1]
        elif (test_number==3):
            if (rotation==1):
                if (figure!=6):
                    test_data=[1, 1]
                else:
                    test_data=[0, -1]
            elif (rotation==2):
                if (figure!=6):
                    test_data=[-1, -1]
                else:
                    test_data=[0, -2]
            elif (rotation==3):
                if (figure!=6):
                    test_data=[1, -1]
                else:
                    test_data=[0, 1]
            elif (rotation==4):
                if (figure!=6):
                    test_data=[-1, 1]
                else:
                    test_data=[0, 2]
        elif (test_number==4):
            if (rotation==1):
                if (figure!=6):
                    test_data=[-2, 0]
                else:
                    test_data=[-1, 2]
            elif (rotation==2):
                if (figure!=6):
                    test_data=[2, 0]
                else:
                    test_data=[2, 1]
            elif (rotation==3):
                if (figure!=6):
                    test_data=[-2, 0]
                else:
                    test_data=[1, -2]
            elif (rotation==4):
                if (figure!=6):
                    test_data=[2, 0]
                else:
                    test_data=[-2, -1]
        elif (test_number==5):
            if (rotation==1):
                if (figure!=6):
                    test_data=[-2, 1]
                else:
                    test_data=[2, -1]
            elif (rotation==2):
                if (figure!=6):
                    test_data=[2, -1]
                else:
                    test_data=[-1, -2]
            elif (rotation==3):
                if (figure!=6):
                    test_data=[-2, -1]
                else:
                    test_data=[-2, 1]
            elif (rotation==4):
                if (figure!=6):
                    test_data=[2, 1]
                else:
                    test_data=[1, 2] 
        
    if (rotate==1):
        if (0<=piece_location[0][0]+test_data[0]+frdr[figure-1][rotation-1][0][0]<bordery and 0<=piece_location[0][1]+test_data[1]+frdr[figure-1][rotation-1][0][1]<borderx and
            0<=piece_location[1][0]+test_data[0]+frdr[figure-1][rotation-1][1][0]<bordery and 0<=piece_location[1][1]+test_data[1]+frdr[figure-1][rotation-1][1][1]<borderx and
            0<=piece_location[2][0]+test_data[0]+frdr[figure-1][rotation-1][2][0]<bordery and 0<=piece_location[2][1]+test_data[1]+frdr[figure-1][rotation-1][2][1]<borderx and
            0<=piece_location[3][0]+test_data[0]+frdr[figure-1][rotation-1][3][0]<bordery and 0<=piece_location[3][1]+test_data[1]+frdr[figure-1][rotation-1][3][1]<borderx):
            if (positions[piece_location[0][0]+test_data[0]+frdr[figure-1][rotation-1][0][0]][piece_location[0][1]+test_data[1]+frdr[figure-1][rotation-1][0][1]]==0 and
                positions[piece_location[1][0]+test_data[0]+frdr[figure-1][rotation-1][1][0]][piece_location[1][1]+test_data[1]+frdr[figure-1][rotation-1][1][1]]==0 and
                positions[piece_location[2][0]+test_data[0]+frdr[figure-1][rotation-1][2][0]][piece_location[2][1]+test_data[1]+frdr[figure-1][rotation-1][2][1]]==0 and
                positions[piece_location[3][0]+test_data[0]+frdr[figure-1][rotation-1][3][0]][piece_location[3][1]+test_data[1]+frdr[figure-1][rotation-1][3][1]]==0):
                return True, test_data
    else:
        if (0<=piece_location[0][0]+test_data[0]+frdl[figure-1][rotation-1][0][0]<bordery and 0<=piece_location[0][1]+test_data[1]+frdl[figure-1][rotation-1][0][1]<borderx and
            0<=piece_location[1][0]+test_data[0]+frdl[figure-1][rotation-1][1][0]<bordery and 0<=piece_location[1][1]+test_data[1]+frdl[figure-1][rotation-1][1][1]<borderx and
            0<=piece_location[2][0]+test_data[0]+frdl[figure-1][rotation-1][2][0]<bordery and 0<=piece_location[2][1]+test_data[1]+frdl[figure-1][rotation-1][2][1]<borderx and
            0<=piece_location[3][0]+test_data[0]+frdl[figure-1][rotation-1][3][0]<bordery and 0<=piece_location[3][1]+test_data[1]+frdl[figure-1][rotation-1][3][1]<borderx):
            if (positions[piece_location[0][0]+test_data[0]+frdl[figure-1][rotation-1][0][0]][piece_location[0][1]+test_data[1]+frdl[figure-1][rotation-1][0][1]]==0 and
                positions[piece_location[1][0]+test_data[0]+frdl[figure-1][rotation-1][1][0]][piece_location[1][1]+test_data[1]+frdl[figure-1][rotation-1][1][1]]==0 and
                positions[piece_location[2][0]+test_data[0]+frdl[figure-1][rotation-1][2][0]][piece_location[2][1]+test_data[1]+frdl[figure-1][rotation-1][2][1]]==0 and
                positions[piece_location[3][0]+test_data[0]+frdl[figure-1][rotation-1][3][0]][piece_location[3][1]+test_data[1]+frdl[figure-1][rotation-1][3][1]]==0):
                return True, test_data
    return False, False
def rotate_cw():
    global positions, padenie, rotation, figure
    if (rotation==4):
        rotation=0
    rotation+=1
    piece_location=get_piece_locations(padenie)
    #piece_location >>> [y,x],[y,x],[y,x],[y,x]
    #          y,x
    result,test_data=wall_kick(1,figure,rotation,piece_location,1)#[0,0]
    if (not result):
        result,test_data=wall_kick(2,figure,rotation,piece_location,1)
    if (not result):
        result,test_data=wall_kick(3,figure,rotation,piece_location,1)
    if (not result):
        result,test_data=wall_kick(4,figure,rotation,piece_location,1)
    if (not result):
        result,test_data=wall_kick(5,figure,rotation,piece_location,1)

    if (not test_data):
        rotation=rotation-1
        return False
    
    #поворот
    p_clear()
    padenie[piece_location[0][0]+test_data[0]+frdr[figure-1][rotation-1][0][0]][piece_location[0][1]+test_data[1]+frdr[figure-1][rotation-1][0][1]]=figure
    padenie[piece_location[1][0]+test_data[0]+frdr[figure-1][rotation-1][1][0]][piece_location[1][1]+test_data[1]+frdr[figure-1][rotation-1][1][1]]=figure
    padenie[piece_location[2][0]+test_data[0]+frdr[figure-1][rotation-1][2][0]][piece_location[2][1]+test_data[1]+frdr[figure-1][rotation-1][2][1]]=figure
    padenie[piece_location[3][0]+test_data[0]+frdr[figure-1][rotation-1][3][0]][piece_location[3][1]+test_data[1]+frdr[figure-1][rotation-1][3][1]]=figure
    return True

def rotate_ccw():
    global positions, padenie, rotation, figure
    if (rotation==0):
        rotation=4
    #if (rotation==1):
    #    rotation=5
    if (figure==5):
        return True
    piece_location=get_piece_locations(padenie)
    #piece_location >>> [y,x],[y,x],[y,x],[y,x]
    #          y,x
    result,test_data=wall_kick(1,figure,rotation,piece_location,2)#[0,0]
    if (not result):
        result,test_data=wall_kick(2,figure,rotation,piece_location,2)
    if (not result):
        result,test_data=wall_kick(3,figure,rotation,piece_location,2)
    if (not result):
        result,test_data=wall_kick(4,figure,rotation,piece_location,2)
    if (not result):
        result,test_data=wall_kick(5,figure,rotation,piece_location,2)
    if (not test_data):
        return False
    
    #поворот
    p_clear()
    padenie[piece_location[0][0]+test_data[0]+frdl[figure-1][rotation-1][0][0]][piece_location[0][1]+test_data[1]+frdl[figure-1][rotation-1][0][1]]=figure
    padenie[piece_location[1][0]+test_data[0]+frdl[figure-1][rotation-1][1][0]][piece_location[1][1]+test_data[1]+frdl[figure-1][rotation-1][1][1]]=figure
    padenie[piece_location[2][0]+test_data[0]+frdl[figure-1][rotation-1][2][0]][piece_location[2][1]+test_data[1]+frdl[figure-1][rotation-1][2][1]]=figure
    padenie[piece_location[3][0]+test_data[0]+frdl[figure-1][rotation-1][3][0]][piece_location[3][1]+test_data[1]+frdl[figure-1][rotation-1][3][1]]=figure
    rotation-=1
    return True
                    
#
#
#
#запуск игры
get_statistic()
#resume_button=((400,40), (20,20))
#restart_button=((400,40), (20,80))
#select_music_button=((400,40), (20,140))
#to_menu_button=((400,40), (20,200))
#quit_game_button=((400,40), (20,260))
def get_file_names(folder,remove_mode):
    fiorfo=os.listdir("resources/"+str(folder))
    try:
        if (remove_mode==1):
            for i in range(0,len(fiorfo)-1):
                if ("." not in fiorfo[i]):
                    fiorfo.pop(i)
        elif (remove_mode==2):
            for i in range(0,len(fiorfo)-1):
                if ("." in fiorfo[i]):
                    fiorfo.pop(i)
    except:
        pass
    for i in range(len(fiorfo)):
        if (fiorfo[i]=="themes.ttl"):
            fiorfo.pop(i)
    return fiorfo

#def themes_menu(in_game_call):
#    mouse_button_pressed=(False,False,False)
#    global settings, polzunok_music, polzunok_sound, starting
#    with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
#        downloaded_themes=json.load(downloaded_themes)
#    themes=downloaded_themes.keys()

def new_mat_menu(in_game_call):
    mouse_button_pressed=(False,False,False)
    global settings, polzunok_music, polzunok_sound, starting
    s_music=settings["music"]
    mbd=False
    selected_music=0
    musics=get_file_names("Music",1)
    for i in range(0,len(musics)):
        if (musics[i]==settings["music"]):
            selected_music=i
            break
    selected_theme=0
    themes=[]
    try:
        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
            downloaded_themes=json.load(downloaded_themes)
    except:
        file=open("resources/Themes/themes.ttl", "w", encoding="utf-8")
        file.write("{}")
        file.close()
        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
            downloaded_themes=json.load(downloaded_themes)
    downloaded_themes["Default"]=["Default",1]
    for i in downloaded_themes.keys():
        themes.append(i)
    for i in range(0,len(themes)):
        if (themes[i]==settings["theme"]):
            selected_theme=i
            break
    while True:
        mouse_pos=pygame.mouse.get_pos()
        #print("mat_menu")
        screen.blit(cbg,(0,0))
        s_text("Выбери музыку", True, (0, 20), (255,255,255), 4, font)
        s_text("Выбери тему", True, (0, 260), (255,255,255), 4, font)
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
        screen.blit(up_button10im, (up_button[1][0]*resize,up_button[1][1]*resize))
        screen.blit(down_button10im, (down_button[1][0]*resize,down_button[1][1]*resize))
        screen.blit(up_button10im, (up_button2[1][0]*resize,up_button2[1][1]*resize))
        screen.blit(down_button10im, (down_button2[1][0]*resize,down_button2[1][1]*resize))
        screen.blit(selection,(30*resize,60*resize))
        screen.blit(selection,(30*resize,300*resize))
        
        #draw_button(musicp, bgreen, "+")
        #draw_button(musicpp, bgreen, "++")
        #draw_button(musicm, bred, "-")
        #draw_button(musicmm, bred, "--")
        #draw_button(effectp, bgreen, "+")
        #draw_button(effectpp, bgreen, "++")
        #draw_button(effectm, bred, "-")
        #draw_button(effectmm, bred, "--")
        s_text("Громкость музыки:", True, (0, 200), (255,255,255), 3, font)
        s_text("Громкость звуков:", True, (0, 230), (255,255,255), 3, font)
        if (selected_music-1>=0):
            s_text(musics[selected_music-1],True,(-25,68),(255,255,255),4,font)#screen.blit(font.render(musics[selected_music-1],True,(255,255,255)),(28*resize,68*resize))
        s_text(musics[selected_music],True,(-25,108),(255,255,255),4,font)#screen.blit(font.render(musics[selected_music],True,(255,255,255)),(28*resize,108*resize))
        if (selected_music+1<len(musics)):
            s_text(musics[selected_music+1],True,(-25,148),(255,255,255),4,font)#screen.blit(font.render(musics[selected_music+1],True,(255,255,255)),(28*resize,148*resize))
            
        if (selected_theme-1>=0):
            s_text(downloaded_themes[themes[selected_theme-1]][0],True,(-25,308),(255,255,255),4,font)#screen.blit(font.render(themes[selected_theme-1],True,(255,255,255)),(28*resize,308*resize))
        s_text(downloaded_themes[themes[selected_theme]][0],True,(-25,348),(255,255,255),4,font)#screen.blit(font.render(themes[selected_theme],True,(255,255,255)),(28*resize,348*resize))
        if (selected_theme+1<len(themes)):
            s_text(downloaded_themes[themes[selected_theme+1]][0],True,(-25,388),(255,255,255),4,font)#screen.blit(font.render(themes[selected_theme+1],True,(255,255,255)),(28*resize,388*resize))
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit(in_game_call)
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    save_settings()
                    if (musics[selected_music]!=s_music):
                        starting=True
                        Thread(target=loading_screen).start()
                        if (in_game_call):
                            music_channel.stop()
                        load_music(settings["music"])
                        if (in_game_call):
                            music_channel.play(music, loops=-1, maxtime=0, fade_ms=0)
                            music_channel.pause()
                        starting=False
                    return
                elif (event.key==pygame.K_SPACE):
                    mat_menu(in_game_call)
                #if (event.key==pygame.K_SPACE):
                #    reload_resources("Old_version")
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                polzunok_start_pos=pygame.mouse.get_pos()
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(back_button, mouse_pos)):
                        nav_back.play()
                        save_settings()
                        if (musics[selected_music]!=s_music):
                            starting=True
                            Thread(target=loading_screen).start()
                            if (in_game_call):
                                music_channel.stop()
                            load_music(settings["music"])
                            if (in_game_call):
                                music_channel.play(music, loops=-1, maxtime=0, fade_ms=0)
                                music_channel.pause()
                            starting=False
                        return
                    elif (press_check(up_button,mouse_pos)):
                        nav.play()
                        if (selected_music-1>=0):
                            selected_music-=1
                            settings["music"]=musics[selected_music]
                    elif (press_check(down_button,mouse_pos)):
                        nav.play()
                        if (selected_music+1<len(musics)):
                            selected_music+=1
                            settings["music"]=musics[selected_music]

                    elif (press_check(up_button2,mouse_pos)):
                        nav.play()
                        if (selected_theme-1>=0):
                            selected_theme-=1
                            settings["theme"]=themes[selected_theme]
                            starting=True
                            Thread(target=loading_screen).start()
                            reload_resources(themes[selected_theme])
                            starting=False
                            change_volume()
                    elif (press_check(down_button2,mouse_pos)):
                        nav.play()
                        if (selected_theme+1<len(themes)):
                            selected_theme+=1
                            settings["theme"]=themes[selected_theme]
                            starting=True
                            Thread(target=loading_screen).start()
                            reload_resources(themes[selected_theme])
                            starting=False
                            change_volume()
        if (mbd):
            if (press_check(back_button, mouse_pos)):
                screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
            elif (press_check(up_button,mouse_pos)):
                screen.blit(up_button11im, (up_button[1][0]*resize,up_button[1][1]*resize))
            elif (press_check(down_button,mouse_pos)):
                screen.blit(down_button11im, (down_button[1][0]*resize,down_button[1][1]*resize))
                
            elif (press_check(up_button2,mouse_pos)):
                screen.blit(up_button11im, (up_button2[1][0]*resize,up_button2[1][1]*resize))
            elif (press_check(down_button2,mouse_pos)):
                screen.blit(down_button11im, (down_button2[1][0]*resize,down_button2[1][1]*resize))
            polzunok_music[1]=polzunok(polzunok_music, polzunok_start_pos)
            polzunok_sound[1]=polzunok(polzunok_sound, polzunok_start_pos)
            settings["music_volume"]=polzunok_music[1]/100
            settings["effect_volume"]=polzunok_sound[1]/100
            change_volume()
        polzunok_ris(polzunok_music)
        polzunok_ris(polzunok_sound)
        pygame.display.flip()
        fps.tick(60)
    
def mat_menu(in_game_call):
    mouse_button_pressed=(False,False,False)
    global settings, polzunok_music, polzunok_sound, starting, polzunok_music_volume, polzunok_sound_volume
    s_music=settings["music"]
    mbd=False
    selected_music=0
    musics=get_file_names("Music",1)
    for i in range(0,len(musics)):
        if (musics[i]==settings["music"]):
            selected_music=i
            break
    selected_theme=0
    themes=get_file_names("Themes",2)
    for i in range(0,len(themes)):
        if (themes[i]==settings["theme"]):
            selected_theme=i
            break
    while True:
        mouse_pos=pygame.mouse.get_pos()
        #print("mat_menu")
        screen.blit(cbg,(0,0))
        s_text("Выбери музыку", True, (0, 20), (255,255,255), 4, font)
        s_text("Выбери тему", True, (0, 260), (255,255,255), 4, font)
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
        screen.blit(up_button10im, (up_button[1][0]*resize,up_button[1][1]*resize))
        screen.blit(down_button10im, (down_button[1][0]*resize,down_button[1][1]*resize))
        screen.blit(up_button10im, (up_button2[1][0]*resize,up_button2[1][1]*resize))
        screen.blit(down_button10im, (down_button2[1][0]*resize,down_button2[1][1]*resize))
        screen.blit(selection,(30*resize,60*resize))
        screen.blit(selection,(30*resize,300*resize))
        
        #draw_button(musicp, bgreen, "+")
        #draw_button(musicpp, bgreen, "++")
        #draw_button(musicm, bred, "-")
        #draw_button(musicmm, bred, "--")
        #draw_button(effectp, bgreen, "+")
        #draw_button(effectpp, bgreen, "++")
        #draw_button(effectm, bred, "-")
        #draw_button(effectmm, bred, "--")
        s_text("Громкость музыки:", True, (0, 200), (255,255,255), 3, font)
        s_text("Громкость звуков:", True, (0, 230), (255,255,255), 3, font)
        if (selected_music-1>=0):
            s_text(musics[selected_music-1],True,(-25,68),(255,255,255),4,font)#screen.blit(font.render(musics[selected_music-1],True,(255,255,255)),(28*resize,68*resize))
        s_text(musics[selected_music],True,(-25,108),(255,255,255),4,font)#screen.blit(font.render(musics[selected_music],True,(255,255,255)),(28*resize,108*resize))
        if (selected_music+1<len(musics)):
            s_text(musics[selected_music+1],True,(-25,148),(255,255,255),4,font)#screen.blit(font.render(musics[selected_music+1],True,(255,255,255)),(28*resize,148*resize))
            
        if (selected_theme-1>=0):
            s_text(themes[selected_theme-1],True,(-25,308),(255,255,255),4,font)#screen.blit(font.render(themes[selected_theme-1],True,(255,255,255)),(28*resize,308*resize))
        s_text(themes[selected_theme],True,(-25,348),(255,255,255),4,font)#screen.blit(font.render(themes[selected_theme],True,(255,255,255)),(28*resize,348*resize))
        if (selected_theme+1<len(themes)):
            s_text(themes[selected_theme+1],True,(-25,388),(255,255,255),4,font)#screen.blit(font.render(themes[selected_theme+1],True,(255,255,255)),(28*resize,388*resize))
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit(in_game_call)
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    save_settings()
                    if (musics[selected_music]!=s_music):
                        starting=True
                        Thread(target=loading_screen).start()
                        if (in_game_call):
                            music_channel.stop()
                        load_music(settings["music"])
                        if (in_game_call):
                            music_channel.play(music, loops=-1, maxtime=0, fade_ms=0)
                            music_channel.pause()
                        starting=False
                    return
                #if (event.key==pygame.K_SPACE):
                #    reload_resources("Old_version")
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                polzunok_start_pos=pygame.mouse.get_pos()
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(back_button, mouse_pos)):
                        nav_back.play()
                        save_settings()
                        if (musics[selected_music]!=s_music):
                            starting=True
                            Thread(target=loading_screen).start()
                            if (in_game_call):
                                music_channel.stop()
                            load_music(settings["music"])
                            if (in_game_call):
                                music_channel.play(music, loops=-1, maxtime=0, fade_ms=0)
                                music_channel.pause()
                            starting=False
                        return
                    elif (press_check(up_button,mouse_pos)):
                        nav.play()
                        if (selected_music-1>=0):
                            selected_music-=1
                            settings["music"]=musics[selected_music]
                    elif (press_check(down_button,mouse_pos)):
                        nav.play()
                        if (selected_music+1<len(musics)):
                            selected_music+=1
                            settings["music"]=musics[selected_music]

                    elif (press_check(up_button2,mouse_pos)):
                        nav.play()
                        if (selected_theme-1>=0):
                            selected_theme-=1
                            settings["theme"]=themes[selected_theme]
                            starting=True
                            Thread(target=loading_screen).start()
                            reload_resources(themes[selected_theme])
                            starting=False
                            change_volume()
                    elif (press_check(down_button2,mouse_pos)):
                        nav.play()
                        if (selected_theme+1<len(themes)):
                            selected_theme+=1
                            settings["theme"]=themes[selected_theme]
                            starting=True
                            Thread(target=loading_screen).start()
                            reload_resources(themes[selected_theme])
                            starting=False
                            change_volume()
        if (mbd):
            if (press_check(back_button, mouse_pos)):
                screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
            elif (press_check(up_button,mouse_pos)):
                screen.blit(up_button11im, (up_button[1][0]*resize,up_button[1][1]*resize))
            elif (press_check(down_button,mouse_pos)):
                screen.blit(down_button11im, (down_button[1][0]*resize,down_button[1][1]*resize))
                
            elif (press_check(up_button2,mouse_pos)):
                screen.blit(up_button11im, (up_button2[1][0]*resize,up_button2[1][1]*resize))
            elif (press_check(down_button2,mouse_pos)):
                screen.blit(down_button11im, (down_button2[1][0]*resize,down_button2[1][1]*resize))
            polzunok_music[1]=polzunok(polzunok_music, polzunok_start_pos)
            polzunok_sound[1]=polzunok(polzunok_sound, polzunok_start_pos)
            polzunok_music_volume[1]=polzunok(polzunok_music, polzunok_start_pos)
            polzunok_sound_volume[1]=polzunok(polzunok_sound, polzunok_start_pos)
            settings["music_volume"]=polzunok_music[1]/100
            settings["effect_volume"]=polzunok_sound[1]/100
            change_volume()
        polzunok_ris(polzunok_music)
        polzunok_ris(polzunok_sound)
        pygame.display.flip()
        fps.tick(60)
def personalization_menu(in_game_call):
    mouse_button_pressed=(False,False,False)
    mbd=False
    while True:
        mouse_pos=pygame.mouse.get_pos()
        #print("tf_dialog")
        screen.blit(cbg,(0,0))
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
        s_text("Персонализация", True, (0,20), (255,255,255), 4, bigfont)
        draw_button(pers_music_menu_button, bgreen, "Музыка")
        draw_button(pers_themes_menu_button, baqua, "Темы")
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit(in_game_call)
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    return
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                #polzunok_start_pos=pygame.mouse.get_pos()
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(back_button, mouse_pos)):
                        nav_back.play()
                        return
                    elif (press_check(pers_music_menu_button, mouse_pos)):
                        nav.play()
                        music_menu(in_game_call)
                    elif (press_check(pers_themes_menu_button, mouse_pos)):
                        nav.play()
                        themes_menu(in_game_call)
        if (mbd):
            if (press_check(back_button, mouse_pos)):
                screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
            elif (press_check(pers_music_menu_button, mouse_pos)):
                draw_button(pers_music_menu_button, bpgreen, "Музыка")
            elif (press_check(pers_themes_menu_button, mouse_pos)):
                draw_button(pers_themes_menu_button, bpaqua, "Темы")
        pygame.display.flip()
        fps.tick(60)
    
def game_paused():
    mouse_button_pressed=(False,False,False)
    mbd=False
    #z zh g k f o
    while True:
        mouse_pos=pygame.mouse.get_pos()
        #print("game_paused")
        screen.blit(pause_bg,(0,0))
        draw_button(resume_button, bgreen, "Возобновить игру")
        draw_button(restart_button, byellow, "Перезапустить игру")
        draw_button(select_mat_button, baqua, "Персонализация игры")
        draw_button(p_settings_button, bred, "Настройки")
        draw_button(to_menu_button, bpurple, "Сохранить и выйти в меню")
        draw_button(quit_game_button, borange, "Сохранить и выйти из игры")
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit(True)
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(resume_button,mouse_pos)):
                        nav.play()
                        start_animation()
                        return True
                    elif (press_check(restart_button,mouse_pos)):
                        nav.play()
                        if (tf_dialog("Перезапустить игру", "Вы уверены?", bgreen, bpgreen, "Да", bred, bpred, "Нет", None, None, None, 3)==1):
                            if (restart()):
                                start_animation()
                                return True
                    elif (press_check(select_mat_button,mouse_pos)):
                        nav.play()
                        personalization_menu(True)
                        #mat_menu(True)
                    elif (press_check(p_settings_button,mouse_pos)):
                        nav.play()
                        settings_menu(True)
                    elif (press_check(to_menu_button,mouse_pos)):
                        nav_back.play()
                        save_game()
                        return False
                    elif (press_check(quit_game_button,mouse_pos)):
                        nav_back.play()
                        save_game()
                        exit()
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    start_animation()
                    return True
        if (mbd):
            if (press_check(resume_button,mouse_pos)):
                draw_button(resume_button, bpgreen, "Возобновить игру")
            elif (press_check(restart_button,mouse_pos)):
                draw_button(restart_button, bpyellow, "Перезапустить игру")
            elif (press_check(select_mat_button,mouse_pos)):
                draw_button(select_mat_button, bpaqua, "Персонализация игры")
            elif (press_check(p_settings_button,mouse_pos)):
                draw_button(p_settings_button, bpred, "Настройки")
            elif (press_check(to_menu_button,mouse_pos)):
                draw_button(to_menu_button, bppurple, "Сохранить и выйти в меню")
            elif (press_check(quit_game_button,mouse_pos)):
                draw_button(quit_game_button, bporange, "Сохранить и выйти из игры")

        pygame.display.flip()
        fps.tick(60)
class sanumber:
    def __init__(self, surface, pleft, pcenter, pright, pos):
        self.surface=surface
        self.pleft=[pleft[0][0]+surface.get_rect()[2]//resize, pleft[0][1]-surface.get_rect()[3]/resize//2]
        self.pcenter=[pcenter[0][0]-surface.get_rect()[2]/resize//2, pcenter[0][1]-surface.get_rect()[3]/resize//2]
        self.pright=[pright[0][0]-surface.get_rect()[2]//resize, pright[0][1]-surface.get_rect()[3]/resize//2]
        if (pos==1):
            self.pos=self.pleft
        elif (pos==2):
            self.pos=self.pcenter
        elif (pos==3):
            self.pos=self.pright
        self.ppos=self.pos
        self.la=pleft[1]
        self.ca=pcenter[1]
        self.ra=pright[1]
    def change_pos(self, ppos, pos):
        if (ppos==1):
            self.ppos=self.pleft
            self.palpha=self.la
        elif (ppos==2):
            self.ppos=self.pcenter
            self.palpha=self.ca
        elif (ppos==3):
            self.ppos=self.pright
            self.palpha=self.ra
            
        if (pos==1):
            self.pos=self.pleft
            self.alpha=self.la
        elif (pos==2):
            self.pos=self.pcenter
            self.alpha=self.ca
        elif (pos==3):
            self.pos=self.pright
            self.alpha=self.ra
        
    def blit(self, proc):
        if (0>proc>1):
            return
        if (self.ppos==self.pos):
            return
        pos=self.pos
        pos2=self.ppos
        alpha=self.alpha
        alpha2=self.palpha
        pos=(round(pos2[0]+(pos[0]-pos2[0])*proc),round(pos2[1]+(pos[1]-pos2[1])*proc))
        alpha=round(alpha2+(alpha-alpha2)*proc)
        self.surface.set_alpha(alpha)
        screen.blit(self.surface, (pos[0]*resize, pos[1]*resize))
        
def start_animation():
    global toleft, todown, toright
    #start.play()
    screen.blit(bg,(0,0))
    pygame.display.flip()
    pleft=((0,220),0)
    pcenter=((220,220),255)
    pright=((440,220),0)
    text3=sanumber(hugefont.render("3", True, (255, 255, 255)), pleft, pcenter, pright, 3)
    text2=sanumber(hugefont.render("2", True, (255, 255, 255)), pleft, pcenter, pright, 3)
    text1=sanumber(hugefont.render("1", True, (255, 255, 255)), pleft, pcenter, pright, 3)
    start_sound.play()
    startTime=time.time()
    a0s=time.time()
    a0e=a0s+0.5
    a1s=a0e+0.5
    a1e=a1s+0.5
    a2s=a1e+0.5
    a2e=a2s+0.5
    a3s=a2e+0.5
    a3e=a3s+0.5
    toleft,todown,toright=False,False,False
    proc=0
    a0=False
    a1=False
    a2=False
    a3=False
    while (round(time.time()-startTime,1)<4.0):
        screen.blit(bg,(0,0))
        if (a0s<=time.time()<a0e):
            if (not a0):
                a0=True
                text3.change_pos(3, 2)
            proc=procras(a0s, a0e)
        elif (a1s<=time.time()<=a1e):
            if (not a1):
                a1=True
                text2.change_pos(3, 2)
                text3.change_pos(2, 1)
            proc=procras(a1s, a1e)
        elif (a2s<=time.time()<=a2e):
            if (not a2):
                a2=True
                text1.change_pos(3, 2)
                text2.change_pos(2, 1)
                text3.change_pos(3, 3)
            proc=procras(a2s, a2e)
        elif (a3s<=time.time()<=a3e):
            if (not a3):
                a3=True
                text2.change_pos(2, 2)
                text1.change_pos(2, 1)
            proc=procras(a3s, a3e)
        else:
            proc=1
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit(True)
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_LEFT):
                    toleft=True
                elif (event.key==pygame.K_RIGHT):
                    toright=True
                elif (event.key==pygame.K_DOWN):
                    todown=True
            elif (event.type==pygame.KEYUP):
                if (event.key==pygame.K_LEFT):
                    toleft=False
                elif (event.key==pygame.K_RIGHT):
                    toright=False
                elif (event.key==pygame.K_DOWN):
                    todown=False
        text3.blit(proc)
        text2.blit(proc)
        text1.blit(proc)
        fps.tick(60)
        pygame.display.flip()
def game():
    global running, r_marathon, toleft, toright, todown
    running=True
    Thread(target=stat_tablo).start()
    music_channel.stop()
    #start_animation()
    tchange=False
    moveLST=time.time()
    moveRST=time.time()
    moveDST=time.time()
    moveDAST=time.time()
    toleft=False
    toright=False
    todown=False
    music_channel.play(music, loops=-1, maxtime=0, fade_ms=0)
    music_channel.pause()
    start_animation()
    music_channel.unpause()
    frame=0
    while (running):
        #print("game")
        if (level<16):
            r_marathon=score
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit(True)
                start_animation()
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_LEFT):
                    toleft=True
                    if (left()):
                        changeST=time.time()
                    else:
                        e_move_error.play()
                elif (event.key==pygame.K_RIGHT):
                    toright=True
                    if (right()):
                        changeST=time.time()
                    else:
                        e_move_error.play()
                elif (event.key==pygame.K_UP):
                    if (rotate_cw()):
                        e_rotation_right.play()
                        changeST=time.time()
                    else:
                        e_move_error.play()
                elif (event.key==pygame.K_z):
                    if (rotate_ccw()):
                        e_rotation_left.play()
                        changeST=time.time()
                    else:
                        e_move_error.play()
                elif (event.key==pygame.K_DOWN):
                    todown=True
                    if (down(True)):
                        changeST=time.time()
                #elif (event.key==pygame.K_v):
                #    p_clear()
                #    figura()
                elif (event.key==pygame.K_c):
                    if (pause()):
                        ris()
                        e_tm_p.play()
                        changeST=time.time()
                    else:
                        e_tm_p_error.play()
                elif (event.key==pygame.K_SPACE):
                    #e_hard_drop.play()
                    if (hard_drop()):
                        e_hard_drop.play()
                    else:
                        e_drop.play()
                    ris()
                    figura()
                elif (event.key==pygame.K_ESCAPE):
                    change_volume()
                    music_channel.pause()
                    pause_music_channel.play(pause_music, loops=-1, maxtime=0, fade_ms=0)
                    if (not game_paused()):
                        pause_music_channel.stop()
                        return
                    pause_music_channel.stop()
                    #start_animation()
                    music_channel.unpause()
                    changeST=time.time()
            elif (event.type==pygame.KEYUP):
                if (event.key==pygame.K_LEFT):
                    toleft=False
                elif (event.key==pygame.K_RIGHT):
                    toright=False
                if (event.key==pygame.K_DOWN):
                    todown=False

        if (toleft):
            if (time.time()-moveLST>piece_cd_move_time and not toright):
                if (left()):
                    moveLST=time.time()
                    changeST=time.time()
        if (toright):
            if (time.time()-moveRST>piece_cd_move_time and not toleft):
                if (right()):
                    moveRST=time.time()
                    changeST=time.time()
        if (todown):
            if (time.time()-moveDST>piece_cd_move_time):
                if (down(True)):
                    moveDST=time.time()
                    moveDAST=time.time()
        if (not toleft):
            moveLST=time.time()
        if (not toright):
            moveRST=time.time()
        if (not todown):
            moveDST=time.time()
            
        if (level<=len(speed_levels)):
            if (time.time()-moveDAST>=speed_levels[level-1]):
                down(False)
                moveDAST=time.time()#frame=0
        else:
            if (time.time()-moveDAST>=speed_levels[-1]):
                down(False)
                moveDAST=time.time()#frame=0
        #if (time.time()-moveDAST>piece_cd_moveD_time):
        #    down(False)
        #    moveDAST=time.time()
        
        oldtchange=tchange
        tchange=down_check()
        if (oldtchange!=tchange or not tchange):
            changeST=time.time()
        if (tchange):
            if (level<=len(change_time_sec)):
                if (time.time()-changeST>=change_time_sec[level-1]):
                    e_drop.play()
                    figura()
                    changeST=time.time()
                    oldtchange=False
            else:
                if (time.time()-changeST>=change_time_sec[-1]):
                    e_drop.play()
                    figura()
                    changeST=time.time()
                    oldtchange=False
        #if (frame==60):
        #    frame=0
        frame+=1
        #print(frame)
        ris()
        pygame.display.flip()
        #fps.tick(60)
    game_overed()
def record():
    #0 - рекорд марафона,
    #1 - рекорд бесконечного режима,
    #2 - рекордный уровень,
    #3 - рекордное кол-во расчищенных линий,
    #4 - кол-во расчищенных линий (накопительный),
    #5 - кол-во 1 подряд,
    #6 - кол-во 2 подряд,
    #7 - кол-во 3 подряд,
    #8 - кол-во 4 подряд
    #9 - кол-во комбо
    file=open("stats.dat","r")
    file_read=file.read()
    file.close()
    file_read=file_read.split("\n")
    if (int(file_read[0])<r_marathon):
        file_read[0]=str(r_marathon)
    if (int(file_read[1])<r_endless):
        file_read[1]=str(r_endless)
    if (int(file_read[2])<level):
        file_read[2]=str(level)
    if (int(file_read[3])<linii):
        file_read[3]=str(linii)
    file_read[4]=int(file_read[4])+linii
    file_read[5]=int(file_read[5])+count1row
    file_read[6]=int(file_read[6])+count2row
    file_read[7]=int(file_read[7])+count3row
    file_read[8]=int(file_read[8])+count4row
    file_read[9]=int(file_read[9])+count_combo
    #запись обратно
    file=open("stats.dat","w")
    for i in range(0,len(file_read)-1):
        file.write(str(file_read[i])+"\n")
    file.write(str(file_read[len(file_read)-1]))
    file.close()
def game_overed():
    global level, score, r_endless, positions
    game_over_sound.play()
    music_channel.stop()
    if (level>=16):
        r_endless=score
    record()
    startTime=time.time()
    while (round(time.time()-startTime,2)<=0.70):
        #print("game_overed_1")
        if (round(time.time()-startTime,2)==0.03):
            screen.blit(bg,(0,0))
            for i in range(3,23):
                screen.blit(clear_animation_0, (100*resize, (i-2)*20*resize-10*resize))
            pygame.display.flip()
        elif (round(time.time()-startTime,2)==0.06):
            screen.blit(bg,(0,0))
            for i in range(3,23):
                screen.blit(clear_animation_1, (100*resize, (i-2)*20*resize-10*resize))
            pygame.display.flip()
        elif (round(time.time()-startTime,2)==0.09):
            screen.blit(bg,(0,0))
            for i in range(3,23):
                screen.blit(clear_animation_2, (100*resize, (i-2)*20*resize-10*resize))
            pygame.display.flip()
        elif (round(time.time()-startTime,2)==0.12):
            screen.blit(bg,(0,0))
            for i in range(3,23):
                screen.blit(clear_animation_3, (100*resize, (i-2)*20*resize-10*resize))
            pygame.display.flip()
        elif (round(time.time()-startTime,2)==0.15):
            screen.blit(bg,(0,0))
            for i in range(3,23):
                screen.blit(clear_animation_4, (100*resize, (i-2)*20*resize-10*resize))
            pygame.display.flip()
        elif (round(time.time()-startTime,2)==0.18):
            screen.blit(bg,(0,0))
            for i in range(3,23):
                screen.blit(clear_animation_5, (100*resize, (i-2)*20*resize-10*resize))
            pygame.display.flip()
        elif (round(time.time()-startTime,2)==0.21):
            screen.blit(bg,(0,0))
            for i in range(3,23):
                screen.blit(clear_animation_6, (100*resize, (i-2)*20*resize-10*resize))
            pygame.display.flip()
        elif (round(time.time()-startTime,2)==0.24):
            screen.blit(bg,(0,0))
            for i in range(3,23):
                screen.blit(clear_animation_7, (100*resize, (i-2)*20*resize-10*resize))
            pygame.display.flip()
        elif (round(time.time()-startTime,2)==0.27):
            screen.blit(bg,(0,0))
            for i in range(3,23):
                screen.blit(clear_animation_8, (100*resize, (i-2)*20*resize-10*resize))
            pygame.display.flip()
        elif (round(time.time()-startTime,2)>=0.30):
            screen.blit(bg,(0,0))
            pygame.display.flip()
        fps.tick(60)
    screen.blit(cbg,(0,0))
    s_text("Игра окончена", True, (0,20), (255,255,255), 4, bigfont)
    s_text("Счёт Marathon:", True, (0, 60), (255, 255, 255), 3, font)
    s_text("Счёт Endless:", True, (0, 100), (255, 255, 255), 3, font)
    s_text("Кол-во расчищенных линий:", True, (0, 140), (255, 255, 255), 3, font)
    s_text("Финальный уровень:", True, (0, 180), (255, 255, 255), 3, font)
    s_text("Одинарная расчистка линий:", True, (0, 220), (255, 255, 255), 3, font)
    s_text("Двойная расчистка линий:", True, (0, 260), (255, 255, 255), 3, font)
    s_text("Тройная расчистка линий:", True, (0, 300), (255, 255, 255), 3, font)
    s_text("Расчистка линий \"TETRIS\":", True, (0, 340), (255, 255, 255), 3, font)
    s_text("Кол-во комбо:", True, (0, 380), (255, 255, 255), 3, font)

    s_text(str(r_marathon), True, (0, 60), (255, 255, 255), 2, font)
    s_text(str(r_endless), True, (0, 100), (255, 255, 255), 2, font)
    s_text(str(linii), True, (0, 140), (255, 255, 255), 2, font)
    s_text(str(level), True, (0, 180), (255, 255, 255), 2, font)
    s_text(str(count1row), True, (0, 220), (255, 255, 255), 2, font)
    s_text(str(count2row), True, (0, 260), (255, 255, 255), 2, font)
    s_text(str(count3row), True, (0, 300), (255, 255, 255), 2, font)
    s_text(str(count4row), True, (0, 340), (255, 255, 255), 2, font)
    s_text(str(count_combo), True, (0, 380), (255, 255, 255), 2, font)
    pygame.display.flip()
    for event in pygame.event.get():
        if (event.type==pygame.QUIT):
            exit()
    while (True):
        #print("game_overed_2")
        global f_readed
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit()
            if (event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN):
                #restart()
                    
                try:
                    music_channel.play(menu_music, loops=-1, maxtime=0, fade_ms=0)
                except:
                    pass
                return
#info
def info(in_game_call=False):
    mouse_button_pressed=(False,False,False)
    mbd=False
    while True:
        mouse_pos=pygame.mouse.get_pos()
        #print("tf_dialog")
        screen.blit(cbg,(0,0))
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
        s_text("Об игре", True, (0,20), (255,255,255), 4, bigfont)
        s_text("Это фанатская игра", True, (0,60), (255,255,255), 4, font)
        s_text("Если вы хотите поддержать Tetris,", True, (0,85), (255,255,255), 4, font)
        s_text("то приобретите официальные игры", True, (0,110), (255,255,255), 4, font)
        s_text("на сайте Tetris.com", True, (0,135), (255,255,255), 4, font)
        
        s_text("Исходный код игры пишет Мартин Вернер с 9.12.2020.", True, (0,170), (255,255,255), 4, font18)
        s_text("Движок игры \"pygame\" (https://www.pygame.org/)", True, (0,190), (255,255,255), 4, font18)
        s_text("Звуви вежливо позаимствованы из Tetris 2011 от EA", True, (0,210), (255,255,255), 4, font18)
        s_text("Все торговые марки принадлежат", True, (0,230), (255,255,255), 4, font18)
        s_text("их уважаемым владельцам", True, (0,250), (255,255,255), 4, font18)
        s_text("Спасибо всем, кто помог в создании этой игры!", True, (0,270), (255,255,255), 4, font18)
        #s_text("", True, (0,290), (255,255,255), 4, font18)
        #s_text("", True, (0,310), (255,255,255), 4, font)
        draw_button(tetriscom, bred, "Посетить Tetris.com")
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit(in_game_call)
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    return
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                #polzunok_start_pos=pygame.mouse.get_pos()
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(back_button, mouse_pos)):
                        nav_back.play()
                        return
                    elif (press_check(tetriscom, mouse_pos)):
                        try:subprocess.check_call(["C:\Program Files\Internet Explorer\iexplore.exe","https://tetris.com/product-list"])
                        except:pass
        if (mbd):
            if (press_check(back_button, mouse_pos)):
                screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
            elif (press_check(tetriscom, mouse_pos)):
                draw_button(tetriscom, bpred, "Посетить Tetris.com")
                
        pygame.display.flip()
        fps.tick(60)
#главное меню
def info_screen(title, subtitle, bcolor, bpcolor, btext):
    mouse_button_pressed=(False,False,False)
    mbd=False
    while True:
        mouse_pos=pygame.mouse.get_pos()
        #print("tf_dialog")
        screen.blit(cbg,(0,0))
        draw_button(info_screen_button, bcolor, btext)
        s_text(title, True, (0,20), (255,255,255), 4, bigfont)
        s_text(subtitle, True, (0,60), (255,255,255), 4, font)
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit()
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(info_screen_button, mouse_pos)):
                        nav.play()
                        return
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    return
        if (mbd):
            if (press_check(info_screen_button, mouse_pos)):
                draw_button(info_screen_button, bpcolor, b1text)
        pygame.display.flip()
def tf_dialog(title, subtitle, b1color, b1pcolor, b1text, b2color, b2pcolor, b2text, b3color=None, b3pcolor=None, b3text=None, mode=1):
    mouse_button_pressed=(False,False,False)
    mbd=False
    while True:
        mouse_pos=pygame.mouse.get_pos()
        #print("tf_dialog")
        screen.blit(cbg,(0,0))
        draw_button(dialog_true_button, b1color, b1text)
        draw_button(dialog_false_button, b2color, b2text)
        if (mode==2):
            draw_button(dialog_cancel_button, b3color, b3text)
        s_text(title, True, (0,20), (255,255,255), 4, bigfont)
        s_text(subtitle, True, (0,60), (255,255,255), 4, font)
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit()
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(dialog_true_button, mouse_pos)):
                        nav.play()
                        return 1
                    elif (press_check(dialog_false_button, mouse_pos)):
                        nav.play()
                        return 2
                    elif (press_check(dialog_cancel_button, mouse_pos) and mode==2):
                        nav.play()
                        return 3
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE and (mode==2 or mode==3)):
                    nav_back.play()
                    return 3
        if (mbd):
            if (press_check(dialog_true_button, mouse_pos)):
                draw_button(dialog_true_button, b1pcolor, b1text)
            elif (press_check(dialog_false_button, mouse_pos)):
                draw_button(dialog_false_button, b2pcolor, b2text)
            elif (press_check(dialog_cancel_button, mouse_pos) and mode==2):
                draw_button(dialog_cancel_button, b3pcolor, b3text)
        pygame.display.flip()
def save_game():
    g_save=open("save.gst","w+")
    #positions
    for i in range(0,bordery):
        for j in range(0,borderx):
            g_save.write(str(positions[i][j]))
            g_save.write(",")
    #padenie
    for i in range(0,bordery):
        for j in range(0,borderx):
            g_save.write(str(padenie[i][j]))
            g_save.write(",")   
    #level
    g_save.write(str(level)+",")
    #score
    g_save.write(str(score)+",")
    #linii
    g_save.write(str(linii)+",")
    #rotation
    g_save.write(str(rotation)+",")
    #next0
    g_save.write(str(0)+",")
    #next1
    g_save.write(str(next1)+",")
    #next2
    g_save.write(str(next2)+",")
    #next3
    g_save.write(str(next3)+",")
    #paused
    g_save.write(str(paused)+",")
    #figure
    g_save.write(str(figure)+",")
    #p_s
    g_save.write(str(p_s)+",")
    #r_marathon
    g_save.write(str(r_marathon)+",")
    #count1row
    g_save.write(str(count1row)+",")
    #count2row
    g_save.write(str(count2row)+",")
    #count3row
    g_save.write(str(count3row)+",")
    #count4row
    g_save.write(str(count4row)+",")
    #combo
    g_save.write(str(combo)+",")
    #p_figure 
    g_save.write(str(p_figure)+",")
    #l_cleared
    g_save.write(str(l_cleared)+",")
    #count_combo
    g_save.write(str(count_combo))
    g_save.close()
def settings_menu(in_game_call=False):
    mouse_button_pressed=(False,False,False)
    global settings, toggleproection, toggleaf, togglecleara, togglefall, piece_cd_move_time
    mbd=False
    while True:
        mouse_pos=pygame.mouse.get_pos()
        #print("settings_menu")
        screen.blit(cbg,(0,0))
        s_text("Настройки", True, (0,20), (255,255,255), 4, bigfont)
        s_text("Проекция", True, (0,60), (255,255,255), 3, font22)
        s_text("Анимация замирания фигуры", True, (0,100), (255,255,255), 3, font22)
        s_text("Анимация очищения линий", True, (0,140), (255,255,255), 3, font22)
        s_text("Анимация падения", True, (0,180), (255,255,255), 3, font22)
        if (settings["toggleproection"]):
            draw_button(proekcon, bdgreen, "вкл.")
            draw_button(proekcoff, bred, "выкл.")
        else:
            draw_button(proekcon, bgreen, "вкл.")
            draw_button(proekcoff, bdred, "выкл.")
        if (settings["toggleaf"]):
            draw_button(azfon, bdgreen, "вкл.")
            draw_button(azfoff, bred, "выкл.")
        else:
            draw_button(azfon, bgreen, "вкл.")
            draw_button(azfoff, bdred, "выкл.")
        if (settings["togglecleara"]):
            draw_button(aolon, bdgreen, "вкл.")
            draw_button(aoloff, bred, "выкл.")
        else:
            draw_button(aolon, bgreen, "вкл.")
            draw_button(aoloff, bdred, "выкл.")
        if (settings["togglefall"]):
            draw_button(apon, bdgreen, "вкл.")
            draw_button(apoff, bred, "выкл.")
        else:
            draw_button(apon, bgreen, "вкл.")
            draw_button(apoff, bdred, "выкл.")
        #345
        draw_button(button_resize_plus, bgreen, "+")
        draw_button(button_resize_minus, bred, "-")
        draw_button(button_pcdmt_plus, bgreen, "+")
        draw_button(button_pcdmt_minus, bred, "-")

        s_text("Масштаб (необходим перезапуск)", True, (0,240), (255,255,255), 3, font18)
        s_text("Скорость передвижения фигуры", True, (0,280), (255,255,255), 3, font18)

        s_text(str(settings["resize"]), True, (140,240), (255,255,255), 4, font)
        s_text(str(piece_cd_move_time), True, (140,280), (255,255,255), 4, font)
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit(in_game_call)
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    return
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                #polzunok_start_pos=pygame.mouse.get_pos()
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(back_button, mouse_pos)):
                        nav_back.play()
                        return
                    
                    elif (press_check(proekcon, mouse_pos)):
                        nav.play()
                        toggleproection=settings["toggleproection"]=False
                        save_settings()
                    elif (press_check(proekcoff, mouse_pos)):
                        nav.play()
                        toggleproection=settings["toggleproection"]=True
                        save_settings()
                        
                    elif (press_check(azfon, mouse_pos)):
                        nav.play()
                        toggleaf=settings["toggleaf"]=False
                        save_settings()
                    elif (press_check(azfoff, mouse_pos)):
                        nav.play()
                        toggleaf=settings["toggleaf"]=True
                        save_settings()
                        
                    elif (press_check(aolon, mouse_pos)):
                        nav.play()
                        togglecleara=settings["togglecleara"]=False
                        save_settings()
                    elif (press_check(aoloff, mouse_pos)):
                        nav.play()
                        togglecleara=settings["togglecleara"]=True
                        save_settings()
                        
                    elif (press_check(apon, mouse_pos)):
                        nav.play()
                        togglefall=settings["togglefall"]=False
                        save_settings()
                    elif (press_check(apoff, mouse_pos)):
                        nav.play()
                        togglefall=settings["togglefall"]=True
                        save_settings()
                        
                    elif (press_check(button_resize_plus, mouse_pos)):
                        nav.play()
                        settings["resize"]+=1
                        save_settings()
                    elif (press_check(button_resize_minus, mouse_pos)):
                        nav.play()
                        if (settings["resize"]-1>0):
                            settings["resize"]-=1
                            save_settings()
                        
                    elif (press_check(button_pcdmt_plus, mouse_pos)):
                        nav.play()
                        if (piece_cd_move_time+0.01<=1):
                            piece_cd_move_time=round(piece_cd_move_time+0.01,2)
                            settings["piece_cd_move_time"]=piece_cd_move_time
                            save_settings()
                    elif (press_check(button_pcdmt_minus, mouse_pos)):
                        nav.play()
                        if (piece_cd_move_time-0.01>0):
                            piece_cd_move_time=round(piece_cd_move_time-0.01,2)
                            settings["piece_cd_move_time"]=piece_cd_move_time
                            save_settings()
        if (mbd):
            if (press_check(back_button, mouse_pos)):
                screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
                
            elif (press_check(proekcon, mouse_pos)):
                draw_button(proekcon, bpgreen, "вкл.")
            elif (press_check(proekcoff, mouse_pos)):
                draw_button(proekcoff, bpred, "выкл.")
                
            elif (press_check(azfon, mouse_pos)):
                draw_button(azfon, bpgreen, "вкл.")
            elif (press_check(azfoff, mouse_pos)):
                draw_button(azfoff, bpred, "выкл.")
                
            elif (press_check(aolon, mouse_pos)):
                draw_button(aolon, bpgreen, "вкл.")
            elif (press_check(aoloff, mouse_pos)):
                draw_button(aoloff, bpred, "выкл.")
                
            elif (press_check(apon, mouse_pos)):
                draw_button(apon, bpgreen, "вкл.")
            elif (press_check(apoff, mouse_pos)):
                draw_button(apoff, bpred, "выкл.")

            elif (press_check(button_resize_plus, mouse_pos)):
                draw_button(button_resize_plus, bpgreen, "+")
            elif (press_check(button_resize_minus, mouse_pos)):
                draw_button(button_resize_minus, bpred, "-")
                
            elif (press_check(button_pcdmt_plus, mouse_pos)):
                draw_button(button_pcdmt_plus, bpgreen, "+")
            elif (press_check(button_pcdmt_minus, mouse_pos)):
                draw_button(button_pcdmt_minus, bpred, "-")

            #polzunok_pcdmt[1]=polzunok(polzunok_pcdmt, polzunok_start_pos)
        #polzunok_ris(polzunok_pcdmt)
        pygame.display.flip()
        fps.tick(60)
def get_catalog(page):
    #слыш ты олух, не забудь, что сейчас каталог грузится не с сайта. не забудь это изменить *изменил*
    #0 - ид, 1 - название, автор, версия, 2 - ссылка на превью, 3 - скриншот 1, 4 - скриншот 2, 5 - скриншот 3, 6 - скриншот 4, 7 - скриншот 5, 8 - описание, 9 - ссылка на скачку
    #catalog2=urlopen("http://"+site+"/TETRIS/catalog.txt").read()
    #print(catalog2)
    sock = socket.socket()
    sock.connect((site, 8684))
    sock.send(bytes("1", "utf-8"))

    catlen = int(sock.recv(1024))
    data = sock.recv(catlen)
    sock.close()

    catalog = pickle.loads(data)
    
    #catalog=[[1,["test0","TESTI",1],"resources/catalog/1.png","resources/catalog/2.png","resources/catalog/3.png","resources/catalog/4.png","resources/catalog/5.png","resources/catalog/6.png",["тест каталога",],"none"],
    #         [2,["test1","BISELISS",1],"resources/catalog/2.png","resources/catalog/3.png","resources/catalog/4.png","resources/catalog/5.png","resources/catalog/6.png","resources/catalog/1.png",["тест каталога","тест каталога"],"none"],
    #         [3,["test2","MARTIN",1],"resources/catalog/3.png","resources/catalog/4.png","resources/catalog/5.png","resources/catalog/6.png","resources/catalog/1.png","resources/catalog/2.png",["тест каталога","тест каталога","тест каталога"],"none"],
    #         [4,["test3","ROMA",1],"resources/catalog/4.png","resources/catalog/5.png","resources/catalog/6.png","resources/catalog/1.png","resources/catalog/2.png","resources/catalog/3.png",["тест каталога","тест каталога","тест каталога","тест каталога"],"none"],
    #         [5,["test4","LAURIS",1],"resources/catalog/5.png","resources/catalog/6.png","resources/catalog/1.png","resources/catalog/2.png","resources/catalog/3.png","resources/catalog/4.png",["тест каталога","тест каталога","тест каталога","тест каталога","тест каталога"],"none"],
    #         [6,["test5","ARSENIJ",1],"resources/catalog/6.png","resources/catalog/1.png","resources/catalog/2.png","resources/catalog/3.png","resources/catalog/4.png","resources/catalog/5.png",["ТЕСТ КАТАЛОГА","тест каталога","тест каталога","тест каталога","тест каталога"],"none"]]
    return catalog

def load_catalog(catalog):
    #0 - ид, 1 - название, автор, версия, 2 - ссылка на превью, 3 - скриншот 1, 4 - скриншот 2, 5 - скриншот 3, 6 - скриншот 4, 7 - скриншот 5, 8 - описание, 9 - ссылка на скачку
    #10 - картинка превью, 11 - скриншот 1, 12 - скриншот 1 mini, 13 - скриншот 2, 14 - скриншот 2 mini, 15 - скриншот 3, 16 - скриншот 3 mini, 17 - скриншот 4, 18 - скриншот 4 mini, 19 - скриншот 5, 20 - скриншот 5 mini
    #21 - скриншот 1 полный размер, 22 - скриншот 2 полный размер, 23 - скриншот 3 полный размер, 24 - скриншот 4 полный размер, 25 - скриншот 5 полный размер
    for i in range(len(catalog)):
        logo=pygame.image.load(io.BytesIO(urlopen(catalog[i][2]).read()))
        catalog[i].append(logo)
        catalog[i][10]=pygame.transform.scale(catalog[i][10],(160*resize,160*resize))
        if (catalog[i][3]!=""):
            screenshot1=pygame.image.load(io.BytesIO(urlopen(catalog[i][3]).read()))
            catalog[i].append(screenshot1) 
            catalog[i].append(screenshot1)
            catalog[i][11]=pygame.transform.scale(catalog[i][11],(200*resize,200*resize))
            catalog[i][12]=pygame.transform.scale(catalog[i][12],(100*resize,100*resize))
        if (catalog[i][4]!=""):
            screenshot2=pygame.image.load(io.BytesIO(urlopen(catalog[i][4]).read()))
            catalog[i].append(screenshot2) 
            catalog[i].append(screenshot2)
            catalog[i][13]=pygame.transform.scale(catalog[i][13],(200*resize,200*resize))
            catalog[i][14]=pygame.transform.scale(catalog[i][14],(100*resize,100*resize))
        else:
            catalog[i].append("")
            catalog[i].append("")
        if (catalog[i][5]!=""):
            screenshot3=pygame.image.load(io.BytesIO(urlopen(catalog[i][5]).read()))
            catalog[i].append(screenshot3) 
            catalog[i].append(screenshot3)
            catalog[i][15]=pygame.transform.scale(catalog[i][15],(200*resize,200*resize))
            catalog[i][16]=pygame.transform.scale(catalog[i][16],(100*resize,100*resize))
        else:
            catalog[i].append("")
            catalog[i].append("")
        if (catalog[i][6]!=""):
            screenshot4=pygame.image.load(io.BytesIO(urlopen(catalog[i][6]).read()))
            catalog[i].append(screenshot4) 
            catalog[i].append(screenshot4)
            catalog[i][17]=pygame.transform.scale(catalog[i][17],(200*resize,200*resize))
            catalog[i][18]=pygame.transform.scale(catalog[i][18],(100*resize,100*resize))
        else:
            catalog[i].append("")
            catalog[i].append("")
        if (catalog[i][7]!=""):
            screenshot5=pygame.image.load(io.BytesIO(urlopen(catalog[i][7]).read()))
            catalog[i].append(screenshot5) 
            catalog[i].append(screenshot5)
            catalog[i][19]=pygame.transform.scale(catalog[i][19],(200*resize,200*resize))
            catalog[i][20]=pygame.transform.scale(catalog[i][20],(100*resize,100*resize))
        else:
            catalog[i].append("")
            catalog[i].append("")
        if (catalog[i][3]!=""):
            catalog[i].append(screenshot1)
        if (catalog[i][4]!=""):
            catalog[i].append(screenshot2)
        if (catalog[i][5]!=""):
            catalog[i].append(screenshot3)
        if (catalog[i][6]!=""):
            catalog[i].append(screenshot4)
        if (catalog[i][7]!=""):
            catalog[i].append(screenshot5)
    return catalog

def download_theme(id, theme_data):
    #return
    global starting, loading_screen_to_show
    if (theme_data[1][0]=="Default"):
        return False
    starting=True
    Thread(target=loading_screen).start()
    loading_screen_to_show="Скачка темы..."
    data=requests.get(theme_data[9],allow_redirects=True)
    try:os.mkdir("tmp")
    except:pass
    open("tmp/"+str(theme_data[0])+".zip","wb").write(data.content)
    loading_screen_to_show="Распаковка темы..."
    with zipfile.ZipFile("tmp/"+str(id)+".zip", 'r') as zip_ref:
        zip_ref.extractall("resources/Themes/"+str(id))
    with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
        downloaded_themes=json.load(downloaded_themes)
    downloaded_themes[str(id)]=[theme_data[1][0],theme_data[1][2]]
    with open("resources/Themes/themes.ttl", "w", encoding="utf-8") as write_file:
        json.dump(downloaded_themes, write_file, ensure_ascii=False, indent=4)
    starting=False
    shutil.rmtree("tmp")
    reload_resources(settings["theme"])
    return True

def remove_theme(id, theme_data):
    global starting, loading_screen_to_show, settings
    if (launch_theme==str(id)):
        return remove_theme2(id,theme_data)
    if (theme_data!=None):
        if (theme_data[0]=="Default"):
            return False
    starting=True
    Thread(target=loading_screen).start()
    if (settings["theme"]==str(id)):
        reload_resources("Default")
        change_volume()
        settings["theme"]="Default"
        save_settings()
    loading_screen_to_show="Удаление темы..."
    try:
        shutil.rmtree("resources/Themes/"+str(id))
    except:
        pass
    loading_screen_to_show=""
    with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
        downloaded_themes=json.load(downloaded_themes)
    try:
        del downloaded_themes[str(id)]
    except:
        pass
    with open("resources/Themes/themes.ttl", "w", encoding="utf-8") as write_file:
        json.dump(downloaded_themes, write_file, ensure_ascii=False, indent=4)
    starting=False
    return True

def remove_theme2(id, theme_data):
    global starting, loading_screen_to_show, settings, ib_mode
    if (theme_data!=None):
        if (theme_data[0]=="Default"):
            return False
    starting=True
    Thread(target=loading_screen).start()
    if (settings["theme"]==str(id)):
        change_volume()
        settings["theme"]="Default"
        save_settings()
    loading_screen_to_show="Подготовка к удалению темы..."
    loading_screen_to_show=""
    with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
        downloaded_themes=json.load(downloaded_themes)
    try:
        del downloaded_themes[str(id)]
    except:
        pass
    settings["rtol"].append(str(id))
    save_settings()
    ib_mode=1
    Thread(target=ib).start()
    with open("resources/Themes/themes.ttl", "w", encoding="utf-8") as write_file:
        json.dump(downloaded_themes, write_file, ensure_ascii=False, indent=4)
    starting=False
    return True

def update_theme(id, theme_data):
    global starting, loading_screen_to_show
    if (launch_theme==str(id)):
        return update_theme2(id,theme_data)
    change_theme=False
    if (theme_data[1][0]=="Default"):
        return False
    starting=True
    Thread(target=loading_screen).start()
    if (settings["theme"]==str(id)):
        loading_screen_to_show="Смена темы перед обновлением..."
        change_theme=True
        reload_resources("Default")
    loading_screen_to_show="Обновление темы..."
    try:
        shutil.rmtree("resources/Themes/"+str(id))
    except:
        pass
    data=requests.get(theme_data[9],allow_redirects=True)
    try:os.mkdir("tmp")
    except:pass
    open("tmp/"+str(theme_data[0])+".zip","wb").write(data.content)
    with zipfile.ZipFile("tmp/"+str(id)+".zip", 'r') as zip_ref:
        zip_ref.extractall("resources/Themes/"+str(id))
    with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
        downloaded_themes=json.load(downloaded_themes)
    downloaded_themes[str(id)]=[theme_data[1][0],theme_data[1][2]]
    with open("resources/Themes/themes.ttl", "w", encoding="utf-8") as write_file:
        json.dump(downloaded_themes, write_file, ensure_ascii=False, indent=4)
    loading_screen_to_show=""
    starting=False
    shutil.rmtree("tmp")
    if (change_theme):
        reload_resources(str(id))
    return True

def update_theme2(id, theme_data):
    global starting, loading_screen_to_show, ib_mode
    if (theme_data[1][0]=="Default"):
        return False
    starting=True
    Thread(target=loading_screen).start()
    loading_screen_to_show="Подготовка к обновлению темы..."
    data=requests.get(theme_data[9],allow_redirects=True)
    try:os.mkdir("tuol")
    except:pass
    try:os.mkdir("tmp")
    except:pass
    open("tmp/"+str(theme_data[0])+".zip","wb").write(data.content)
    with zipfile.ZipFile("tmp/"+str(id)+".zip", 'r') as zip_ref:
        zip_ref.extractall("tuol/"+str(id))
    with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
        downloaded_themes=json.load(downloaded_themes)
    downloaded_themes[str(id)]=[theme_data[1][0],theme_data[1][2]]
    with open("resources/Themes/themes.ttl", "w", encoding="utf-8") as write_file:
        json.dump(downloaded_themes, write_file, ensure_ascii=False, indent=4)
    loading_screen_to_show=""
    starting=False
    shutil.rmtree("tmp")
    ib_mode=1
    Thread(target=ib).start()
    return True
    
def fullscreen_screenshot(screenshot):
    mouse_button_pressed=(False,False,False)
    screenshot=pygame.transform.scale(screenshot,(screen_size,screen_size))
    screen.blit(cbg, (0,0))
    screen.blit(screenshot, (0,0))
    #screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
    mbd=False
    while True:
        mouse_pos=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit()
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    return
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    #if (press_check(back_button,mouse_pos)):
                    nav_back.play()
                    return
        #if (mbd):
        #    if (press_check(back_button,mouse_pos)):
        #        screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
        pygame.display.flip()
        fps.tick(60)

def catalog_theme_info(full_theme_data):
    global starting
    mouse_button_pressed=(False,False,False)
    with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
        downloaded_themes=json.load(downloaded_themes)
    try:
        theme_data=downloaded_themes[str(full_theme_data[0])]
        if (theme_data[1]<full_theme_data[1][2]):
            update_available=True
        else:
            update_available=False
        not_downloaded=False
    except:
        update_available=False
        not_downloaded=True
    #if (full_theme_data[1][0] not in downloaded_themes):
    #    not_downloaded=True
    #else:
    #    not_downloaded=False
    selected_screenshot=1
    mbd=False
    nalevo=((100,100),(10,90))
    napravo=((100,100),(330,90))
    centre=((200,200),(120,40))

    ibtup=((360,40),(40,300))
    while True:
        mouse_pos=pygame.mouse.get_pos()
        screen.blit(cbg,(0,0))
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
        screen.blit(full_theme_data[9+selected_screenshot*2],(centre[1][0]*resize,centre[1][1]*resize))
        s_text(full_theme_data[1][0], True, (0,10), (255,255,255), 4, bigfont)
        if (not_downloaded):
            draw_button(catalog_theme_download, bgreen, "Скачать")
        else:
            if (update_available):
                draw_button(catalog_theme_update, baqua, "Обновить")
                draw_button(catalog_theme_remove, bred, "Удалить")
            else:
                draw_button(catalog_theme_download, bred, "Удалить")
        for i in range(len(full_theme_data[8])):
            s_text(full_theme_data[8][i], True, (0,244+20*i), (255,255,255), 4, font18)
        s_text("Автор: "+full_theme_data[1][1], True, (0,354), (255,255,255), 4, font22)
        if (selected_screenshot>1):
            screen.blit(full_theme_data[8+selected_screenshot*2],(nalevo[1][0]*resize,nalevo[1][1]*resize))
        if (12+selected_screenshot*2<len(full_theme_data) and full_theme_data[12+selected_screenshot*2]!=""):
            screen.blit(full_theme_data[12+selected_screenshot*2],(napravo[1][0]*resize,napravo[1][1]*resize))
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit()
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    return
                elif (event.key==pygame.K_LEFT):
                    if (selected_screenshot>1):
                        selected_screenshot-=1
                elif (event.key==pygame.K_RIGHT):
                    if (selected_screenshot<5):
                        selected_screenshot+=1
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(back_button,mouse_pos)):
                        nav_back.play()
                        return
                    elif (press_check(nalevo,mouse_pos)):
                        if (selected_screenshot>1):
                            selected_screenshot-=1
                    elif (press_check(napravo,mouse_pos)):
                        if (12+selected_screenshot*2<len(full_theme_data) and full_theme_data[12+selected_screenshot*2]!=""):
                            selected_screenshot+=1
                    elif (press_check(centre,mouse_pos)):
                        nav.play()
                        fullscreen_screenshot(full_theme_data[20+selected_screenshot])

                    if (not_downloaded):
                        if (press_check(catalog_theme_download,mouse_pos)):
                            download_theme(full_theme_data[0], full_theme_data)
                            not_downloaded=False
                        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
                            downloaded_themes=json.load(downloaded_themes)
                        try:
                            theme_data=downloaded_themes[str(full_theme_data[0])]
                            if (theme_data[1]<full_theme_data[1][2]):
                                update_available=True
                            else:
                                update_available=False
                            not_downloaded=False
                        except:
                            update_available=False
                            not_downloaded=True
                            
                    else:
                        if (update_available):
                            if (press_check(catalog_theme_update,mouse_pos)):
                                update_theme(full_theme_data[0], full_theme_data)
                                not_downloaded=False
                            elif (press_check(catalog_theme_remove,mouse_pos)):
                                try:
                                    remove_theme(full_theme_data[0], full_theme_data)
                                except Exception as error:
                                    starting=False
                                    print(error)
                                not_downloaded=True
                        else:
                            if (press_check(catalog_theme_download,mouse_pos)):
                                try:
                                    remove_theme(full_theme_data[0], full_theme_data)
                                except Exception as error:
                                    starting=False
                                    print(error)
                                not_downloaded=True
                        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
                            downloaded_themes=json.load(downloaded_themes)
                        try:
                            theme_data=downloaded_themes[str(full_theme_data[0])]
                            if (theme_data[1]<full_theme_data[1][2]):
                                update_available=True
                            else:
                                update_available=False
                            not_downloaded=False
                        except:
                            update_available=False
                            not_downloaded=True
                                
                    """
                    elif (press_check(catalog_theme_download,mouse_pos)):
                        nav.play()
                        if (not_downloaded):
                            download_theme(full_theme_data[1][0], full_theme_data[9])
                        else:
                            try:
                                remove_theme(full_theme_data[1][0])
                            except Exception as error:
                                starting=False
                                print(error)
                            file=open("resources/Themes/themes.ttl","r")
                            downloaded_themes=file.read()
                            file.close()
                            downloaded_themes=downloaded_themes.split(",")
                            if (full_theme_data[1][0] not in downloaded_themes):
                                not_downloaded=True
                            else:
                                not_downloaded=False
                    """
        if (mbd):
            if (press_check(back_button,mouse_pos)):
                screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
            if (not_downloaded):
                if (press_check(catalog_theme_download,mouse_pos)):
                    draw_button(catalog_theme_download, bpgreen, "Скачать")
            else:
                if (update_available):
                    if (press_check(catalog_theme_update,mouse_pos)):
                        draw_button(catalog_theme_update, bpaqua, "Обновить")
                    elif (press_check(catalog_theme_remove,mouse_pos)):
                        draw_button(catalog_theme_remove, bpred, "Удалить")
                else:
                    if (press_check(catalog_theme_download,mouse_pos)):
                        draw_button(catalog_theme_download, bpred, "Удалить")

        if (show_ib):
            screen.blit(ibtu, (ibtup[1][0]*resize, ibtup[1][1]*resize))
            s_text("Тема будет обновлена после перезапуска", True, (220,320), (255,255,255), 5, font18)
        
        pygame.display.flip()
        fps.tick(60)
        
def themes_catalog():
    global starting, loading_screen_to_show
    mouse_button_pressed=(False,False,False)
    #return
    starting=True
    Thread(target=loading_screen).start()
    #начало загрузки
    loading_screen_to_show="Получение и загрузка каталога..."
    catalog=load_catalog(get_catalog(1))
    #test1=pygame.image.load(io.BytesIO(urlopen(file_r[0][1]).read()))
    #file=open("test1.png","wb")
    #file.write(requests.get(file_r[0][1]).content)
    #file.close()
    #test1=pygame.image.load("test1.png")
    #loading_screen_to_show="Чтение themes.ttl"
    #with open("resources/Themes/themes.ttl", encoding="utf-8") as file_read:
    #    file_read=json.load(file_read)
    #id: name, version
    #file=open("resources/Themes/themes.ttl","r")
    #file_read=file.read()
    #file.close()
    #file_read=file_read.split(",")
    loading_screen_to_show=""
    #конец загрузки
    starting=False
    mbd=False
    scroll=0
    p_scroll=0
    #0 - размер; 1 - координаты
    catalog_button0=[[160,160],[40,-160]]
    catalog_button1=[[160,160],[240,-160]]
    catalog_button2=[[160,160],[40,40]]
    catalog_button3=[[160,160],[240,40]]
    catalog_button4=[[160,160],[40,240]]
    catalog_button5=[[160,160],[240,240]]
    catalog_button6=[[160,160],[40,440]]
    catalog_button7=[[160,160],[240,440]]

    ibtup=((360,40),(40,360))
    while True:
        #0 - размер; 1 - координаты
        catalog_button0[1][1]=(-160-p_scroll)
        catalog_button1[1][1]=(-160-p_scroll)
        catalog_button2[1][1]=(40-p_scroll)
        catalog_button3[1][1]=(40-p_scroll)
        catalog_button4[1][1]=(240-p_scroll)
        catalog_button5[1][1]=(240-p_scroll)
        catalog_button6[1][1]=(440-p_scroll)
        catalog_button7[1][1]=(440-p_scroll)
        
        if (p_scroll>=200):
            p_scroll-=200
            if (scroll+2<len(catalog)):
                scroll+=2
        if (p_scroll<=-200):
            p_scroll+=200
            if (scroll-2>=0):
                scroll-=2
        
        mouse_pos=pygame.mouse.get_pos()
        screen.blit(cbg,(0,0))
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
        screen.blit(up_button10im, (catalog_up[1][0]*resize,catalog_up[1][1]*resize))
        screen.blit(down_button10im, (catalog_down[1][0]*resize,catalog_down[1][1]*resize))
        if (-1+scroll>=0):
            screen.blit(catalog[-2+scroll][10],(40*resize,(-160-p_scroll)*resize))
        if (-1+scroll>=0):
            screen.blit(catalog[-1+scroll][10],(240*resize,(-160-p_scroll)*resize))
        if (len(catalog)>=1+scroll):
            screen.blit(catalog[0+scroll][10],(40*resize,(40-p_scroll)*resize))
        if (len(catalog)>=2+scroll):
            screen.blit(catalog[1+scroll][10],(240*resize,(40-p_scroll)*resize))
        if (len(catalog)>=3+scroll):
            screen.blit(catalog[2+scroll][10],(40*resize,(240-p_scroll)*resize))
        if (len(catalog)>=4+scroll):
            screen.blit(catalog[3+scroll][10],(240*resize,(240-p_scroll)*resize))
        if (len(catalog)>=5+scroll):
            screen.blit(catalog[4+scroll][10],(40*resize,(440-p_scroll)*resize))
        if (len(catalog)>=5+scroll):
            screen.blit(catalog[5+scroll][10],(240*resize,(440-p_scroll)*resize))
        #draw_button(catalog_button0, (100,0,0), "-2")
        #draw_button(catalog_button1, (200,0,0), "-1")
        #draw_button(catalog_button2, (0,100,0), "0")
        #draw_button(catalog_button3, (0,200,0), "1")
        #draw_button(catalog_button4, (0,0,100), "2")
        #draw_button(catalog_button5, (0,0,200), "3")
        #draw_button(catalog_button6, (100,0,100), "4")
        #draw_button(catalog_button7, (200,0,200), "5")
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit()
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    return
                elif (event.key==pygame.K_UP):
                    if (scroll-2>=0):
                        scroll-=2
                        p_scroll=0
                elif (event.key==pygame.K_DOWN):
                    if (scroll+2<len(catalog)):
                        scroll+=2
                        p_scroll=0
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
                if (event.button==4):
                    if (scroll-2>=0 or p_scroll!=0):
                        p_scroll-=25
                elif (event.button==5):
                    if (scroll+2<len(catalog) or p_scroll!=0):
                        p_scroll+=25
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(back_button,mouse_pos)):
                        nav_back.play()
                        return
                    elif (press_check(catalog_up,mouse_pos)):
                        if (scroll-2>=0):
                            scroll-=2
                            p_scroll=0
                        nav.play()
                    elif (press_check(catalog_down,mouse_pos)):
                        if (scroll+2<len(catalog)):
                            scroll+=2
                            p_scroll=0
                        nav.play()
                    elif (press_check(catalog_button0,mouse_pos)):
                        nav.play()
                        catalog_theme_info(catalog[-2+scroll])
                    elif (press_check(catalog_button1,mouse_pos)):
                        nav.play()
                        catalog_theme_info(catalog[-1+scroll])
                    elif (press_check(catalog_button2,mouse_pos)):
                        nav.play()
                        catalog_theme_info(catalog[0+scroll])
                    elif (press_check(catalog_button3,mouse_pos)):
                        nav.play()
                        catalog_theme_info(catalog[1+scroll])
                    elif (press_check(catalog_button4,mouse_pos)):
                        nav.play()
                        catalog_theme_info(catalog[2+scroll])
                    elif (press_check(catalog_button5,mouse_pos)):
                        nav.play()
                        catalog_theme_info(catalog[3+scroll])
                    elif (press_check(catalog_button6,mouse_pos)):
                        nav.play()
                        catalog_theme_info(catalog[4+scroll])
                    elif (press_check(catalog_button7,mouse_pos)):
                        nav.play()
                        catalog_theme_info(catalog[5+scroll])
        if (mbd):
            if (press_check(back_button,mouse_pos)):
                screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
            elif (press_check(catalog_up,mouse_pos)):
                screen.blit(up_button11im, (catalog_up[1][0]*resize,catalog_up[1][1]*resize))
            elif (press_check(catalog_down,mouse_pos)):
                screen.blit(down_button11im, (catalog_down[1][0]*resize,catalog_down[1][1]*resize))

        
        if (show_ib):
            screen.blit(ibtu, (ibtup[1][0]*resize, ibtup[1][1]*resize))
            s_text("Тема будет обновлена после перезапуска", True, (220,380), (255,255,255), 5, font18)
            
        pygame.display.flip()
        fps.tick(60)
def get_downloaded_themes():
    global downloaded_themes, downloaded_themes_keys
    try:
        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
            downloaded_themes=json.load(downloaded_themes)
    except:
        file=open("resources/Themes/themes.ttl", "w", encoding="utf-8")
        file.write("{}")
        file.close()
        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
            downloaded_themes=json.load(downloaded_themes)
    downloaded_themes["Default"]=["Default",1]
    downloaded_themes_keys=[]
    for i in downloaded_themes.keys():
        downloaded_themes[i].append(None)
        downloaded_themes[i].append(False)
        downloaded_themes[i].append(None)
    downloaded_themes_keys=list(downloaded_themes.keys())
def themes_menu(in_game_call):
    global downloaded_themes, settings, downloaded_themes_keys, ib_mode
    """
    try:
        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
            downloaded_themes=json.load(downloaded_themes)
    except:
        file=open("resources/Themes/themes.ttl", "w", encoding="utf-8")
        file.write("{}")
        file.close()
        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
            downloaded_themes=json.load(downloaded_themes)
    downloaded_themes["Default"]=["Default",1]
    downloaded_themes_keys=[]
    for i in downloaded_themes.keys():
        downloaded_themes[i].append(None)
        downloaded_themes[i].append(False)
        downloaded_themes[i].append(None)
    downloaded_themes_keys=list(downloaded_themes.keys())
    """
    get_downloaded_themes()
    #print(downloaded_themes)
    
    prevp=((100,100),(0,0))

    for i in range(0,5):
        if (i<len(downloaded_themes_keys)):
            downloaded_themes[downloaded_themes_keys[i]][2]=noprev
            Thread(target=load_prev,args=(downloaded_themes_keys[i],prevp[0],)).start()
    if (connection):
        try:
            Thread(target=themes_cfu).start()
        except:
            pass
    mouse_button_pressed=(False,False,False)
    mbd=False
    scroll=0
    max_scroll=0
    p_scroll=0
    #0 - размер; 1 - координаты
    themes_button0=[[360,100],[40,-80]]
    themes_button1=[[360,100],[40,40]]
    themes_button2=[[360,100],[40,160]]
    themes_button3=[[360,100],[40,280]]
    themes_button4=[[360,100],[40,400]]
    themes_button5=[[360,100],[40,520]]

    load_button=((130,50),(100,50))
    load2_button=((260,50),(100,50))
    remove_button=((130,50),(230,50))
    remove2_button=((130,25),(230,50))
    update_button=((130,25),(230,75))
    prevp=((100,100),(0,0))
    tbgp=((360,100),(0,0))

    ibtup=((360,40),(40,360))
    
    while True:
        #0 - размер; 1 - координаты
        themes_button0[1][1]=(-80-p_scroll)
        themes_button1[1][1]=(40-p_scroll)
        themes_button2[1][1]=(160-p_scroll)
        themes_button3[1][1]=(280-p_scroll)
        themes_button4[1][1]=(400-p_scroll)
        themes_button5[1][1]=(520-p_scroll)
        
        tlb0=[[load_button[0][0],load_button[0][1]],[themes_button0[1][0]+load_button[1][0],themes_button0[1][1]+load_button[1][1]]]
        tl2b0=[[load2_button[0][0],load2_button[0][1]],[themes_button0[1][0]+load2_button[1][0],themes_button0[1][1]+load2_button[1][1]]]
        trb0=[[remove_button[0][0],remove_button[0][1]],[themes_button0[1][0]+remove_button[1][0],themes_button0[1][1]+remove_button[1][1]]]
        tr2b0=[[remove2_button[0][0],remove2_button[0][1]],[themes_button0[1][0]+remove2_button[1][0],themes_button0[1][1]+remove2_button[1][1]]]
        tub0=[[update_button[0][0],update_button[0][1]],[themes_button0[1][0]+update_button[1][0],themes_button0[1][1]+update_button[1][1]]]
        prevp0=[[prevp[0][0],prevp[0][1]],[themes_button0[1][0]+prevp[1][0],themes_button0[1][1]+prevp[1][1]]]
        tbgp0=[[tbgp[0][0],tbgp[0][1]],[themes_button0[1][0]+tbgp[1][0],themes_button0[1][1]+tbgp[1][1]]]

        tlb1=[[load_button[0][0],load_button[0][1]],[themes_button1[1][0]+load_button[1][0],themes_button1[1][1]+load_button[1][1]]]
        tl2b1=[[load2_button[0][0],load2_button[0][1]],[themes_button1[1][0]+load2_button[1][0],themes_button1[1][1]+load2_button[1][1]]]
        trb1=[[remove_button[0][0],remove_button[0][1]],[themes_button1[1][0]+remove_button[1][0],themes_button1[1][1]+remove_button[1][1]]]
        tr2b1=[[remove2_button[0][0],remove2_button[0][1]],[themes_button1[1][0]+remove2_button[1][0],themes_button1[1][1]+remove2_button[1][1]]]
        tub1=[[update_button[0][0],update_button[0][1]],[themes_button1[1][0]+update_button[1][0],themes_button1[1][1]+update_button[1][1]]]
        prevp1=[[prevp[0][0],prevp[0][1]],[themes_button1[1][0]+prevp[1][0],themes_button1[1][1]+prevp[1][1]]]
        tbgp1=[[tbgp[0][0],tbgp[0][1]],[themes_button1[1][0]+tbgp[1][0],themes_button1[1][1]+tbgp[1][1]]]
        
        tlb2=[[load_button[0][0],load_button[0][1]],[themes_button2[1][0]+load_button[1][0],themes_button2[1][1]+load_button[1][1]]]
        tl2b2=[[load2_button[0][0],load2_button[0][1]],[themes_button2[1][0]+load2_button[1][0],themes_button2[1][1]+load2_button[1][1]]]
        trb2=[[remove_button[0][0],remove_button[0][1]],[themes_button2[1][0]+remove_button[1][0],themes_button2[1][1]+remove_button[1][1]]]
        tr2b2=[[remove2_button[0][0],remove2_button[0][1]],[themes_button2[1][0]+remove2_button[1][0],themes_button2[1][1]+remove2_button[1][1]]]
        tub2=[[update_button[0][0],update_button[0][1]],[themes_button2[1][0]+update_button[1][0],themes_button2[1][1]+update_button[1][1]]]
        prevp2=[[prevp[0][0],prevp[0][1]],[themes_button2[1][0]+prevp[1][0],themes_button2[1][1]+prevp[1][1]]]
        tbgp2=[[tbgp[0][0],tbgp[0][1]],[themes_button2[1][0]+tbgp[1][0],themes_button2[1][1]+tbgp[1][1]]]
        
        tlb3=[[load_button[0][0],load_button[0][1]],[themes_button3[1][0]+load_button[1][0],themes_button3[1][1]+load_button[1][1]]]
        tl2b3=[[load2_button[0][0],load2_button[0][1]],[themes_button3[1][0]+load2_button[1][0],themes_button3[1][1]+load2_button[1][1]]]
        trb3=[[remove_button[0][0],remove_button[0][1]],[themes_button3[1][0]+remove_button[1][0],themes_button3[1][1]+remove_button[1][1]]]
        tr2b3=[[remove2_button[0][0],remove2_button[0][1]],[themes_button3[1][0]+remove2_button[1][0],themes_button3[1][1]+remove2_button[1][1]]]
        tub3=[[update_button[0][0],update_button[0][1]],[themes_button3[1][0]+update_button[1][0],themes_button3[1][1]+update_button[1][1]]]
        prevp3=[[prevp[0][0],prevp[0][1]],[themes_button3[1][0]+prevp[1][0],themes_button3[1][1]+prevp[1][1]]]
        tbgp3=[[tbgp[0][0],tbgp[0][1]],[themes_button3[1][0]+tbgp[1][0],themes_button3[1][1]+tbgp[1][1]]]
        
        tlb4=[[load_button[0][0],load_button[0][1]],[themes_button4[1][0]+load_button[1][0],themes_button4[1][1]+load_button[1][1]]]
        tl2b4=[[load2_button[0][0],load2_button[0][1]],[themes_button4[1][0]+load2_button[1][0],themes_button4[1][1]+load2_button[1][1]]]
        trb4=[[remove_button[0][0],remove_button[0][1]],[themes_button4[1][0]+remove_button[1][0],themes_button4[1][1]+remove_button[1][1]]]
        tr2b4=[[remove2_button[0][0],remove2_button[0][1]],[themes_button4[1][0]+remove2_button[1][0],themes_button4[1][1]+remove2_button[1][1]]]
        tub4=[[update_button[0][0],update_button[0][1]],[themes_button4[1][0]+update_button[1][0],themes_button4[1][1]+update_button[1][1]]]
        prevp4=[[prevp[0][0],prevp[0][1]],[themes_button4[1][0]+prevp[1][0],themes_button4[1][1]+prevp[1][1]]]
        tbgp4=[[tbgp[0][0],tbgp[0][1]],[themes_button4[1][0]+tbgp[1][0],themes_button4[1][1]+tbgp[1][1]]]
        
        tlb5=[[load_button[0][0],load_button[0][1]],[themes_button5[1][0]+load_button[1][0],themes_button5[1][1]+load_button[1][1]]]
        tl2b5=[[load2_button[0][0],load2_button[0][1]],[themes_button5[1][0]+load2_button[1][0],themes_button5[1][1]+load2_button[1][1]]]
        trb5=[[remove_button[0][0],remove_button[0][1]],[themes_button5[1][0]+remove_button[1][0],themes_button5[1][1]+remove_button[1][1]]]
        tr2b5=[[remove2_button[0][0],remove2_button[0][1]],[themes_button5[1][0]+remove2_button[1][0],themes_button5[1][1]+remove2_button[1][1]]]
        tub5=[[update_button[0][0],update_button[0][1]],[themes_button5[1][0]+update_button[1][0],themes_button5[1][1]+update_button[1][1]]]
        prevp5=[[prevp[0][0],prevp[0][1]],[themes_button5[1][0]+prevp[1][0],themes_button5[1][1]+prevp[1][1]]]
        tbgp5=[[tbgp[0][0],tbgp[0][1]],[themes_button5[1][0]+tbgp[1][0],themes_button5[1][1]+tbgp[1][1]]]
        
        if (p_scroll>=120):
            p_scroll-=120
            if (scroll+1<len(downloaded_themes_keys)):
                scroll+=1
        if (p_scroll<=-120):
            p_scroll+=120
            if (scroll-1>=0):
                scroll-=1
        
        mouse_pos=pygame.mouse.get_pos()
        screen.blit(cbg,(0,0))
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
        screen.blit(up_button10im, (catalog_up[1][0]*resize,catalog_up[1][1]*resize))
        screen.blit(down_button10im, (catalog_down[1][0]*resize,catalog_down[1][1]*resize))
        screen.blit(mat_button10im, (mat_button[1][0]*resize,mat_button[1][1]*resize))
        draw_button(catalog_button, bred, "Посетить каталог тем")
        if (scroll-1>=0):
            #draw_button(themes_button0, (100,0,0), downloaded_themes_keys[scroll-1])
            screen.blit(tbg, (tbgp0[1][0]*resize,tbgp0[1][1]*resize))
            s_text(downloaded_themes[downloaded_themes_keys[scroll-1]][0], True, (270,-55-p_scroll), (255,255,255), 5, font)
            if (downloaded_themes[downloaded_themes_keys[scroll-1]][2]!=None):
                screen.blit(downloaded_themes[downloaded_themes_keys[scroll-1]][2], (prevp0[1][0]*resize,prevp0[1][1]*resize))
            else:
                screen.blit(noprev, (prevp0[1][0]*resize,prevp0[1][1]*resize))
            if (downloaded_themes_keys[scroll-1]!="Default"):
                if (downloaded_themes[downloaded_themes_keys[scroll-1]][3]):
                    draw_button(tlb0, bgreen, "Применить", font18)
                    draw_button(tr2b0, bred, "Удалить", font18)
                    draw_button(tub0, baqua, "Обновить", font18)
                else:
                    draw_button(tlb0, bgreen, "Применить", font18)
                    draw_button(trb0, bred, "Удалить", font18)
            else:
                draw_button(tl2b0, bgreen, "Применить", font18)
        if (scroll<len(downloaded_themes_keys)):
            #draw_button(themes_button1, (200,0,0), downloaded_themes_keys[scroll])
            screen.blit(tbg, (tbgp1[1][0]*resize,tbgp1[1][1]*resize))
            s_text(downloaded_themes[downloaded_themes_keys[scroll]][0], True, (270,65-p_scroll), (255,255,255), 5, font)
            if (downloaded_themes[downloaded_themes_keys[scroll]][2]!=None):
                screen.blit(downloaded_themes[downloaded_themes_keys[scroll]][2], (prevp1[1][0]*resize,prevp1[1][1]*resize))
            else:
                screen.blit(noprev, (prevp1[1][0]*resize,prevp1[1][1]*resize))
            if (downloaded_themes_keys[scroll]!="Default"):
                if (downloaded_themes[downloaded_themes_keys[scroll]][3]):
                    draw_button(tlb1, bgreen, "Применить", font18)
                    draw_button(tr2b1, bred, "Удалить", font18)
                    draw_button(tub1, baqua, "Обновить", font18)
                else:
                    draw_button(tlb1, bgreen, "Применить", font18)
                    draw_button(trb1, bred, "Удалить", font18)
            else:
                draw_button(tl2b1, bgreen, "Применить", font18)
        if (scroll+1<len(downloaded_themes_keys)):
            #draw_button(themes_button2, (0,100,0), downloaded_themes_keys[scroll+1])
            screen.blit(tbg, (tbgp2[1][0]*resize,tbgp2[1][1]*resize))
            s_text(downloaded_themes[downloaded_themes_keys[scroll+1]][0], True, (270,185-p_scroll), (255,255,255), 5, font)
            if (downloaded_themes[downloaded_themes_keys[scroll+1]][2]!=None):
                screen.blit(downloaded_themes[downloaded_themes_keys[scroll+1]][2], (prevp2[1][0]*resize,prevp2[1][1]*resize))
            else:
                screen.blit(noprev, (prevp2[1][0]*resize,prevp2[1][1]*resize))
            if (downloaded_themes_keys[scroll+1]!="Default"):
                if (downloaded_themes[downloaded_themes_keys[scroll+1]][3]):
                    draw_button(tlb2, bgreen, "Применить", font18)
                    draw_button(tr2b2, bred, "Удалить", font18)
                    draw_button(tub2, baqua, "Обновить", font18)
                else:
                    draw_button(tlb2, bgreen, "Применить", font18)
                    draw_button(trb2, bred, "Удалить", font18)
            else:
                draw_button(tl2b2, bgreen, "Применить", font18)
        if (scroll+2<len(downloaded_themes_keys)):
            #draw_button(themes_button3, (0,200,0), downloaded_themes_keys[scroll+2])
            screen.blit(tbg, (tbgp3[1][0]*resize,tbgp3[1][1]*resize))
            s_text(downloaded_themes[downloaded_themes_keys[scroll+2]][0], True, (270,305-p_scroll), (255,255,255), 5, font)
            if (downloaded_themes[downloaded_themes_keys[scroll+2]][2]!=None):
                screen.blit(downloaded_themes[downloaded_themes_keys[scroll+2]][2], (prevp3[1][0]*resize,prevp3[1][1]*resize))
            else:
                screen.blit(noprev, (prevp3[1][0]*resize,prevp3[1][1]*resize))
            if (downloaded_themes_keys[scroll+2]!="Default"):
                if (downloaded_themes[downloaded_themes_keys[scroll+2]][3]):
                    draw_button(tlb3, bgreen, "Применить", font18)
                    draw_button(tr2b3, bred, "Удалить", font18)
                    draw_button(tub3, baqua, "Обновить", font18)
                else:
                    draw_button(tlb3, bgreen, "Применить", font18)
                    draw_button(trb3, bred, "Удалить", font18)
            else:
                draw_button(tl2b3, bgreen, "Применить", font18)
        if (scroll+3<len(downloaded_themes_keys)):
            #draw_button(themes_button4, (0,0,100), downloaded_themes_keys[scroll+3])
            screen.blit(tbg, (tbgp4[1][0]*resize,tbgp4[1][1]*resize))
            s_text(downloaded_themes[downloaded_themes_keys[scroll+3]][0], True, (270,425-p_scroll), (255,255,255), 5, font)
            if (downloaded_themes[downloaded_themes_keys[scroll+3]][2]!=None):
                screen.blit(downloaded_themes[downloaded_themes_keys[scroll+3]][2], (prevp4[1][0]*resize,prevp4[1][1]*resize))
            else:
                screen.blit(noprev, (prevp4[1][0]*resize,prevp4[1][1]*resize))
            if (downloaded_themes_keys[scroll+3]!="Default"):
                if (downloaded_themes[downloaded_themes_keys[scroll+3]][3]):
                    draw_button(tlb4, bgreen, "Применить", font18)
                    draw_button(tr2b4, bred, "Удалить", font18)
                    draw_button(tub4, baqua, "Обновить", font18)
                else:
                    draw_button(tlb4, bgreen, "Применить", font18)
                    draw_button(trb4, bred, "Удалить", font18)
            else:
                draw_button(tl2b4, bgreen, "Применить", font18)
        if (scroll+4<len(downloaded_themes_keys)):
            #draw_button(themes_button5, (0,0,200), downloaded_themes_keys[scroll+4])
            screen.blit(tbg, (tbgp5[1][0]*resize,tbgp5[1][1]*resize))
            s_text(downloaded_themes[downloaded_themes_keys[scroll+4]][0], True, (270,545-p_scroll), (255,255,255), 5, font)
            if (downloaded_themes[downloaded_themes_keys[scroll+4]][2]!=None):
                screen.blit(downloaded_themes[downloaded_themes_keys[scroll+4]][2], (prevp5[1][0]*resize,prevp5[1][1]*resize))
            else:
                screen.blit(noprev, (prevp5[1][0]*resize,prevp5[1][1]*resize))
            if (downloaded_themes_keys[scroll+4]!="Default"):
                if (downloaded_themes[downloaded_themes_keys[scroll+4]][3]):
                    draw_button(tlb5, bgreen, "Применить", font18)
                    draw_button(tr2b5, bred, "Удалить", font18)
                    draw_button(tub5, baqua, "Обновить", font18)
                else:
                    draw_button(tlb5, bgreen, "Применить", font18)
                    draw_button(trb5, bred, "Удалить", font18)
            else:
                draw_button(tl2b5, bgreen, "Применить", font18)
        """
        draw_button(themes_button0, (100,0,0), "-2")
        draw_button(themes_button1, (200,0,0), "-1")
        draw_button(themes_button2, (0,100,0), "0")
        draw_button(themes_button3, (0,200,0), "1")
        draw_button(themes_button4, (0,0,100), "2")
        draw_button(themes_button5, (0,0,200), "3")
        
        draw_button(tlb0, (100,0,0), "-2")
        draw_button(trb0, (200,0,0), "-1")
        draw_button(tr2b0, (0,100,0), "0")
        draw_button(tlb0, (0,200,0), "1")

        draw_button(tlb1, (100,0,0), "-2")
        draw_button(trb1, (200,0,0), "-1")
        draw_button(tr2b1, (0,100,0), "0")
        draw_button(tlb1, (0,200,0), "1")

        draw_button(tlb2, (100,0,0), "-2")
        draw_button(trb2, (200,0,0), "-1")
        draw_button(tr2b2, (0,100,0), "0")
        draw_button(tlb2, (0,200,0), "1")

        draw_button(tlb3, (100,0,0), "-2")
        draw_button(trb3, (200,0,0), "-1")
        draw_button(tr2b3, (0,100,0), "0")
        draw_button(tlb3, (0,200,0), "1")

        draw_button(tlb4, (100,0,0), "-2")
        draw_button(trb4, (200,0,0), "-1")
        draw_button(tr2b4, (0,100,0), "0")
        draw_button(tlb4, (0,200,0), "1")

        draw_button(tlb5, (100,0,0), "-2")
        draw_button(trb5, (200,0,0), "-1")
        draw_button(tr2b5, (0,100,0), "0")
        draw_button(tlb5, (0,200,0), "1")
        """
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit()
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    return
                elif (event.key==pygame.K_UP):
                    if (scroll-1>=0):
                        scroll-=1
                        p_scroll=0
                elif (event.key==pygame.K_DOWN):
                    if (scroll+1<len(downloaded_themes_keys)):
                        scroll+=1
                        p_scroll=0
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
                if (event.button==4):
                    if (scroll-1>=0 or p_scroll!=0):
                        p_scroll-=20
                elif (event.button==5):
                    if (scroll+1<len(downloaded_themes_keys) or p_scroll!=0):
                        p_scroll+=20
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(back_button,mouse_pos)):
                        nav_back.play()
                        return
                    elif (press_check(catalog_up,mouse_pos)):
                        if (scroll-1>=0):
                            scroll-=1
                            p_scroll=0
                        nav.play()
                    elif (press_check(catalog_down,mouse_pos)):
                        if (scroll+1<len(downloaded_themes_keys)):
                            scroll+=1
                            p_scroll=0
                        nav.play()
                    elif (press_check(catalog_button,mouse_pos)):
                        nav.play()
                        try:
                            if (connection):
                                themes_catalog()
                                get_downloaded_themes()
                                Thread(target=themes_cfu).start()
                                for i in range(0,5):
                                    if (i<len(downloaded_themes_keys)):
                                        downloaded_themes[downloaded_themes_keys[i]][2]=noprev
                                        Thread(target=load_prev,args=(downloaded_themes_keys[i],prevp[0],)).start()
                            else:
                                ib_mode=2
                                Thread(target=ib).start()
                        except:
                            ib_mode=2
                            Thread(target=ib).start()
                    elif (press_check(mat_button, mouse_pos)):
                        nav.play()
                        mat_menu(True)

                    
                    elif (press_check(themes_button0,mouse_pos)):
                        if (scroll-1<len(downloaded_themes_keys)):
                            if (downloaded_themes[downloaded_themes_keys[scroll-1]][3]):
                                if (press_check(tlb0,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll-1])
                                elif (press_check(tr2b0,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll-1])
                                elif (press_check(tub0,mouse_pos)):
                                    tmut(downloaded_themes_keys[scroll-1])
                            elif (downloaded_themes_keys[scroll-1]=="Default"):
                                if (press_check(tl2b0,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll-1])
                            else:
                                if (press_check(tlb0,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll-1])
                                elif (press_check(trb0,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll-1])
                    
                    elif (press_check(themes_button1,mouse_pos)):
                        if (scroll<len(downloaded_themes_keys)):
                            if (downloaded_themes[downloaded_themes_keys[scroll]][3]):
                                if (press_check(tlb1,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll])
                                elif (press_check(tr2b1,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll])
                                elif (press_check(tub1,mouse_pos)):
                                    tmut(downloaded_themes_keys[scroll])
                            elif (downloaded_themes_keys[scroll]=="Default"):
                                if (press_check(tl2b1,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll])
                            else:
                                if (press_check(tlb1,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll])
                                elif (press_check(trb1,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll])

                    elif (press_check(themes_button2,mouse_pos)):
                        if (scroll+1<len(downloaded_themes_keys)):
                            if (downloaded_themes[downloaded_themes_keys[scroll+1]][3]):
                                if (press_check(tlb2,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+1])
                                elif (press_check(tr2b2,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll+1])
                                elif (press_check(tub2,mouse_pos)):
                                    tmut(downloaded_themes_keys[scroll+1])
                            elif (downloaded_themes_keys[scroll+1]=="Default"):
                                if (press_check(tl2b2,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+1])
                            else:
                                if (press_check(tlb2,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+1])
                                elif (press_check(trb2,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll+1])

                    elif (press_check(themes_button3,mouse_pos)):
                        if (scroll+2<len(downloaded_themes_keys)):
                            if (downloaded_themes[downloaded_themes_keys[scroll+2]][3]):
                                if (press_check(tlb3,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+2])
                                elif (press_check(tr2b3,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll+2])
                                elif (press_check(tub3,mouse_pos)):
                                    tmut(downloaded_themes_keys[scroll+2])
                            elif (downloaded_themes_keys[scroll+2]=="Default"):
                                if (press_check(tl2b3,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+2])
                            else:
                                if (press_check(tlb3,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+2])
                                elif (press_check(trb3,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll+2])

                    elif (press_check(themes_button4,mouse_pos)):
                        if (scroll+3<len(downloaded_themes_keys)):
                            if (downloaded_themes[downloaded_themes_keys[scroll+3]][3]):
                                if (press_check(tlb4,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+3])
                                elif (press_check(tr2b4,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll+3])
                                elif (press_check(tub4,mouse_pos)):
                                    tmut(downloaded_themes_keys[scroll+3])
                            elif (downloaded_themes_keys[scroll+3]=="Default"):
                                if (press_check(tl2b4,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+3])
                            else:
                                if (press_check(tlb4,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+3])
                                elif (press_check(trb4,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll+3])

                    elif (press_check(themes_button5,mouse_pos)):
                        if (scroll+4<len(downloaded_themes_keys)):
                            if (downloaded_themes[downloaded_themes_keys[scroll+4]][3]):
                                if (press_check(tlb5,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+4])
                                elif (press_check(tr2b5,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll+4])
                                elif (press_check(tub5,mouse_pos)):
                                    tmut(downloaded_themes_keys[scroll+4])
                            elif (downloaded_themes_keys[scroll+4]=="Default"):
                                if (press_check(tl2b5,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+4])
                            else:
                                if (press_check(tlb5,mouse_pos)):
                                    tmlt(downloaded_themes_keys[scroll+4])
                                elif (press_check(trb5,mouse_pos)):
                                    tmrt(downloaded_themes_keys[scroll+4])
                    """
                    elif (press_check(themes_button2,mouse_pos)):
                        if (downloaded_themes[downloaded_themes_keys[scroll+1]][3]):
                    elif (press_check(themes_button3,mouse_pos)):
                        if (downloaded_themes[downloaded_themes_keys[scroll+2]][3]):
                    elif (press_check(themes_button4,mouse_pos)):
                        if (downloaded_themes[downloaded_themes_keys[scroll+3]][3]):
                    elif (press_check(themes_button5,mouse_pos)):
                        if (downloaded_themes[downloaded_themes_keys[scroll+4]][3]):
                    """
        if (mbd):
            if (press_check(back_button,mouse_pos)):
                screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
            elif (press_check(catalog_up,mouse_pos)):
                screen.blit(up_button11im, (catalog_up[1][0]*resize,catalog_up[1][1]*resize))
            elif (press_check(catalog_down,mouse_pos)):
                screen.blit(down_button11im, (catalog_down[1][0]*resize,catalog_down[1][1]*resize))
            elif (press_check(catalog_button,mouse_pos)):
                draw_button(catalog_button, bpred, "Посетить каталог тем")
            elif (press_check(mat_button, mouse_pos)):
                screen.blit(mat_button11im, (mat_button[1][0]*resize,mat_button[1][1]*resize))

            elif (press_check(themes_button0,mouse_pos)):
                if (scroll-1<len(downloaded_themes_keys)):
                    if (downloaded_themes[downloaded_themes_keys[scroll-1]][3]):
                        if (press_check(tlb0,mouse_pos)):
                            draw_button(tlb0, bpgreen, "Применить", font18)
                        elif (press_check(tr2b0,mouse_pos)):
                            draw_button(tr2b0, bpred, "Удалить", font18)
                        elif (press_check(tub0,mouse_pos)):
                            draw_button(tub0, bpaqua, "Обновить", font18)
                    elif (downloaded_themes_keys[scroll-1]=="Default"):
                        if (press_check(tl2b0,mouse_pos)):
                            draw_button(tl2b0, bpgreen, "Применить", font18)
                    else:
                        if (press_check(tlb0,mouse_pos)):
                            draw_button(tlb0, bpgreen, "Применить", font18)
                        elif (press_check(trb0,mouse_pos)):
                            draw_button(trb0, bpred, "Удалить", font18)
                        
            elif (press_check(themes_button1,mouse_pos)):
                if (scroll<len(downloaded_themes_keys)):
                    if (downloaded_themes[downloaded_themes_keys[scroll]][3]):
                        if (press_check(tlb1,mouse_pos)):
                            draw_button(tlb1, bpgreen, "Применить", font18)
                        elif (press_check(tr2b1,mouse_pos)):
                            draw_button(tr2b1, bpred, "Удалить", font18)
                        elif (press_check(tub1,mouse_pos)):
                            draw_button(tub1, bpaqua, "Обновить", font18)
                    elif (downloaded_themes_keys[scroll]=="Default"):
                        if (press_check(tl2b1,mouse_pos)):
                            draw_button(tl2b1, bpgreen, "Применить", font18)
                    else:
                        if (press_check(tlb1,mouse_pos)):
                            draw_button(tlb1, bpgreen, "Применить", font18)
                        elif (press_check(trb1,mouse_pos)):
                            draw_button(trb1, bpred, "Удалить", font18)
                        
            elif (press_check(themes_button2,mouse_pos)):
                if (scroll+1<len(downloaded_themes_keys)):
                    if (downloaded_themes[downloaded_themes_keys[scroll+1]][3]):
                        if (press_check(tlb2,mouse_pos)):
                            draw_button(tlb2, bpgreen, "Применить", font18)
                        elif (press_check(tr2b2,mouse_pos)):
                            draw_button(tr2b2, bpred, "Удалить", font18)
                        elif (press_check(tub2,mouse_pos)):
                            draw_button(tub2, bpaqua, "Обновить", font18)
                    elif (downloaded_themes_keys[scroll+1]=="Default"):
                        if (press_check(tl2b2,mouse_pos)):
                            draw_button(tl2b2, bpgreen, "Применить", font18)
                    else:
                        if (press_check(tlb2,mouse_pos)):
                            draw_button(tlb2, bpgreen, "Применить", font18)
                        elif (press_check(trb2,mouse_pos)):
                            draw_button(trb2, bpred, "Удалить", font18)
                        
            elif (press_check(themes_button3,mouse_pos)):
                if (scroll+2<len(downloaded_themes_keys)):
                    if (downloaded_themes[downloaded_themes_keys[scroll+2]][3]):
                        if (press_check(tlb3,mouse_pos)):
                            draw_button(tlb3, bpgreen, "Применить", font18)
                        elif (press_check(tr2b3,mouse_pos)):
                            draw_button(tr2b3, bpred, "Удалить", font18)
                        elif (press_check(tub3,mouse_pos)):
                            draw_button(tub3, bpaqua, "Обновить", font18)
                    elif (downloaded_themes_keys[scroll+2]=="Default"):
                        if (press_check(tl2b3,mouse_pos)):
                            draw_button(tl2b3, bpgreen, "Применить", font18)
                    else:
                        if (press_check(tlb3,mouse_pos)):
                            draw_button(tlb3, bpgreen, "Применить", font18)
                        elif (press_check(trb3,mouse_pos)):
                            draw_button(trb3, bpred, "Удалить", font18)
                        
            elif (press_check(themes_button4,mouse_pos)):
                if (scroll+3<len(downloaded_themes_keys)):
                    if (downloaded_themes[downloaded_themes_keys[scroll+3]][3]):
                        if (press_check(tlb4,mouse_pos)):
                            draw_button(tlb4, bpgreen, "Применить", font18)
                        elif (press_check(tr2b4,mouse_pos)):
                            draw_button(tr2b4, bpred, "Удалить", font18)
                        elif (press_check(tub4,mouse_pos)):
                            draw_button(tub4, bpaqua, "Обновить", font18)
                    elif (downloaded_themes_keys[scroll+3]=="Default"):
                        if (press_check(tl2b4,mouse_pos)):
                            draw_button(tl2b4, bpgreen, "Применить", font18)
                    else:
                        if (press_check(tlb4,mouse_pos)):
                            draw_button(tlb4, bpgreen, "Применить", font18)
                        elif (press_check(trb4,mouse_pos)):
                            draw_button(trb4, bpred, "Удалить", font18)
                        
            elif (press_check(themes_button5,mouse_pos)):
                if (scroll+4<len(downloaded_themes_keys)):
                    if (downloaded_themes[downloaded_themes_keys[scroll+4]][3]):
                        if (press_check(tlb5,mouse_pos)):
                            draw_button(tlb5, bpgreen, "Применить", font18)
                        elif (press_check(tr2b5,mouse_pos)):
                            draw_button(tr2b5, bpred, "Удалить", font18)
                        elif (press_check(tub5,mouse_pos)):
                            draw_button(tub5, bpaqua, "Обновить", font18)
                    elif (downloaded_themes_keys[scroll+4]=="Default"):
                        if (press_check(tl2b5,mouse_pos)):
                            draw_button(tl2b5, bpgreen, "Применить", font18)
                    else:
                        if (press_check(tlb5,mouse_pos)):
                            draw_button(tlb5, bpgreen, "Применить", font18)
                        elif (press_check(trb5,mouse_pos)):
                            draw_button(trb5, bpred, "Удалить", font18)
        
        if (max_scroll<scroll):
            max_scroll=scroll
        #print(max_scroll, len(downloaded_themes_keys), downloaded_themes[downloaded_themes_keys[max_scroll+4]][2])
        if (max_scroll+4<len(downloaded_themes_keys) and downloaded_themes[downloaded_themes_keys[max_scroll+4]][2]==None):
            downloaded_themes[downloaded_themes_keys[max_scroll+4]][2]=noprev
            Thread(target=load_prev,args=(downloaded_themes_keys[max_scroll+4],prevp[0],)).start()
        
        if (p_scroll>=120):
            p_scroll-=120
            if (scroll+1<len(downloaded_themes_keys)):
                scroll+=1
        if (p_scroll<=-120):
            p_scroll+=120
            if (scroll-1>=0):
                scroll-=1
        if (show_ib and ib_mode==1):
            screen.blit(ibtu, (ibtup[1][0]*resize, ibtup[1][1]*resize))
            s_text("Тема будет обновлена после перезапуска", True, (220,380), (255,255,255), 5, font18)
        if (show_ib and ib_mode==2):
            screen.blit(ibtu, (ibtup[1][0]*resize, ibtup[1][1]*resize))
            s_text("Не удалось установить соединение", True, (220,380), (255,255,255), 5, font18)
        #draw_button(((360,40),(40,360)),bblack,"Тема будет обновлена после перезапуска",font18)
        pygame.display.flip()
        fps.tick(60)
def ib():
    global show_ib
    show_ib=True
    time.sleep(5)
    show_ib=False
    
def tmlt(theme):
    global settings, starting
    starting=True
    Thread(target=loading_screen).start()
    settings["theme"]=theme
    save_settings()
    reload_resources(theme)
    change_volume()
    starting=False

def tmrt(theme):
    global settings, downloaded_themes, downloaded_themes_keys
    remove_theme(theme, downloaded_themes[theme][4])
    try:
        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
            downloaded_themes=json.load(downloaded_themes)
    except:
        file=open("resources/Themes/themes.ttl", "w", encoding="utf-8")
        file.write("{}")
        file.close()
        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
            downloaded_themes=json.load(downloaded_themes)
    downloaded_themes["Default"]=["Default",1]
    downloaded_themes_keys=[]
    for i in downloaded_themes.keys():
        downloaded_themes[i].append(None)
        downloaded_themes[i].append(False)
        downloaded_themes[i].append(None)
    downloaded_themes_keys=list(downloaded_themes.keys())
    
    prevp=((100,100),(0,0))

    for i in range(0,5):
        if (i<len(downloaded_themes_keys)):
            downloaded_themes[downloaded_themes_keys[i]][2]=noprev
            Thread(target=load_prev,args=(downloaded_themes_keys[i],prevp[0],)).start()

    Thread(target=themes_cfu).start()

def tmut(theme):
    global settings, downloaded_themes
    update_theme(theme, downloaded_themes[theme][4])
    try:
        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
            downloaded_themes=json.load(downloaded_themes)
    except:
        file=open("resources/Themes/themes.ttl", "w", encoding="utf-8")
        file.write("{}")
        file.close()
        with open("resources/Themes/themes.ttl", encoding="utf-8") as downloaded_themes:
            downloaded_themes=json.load(downloaded_themes)
    downloaded_themes["Default"]=["Default",1]
    downloaded_themes_keys=[]
    for i in downloaded_themes.keys():
        downloaded_themes[i].append(None)
        downloaded_themes[i].append(False)
        downloaded_themes[i].append(None)
    downloaded_themes_keys=list(downloaded_themes.keys())
    
    prevp=((100,100),(0,0))

    for i in range(0,5):
        if (i<len(downloaded_themes_keys)):
            downloaded_themes[downloaded_themes_keys[i]][2]=noprev
            Thread(target=load_prev,args=(downloaded_themes_keys[i],prevp[0],)).start()

    Thread(target=themes_cfu).start()

def load_prev(name, size):
    global downloaded_themes
    try:
        file=pygame.image.load("resources/Themes/"+name+"/resources/prev.png").convert_alpha()
        file=pygame.transform.scale(file, (size[0]*resize, size[1]*resize))
        downloaded_themes[name][2]=file
    except:
        pass
def themes_cfu():
    global downloaded_themes
    catalog=get_catalog(1)
    for i in catalog:
        try:
            if (str(i[0]) in downloaded_themes.keys()):
                if (i[1][2]>downloaded_themes[str(i[0])][1]):
                    downloaded_themes[str(i[0])][3]=True
                downloaded_themes[str(i[0])][4]=i
        except Exception as error:
            print(error)

def procras(starttime, endtime):
    return (time.time()-starttime)*100/(endtime-starttime)

discpos=[{"pos":[-50,135],"size":[50,50],"alpha":75},   #-2
         {"pos":[90,110],"size":[100,100],"alpha":125}, #-1
         {"pos":[145,85],"size":[150,150],"alpha":255},#0
         {"pos":[245,110],"size":[100,100],"alpha":125},#1
         {"pos":[440,135],"size":[50,50],"alpha":75}]   #2

last_disc=-1
def get_disc():
    global last_disc
    dcount=7
    last_disc+=1
    if (last_disc>=dcount):
        last_disc=0
    if (last_disc==0):
        return red_disc
    elif (last_disc==1):
        return orange_disc
    elif (last_disc==2):
        return yellow_disc
    elif (last_disc==3):
        return green_disc
    elif (last_disc==4):
        return aqua_disc
    elif (last_disc==5):
        return blue_disc
    elif (last_disc==6):
        return purple_disc
    print(last_disc)

class music_disc:
    def __init__(self, selected_music, pos, music_name):
        self.pos=pos
        self.ppos=0
        #self.color=(randint(0,255),randint(0,255),randint(0,255))
        #сделать, чтобы были не картинки, а цветные круги
        self.image=get_disc().copy()#disc.copy()
        #self.image=colorize(disc,self.color)
        self.music_name=music_name
        #Thread(target=colorize,args=(disc,self.color,self)).start()
        
    def blit(self, selected_music, proc):
        posc=self.pos-selected_music
        if (posc<-2): posc=-2
        elif (posc>2): posc=2
        posc=self.pos-selected_music
        pposc=posc+self.ppos
        if (pposc<-2): pposc=-2
        elif (pposc>2): pposc=2
        data=discpos[posc+2]
        pdata=discpos[pposc+2]

        pos=data["pos"]
        size=data["size"]
        alpha=data["alpha"]
        pos2=pdata["pos"]
        size2=pdata["size"]
        alpha2=pdata["alpha"]

        pr=1/proc
        #print(pos, pos2)
        if (proc!=1):
            pos=(round(pos2[0]+(pos[0]-pos2[0])*proc),round(pos2[1]+(pos[1]-pos2[1])*proc))
            size=(round(size2[0]+(size[0]-size2[0])*proc),round(size2[1]+(size[1]-size2[1])*proc))
        alpha=round(alpha2+(alpha-alpha2)*proc)
        self.image.set_alpha(alpha)
            #pos=(round((pos[0]-pos2[0])*pr+pos[0]), round((pos[1]-pos2[1])*pr+pos[1]))
            #size=(round((size[0]-size2[0])*pr+size[0]), round((size[1]-size2[1])*pr+size[1]))
            #alpha=round((alpha-alpha2)*pr+alpha)
        
        #print("self.pos:", self.pos, "pos:", pos, "posc:", posc, "pposc:", pposc, "self.ppos:", self.ppos, "selected_music:", selected_music)
        screen.blit(pygame.transform.scale(self.image, (size[0]*resize, size[1]*resize)), (pos[0]*resize, pos[1]*resize))

    def test(self):
        print("test")

def procras(starttime, endtime):
    return (time.time()-starttime)*1/(endtime-starttime)

def music_menu(in_game_call):
    global settings, starting, polzunok_music_volume, polzunok_sound_volume, colored_discs_mass, last_disc
    last_disc=-1
    colored_discs_mass=[]
    proc=1
    s_music=settings["music"]
    mbd=False
    selected_music=0
    music_list=get_file_names("Music",1)
    for i in range(0,len(music_list)):
        if (music_list[i]==settings["music"]):
            selected_music=i
            break
    music_discs=[]
    for i in range(len(music_list)):
        music_discs.append(music_disc(selected_music,i,music_list[i]))
    
    disc_left_press_box=((220, discpos[2]["size"][1]),(0, discpos[2]["pos"][1]))
    disc_right_press_box=((220, discpos[2]["size"][1]),(220, discpos[2]["pos"][1]))
    mouse_button_pressed=(False,False,False)
    while True:
        mouse_pos=pygame.mouse.get_pos()
        if (proc<1):
            proc=procras(stime, stime+0.25)
        screen.blit(cbg, (0,0))
        s_text("Музыка", True, (0, 20), (255,255,255), 4, font)
        s_text("Громкость музыки:", True, (0, 300), (255,255,255), 3, font)
        s_text("Громкость звуков:", True, (0, 330), (255,255,255), 3, font)
        if (selected_music-2>=0): music_discs[selected_music-2].blit(selected_music, proc)
        if (selected_music+2<len(music_discs)): music_discs[selected_music+2].blit(selected_music, proc)
        if (selected_music-1>=0): music_discs[selected_music-1].blit(selected_music, proc)
        if (selected_music+1<len(music_discs)): music_discs[selected_music+1].blit(selected_music, proc)
        music_discs[selected_music].blit(selected_music, proc)
        s_text(music_discs[selected_music].music_name, True, (0, 255), (255,255,255), 4, font)
        screen.blit(back_button10im, (back_button[1][0]*resize,back_button[1][1]*resize))
        draw_button(explorer_music_button, bred, "Открыть папку с музыкой", font)
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit()
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_ESCAPE):
                    nav_back.play()
                    save_settings()
                    if (music_list[selected_music]!=s_music):
                        settings["music"]=music_list[selected_music]
                        starting=True
                        Thread(target=loading_screen).start()
                        if (in_game_call):
                            music_channel.stop()
                        load_music(settings["music"])
                        if (in_game_call):
                            music_channel.play(music, loops=-1, maxtime=0, fade_ms=0)
                            music_channel.pause()
                        starting=False
                    return
                elif (event.key==pygame.K_LEFT or event.key==pygame.K_a):
                    if (selected_music-1>=0):
                        selected_music-=1
                        if (selected_music-2>=0):
                            music_discs[selected_music-2].ppos=-1
                        if (selected_music-1>=0):
                            music_discs[selected_music-1].ppos=-1
                        if (selected_music+1<len(music_discs)):
                            music_discs[selected_music+1].ppos=-1
                        if (selected_music+3<len(music_discs)):
                            music_discs[selected_music+2].ppos=-1
                        music_discs[selected_music].ppos=-1
                        proc=0
                        stime=time.time()
                elif (event.key==pygame.K_RIGHT or event.key==pygame.K_d):
                    if (selected_music+1<len(music_list)):
                        selected_music+=1
                        if (selected_music+2<len(music_discs)):
                            music_discs[selected_music+2].ppos=+1
                        if (selected_music+1<len(music_discs)):
                            music_discs[selected_music+1].ppos=+1
                        if (selected_music-1>=0):
                            music_discs[selected_music-1].ppos=+1
                        if (selected_music-2>=0):
                            music_discs[selected_music-2].ppos=+1
                        music_discs[selected_music].ppos=+1
                        proc=0
                        stime=time.time()
                    cw=False
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                polzunok_start_pos=pygame.mouse.get_pos()
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (press_check(back_button,mouse_pos)):
                        nav_back.play()
                        if (music_list[selected_music]!=s_music):
                            settings["music"]=music_list[selected_music]
                            starting=True
                            Thread(target=loading_screen).start()
                            if (in_game_call):
                                music_channel.stop()
                            load_music(settings["music"])
                            if (in_game_call):
                                music_channel.play(music, loops=-1, maxtime=0, fade_ms=0)
                                music_channel.pause()
                            starting=False
                        return
                    elif (press_check(disc_left_press_box, mouse_pos)):
                        if (selected_music-1>=0):
                            selected_music-=1
                            if (selected_music-2>=0):
                                music_discs[selected_music-2].ppos=-1
                            if (selected_music-1>=0):
                                music_discs[selected_music-1].ppos=-1
                            if (selected_music+1<len(music_discs)):
                                music_discs[selected_music+1].ppos=-1
                            if (selected_music+3<len(music_discs)):
                                music_discs[selected_music+2].ppos=-1
                            music_discs[selected_music].ppos=-1
                            proc=0
                            stime=time.time()
                    elif (press_check(disc_right_press_box, mouse_pos)):
                        if (selected_music+1<len(music_list)):
                            selected_music+=1
                            if (selected_music+2<len(music_discs)):
                                music_discs[selected_music+2].ppos=+1
                            if (selected_music+1<len(music_discs)):
                                music_discs[selected_music+1].ppos=+1
                            if (selected_music-1>=0):
                                music_discs[selected_music-1].ppos=+1
                            if (selected_music-2>=0):
                                music_discs[selected_music-2].ppos=+1
                            music_discs[selected_music].ppos=+1
                            proc=0
                            stime=time.time()
                    elif (press_check(explorer_music_button, mouse_pos)):
                        nav.play()
                        path=os.path.abspath(os.getcwd())+"\\resources\\Music"
                        try:subprocess.Popen("explorer "+"\""+path+"\"")
                        except:pass
        if (mbd):
            if (press_check(back_button,mouse_pos)):
                screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
            elif (press_check(explorer_music_button, mouse_pos)):
                draw_button(explorer_music_button, bpred, "Открыть папку с музыкой", font)
            polzunok_music_volume[1]=polzunok(polzunok_music_volume, polzunok_start_pos)
            polzunok_sound_volume[1]=polzunok(polzunok_sound_volume, polzunok_start_pos)
            settings["music_volume"]=polzunok_music_volume[1]/100
            settings["effect_volume"]=polzunok_sound_volume[1]/100
            change_volume()
        polzunok_ris(polzunok_music_volume)
        polzunok_ris(polzunok_sound_volume)
        pygame.display.flip()
        fps.tick(60)
            
def menu():
    mouse_button_pressed=(False,False,False)
    global music_channel, running
    change_volume()
    music_channel.play(menu_music, loops=-1, maxtime=0, fade_ms=0)
    #mouse_pos=(0,0)
    menu_type=1
    mbd=False
    while True:
        mouse_pos=pygame.mouse.get_pos()
        menu_ris(menu_type)
        #pygame.draw.rect(screen, bred, (0, 0, 200, 50))
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                exit()
            elif (event.type==pygame.MOUSEBUTTONDOWN):
                mouse_button_pressed=pygame.mouse.get_pressed()
                if (mouse_button_pressed[0]):
                    mbd=True
            elif (event.type==pygame.MOUSEBUTTONUP):
                if (mouse_button_pressed[0]):
                    mbd=False
                    if (menu_type==1):
                        if (press_check(marathon_button, mouse_pos)):
                            nav.play()
                            if (restart()):
                                game()
                                running=False
                                music_channel.stop()
                                music_channel.play(menu_music, loops=-1, maxtime=0, fade_ms=0)
                        elif (press_check(settings_button, mouse_pos)):
                            nav.play()
                            settings_menu()#menu_type=2
                        elif (press_check(scores_button, mouse_pos)):
                            nav.play()
                            menu_type=3
                        #elif (press_check(mat_button, mouse_pos)):
                        #    nav.play()
                        #    mat_menu(False)
                        elif (press_check(info_button, mouse_pos)):
                            nav.play()
                            info()
                        elif (press_check(themes_button, mouse_pos)):
                            nav.play()
                            themes_menu(False)
                        elif (press_check(music_button, mouse_pos)):
                            nav.play()
                            music_menu(False)
                    elif (menu_type==2):
                        if (press_check(back_button, mouse_pos)):
                            menu_type=1
                        elif (press_check(select_mat_button, mouse_pos)):
                            mat_menu(False)
                    elif (menu_type==3):
                        if (press_check(back_button, mouse_pos)):
                            nav_back.play()
                            menu_type=1
                    elif (menu_type==4):
                        if (press_check(back_button, mouse_pos)):
                            menu_type=2
            elif (event.type==pygame.KEYDOWN):
                if (event.key==pygame.K_SPACE):
                    #info_screen("Внимание", "Тема будет обновлена после перезапуска", bgreen, bpgreen, "Ок")
                    #themes_menu(True)
                    #pass
                    #try:
                    themes_catalog()
                    #except Exception as error:
                    #    print(error)
                    #if (event.key==pygame.K_SPACE):
                    #    if (tf_dialog("Ты лix?", "кто прочитал тот здохнет", bgreen, bpgreen, "Да.", bred, bpred, "Нет!")):
                    #        print("реал лох")
                #elif (event.key==pygame.K_v):
                #    themes_menu(False)
                #elif (event.key==pygame.K_b):
                #    music_menu(False)
        if (mbd):
            if (menu_type==1):
                if (press_check(marathon_button, mouse_pos)):
                    screen.blit(marathon_button11im, (marathon_button[1][0]*resize,marathon_button[1][1]*resize))
                elif (press_check(settings_button, mouse_pos)):
                    screen.blit(settings_button11im, (settings_button[1][0]*resize,settings_button[1][1]*resize))
                elif (press_check(scores_button, mouse_pos)):
                    screen.blit(scores_button11im, (scores_button[1][0]*resize,scores_button[1][1]*resize))
                #elif (press_check(mat_button, mouse_pos)):
                #    screen.blit(mat_button11im, (mat_button[1][0]*resize,mat_button[1][1]*resize))
                elif (press_check(info_button, mouse_pos)):
                    screen.blit(info_button11im, (info_button[1][0]*resize,info_button[1][1]*resize))
                elif (press_check(themes_button, mouse_pos)):
                    screen.blit(themes_button11im, (themes_button[1][0]*resize,themes_button[1][1]*resize))
                elif (press_check(music_button, mouse_pos)):
                    screen.blit(music_button11im, (music_button[1][0]*resize,music_button[1][1]*resize))
            elif (menu_type==2):
                if (press_check(back_button, mouse_pos)):
                    screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
                elif (press_check(select_mat_button, mouse_pos)):
                    draw_button(select_mat_button, bpgreen, "Выбор темы")
            elif (menu_type==3):
                if (press_check(back_button, mouse_pos)):
                    screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))
            elif (menu_type==4):
                if (press_check(back_button, mouse_pos)):
                    screen.blit(back_button11im, (back_button[1][0]*resize,back_button[1][1]*resize))

        #Button.press_check((100,100), (0,0), bred, bpred)
        pygame.display.flip()
        fps.tick(60)
def stat_tablo():
    global stat_tablo_mass, stat_tablo_to_show
    while (running):
        #print("RUNNING", round(time.time(),5))
        if (len(stat_tablo_mass)!=0):
            stat_tablo_to_show=stat_tablo_mass[0]
            #print(stat_tablo_mass[0])
            stat_tablo_mass.pop(0)
            time.sleep(1)
        else:
            stat_tablo_to_show=""
        fps.tick(60)
starting=False
menu()
