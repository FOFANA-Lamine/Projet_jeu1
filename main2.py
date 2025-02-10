import  random
import  time


class Robot:
    def __init__(self, type:str , sn:int, orientation = 1 , etat = False):
        self.type = type
        self.sn = sn
        self.orientation = orientation
        self.etat = etat

    def getType(self):
        return self.type

    def getSN(self):
        return self.sn

    def getOrientation(self):
        return self.orientation

    def getEtat(self):
        return self.etat

    def setOrientation(self, nouvelle_orientation):
        self.orientation = nouvelle_orientation

    def setEtat(self , nouvel_etat:bool):
        self.etat = nouvel_etat

    # Par défaut tourne vers la gauche
    def tourner(self, sens = 1):
        if sens == 1:
            if self.orientation == 4:
                self.orientation = 1
            else:
                self.orientation += 1
        else:
            if self.orientation == 1:
                self.orientation = 4
            else:
                self.orientation -= 1

    def afficheInfos(self):
        print(f"Numéro de série :{self.getSN() } ")
        print(f"Etat :{self.getEtat()} ")
        print(f"Orientation :{self.getOrientation()} ")
        print(f"Type :{self.getType()} ")

# ----------
class RobotMobile(Robot):
    def __init__(self, origine_x = 0, origine_y = 0):
        super().__init__("Mobile",25)
        self.x = origine_x
        self.y = origine_y

    def avancer(self, pas):
        # NORD
        if self.orientation == 1:
            self.y += pas

        # SUD
        if self.orientation == 3:
            self.y -= pas

        # EST
        if self.orientation == 2:
            self.x += pas

        # OUEST
        if self.orientation == 4:
            self.x -= pas

    def affichePosition(self):
        print(f"x (abscisse) : {self.x}")
        print(f"Y (ordonnée) : {self.y}")

    def getPosition(self):
        return (self.x, self.y)


    def afficheInfos(self):
        super().afficheInfos()
        self.affichePosition()

# ------------------------------------


def demarrer_niveau(niveau):
    print(f"\n--- Démarrage du niveau {niveau} ! ---")
    print(f"Obstacles à éviter : {niveaux[niveau]['obstacles']}, Temps limite : {niveaux[niveau]['temps_limite']} secondes")
    min, max = -20, 20
    aX, aY= random.randint(min, max), random.randint(min, max)
    if aX > 0:
        cibleX = ("Est:", aX)
        bX = aX
    else:
        cibleX = ("Ouest:", aX)
        bX = aX

    if aY > 0:
        cibleY = ("Nord:", aY)
        bY = aY
    else:
        cibleY = ("Sud:", aY)
        bY = aY
    cible_Explicatif = (cibleX, cibleY)
    cible = (bX, bY)
    print(f"Votre cible se trouve exactement à :{cible_Explicatif} ")
    print(f"Vous devez rejoindre ce cible pour remporter la partie.\nVotre position actuelle est:")
    robot.affichePosition()

    print(f"Obstacles à éviter : {niveaux[niveau]['obstacles']}, Temps limite : {niveaux[niveau]['temps_limite']} secondes")
    return niveaux[niveau]['temps_limite'], cible




# ----------------------- Programme principal  ------------------------------------------
pas_liste = [1, 2, 3]
direction = {"NORD": 1, "EST": 2, "SUD": 3, "OUEST": 4}
direction_liste = ("NORD", "EST", "SUD","OUEST")
robot = RobotMobile()

# Gerer le debut du jeu
commencer_int = False
while not commencer_int:
    # demarrer_niveau(niveau_actuel)
    commencer_str = input("Tapez 1 pour commencer le jeu ou 2 pour terminer : ")
    try:
        commencer_int = int(commencer_str)
        if commencer_int != 1 and commencer_int != 2:
            print("Vous devez entrer un nombre entre 1 et 2 :\n1 : Pour commencer le jeu\n2 : Pour annuler")
            commencer_int = False  # Reste à False pour redemander l'entrée
        elif commencer_int == 2:
            print("Vous êtes sorti du jeu")
            break
        elif commencer_int == 1:
            print("Vous avez choisi de commencer le jeu.")
            # On peut sortir de la boucle ici pour commencer le jeu
            break
    except ValueError:
        print("ERREUR : Vous devez entrer un chiffre entre 1 et 2")
        commencer_int = False  # Reste à False pour redemander l'entrée


# Définition des niveaux avec un temps limite
niveaux = {
    1: {"obstacles": 0, "temps_limite": 240},
    2: {"obstacles": 2, "temps_limite": 120},
    3: {"obstacles": 4, "temps_limite": 60},
}


niveau_actuel = 1

# Si on a choisi de commencer le jeu, alors on initialise la position
if commencer_int == 1:
    while niveau_actuel <= len(niveaux):
        temps_limite, cible = demarrer_niveau(niveau_actuel)
        temps_debut = time.time()  # Enregistre le temps de début

        position_utilisateur = robot.getPosition()
        # Boucle de jeu
        while position_utilisateur != cible:
            temps_ecoule = time.time() - temps_debut  # Calcule le temps écoulé
            temps_restant = temps_limite - temps_ecoule  # Calcule le temps restant
            if temps_restant <= 0:
               print("Temps écoulé ! Vous avez perdu ce niveau.")
               break
            print(f"Temps restant : {max(0, int(temps_restant))} secondes")
            # Gerer la direction
            while True and temps_restant > 0:
                direction_utilisateur = input("Choisir une direction (NORD, SUD, EST ou OUEST) : ").upper()
                if direction_utilisateur in direction_liste:
                    robot.setOrientation(direction[direction_utilisateur])
                    break
                else:
                    print("Vous devez entrez une direction correcte (NORD, SUD, EST ou OUEST)")


            # Gerer les pas
            while True and temps_restant >0:
                pas_utlisateur = input("Entrez vos pas d'avancement (1, 2 ou 3) : ")
                try:
                    pas = int(pas_utlisateur)
                    if pas in pas_liste:
                        robot.avancer(pas)
                        position_utilisateur = robot.getPosition()
                        break
                    else:
                        print("Vos pas d'avancement doit etre entre 1 ou 2 ou 3")
                except ValueError:
                    print("ERREUR : vos pas d'avancement doit etre un entier : 1 , 2 ou 3")

            print("Votre nouvelle position :")
            robot.affichePosition()

        if position_utilisateur == cible:
            print(f"Félicitations ! Vous avez terminé le niveau {niveau_actuel}.")
            niveau_actuel += 1  # Passez au niveau suivant
            t = 15
            print(f"Veuillez patientez pendant {time.time() - t} secondes avant le demarrage du niveau {niveau_actuel} .")
            time.sleep(t)

        else:
            print("Vous n'avez pas réussi à atteindre la cible dans le temps imparti.")
            break  # Sortir de la boucle si le joueur échoue

    print("Fin du jeu.")













