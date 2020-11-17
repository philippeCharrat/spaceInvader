"""
    Nom du projet : Space Invader

    auteurs  :  - Philippe Charrat
                - Lucie Dole

    contenue du fichier : les fonctions et le programme principale

    dernière modification : 19/01/2018
    modification :  - ajout du market
                    - "base de données" joueurs améliorés

    Note des auteurs : Nous avons laissez de nombreuse références et un Easter
    Eggs donc si vous souhaiter une expérience de jeu optimal, il est conseillé
    de jouer avant de lire le code. Bon jeu !

    ToDo :  - Ajouter des try/exceptions sur fichiers et bibliothèque pour éviter les erreurs
            - menu graphique pour le market


"""

#-- Imports des Bibliothèques
from Tkinter import *
import random
from tkMessageBox import *
#--

#-- Fonctions Principales du code
def Clavier(event) :
    """ fonction qui permet de déplacer le pion, de créer et de lancer un missile à partir des touches du clavier
        input : event : les touches du clavier
        output : none
    """
    global PosX, PosY, fenetre, Pion, PosXTir, PosYTir, PionTir, PionTirAlienBonus,PionAlienBonus,liste,listeAlien,txt,dicoAlien,img,imageVaisseau,vie,strrVar,Canevas

    touche = event.keysym
    if etatPartie == "easteregg" : coupEasterEgg(touche)
    else :
        if (touche == "q" or touche =="Left") and PosX >= 30 :
            PosX -= 20
        if (touche == "d" or touche =="Right") and PosX <= 470 :
            PosX += 20
        if touche == "z" and PionTir == "" and Pion != "" :
            PosXTir = PosX
            PosYTir = PosY
            PionTir = Canevas.create_rectangle(PosXTir, PosYTir-10,PosXTir+5,PosYTir+10,width=2,outline='white')
        if touche == 'Escape' :
            fenetre.destroy()
        if touche == "m" : shop()
        if touche == "w" and PosX <= 30 : murDeGauche(Canevas)
        if touche == "n" and PosX >= 470 and cle==True : murDeDroite(Canevas)
        if touche == 's' and ("flam" in imageVaisseau or "cowboy" in imageVaisseau):
            liste = dicoAlien.keys()
            for i in range (len(dicoAlien)) :
                if dicoAlien[liste[i]][1]-25 < PosX < dicoAlien[liste[i]][1]+25 :
                    Canevas.delete(dicoAlien[liste[i]][0])
                    del dicoAlien[liste[i]]

        if touche == 's' and ("who" in imageVaisseau or "star" in imageVaisseau or "albator" in imageVaisseau):
            vie = 9
            chnn = "Nombre Vie : "+ str(vie)
            strVar.set(chnn)
        if touche == 'h' :
            showinfo('Aide','Ground Controle To Major Tom \n ton but est de protéger de la terre contre cette invasion ! \n Touches : \n - Flèches directionnels : mouvement du vaisseau \n - z : tir \n - s : qui sais peut être une fonction caché \n - m : le marché ou tu peux venir y dépenser ton argent durement acquis \n N\'hésiter pas à remplir le champs de votre pseudo pour conserver tes pièces(ou peut être une référence qui sais)\n Bien observer les menus déroulants y a plein de truc cool\n Enfin fait attention au coté gauche, il me semble ... étrange une simple commande et tous pourrais changer ... \n  Check ignition and may God\'s love be with you ')
        Canevas.coords(Pion,PosX, PosY)

