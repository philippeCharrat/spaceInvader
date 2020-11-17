import os,sys
import numpy as np
from Tkinter import *

def grille(): #fonction dessinant le tableau
    lignes_verticales()
    lignes_horizontales()

def lignes_verticales():
    x = 0
    while x != width:
        canevas.create_line(x,0,x,height,width=1,fill='black')
        x += taille

def lignes_horizontales():
    y = 0
    while y != height:
        canevas.create_line(0,y,width,y,width=1,fill='black')
        y += taille

def clic_gauche(event): #fonction rendant vivante la cellule cliquée en attribuant la valeur
    x = event.x -(event.x%taille) #1 pour une cellule vivante
    y = event.y -(event.y%taille)
    canevas.create_rectangle(x, y, x+taille, y+taille, fill='black')
    plateau[x,y]=1

def clic_droit(event): #fonction tuant la cellule cliquée en attribuant la valeur 0 pour une
    x = event.x -(event.x%taille) #cellule morte
    y = event.y -(event.y%taille)
    canevas.create_rectangle(x, y, x+taille, y+taille, fill='white')
    plateau[x,y]=0


def debut(): #démarrage du jeu
    global autorisation
    if autorisation == 0:
        autorisation = 1
        jeu()

def stop(): #fin du jeu
    global autorisation
    autorisation = 0

def jeu():
    for i in range(0,cote_du_plateau):
        for j in range(0,cote_du_plateau):
            compte = 0

            dfr,dfw = os.pipe() #creation du pipe et des 5 processus
            pid1 = os.fork()
            if pid1 > 0:
                pid2 = os.fork()
            if pid1 > 0 and pid2 > 0:
                pid3 = os.fork()
            if pid1 > 0 and pid2 > 0 and pid3 > 0:
                pid4 = os.fork()
            print('ooo')
            if pid1 > 0 and pid2 == 0:  #2eme processus qui teste les cases gauche et droite
                if plateau[i,j-1] == 1:
                    compte += 1
                if plateau[i,j+1] == 1:
                    compte += 1

            if pid1 > 0 and pid2 > 0 and pid3 == 0: #3eme processus qui teste les
                if plateau[i-1,j] == 1:             #cases en haut et en bas
                    compte += 1
                if plateau[i+1,j] == 1:
                    compte += 1

            if pid1 > 0 and pid2 > 0 and pid3 >0 and pid4 == 0: #4eme processus qui teste les
                if plateau[i-1,j-1] == 1:             #cases en diagonale haut+gauche et
                    compte += 1                     #bas+gauche
                if plateau[i+1,j-1] == 1:
                    compte += 1

            if pid1 > 0 and pid2 > 0 and pid3 >0 and pid4 > 0: #5eme processus qui teste les
                if plateau[i-1,+1] == 1:             #cases en diagonale haut+droite et
                    compte += 1                      #bas+droite
                if plateau[i+1,j+1] == 1:
                    compte += 1
            print('iii')
            n = os.write(dfw,str(compte).encode())








#les différentes variables:

# taille de la grille
height = 400
width = 400

#taille des cellules
cote_du_plateau = 5
taille = height/cote_du_plateau

#Réactivité de la partie
laps = 1

#Contrôleur de la boucle
autorisation = 0


fenetre = Tk()
fenetre.title('Game of Life')
plateau = np.zeros((cote_du_plateau,cote_du_plateau))
canevas = Canvas(fenetre, width =width, height =height, bg ='white')
canevas.bind("<1>", clic_gauche)
canevas.bind("<3>", clic_droit)
canevas.pack(side =TOP, padx =5, pady =5)
debut()
grille()



fenetre.mainloop()



