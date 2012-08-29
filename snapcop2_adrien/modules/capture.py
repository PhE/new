#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import piggyphoto
import pyexiv2
import pygame
import pygame.locals
import redis
import shutil
import sys
import time


pygame.joystick.init()
pygame.display.init()
window = pygame.display.set_mode((1056, 704)) 
pygame.display.set_caption('Display Preview')
screen = pygame.display.get_surface()

try:
    stick = pygame.joystick.Joystick(0)
    stick.init()
    print 'joystick trouvé !'
except:
    print 'pas de joystick !!'
    sys.exit()

def main():
    capt = 'no'
    frames_raz = 'yes'
    camera = piggyphoto.camera()
    camera.leave_locked()
    cx = redis.Redis()
    frames = 0
    cx.set('frames', 0)    
    stop = False
    while not stop:    
        print time.time(), 'capture preview ...'
        camera.capture_preview('data/preview.jpg')      
        preview = pygame.image.load('data/preview.jpg')
        screen.blit(preview, (0, 0))
        pygame.display.update()
        
        #cx.publish('preview', '')
        
        evts = pygame.event.get()
        for evt in evts:
            if evt.type == pygame.locals.KEYDOWN:
                if evt.key == 27:
                    print "Fin du programme"
                    cx.publish('exit','sys.exit()')
                    stop = True
                elif evt.key == 112: # P
                    pass
                

                elif evt.key == 115: # S
                    print 'demande de stacking rapide ...'
                    cx.publish('stack_rapide', '')

                
                    
                else:
                    print 'touche inconnue ', evt.key
                
            elif evt.type == pygame.locals.JOYBUTTONDOWN:
                i = evt.button
                nb_photo = ((i-3)*5)
                      
                if nb_photo == -15:
                    nb_photo = 1
                    cx.set('nb_photo', nb_photo)
                    frames_raz = 'no'
                    capt = 'yes'        
                if nb_photo >=5 and nb_photo <=30:
                    cx.set('nb_photo', nb_photo)
                    frames_raz = 'yes'
                    capt = 'yes'
                if evt.button == 11:
                    cx.publish('exit','sys.exit()')
                    sys.exit()
                if evt.button == 1: # Boutton 2
                    print 'demande de stacking lent ...'
                    frames = 0
                    cx.publish('stack_lent', '')
                if evt.button == 3: # Boutton 4
                    frames = 0
                else:
                    pass
                
            else:
                pass
        while capt == "yes":
            for i in range(0, nb_photo):
                    
                print 'capture image ...'
                source_capture = 'data/capture.jpg'
                camera.capture_image(source_capture)
                frames += 1          
                cx.set('frames', frames)
                
                # Déplacer la photo 
                time_stamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
                dest_capture = os.path.join('data/images', 'capt%s.jpg' % time_stamp)
                shutil.move(source_capture, dest_capture)
                
                # obtenir les infos saisis
                souche = cx.get('souche')
                substrat = cx.get('substrat')
                fermentation = cx.get('fermentation')
                
                # Modification des données "EXIF"
                metadata = pyexiv2.ImageMetadata(dest_capture)
                metadata.read()
                try:
                    pyexiv2.xmp.register_namespace('Souche/', 'Souche')
                except:
                    pass
                try: 
                    pyexiv2.xmp.register_namespace('Substrat/', 'Substrat')
                except:
                    pass
                try:
                    pyexiv2.xmp.register_namespace('Fermentation/', 'Fermentation')
                except:
                    pass
                metadata['Xmp.Souche.Souche'] = souche
                metadata['Xmp.Substrat.Substrat'] = substrat
                metadata['Xmp.Fermentation.Fermentation'] = fermentation
                tag = metadata['Xmp.Souche.Souche']
                tag2 = metadata['Xmp.Substrat.Substrat']
                tag3 = metadata['Xmp.Fermentation.Fermentation']
                print 'Souche : ', tag.value
                print 'Substrat : ', tag2.value
                print 'Fermentation : ', tag3.value
                
                
                # On ajoute à la liste des photos prises
                cx.rpush('captures', dest_capture)
                # trim de la liste ???
                
                # on informe qu'une capture vient d'être faite
                cx.publish('capture', dest_capture)
                time.sleep(2)
            if frames_raz == 'yes':
                frames = 0
            capt = "no"                