def maj() :
    """
        fonction qui permet de jouer au jeu en ré-actualisant la fonction
        input : none
        output : none

    """
    global PosYAlien, PosXAlien, signe, signeA
    global PionTir, PosXTir, PosYTir, etatPartie
    global PionTirAlien, PosXTirAlien, PosYTirAlien, PionAlienBonus, PionTirAlienBonus
    global dicoAlien, vitesse
    if len(dicoAlien) == 0 and PionAlienBonus =="": etatPartie = False
    if etatPartie == True :

        if len(dicoAlien) != 0 :

            dicoAlien = deplacementAlien(dicoAlien)
            if PosYTir > 0 :
                PosYTir -= 20
            else :
                Canevas.delete(PionTir)
                PionTir = ""
                PosXTir = 0
                PosYTir = 0

            vitesseAlien()
            touche()
            toucheAlien(dicoAlien)
            Canevas.coords(PionTirAlien,PosXTirAlien, PosYTirAlien-10,PosXTirAlien+5,PosYTirAlien+10)
            Canevas.coords(PionTir,PosXTir, PosYTir-10,PosXTir+5,PosYTir+10)

        else :

            Canevas.delete(PionTirAlien)
            deplacementAlien(dicoAlien)
            touche()
            toucheAlien(dicoAlien)
            Canevas.coords(PionTir,PosXTir, PosYTir-10,PosXTir+5,PosYTir+10)
            Canevas.coords(PionAlienBonus,PosXAlien,PosYAlien)
            Canevas.coords(PionTirAlienBonus,PosXTirAlien, PosYTirAlien-10,PosXTirAlien+5,PosYTirAlien+10)

        fenetre.after(vitesse,maj)
    else :
        if etatPartie == "easteregg" :
            Canevas.coords(Pion,PosX, PosY)
            fenetre.after(vitesse,maj)
        else :
            if len(dicoAlien) == 0 and PionAlienBonus == "" :
                meilleurScore()
                showinfo("Bravo"," Bravo, tu as gagné la partie !!Ton score est de : "+str(score))
            elif etatPartie == 0 : etatPartie = False
            else : showinfo("Perdu"," Perdu, tu n'as pas réussi \n et ton score est de : "+str(score))
            recommencer()

def touche():
    """
        fonction qui permet de gérer la collision entre un tir d'alien et le joueur ou avec un mur. La fonction enlève une vie au joueur
        à chaque collision.
        input : none
        return : none
    """
    global PionTirAlien,etatPartie,Pion,vie,starVar,dicoMur,PionTirAlienBonus, dicoAlien
    coordTir = []
    if PionTirAlien != "" :
        coordTir = Canevas.coords(PionTirAlien)

    if PionTirAlienBonus != "" :
        coordTir = Canevas.coords(PionTirAlienBonus)


    if (len(coordTir) > 0) :
        liste =  Canevas.find_overlapping(coordTir[0],coordTir[1],coordTir[2],coordTir[3])

        if Pion in liste :
            vie -= 1
            chnn = "Nombre Vie : "+ str(vie)
            strVar.set(chnn)
            Canevas.delete(PionTirAlien)

            if PionTirAlienBonus != "":
                vie == 0
                chnn = "Nombre Vie : "+ str(vie)
                strVar.set(chnn)
                Canevas.delete(PionTirAlienBonus)

            if vie == 0 :
                Canevas.delete(Pion)
                Pion = ""
                etatPartie = 0
                showinfo("Perdu"," Perdu, tu n'as pas r?ussi \n et ton score est de : "+str(score))
                Canevas.delete(PionTirAlien)
        else :

            listeMur = dicoMur.values()
            for i in listeMur :
                if i in liste :
                    Canevas.delete(PionTirAlien)
                    Canevas.delete(i)


def toucheAlien(dicoAlien):
    """
        fonction qui gère les collisions entre les tirs du joueur avec les aliens, l'alien bonus et les murs.
        input : dicoAlien : dictionnaire crée par la fonction creationAlien
        output : none
    """
    global PionTir, Canevas, score, PionAlienBonus, vieAlienBonus, strVarBonus,dicoMur,Coin

    coordTir = Canevas.coords(PionTir)
    if (len(coordTir) >= 4) :
        liste =  Canevas.find_overlapping(coordTir[0],coordTir[1],coordTir[2],coordTir[3])
        listeAlien = dicoAlien.keys()
        listeMur   = dicoMur.keys()

        for i in range (len(listeAlien)) :
            pionAlien = dicoAlien[listeAlien[i]][0]
            if pionAlien in liste :
                score += 50
                Coin += 1
                chaineCoin = "Coins :"+str(Coin)
                strVarCoin.set(chaineCoin)
                chnn = "Score : "+ str(score)
                strrVar.set(chnn)
                Canevas.delete(pionAlien)
                Canevas.delete(PionTir)
                del dicoAlien[listeAlien[i]]

        for i in range (len(listeMur)) :
            pionMur = dicoMur[listeMur[i]]
            if pionMur in liste :
                score -= 10
                Coin-=1
                if Coin <0 :
                    Coin = 0
                chaineCoin = "Coins :"+str(Coin)
                strVarCoin.set(chaineCoin)
                chnn = "Score : "+ str(score)
                strrVar.set(chnn)
                Canevas.delete(pionMur)
                Canevas.delete(PionTir)
                del dicoMur[listeMur[i]]

        if PionAlienBonus in liste and len(listeAlien) == 0 :
            vieAlienBonus -=1
            strVarBonus.set("Vies de l'alien bonus :" + str(vieAlienBonus))
            Canevas.delete(PionTir)
            if vieAlienBonus == 0 :
                score += 100
                Coin += 5
                chaineCoin = "Coins :"+str(Coin)
                strVarCoin.set(chaineCoin)
                strrVar.set("Score : "+ str(score))
                Canevas.delete(PionAlienBonus)
                Canevas.delete(PionTir)
                PionAlienBonus = ""




