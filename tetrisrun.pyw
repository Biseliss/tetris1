import subprocess
import sys
try:
    import requests
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
import shutil
import zipfile
import io
from urllib.request import urlopen
from threading import Thread
try:
    import pygame
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame
import json
import os
pygame.init()
pygame.font.init()

def exit():
    pygame.quit()

site="vmartin.codead.dev"
connection=True
try:
    requests.get("http://"+site,timeout=100)
except:
    connection=False

try:
    with open('settings.tse2', encoding="utf-8") as settings:
        settings=json.load(settings)
except:
    file=open("settings.tse2", "w")
    file.write("{\"resize\": 1,\"version\": 0}")
    file.close()
    with open('settings.tse2', encoding="utf-8") as settings:
        settings=json.load(settings)

resize=settings["resize"]
screen_size=440*resize
fps=pygame.time.Clock()
if (connection):
    font12=pygame.font.Font(io.BytesIO(urlopen("http://"+site+"/TETRIS/font.ttf").read()), 12*resize)

loading_screen_to_show=""

def s_text(text, ttx, place, color, mode, font):
    #1 - нормальный режим; 2 - режим с отстопом от правого края; 3 - режим с отступом от левого края; 4 - по центру (y); 5 - по центру (х, у)
    if (mode==1):
        screen.blit(font.render(text, ttx, color),(place[0]*resize,place[1]*resize))
    elif (mode==2):
        texti=font.render(text, ttx, color)
        screen.blit(texti,(screen_size-texti.get_rect()[2]-otstup_ot_kraja,place[1]*resize))
    elif (mode==3):
        texti=font.render(text, ttx, color)
        screen.blit(texti,(0+otstup_ot_kraja,place[1]*resize))
    elif (mode==4):
        texti=font.render(text, ttx, color)
        screen.blit(texti,((screen_size-texti.get_rect()[2])//2+place[0]*resize,place[1]*resize))
    elif (mode==5):
        texti=font.render(text, ttx, color)
        screen.blit(texti, ((place[0]*resize)-(texti.get_rect()[2]//2), (place[1]*resize)-(texti.get_rect()[3]//2)))
        #screen.blit(texti,((screen_size-texti.get_rect()[2])//2+place[0]*resize,(screen_size-texti.get_rect()[3])//2+place[1]*resize))
    
starting=True

def loading_screen():
    global display
    logo=pygame.image.load(io.BytesIO(urlopen("http://"+site+"/TETRIS/logo.png").read())).convert_alpha()
    logo=pygame.transform.scale(logo, (logo.get_rect()[2]*resize,logo.get_rect()[3]*resize))
    loading_circle=pygame.image.load(io.BytesIO(urlopen("http://"+site+"/TETRIS/loading_circle.png").read())).convert_alpha()
    loading_circle=pygame.transform.scale(loading_circle,(50*resize,50*resize))
    ugol=0
    while (starting):
        screen.fill((0,0,0))
        screen.blit(logo, (40*resize, 0*resize))
        #for event in pygame.event.get():
        #    if (event.type==pygame.QUIT):
        #        exit()
        ugol+=3
        if (ugol==360):
            ugol=0
        rotated=pygame.transform.rotozoom(loading_circle,-ugol,1)
        screen.blit(rotated,rotated.get_rect(center=(220*resize,380*resize)))
        s_text(loading_screen_to_show, True, (0,420), (255,255,255), 4, font12)
        pygame.display.flip()
        fps.tick(60)
if (connection):
    if (not "version" in settings.keys()):
        settings["version"]=0
    update=False
    try:
        if (settings["version"]<int(requests.get("http://"+site+"/TETRIS/tve.txt").content)):
            update=True
            settings["version"]=int(requests.get("http://"+site+"/TETRIS/tve.txt").content)
            with open("settings.tse2", "w", encoding="utf-8") as write_file:
                json.dump(settings, write_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(e)
        update=True
    if (update):
        screen=pygame.display.set_mode((screen_size, screen_size))
        Thread(target=loading_screen).start()
        pygame.display.set_icon(pygame.image.load(io.BytesIO(urlopen("http://"+site+"/TETRIS/logo.png").read())))
        pygame.display.set_caption('Tetris')
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                pass
        try:shutil.rmtree("tmp")
        except:pass
        loading_screen_to_show="Скачка TETRISUPDATE.zip"
        data=requests.get("http://"+site+"/TETRIS/tetrisupdate.zip",allow_redirects=True)
        try:os.mkdir("tmp")
        except:pass
        open("tmp/tetrisupdate.zip","wb").write(data.content)
        loading_screen_to_show="Распаковка TETRISUPDATE.zip"
        with zipfile.ZipFile("tmp/tetrisupdate.zip", 'r') as zip_ref:
            zip_ref.extractall("tmp/tetrisupdate")
        loading_screen_to_show="Установка TETRISUPDATE.zip"
        try:os.remove("tetris.pyw")
        except:pass
        try:shutil.rmtree("resources/Themes/Default")
        except:pass
        shutil.move("tmp/tetrisupdate/tetris.pyw","tetris.pyw")
        shutil.move("tmp/tetrisupdate/Default","resources/Themes/Default")
        shutil.rmtree("tmp")
        if (not os.path.exists("resources/Music/Default.ogg")):
            if (not os.path.exists("resources/Music")):
                os.mkdir("resources/Music")
            data=requests.get("http://"+site+"/TETRIS/Default.ogg",allow_redirects=True)
            open("resources/Music/Default.ogg","wb").write(data.content)
        starting = False
        exit()
sys.path.append(".")
import tetris
