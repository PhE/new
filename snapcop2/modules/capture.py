#!/usr/bin/env python
#-*- coding:utf-8 -*-

import piggyphoto
import pygame
import pygame.locals
import redis
import time


#pygame.font.init()
pygame.joystick.init()
pygame.display.init()
window = pygame.display.set_mode((800, 800)) 
#pygame.display.set_caption('Visu photo stacker %s' % day)

def main():
    print 'capture ...'

    camera = piggyphoto.camera()
    camera.leave_locked()

    cx = redis.Redis()
    
    stop = False
    while not stop:    
        time.sleep(0.3)
        print time.time(), 'capture preview ...'
        camera.capture_preview('data/preview.jpeg')
        cx.publish('preview', '')
        
        evts = pygame.event.get()
        for evt in evts:
            if evt.type == pygame.locals.KEYDOWN:
                if evt.key == 27:
                    print "Fin du programme"
                    stop = True
                elif evt.key == 112: # P
                    pass
                elif evt.key == 99: # C
                    print 'capture image ...'
                    camera.capture_image('data/capture.jpeg')
                    
                    # obtenir les infos saisis
                    auteur = cx.get('auteur')
                    souche = cx.get('souche')
                    desc = cx.get('desc')
                    
                    # Modifier les données "EXIF"
                    print "info:", auteur, desc
                    
                    # Déplacer la photo 

                elif evt.key == 115: # S
                    print 'demande de stacking rapide ...'
                    cx.publish('stack_rapide', '')

                elif evt.key == 116: # T
                    print 'demande de stacking lent ...'
                    cx.publish('stack_lent', '')
                    
                else:
                    print 'touche inconnue ', evt.key