def tirAlien(posXAlien,posYAlien,dicoAlien) :
    """
        fonction qui crée les tirs des aliens
        input : posXAlien : position X de l'Alien
                posYAlien : position Y de l'Alien
                dicoAlien : dictionnaire contenant les Aliens
        output : none
    """
    global PionTirAlien, PosXTirAlien, PosYTirAlien, PionTirAlienBonus
    PosXTirAlien = posXAlien
    PosYTirAlien = posYAlien
    PionTirAlien = Canevas.create_rectangle(PosXTirAlien, PosYTirAlien-10,PosXTirAlien+5,PosYTirAlien+10,width=2,outline='white')
    if len(dicoAlien) == 0 :
        PionTirAlienBonus = Canevas.create_rectangle(PosXTirAlien, PosYTirAlien-10,PosXTirAlien+5,PosYTirAlien+10,width=2,outline='white')

def afficherObjet(PosX,PosY,couleur) :
    """
        fonction qui permet d'afficher les murs
        input : posX : position X de l'objet
                posY : position Y de l'objet
                couleur : couleur pour afficher l'objet
        output : none
    """
    global Canevas
    return Canevas.create_rectangle(PosX-10, PosY-10,PosX+10,PosY+10,width=2,outline=couleur)

def afficherAlien(PosXAlien,PosYAlien,nombre) :
    """
        fonction qui permet d'afficher les aliens
        input : posX : position X de l'objet
                posY : position Y de l'objet
                nombre : numéro de la ligne d'Aliens
        output : l'image de l'alien
    """
    global Canevas,img1,img2,img3
    if nombre == 1 :
        return Canevas.create_image(PosXAlien, PosYAlien,image=img1)
    elif nombre == 2 :
        return Canevas.create_image(PosXAlien, PosYAlien,image=img2)
    else :
        return Canevas.create_image(PosXAlien, PosYAlien,image=img3)

def creationAlien() :
    """
        fonction qui permet de créer des Aliens
        input : none
        output : dicoAlien : dictionnaire comprenant les Aliens
    """
    global PosXAlien,PosYAlien,nombreAlien
    listeAlien = []
    dicoAlien  = {}
    for i in range (nombreAlien) :
        listeAlien.append('Pion'+str(i))

    for j in range (len(listeAlien)) :

        i = j
        if i < 9 :
            alien = afficherAlien(PosXAlien+j*100,PosYAlien,1)
            dicoAlien[listeAlien[j]] = [alien,PosXAlien+j*50,PosYAlien,"+",1]
        elif 9 <= i < 18 :
            i = i -9
            alien = afficherAlien(PosXAlien+j*100,PosYAlien,2)
            dicoAlien[listeAlien[j]] = [alien,PosXAlien+i*50,PosYAlien+50,"+",2]
        elif 18  <= i < 27 :
            i = i -18
            alien = afficherAlien(PosXAlien+j*100,PosYAlien,3)
            dicoAlien[listeAlien[j]] = [alien,PosXAlien+i*50,PosYAlien+100,"+",3]
    return dicoAlien


