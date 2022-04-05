import pyxel
import random

class Ship:
    """
        Vaisseau principal
    """
    def __init__(self, x, y):
        """
            Caractéristiques du vaisseau.
            C'est un carré dans un premier temps.
        """
        self.x = x
        self.y = y
        self.taille = 10

    def draw(self):
        """
            Affichage du vaisseau
        """
        decal = self.taille // 2
        pyxel.blt(self.x-4, self.y-4, 0, 8,0, 7, 7)

    def move(self, dx, dy):
        """
            Déplacement du vaisseau
        
    """
        
        self.x += dx
        
        self.y += dy
        
        if self.x < 0:
            self.x=0
        if self.x > 120:
            self.x=120
            

class Mob:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.taille = 3
        self.isDeath = False
        self.compteur = 0
        

        
    def draw(self):
        """
            Affichage  de l'ennemi
        """
        
        decal = self.taille // 2
        pyxel.blt(self.x-4, self.y-4, 0, 0,8, 7, 7)
    #mouvement de l'ennemi
    def moveLeft(self):
        
        self.x -= 1
            
    def moveRight(self):
        
        self.x += 1
    
    def down(self):
        
        self.y += 1


        

class Missiles:
    """
        Création des projectiles du joueur
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.taille = 2
        
    def draw(self):
        """
            Affichage du missiles
        """
        decal = self.taille // 2
        pyxel.blt(self.x-4, self.y-4, 0, 0,0, 7, 7)
    
    def move(self,dx,dy):
        """
            mouvement des missiles du vaisseau
        """
        self.x += dx
        self.y += dy
    
   

class missilesMob:
    """
        Création des projectiles des ennemis
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.taille = 2
        
    def draw(self):
        """
            Affichage du missiles
        """
        decal = self.taille // 2
        pyxel.blt(self.x-4, self.y-4, 0, 16,0, 7, 7)
    
   
    
    def fall(self,dx,dy):
        """
            mouvement des missiles ennemis
        """
        self.x -= dx
        self.y -= dy       
        
        
        
        
