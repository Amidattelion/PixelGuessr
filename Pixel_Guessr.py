"""
https://github.com/Amidattelion

Copyright (C)  2013-2014 np1

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import scipy
from PIL import Image
import requests
from io import BytesIO
import base64
import time


pic_list = os.listdir('./images')

def img_from_url(url):
    '''
    Renvoit un objet Image de PIL à partir de l'url de l'image, directement lisible par plt.imshow()
    '''
    # Si l'url renvoit vers une image en base64 (début sous forme 'data:image/jpeg;base64,base64_code') : la conversion est différente
    if('data:image/jpeg;base64,' in url):
        url = url.replace('data:image/jpeg;base64,','')
        img = Image.open(BytesIO(base64.b64decode(url)))

    # Pour un url classique vers l'image:
    else:
        r = requests.get(url)
        img = Image.open(BytesIO(r.content))

    return(np.array(img))

def show_pic(path_to_pic,category='No category',name='Untitled'):
    '''
    Joue l'animation de pixel guess pour l'image dont le chemin d'accès est donné en argument
    '''
    try:
        pic = img_from_url(path_to_pic)
    except Exception as e:
        print(e)
        try:
            pic = plt.imread(path_to_pic)
        except:
            print('pic must be an image in ndarray format or a path to an image')
            return()

    fig = plt.figure('fig')
    plt.clf()
    ax = plt.gca()

    titre = ax.text(0.5,1.05,f'Categorie : {category}',bbox={'facecolor':'w', 'alpha':0.5, 'pad':5},
                transform=ax.transAxes, ha="center",fontsize=50)

    n,m,l = pic.shape
    nb_frame = max(n,m)
    # tps entre chaque frame en milisec
    interval = 50

    image = ax.imshow(np.zeros((n,m,l)),interpolation='None')

    def init():
        image.set_data(np.ones((n,m,l)))
        return image,

    def animate(i,nb_frame):
        # i est le n° de la frame en cours de lecture
        # a et b sont deux coeffs indiquant le nb de pixels utilisés pour la résolution de la frame n°i
        # print(i)

        # on utilise une loi exponentielle pour l'échantillonnage : donne un aspect visuellement plus équilibré à l'évolution de la résolution
        a = int(np.exp(np.linspace(0,np.log(n),nb_frame))[i])
        b = int(np.exp(np.linspace(0,np.log(m),nb_frame))[i])

        f = n//a
        h = m//b

        pic_pix = pic[::f,::h,:]
        image.set_data(pic_pix)
        return image,

    nb_frame = 200
    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=nb_frame, interval=interval, fargs = [nb_frame], blit=True, repeat=False)

    figManager = plt.get_current_fig_manager()
    figManager.window.state('zoomed')
    plt.axis('off')

    plt.show(block=False)

    # attendre la fin de l'animation : sort de la boucle quand l'image pixellisée est égale à l'image d'origine
    while True:
        try:
            if( (pic == image.get_array()).all() ) :
                plt.pause(0.1)
                break
            else:
                plt.pause(0.5)
        except:
            plt.pause(1)

    titre.set_text(f"Il s'agissait de : {name}")
    fig.canvas.draw()
    time.sleep(2)
    image.set_data(np.zeros((n,m,l)))
    time.sleep(0.5)
    fig.canvas.draw_idle()
    fig.canvas.flush_events()

def launch_game(file,history_file=None):
    '''
    lance le jeu avec les liens du fichier indiqué
    '''
    with open(file,'r',encoding='utf-8') as f:
        pic_list = f.readlines()

    use_hist = False
    if type(history_file) is str:
        use_hist = True
        with open(history_file,'r',encoding='utf-8') as hist:
            for deja_vu in hist.readlines():
                if deja_vu in pic_list: pic_list.remove(deja_vu)

    index = np.arange(len(pic_list))
    np.random.shuffle(index)

    pic_dico = {}

    for k in index:
        unpack = pic_list[k].split(' : ')
        category = unpack[0]
        name = ' '.join(unpack[1:-1])
        pic_url = unpack[-1]

        if not category in pic_dico.keys():
            pic_dico[category] = []

        if(pic_url[:-2:-1]=='\n'):pic_url = pic_url[:-1]

        pic_dico[category].append( [name,pic_url] )

    category_list = list(pic_dico.keys())
    to_be_removed = None
    # on arrête la boucle quand il n'y a plus de catégories à explorer (ie toute les images ont été vues)

    while (len(category_list)>0):
        # remove une category si l'iteration précédente en a trouvée une vide:
        if type(to_be_removed) is str:
            category_list.remove(to_be_removed)
            to_be_removed = None

        # ranger les categories au hasard:
        category_random_index = np.arange(len(category_list))
        np.random.shuffle(category_random_index)

        # parcourir cette liste triée au hasard de catégorie et prendre une image dans chaque pour jouer:
        for k in category_random_index:
            try:
                category = category_list[k]
                # si il n'y a plus d'image dans la catégorie indiqué : on enlève la catégorie de la liste et on passe à la suivante
                if len(pic_dico[category]) == 0:
                    # on stock la category à éliminer pour la remove après le tour de boucle, car si on la remove maintenant on change les index des autres category de la liste en train d'etre exploree
                    to_be_removed = category
                    continue

                # .pop() permet de récupérer le couple [name,pic_url] tout en l'enlevant du dico
                name, pic_url = pic_dico[category].pop()

                # sinon le jeu continue avec l'image ainsi sélectionnée
                print(pic_url)
                # print(category,name)
                show_pic(pic_url,category,name)

                if use_hist:
                    with open(history_file,'a',encoding='utf-8') as hist:
                        if (pic_url[k][:-2:-1]=='\n') : hist.write(pic_url[k][:-1])
                        else: hist.write(pic_list[k])

            except Exception as e:
                print(e)

    print('Terminé !')
    plt.close('all')