def deplacementAlien(dicoAlien) :
    """
        fonction qui gère le déplacement des Aliens et de l'Alien Bonus. Si un Alien touche un mur, la partie est perdue.
        input : dicoAlien : dictionnaire comprenant les Aliens
        output : dicoAlien
    """
    global PosXTirAlien, PosYTirAlien, PionTirAlien, Pion, etatPartie, dicoMur, frequencetirAlien, vitesseTir
    global PosYAlien, PosXAlien, signeA
    global PionTir, PosXTir, PosYTir, etatPartie
    global PionTirAlien, PosXTirAlien, PosYTirAlien, PionAlienBonus, PionTirAlienBonus

    listeAlien = dicoAlien.keys()

    if len(dicoAlien) == 0 :
        test = random.randint(1,2)

        if test < 2 and PionTirAlienBonus == "":
            tirAlien(PosXAlien,PosYAlien,dicoAlien)

        if PosYTirAlien < 500 and PionTirAlienBonus != "" :
            PosYTirAlien += 25


        else :
            Canevas.delete(PionTirAlienBonus)
            PionTirAlienBonus = ""
            PosXTirAlien = 0
            PosYTirAlien = 0

        if signeA == "+" and PosXAlien <= 470 :
            PosXAlien += 5
        elif signeA == "-" and PosXAlien >= 30 :
            PosXAlien -= 5

        if PosXAlien >= 470 :
            signeA = "-"
            PosYAlien += 30

        if PosXAlien <= 30 :
            signeA = "+"
            PosYAlien += 30

        if PosYTir > 0 :
                PosYTir -= 20

        else :
            Canevas.delete(PionTir)
            PionTir = ""
            PosXTir = 0
            PosYTir = 0

    else:

        for i in range(len(listeAlien)) :
            caracteristique = dicoAlien.get(listeAlien[i])
            pionAlien = caracteristique[0]
            posXAlien = caracteristique[1]
            posYAlien = caracteristique[2]
            signeA    = caracteristique[3]

            if signeA == "+" and posXAlien <= 470 :
                posXAlien += 5
            elif signeA == "-" and posXAlien >= 30 :
                posXAlien -= 5
            if posXAlien >= 470 :
                signeA = "-"
                posYAlien += 30
            if posXAlien <= 30 :
                signeA = "+"
                posYAlien += 30

            listeMur = dicoMur.keys()
            coordAlien = Canevas.coords(pionAlien)
            liste =  Canevas.find_overlapping(coordAlien[0]-10,coordAlien[1]-10,coordAlien[0]+10,coordAlien[1]+10)
            for j in range (len(listeMur)) :
                if dicoMur[listeMur[j]] in liste :
                    Canevas.delete(pionAlien)
                    Canevas.delete(dicoMur[listeMur[j]])
                    showinfo("état partie","tu as perdu !")
                    etatPartie = False
                    break


            Canevas.coords(pionAlien,posXAlien, posYAlien)
            dicoAlien[listeAlien[i]] = [pionAlien,posXAlien,posYAlien,signeA]

        if PosYTirAlien < 500 :
            PosYTirAlien += 20
        else :
            Canevas.delete(PionTirAlien)
            PionTirAlien = ""
            PosXTirAlien = 0
            PosYTirAlien = 0

        test = random.randint(0,frequencetirAlien)
        if test < 20 and PionTirAlien == "":
            tirAlien(posXAlien,posYAlien,dicoAlien)

        if PosY-10 < posYAlien+10 :
            Pion = ""
            etatPartie= False




    return  dicoAlien

def jouerPartie() :
    """
        fonction qui permet de jouer une partie en cliquant sur commencer
        input : none
        output : none
    """
    global boutonCommencer,vie
    boutonCommencer.destroy()
    showwarning("Alerte","Alerte ! Ils arrivent ! \n Des aliens sont entrain de nous attaqués et vous avez été choisit pour sauver la terre. \n C'est ta première mission ? \n Alors n'hésite pas a appuyer sur h pour obtenir l'aide. \n Bonne chance Major Tom et que le sort vous soit favorable.\n - Ground Control ")

    vie = 3
    maj()

def recommencer() :
    """
        fonction qui permet de recommencer la partie. Ré-initialise tous les paramètres.
        input : none
        output : none
    """

    global Canevas,Pion,dicoAlien,etatPartie,vieAlienBonus,boutonCommencer,dicoMur,vie,score,PionAlienBonus,strVarBonus,PosXAlien,PosYAlien,strVar,strrVar,img,photo,PionTirAlienBonus,PosX,PosY

    Canevas.delete("all")

    PosX = 250
    PosY = 450
    PosXAlien = 40
    PosYAlien = 50
    score = 0
    vie = 3
    vieAlienBonus = 5
    Pion = Canevas.create_image(PosX, PosY,image=photo)

    img = PhotoImage(file ='alien.ppm')
    PionAlienBonus = Canevas.create_image(PosXAlien, PosYAlien,image=img)
    PionTirAlienBonus = ""
    dicoAlien = creationAlien()
    deplacementAlien(dicoAlien)
    dicoMur = genMur()

    strrVar.set("score : 0")

    chaine = "Vies de l'alien Bonus :"+str(vieAlienBonus)
    strVarBonus.set(chaine)

    etatPartie = True
    chn = "Vie: "+ str(vie)
    strVar.set(chn)

    if Pion == "" : Pion = Canevas.create_rectangle(PosX-10, PosY-10,PosX+10,PosY+10,width=2,outline='white')

    boutonCommencer = Button(fenetre,text = 'Recommencer une partie', command = jouerPartie)
    boutonCommencer.grid(column=1,row=4)