class App:
    def __init__(self):
        """
            Initialisation de la fenêtre et des éléments 
        """
        self.spawner = []
        self.danger = []
        self.weapon = []
        self.mob_mort = []
        self.score = 0
        self.coup = 0
        self.data = 0
        self.cpt = 0
        self.bip = 0
        self.vitesse = 1
        
        # Fenêtre de 120 par 200 pyxels
        pyxel.init(120, 200,"Pizza Invaders",60)
        pyxel.load("pack.pyxres")
       
        
        # Vaisseau en (60,180)
        self.ship = Ship(60,180)

        self.monster()
        

        # On lance le moteur du jeu
        pyxel.run(self.update, self.draw)
        
    def missiles(self):
        """
            on crée une instance pour chaque projectiles et on les insères dans un tableau
        """
        missiles = Missiles(self.ship.x,self.ship.y)
        self.weapon.append(missiles)
    
    def attaque(self,monstre):
        missiles = missilesMob(monstre.x,monstre.y)
        self.danger.append(missiles)
        
    def monster(self):
        """
            création des monstres
        """
        x = 16
        y = 30
        for i in range(5):
            for i in range(9):
                monster = Mob(x,y)
                self.spawner.append(monster)
                x += 12
            y=y+10
            x = 16

       
    def update(self):
        """
            Mise à jour des positions et des états
        """
        a=0
        if self.coup == 1 :
            return 
            
        self.cpt += 1
        
        #compteur qui permet de ne pas faire certaines actions a chaque tour
        if self.cpt == 100:
            self.cpt = 0
            self.bip +=1
        if self.bip  == 10 and self.cpt == 20:
            self.bip = 0
        
        # Déplacement à droite
        
        if self.cpt == 50:
            # entre 1 et 5 ennemis lance un projectile aléatoirement
            for i in range(random.randint(1,5)):
               
                self.attaque(random.choice(self.spawner))
        #une grande vague de projectiles tous les 50 ennemis battu
        if self.score % 50 == 0 and self.score !=0:
            self.attaque(random.choice(self.spawner))
                
        #mouvement du vaisseau
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.ship.move(1,0)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.ship.move(-1,0)

        if pyxel.btnr(pyxel.KEY_SPACE):
            self.missiles()
        
        #detecte si un des projectiles du vaisseau touche un ennemi
        for i in self.weapon:
            for b in self.spawner:
                if b.x - i.x > -5 and b.x - i.x < 5:
                    if b.y-i.y > -5 and b.y-i.y < 5:
                        a = b
                        b.isDeath = True
                        b.compteur = 1
                        self.mob_mort.append(b)
                        self.spawner.remove(b)
                        self.score +=1
                        
        
                        
            #supprime les projectiles si ils quittent l'ecran            
            if a != 0 :
    
                self.weapon.remove(i)
                a=0
            if i.y < 0:
            
                self.weapon.remove(i)
        #detecte si le vaisseau est touché
        for i in self.danger:
            b=self.ship
            if b.x - i.x > -5 and b.x - i.x < 5:
                if b.y-i.y > -5 and b.y-i.y < 5:
                    self.coup += 1
                    a=b
                            
                    
                    
            if a != 0 :

                self.danger.remove(i)
                b=0
            if i.y >200:
        
                self.danger.remove(i)
        for i in self.spawner:
            b=self.ship
            if b.x - i.x > -5 and b.x - i.x < 5:
                if b.y-i.y > -5 and b.y-i.y < 5:
                    self.coup += 1
    
    
        #recrée des monstres quand il n'y en a plus
        if len(self.spawner) == 0:
            self.monster()
        
        #fait bouger les ennemis
        for i in self.spawner:
                
            if self.cpt < 50 and self.cpt % 5 == 0:
                if i.x > 0:
                        i.moveLeft()
                
            if self.cpt >= 50 and self.cpt % 5 == 0:
                
                i.moveRight()
        #fait descendre les ennemis apres un certain temps
        if self.bip% 5 == 0 and self.cpt < 20 and self.bip !=0 :
            for i in self.spawner:
                i.down()
        #update l'etat de l'ennemi
        for i in range (len(self.spawner)):
            
            pass
            

            
               

    def draw(self):
        """
            On affiche les éléments
        """
        # On rempli le fond avec une couleur
        pyxel.cls(1)
        # On affiche le vaisseau
        self.ship.draw()
        pyxel.text(0,5,"Score: ",3)
        pyxel.text(25,5,str(self.score),3)
        pyxel.text(0,12,"Vague dans : ",3)
        pyxel.text(50,12,str(50-(self.score%50)),3)

        

        #deplace les projectiles
        for i in range(len(self.weapon)):
            self.weapon[i].draw()
            self.weapon[i].move(0,-2)
            
        for i in range(len(self.danger)):
            self.danger[i].draw()
            self.danger[i].fall(0,-2)  
                       
        #dessine les ennemis
        for i in range(len(self.spawner)):
            self.spawner[i].draw()
        #fait disparaitre les ennemis petit a petit quand ils sont touché
        for i in self.mob_mort:
            if i.compteur >= 1 and i.compteur <10:
                pyxel.blt(i.x-4, i.y-4, 0, 8,8, 7, 7)
                
            if i.compteur >= 10 and i.compteur < 20:
            
                pyxel.blt(i.x-4, i.y-4, 0, 16,8, 7, 7)
            
            if i.compteur == 30:
                self.mob_mort.remove(i)
            
            if i.compteur > 0:
                i.compteur += 1
        #game over quand un projectile touche le vaisseau
        if self.coup==1 :
            pyxel.blt(self.ship.x-4, self.ship.y-4, 0, 24,0, 7, 7)
            self.spawner=[]
            pyxel.text(45,90,"GAME OVER ",3)
            

           
        



App()