def genMur() :
    """
        fonction qui génère des murs.
        input : none
        ouput : dicoMur : dictionnaire comprenant les murs
    """
    global Canevas,nombreMur
    listeMur = []
    dicoMur  = {}
    for i in range (nombreMur) :
        listeMur.append('Mur'+str(i))

    for j in range (len(listeMur)) :
        i = j
        if j < 5 :
            mur = afficherObjet(PosXMur+j*20,PosYMur,"white")
            dicoMur[listeMur[j]] = mur
        elif 5 <= j < 10:
            mur = afficherObjet(PosXMur+j*20+50,PosYMur,"white")
            dicoMur[listeMur[j]] = mur
        elif 10<= j < 15:
            mur = afficherObjet(PosXMur+j*20+100,PosYMur,"white")
            dicoMur[listeMur[j]] = mur
        elif 15 <= j < 20:
            i = j-15
            mur = afficherObjet(PosXMur+i*20,PosYMur+20,"white")
            dicoMur[listeMur[j]] = mur
        elif 20<= j < 25:
            i = j-15
            mur = afficherObjet(PosXMur+i*20+50,PosYMur+20,"white")
            dicoMur[listeMur[j]] = mur
        elif 25<= j < 30:
            i = j-15
            mur = afficherObjet(PosXMur+i*20+100,PosYMur+20,"white")
            dicoMur[listeMur[j]] = mur

    return dicoMur

def abandon():
    """
        fonction qui permet d'abandonner la partie commencée
        input : none
        output :none
    """
    global etatPartie,photo
    etatPartie  = 0

def accel():
    """
        fonction qui permet d'augmenter la vitesse de déplacement des aliens.
        input : none
        output : none
    """
    global vitesse
    if askyesno('Configuration','Plus rapide ? ') : vitesse = 50
    else  : vitesse = 100

def moinsdalien() :
    """
        fonction qui permet de diminuer le nombre d'alien apparaissant
        input : none
        output : none
    """
    global nombreAlien, etatPartie
    if askyesno('Configuration','Moins d\'alien ? ') :
        nombreAlien = 2
        etatPartie = False
    else  :
        nombreAlien = 27
        etatPartie = False

def pasdemur() :
    """
        fonction qui enlève les murs
        input : none
        output : none
    """
    global nombreMur,etatPartie
    if askyesno('Configuration','Plus de mur ? ') :
        nombreMur = 0
        etatPartie = False
    else  :
        nombreMur = 30
        etatPartie = False

def pasdetir() :
    """
        fonction qui enlève les tirs des aliens (mais pas de l'alienBonus)
        input : none
        output : none
    """
    global frequencetirAlien,etatPartie
    if askyesno('Configuration','Fréquence de tir proche de 0 ? ') :frequencetirAlien = 50000
    else  : frequencetirAlien = 500


def enregistrementJoueur():
    """
        fonction qui permet d'enregistrer le nom du joueur et son meilleur score  et ses pièces.
        input : none
        output : none
    """

    global nomJoueur,photo,Pion,imageVaisseau,Coin,score,strVarCoin,up
    nomJoueurATester = nomJoueur.get()
    scoreMax = score
    if nomJoueurATester in ["star","flam","who","cowboy"] or (nomJoueurATester == "albator" and "a" in up ):

        imageVaisseau = nomJoueurATester
        var = nomJoueurATester+'.ppm'
        photo = PhotoImage(file =var)
        Pion = Canevas.create_image(PosX, PosY,image=photo)
        Canevas.focus_set()
        Canevas.bind('<Key>',Clavier)
        abandon()
    else :

        fichierEnregistrement = open('enregistrement.txt','r')
        contenu = fichierEnregistrement.read()
        print(contenu)
        if nomJoueurATester in contenu :
            listetemp = contenu.split("\n")
            for i in range (len(listetemp)) :
                joueur = listetemp[i].split(":")
                if joueur[0] == nomJoueurATester :

                    Coin = int(joueur[2]) + Coin
                    scoreMax = joueur[1]
                    up = joueur[3]
                    chaineCoin = "Coins :"+str(Coin)
                    strVarCoin.set(chaineCoin)
                    if scoreMax < score : scoreMax = score
            fichierEnregistrement.close()

            fichierEnregistrement = open('enregistrement.txt','w')
            for j in range (len(listetemp)) :
                joueur = listetemp[j].split(":")
                if joueur[0] == nomJoueurATester : fichierEnregistrement.write(nomJoueurATester+":"+str(scoreMax) +":"+str(Coin)+":"+str(up)+"\n")
                else :
                    if len(joueur) == 4 : fichierEnregistrement.write(joueur[0]+":"+joueur[1]+":"+joueur[2]+joueur[3]+"\n")
            fichierEnregistrement.close()



        else :

            fichierEnregistrement = open('enregistrement.txt','a')
            if len(nomJoueurATester) == 0 :
                showwarning('Sauvegarde','Saisie incorrect')
            elif  len(nomJoueurATester) >= 15:
                showwarning('Sauvegarde','Nombre maximal de caractère atteint')
            else:
                fichierEnregistrement.write(nomJoueurATester+":"+str(scoreMax) +":"+str(Coin)+":"+str(up)+"\n")
                fichierEnregistrement.close
        Canevas.focus_set()
        Canevas.bind('<Key>',Clavier)

def meilleurScore():
    """
        fonction qui calcule le meilleur score
        input : none
        output : none
    """
    global score, scoreMax
    if score > scoreMax :
        scoreMax = score
        showinfo("Bravo","tu as battu ton record !")

def vitesseAlien():
    """
        fonction qui permet d'augmenter la vitesse des aliens quand ils sont moins nombreux
        input : none
        output : none
    """
    global dicoAlien,vitesse
    if len(dicoAlien) <5 :
        vitesse = 50
    elif 5 <= len(dicoAlien)< 10:
        vitesse = 70
    elif 10<=len(dicoAlien) <15 :
        vitesse = 80
    else :
        vitesse = 100

def bonus():
    """
    Fonction qui va afficher un pop-up ou l'on va pouvoir lire un texte fesant référence à une oeuvre pour obtenir les vaisseaux bonus.
    input : none
    output : none
    """
    liste = [u"Quel série d'animation japonaise crée en 1998 reprend les codes de la science fiction, western, ou l'on va suivre les aventures de Spike, un chasseur de prime des années 2070.\n Astuce : ne prend que le 1er mot du nom de la série ", "Quel série britanique est diffusé depuis Novembre 1963 sur BBC ou l'on suit les aventures d'un voyageur temporelle et ses assistantes. \n Astuce : ne prend que le deuxième mot du nom de la série.","Quel est la série d'animation Japonaise de 1978 à des années lumières vielle celui que le gourvenement intersidérale appel quand il n'est plus capable de trouver une solution à ses problèmes.\n Astuce : Prend le deuxième mot du nom de la série.","film qui a du mal avec la numérotation ou l'on suit des combattans il y a des années lumières. \n Astuce : Ne prend que le 1er mot du nom."]
    i = random.randint(0,len(liste)-1)
    showinfo("Bonus", liste[i])


def shop():
    """
        fonction qui permet de créer une fenètre graphique pour le market
        input : none
        output : none

    """
    global Coin, nomJoueur, StrVarVaisseau,img4,CanevasShop,img,fenetreShop

    fenetreShop = Tk()
    fenetreShop.title("Magasin de l'espace")

    largeurShop = 200
    hauteurShop = 160

    Label1 = Label(fenetreShop, text =u"Bienvenue dans le Magasin de l'espace. \n Avec l'argent récolté, vous pouvez acheter des vaisseaux.\n ")
    Label1.grid(column = 1, row =  1)

    bouton1 = Button(fenetreShop,text = 'Atlantis, 100 pièces', command = acheter)
    bouton1.grid(column=1,row=4)

def acheter():
    """
        fonction qui permet d'acheter un vaisseau
        input : none
        output : none

    """
    global strVarVaisseau, Coin,up,photo,Pion,imageVaisseau
    if Coin >= 100 :
        Coin -= 100
        up +="a"
        showinfo("Bravo","Tu vient d'acheteter Atlantis le vaisseau d'Albator qui possède 9 vie et tu pourra retrouver ce bateau sous le nom de : albator ! bonne chance")
        var = 'albator.ppm'
        imageVaisseau = var
        photo = PhotoImage(file =var)
        Pion = Canevas.create_image(PosX, PosY,image=photo)
        Canevas.focus_set()
        Canevas.bind('<Key>',Clavier)
        abandon()
    else : showwarning("Errerur","tu ne possède pas assez d'argent pour acheter un tel vaisseau")


#--

#-- Partie Easter Egg --
def murDeGauche(Canevas) :
    """
    Fonction permetant de débuter l'easter Egg en générant un labyrinthe à partir d'une variable ainsi que "stoppant" la partie en cours.
    input : Canevas
    output : none
    """
    global etatPartie,dicoAlien,Pion,PosX,PosY,photo,images
    Canevas.delete("all")
    laby = [
    "******************",
    "*  ******     ****",
    "*    **  **      *",
    "**  **** ***   ***",
    "*       *      ***",
    "** ***  ****  * **",
    "*    *   *** ** **",
    "*  ***  **** *  **",
    "*               **",
    "* **** * *** *  **",
    "* ********** *  **",
    "*               **",
    "***    * *** * ***",
    "*      * *** *  **",
    "*  ********* *  **",
    "*                 ",
    "******************"]
    posX = 0
    posY = 15
    PosX = 470
    PosY = 465
    etatPartie = "easteregg"
    for i in range (len(laby)) :
        for j in range (len(laby[i])) :
            if laby[i][j] == "*" :
                Canevas.create_rectangle(posX-15, posY-15,posX+15,posY+15,width=2,outline='white')
            posX += 30

        posY += 30
        posX = 0
    images = PhotoImage(file ="cle.ppm")
    cle = Canevas.create_image(30, 40,image=images)
    photo = PhotoImage(file ="carre.ppm")
    Pion = Canevas.create_image(PosX, PosY,image=photo)

def murDeDroite(Canevas) :
    """
    Fonction permetant de faire la partie deux de l'easter Egg en générant une salle avec la coupe.
    input : Canevas
    output : none
    """
    global etatPartie,dicoAlien,Pion,PosX,PosY,photo,images
    Canevas.delete("all")
    laby = [
    "******************",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "*                *",
    "                 *",
    "******************"]
    posX = 0
    posY = 15
    PosX = 15
    PosY = 465
    etatPartie = "easteregg"
    for i in range (len(laby)) :
        for j in range (len(laby[i])) :
            if laby[i][j] == "*" :
                Canevas.create_rectangle(posX-15, posY-15,posX+15,posY+15,width=2,outline='white')
            posX += 30

        posY += 30
        posX = 0
    images = PhotoImage(file ="coupe.ppm")
    cle = Canevas.create_image(250, 250,image=images)
    photo = PhotoImage(file ="carre.ppm")
    Pion = Canevas.create_image(PosX, PosY,image=photo)

def coupEasterEgg(touche) :
    """
    Fonction permetant de vérifier que le coups désirer par l'utilisateur est possible et gère la fin de
    la partie Easter Egg.
    input : touche (variable contenant la valeur de la touche fait par l'utilisateur)
    output : none
    """
    global PosX,PosY,Pion,cle,photo
    tmp1 = int(PosX)
    tmp2 = int(PosY)
    if touche == "Left" and PosX >= 0 and PosX <= 500:
        PosX -= 30
    if touche == "Right" :
        PosX += 30
    if touche == "Up" :
        PosY -= 30
    if touche == "Down" :
        PosY += 30
    Canevas.coords(Pion,PosX, PosY)
    coordTir = Canevas.coords(Pion)
    tupl =  Canevas.find_overlapping(coordTir[0]-10,coordTir[1]-10,coordTir[0]+10,coordTir[1]+10)
    if len(tupl) > 1 :
        PosX = tmp1
        PosY = tmp2
    Canevas.coords(Pion,PosX, PosY)
    if touche == "k" and PosX-30 <= 30 and PosY-40<=40 :
        cle = True
        showinfo("Bravo",u"Tu a réussi la première partie de cette Easter Egg  ")
        photo = PhotoImage(file ='image/vaisseau.ppm')
        abandon()

    if touche =="v" and 195 <= PosX <= 285 and 225 <= PosY <= 285:
        global score,strrVar
        showinfo("Bravo",u"Félicitation ! \n Tu a réussi cette Easter Eggs réalisé par Philippe Charrat et Lucie Dole\n Nous nous somme inspiré du premiere Easter Eggs : \n https://hitek.fr/bonasavoir/histoire-premier-easter-egg-oeuf-de-paque-jeu-video-adventure-atari_1062\n Pour ce temps passer je te t'offre pas moins de 100000 points ! \n Merci encore d'avoir joué et bonne chance fasse à cette invasion ! Philippe et Lucie")
        score = 100000
        chnn = "Score : "+ str(score)
        cle = False
        strrVar.set(chnn)
        photo = PhotoImage(file ='vaisseau.ppm')


    if touche == "r" :
        abandon()
    if touche == "h" :
        showinfo("Aide",u" Bienvenue dans l'Easter Egg de notre Space Invader, les commandes sont : \n - Flèches directionnels : se déplacer \n - k : récupérer une clé \n - r : retour à la partie classique \n - v : récupérer une coupe")

#--

#-- Programme Principale
fenetre = Tk()
fenetre.title("Space Invader")
fenetreShop = ""
largeur = 500
hauteur = 500

signe = "+"
PosX = 250
PosY = 450

PosXAlien = 40
PosYAlien = 50

PosXMur = 40
PosYMur = 350

PosXTir = 0
PosYTir = 0
PionTir = ""

PosXTirAlien = 0
PosYTirAlien = 0
PionTirAlien = ""

PionTirAlienBonus = ""
vieAlienBonus = 5

scoreMax = 0
score = 0
etatPartie = True
vie = 3
vitesse = 100
nombreMur = 30
nombreAlien = 27
frequencetirAlien = 50
signeA = "+"
listeAlien =[]
liste =[]
Coin = 0
up = "n"
imageVaisseau = "classique"
Canevas = Canvas(fenetre,width = largeur, height = hauteur, bg="black")

photo = PhotoImage(file ='vaisseau.ppm')
Pion = Canevas.create_image(PosX, PosY,image=photo)

img = PhotoImage(file ='alien.ppm')
PionAlienBonus = Canevas.create_image(PosXAlien, PosYAlien,image=img)
images = ""
cle =False
img1 = PhotoImage(file ='1.ppm')
img2 = PhotoImage(file ='2.ppm')
img3 = PhotoImage(file ='3.ppm')
img4 = ""
dicoAlien = creationAlien()
dicoMur = genMur()
deplacementAlien(dicoAlien)
Canevas.focus_set()
Canevas.bind('<Key>',Clavier)

Canevas.grid(column=1,row=4)
strVar = StringVar()
strVar.set("Nombre Vie : 3 ")
Label1 = Label(fenetre,textvariable = strVar)
Label1.grid(column=1,row=1)

strrVar = StringVar()
strrVar.set("Score : 0 ")
Label2 = Label(fenetre,textvariable = strrVar)
Label2.grid(column=1,row=3)

strVarCoin = StringVar()
strVarCoin.set("Coins : 0 ")
Label6 = Label(fenetre,textvariable = strVarCoin)
Label6.grid(column=2,row=4)

strVarBonus = StringVar()
strVarBonus.set("Vies de l'alien bonus : 5")
Label3 = Label(fenetre,textvariable = strVarBonus)
Label3.grid(column=1,row=2)


nomJoueur = StringVar()
Label4 = Entry(fenetre,textvariable = nomJoueur)
Label4.grid(column = 2, row = 2)

Label5 = Label(fenetre, text="Sauvegarder votre partie au nom de :")
Label5.grid(column = 2, row = 1)

BoutonEnregistrer = Button(fenetre, text="Enregistrer", command=enregistrementJoueur)
BoutonEnregistrer.grid(column = 2, row = 3)

boutonCommencer = Button(fenetre,text = 'Commencer une partie', command = jouerPartie)
boutonCommencer.grid(column=1,row=4)

menubar = Menu(fenetre)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Recommencer", command=abandon)
menu1.add_command(label="Quitter", command=fenetre.destroy)
menu1.add_command(label="Bonus",command=bonus)
menubar.add_cascade(label="Fichier", menu=menu1)


menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Vitesse", command=accel)
menu2.add_command(label="moins d'alien", command=moinsdalien)
menu2.add_command(label="pas de mur", command=pasdemur)
menu2.add_command(label="pas de tir", command=pasdetir)
menubar.add_cascade(label="Configuration", menu=menu2)


fenetre.config(menu=menubar)

fenetre.mainloop()
#--