import random
import pandas as pd
import numpy as np
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

pokedf = pd.read_csv('datos/Pokemon.csv',header=None)
atqdf = pd.read_csv('datos/Ataques.csv',header=None)
tipodf = pd.read_csv('datos/Tipos.csv',header=None)
efectividaddf = pd.read_csv('datos/Efectividad.csv',header=None)
pokemonesA = []
pokemonesB = []
tiposA=[]
tiposB=[]
ataquesB =[]
ataquesA = []
pokemonActualA=0
pokemonActualB=0
vidaActualA=0
vidaActualB=0
vidaActualTotalA=0
vidaActualTotalB=0
dano=0
DanoB=None
DanoA=None
A_Ataque1=None
A_Ataque2=None
A_Ataque3=None
A_Ataque4=None
A_Tipo1=None
A_Tipo2=None
A_Tipo3=None
A_Tipo4=None
NamePokemonA=None
VidaPokemonA=None
NamePokemonB=None
VidaPokemonB=None
B_Ataque1=None
B_Ataque2=None
B_Ataque3=None
B_Ataque4=None
B_Tipo1=None
B_Tipo2=None
B_Tipo3=None
B_Tipo4=None
PokemonA1=None
PokemonA2=None
PokemonA3=None
PokemonB1=None
PokemonB2=None
PokemonB3=None
PokemonTipoA1=None
PokemonTipoA2=None
PokemonTipoB1=None
PokemonTipoB2=None
root=None
imgA1=None
imgA2=None
imgA3=None
imgB1=None
imgB2=None
imgB3=None
tipo1PokeA=None
tipo1PokeB=None
tipo2PokeA=None
tipo2PokeB=None
lasVidas=0
menos_vida=0

def init(top, gui, *args, **kwargs):
    global w,root
    w = gui
    top_level = top
    root = top

def vp_start_gui():
    global w,root
    root = tk.Tk()
    top = Battalla (root)
    init(root, top)
    root.mainloop()

w = None
def create_Battalla(root, *args, **kwargs):
    global w
    rt = root
    w = tk.Toplevel (root)
    top = Battalla (w)
    init(w, top, *args, **kwargs)
    return (w, top)

def heuristica(eleccionDano):
    global menos_vida
    ataquesMayores=[0]
    maximoAtaqueB=0
    for n in range (1,5):
        for x in range(3):
            for y in range(3):
                ataquesMayores.append(np.ceil(heuristica_auxiliar(n,x,y)))
    maximoAtaqueB=max(ataquesMayores)
    heuristica_parcial = pokedf.iloc[pokemonesA[0], 4] + pokedf.iloc[pokemonesA[1], 4] + pokedf.iloc[pokemonesA[2], 4]
    menos_vida = menos_vida + np.ceil(maximizarB(eleccionDano, False))
    heuristica=(heuristica_parcial-menos_vida)/maximoAtaqueB
    print("*******************************************")
    print("heurística: ", heuristica)

def heuristica_auxiliar(n,pokemonActualA,pokemonActualB):
    global dano
    tipoAtaque=atqdf.iloc[ataquesB[n-1],2]
    tipo1PokeA=pokedf.iloc[pokemonesA[pokemonActualA],2]
    tipo1PokeB=pokedf.iloc[pokemonesB[pokemonActualB],2]
    tipo2PokeA=pokedf.iloc[pokemonesA[pokemonActualA],3]
    tipo2PokeB=pokedf.iloc[pokemonesB[pokemonActualB],3]
    A=pokedf.iloc[pokemonesB[pokemonActualB],5]# Ataque del Pokemon Aliado
    D=pokedf.iloc[pokemonesA[pokemonActualA],6]# Defensa del Pokemon Enemigo
    P=atqdf.iloc[ataquesB[(n-1)],3]# Potencia del ataque Aliado
    V=atqdf.iloc[ataquesB[(n-1)],4]# Precision del ataque Aliado
    E1=efectividaddf.iloc[tipoAtaque,tipo1PokeA]# Efectividad del ataque segun tipo
    E2=efectividaddf.iloc[tipoAtaque,tipo2PokeA]
    if(E1>E2):
        E=E1
    else:
        E=E2
    if(tipo1PokeA==tipo1PokeB or tipo1PokeA==tipo2PokeB or tipo2PokeA==tipo1PokeB):
        B=1.5
    else:
        B=1
    dano = 0.01*B*E*V*((((0.2+1)*A*P)/(25*D))+2)
    return dano

def minmax():
    global pokemonActualB
    for i in range(3):
        eldano=maximizarB(i,False)
        if(eldano>maximizarB(i+1,False)):
            danoescogido=eldano
            eleccionDano=i
        else:
            danoescogido=maximizarB(i+1,False)
            eleccionDano=i+1
    heuristica(eleccionDano)
    maximizarB(eleccionDano+(pokemonActualB*4),True)

def ponerAtaquesDeB():
    global pokemonActualB
    B_Ataque1.configure(text='{}'.format(atqdf.iloc[ataquesB[0+(pokemonActualB*4)],1]))
    tipo1=atqdf.iloc[ataquesB[0+(pokemonActualB*4)],2]
    B_Tipo1.configure(text='{}'.format(tipodf.iloc[tipo1,1]))
    B_Ataque2.configure(text='{}'.format(atqdf.iloc[ataquesB[1+(pokemonActualB*4)],1]))
    tipo2=atqdf.iloc[ataquesB[1+(pokemonActualB*4)],2]
    B_Tipo2.configure(text='{}'.format(tipodf.iloc[tipo2,1]))
    B_Ataque3.configure(text='{}'.format(atqdf.iloc[ataquesB[2+(pokemonActualB*4)],1]))
    tipo3=atqdf.iloc[ataquesB[2+(pokemonActualB*4)],2]
    B_Tipo3.configure(text='{}'.format(tipodf.iloc[tipo3,1]))
    B_Ataque4.configure(text='{}'.format(atqdf.iloc[ataquesB[3+(pokemonActualB*4)],1]))
    tipo4=atqdf.iloc[ataquesB[3+(pokemonActualB*4)],2]
    B_Tipo4.configure(text='{}'.format(tipodf.iloc[tipo4,1]))

def ponerAtaquesDeA():
    global pokemonActualA
    A_Ataque1.configure(text='{}'.format(atqdf.iloc[ataquesA[0+(pokemonActualA*4)],1]))
    tipo1=atqdf.iloc[ataquesA[0+(pokemonActualA*4)],2]
    A_Tipo1.configure(text='{}'.format(tipodf.iloc[tipo1,1]))
    A_Ataque2.configure(text='{}'.format(atqdf.iloc[ataquesA[1+(pokemonActualA*4)],1]))
    tipo2=atqdf.iloc[ataquesA[1+(pokemonActualA*4)],2]
    A_Tipo2.configure(text='{}'.format(tipodf.iloc[tipo2,1]))
    A_Ataque3.configure(text='{}'.format(atqdf.iloc[ataquesA[2+(pokemonActualA*4)],1]))
    tipo3=atqdf.iloc[ataquesA[2+(pokemonActualA*4)],2]
    A_Tipo3.configure(text='{}'.format(tipodf.iloc[tipo3,1]))
    A_Ataque4.configure(text='{}'.format(atqdf.iloc[ataquesA[3+(pokemonActualA*4)],1]))
    tipo4=atqdf.iloc[ataquesA[3+(pokemonActualA*4)],2]
    A_Tipo4.configure(text='{}'.format(tipodf.iloc[tipo4,1]))

def ponertiposparaataques():
    global tipo1PokeA,tipo1PokeB,tipo2PokeA,tipo2PokeB
    tipo1PokeA=pokedf.iloc[pokemonesA[pokemonActualA],2]
    tipo1PokeB=pokedf.iloc[pokemonesB[pokemonActualB],2]
    tipo2PokeA=pokedf.iloc[pokemonesA[pokemonActualA],3]
    tipo2PokeB=pokedf.iloc[pokemonesB[pokemonActualB],3]

def efectuarDanoA_B(dano):
    global vidaActualB,pokemonActualB,vidaActualTotalB,pokemonActualB,lasVidas
    vidaActualB-=dano
    DanoB.configure(text='{} le ha causado {} de daño a {}'.format(NamePokemonA.cget("text"),int(dano),NamePokemonB.cget("text")))
    if(vidaActualB<=0):
        pokemonActualB+=1
        if(pokemonActualB>2):
            messagebox.showinfo(message="¡¡¡Has Ganado!!!", title="¡GAME OVER!")
            root.destroy()
        else:
            vidaActualB=vidaActualTotalB=pokedf.iloc[pokemonesB[pokemonActualB],4]
            if(pokemonActualB==1):
                PokemonB1.configure(image=imgB2)
                PokemonB2.configure(image='')
            else:
                PokemonB1.configure(image=imgB3)
                PokemonB3.configure(image='')
            NamePokemonB.configure(text='{}'.format(pokedf.iloc[pokemonesB[pokemonActualB],1]))
            tipo1=pokedf.iloc[pokemonesB[pokemonActualB],2]
            tipo2=pokedf.iloc[pokemonesB[pokemonActualB],3]
            PokemonTipoB1.configure(text='{}'.format(tipodf.iloc[tipo1,1]))
            if(tipo2==0):
                PokemonTipoB2.configure(text='')
            else:
                PokemonTipoB2.configure(text='{}'.format(tipodf.iloc[tipo2,1]))
            ponerAtaquesDeB()
    VidaPokemonB.configure(text='{}/{}'.format(int(vidaActualB),vidaActualTotalB))
    time.sleep(1)
    minmax()

def efectuarDanoB_A(dano):
    global vidaActualA,pokemonActualA,vidaActualTotalA
    vidaActualA-=dano
    DanoA.configure(text='{} le ha causado {} de daño a {}'.format(NamePokemonB.cget("text"),int(dano),NamePokemonA.cget("text")))
    if(vidaActualA<=0):
        pokemonActualA+=1
        if(pokemonActualA>2):
            messagebox.showinfo(message="¡¡¡¡¡¡¡¡¡ Ha Ganado La IA :( !!!!!!!!!", title="¡GAME OVER!")
            root.destroy()
        else:
            vidaActualA=vidaActualTotalA=pokedf.iloc[pokemonesA[pokemonActualA],4]
            if(pokemonActualA==1):
                PokemonA1.configure(image=imgA2)
                PokemonA2.configure(image='')
            else:
                PokemonA1.configure(image=imgA3)
                PokemonA3.configure(image='')
            NamePokemonA.configure(text='{}'.format(pokedf.iloc[pokemonesA[pokemonActualA],1]))
            tipo1=pokedf.iloc[pokemonesA[pokemonActualA],2]
            tipo2=pokedf.iloc[pokemonesA[pokemonActualA],3]
            PokemonTipoA1.configure(text='{}'.format(tipodf.iloc[tipo1,1]))
            if(tipo2==0):
                PokemonTipoA2.configure(text='')
            else:
                PokemonTipoA2.configure(text='{}'.format(tipodf.iloc[tipo2,1]))
            ponerAtaquesDeA()
    VidaPokemonA.configure(text='{}/{}'.format(int(vidaActualA),vidaActualTotalA))

def Aataca(n):
    global dano,pokemonActualA,pokemonActualB,vidaActualB,vidaActualTotalB
    vidaActualTotalB=pokedf.iloc[pokemonesB[pokemonActualB],4]
    tipoAtaque=atqdf.iloc[ataquesA[n-1],2]
    ponertiposparaataques()
    A=pokedf.iloc[pokemonesA[pokemonActualA],5]# Ataque del Pokemon Aliado
    D=pokedf.iloc[pokemonesB[pokemonActualB],6]# Defensa del Pokemon Enemigo
    P=atqdf.iloc[ataquesA[(n-1)],3]# Potencia del ataque Aliado
    V=atqdf.iloc[ataquesA[(n-1)],4]# Precision del ataque Aliado
    E1=efectividaddf.iloc[tipoAtaque,tipo1PokeB]# Efectividad del ataque segun tipo
    E2=efectividaddf.iloc[tipoAtaque,tipo2PokeB]
    if(E1>E2):
        E=E1
    else:
        E=E2
    if(tipo1PokeA==tipo1PokeB or tipo1PokeA==tipo2PokeB or tipo2PokeA==tipo1PokeB):
        B=1.5
    else:
        B=1
    dano = 0.01*B*E*V*((((0.2+1)*A*P)/(25*D))+2)
    print("******************HUMANO*******************")
    print("Vida B",vidaActualB)
    print("Ataque del Pokemon A",A)
    print("Defensa del Pokemon B",D)
    print("Potencia del Ataq ",n,P)
    print("Precision del Atq ",n,V)
    print("Factor de tipos ",B)
    print("Efectividad del ataque",E)
    print("Daño:",dano)
    print("Daño real:",np.ceil(dano))
    efectuarDanoA_B(np.ceil(dano))

def maximizarB(n,hacerlo):
    global dano,pokemonActualA,pokemonActualB,vidaActualB,vidaActualTotalA
    vidaActualTotalA=pokedf.iloc[pokemonesA[pokemonActualA],4]
    tipoAtaque=atqdf.iloc[ataquesB[n-1],2]
    ponertiposparaataques()
    A=pokedf.iloc[pokemonesB[pokemonActualB],5]# Ataque del Pokemon Aliado
    D=pokedf.iloc[pokemonesA[pokemonActualA],6]# Defensa del Pokemon Enemigo
    P=atqdf.iloc[ataquesB[(n-1)],3]# Potencia del ataque Aliado
    V=atqdf.iloc[ataquesB[(n-1)],4]# Precision del ataque Aliado
    E1=efectividaddf.iloc[tipoAtaque,tipo1PokeA]# Efectividad del ataque segun tipo
    E2=efectividaddf.iloc[tipoAtaque,tipo2PokeA]
    if(E1>E2):
        E=E1
    else:
        E=E2
    if(tipo1PokeA==tipo1PokeB or tipo1PokeA==tipo2PokeB or tipo2PokeA==tipo1PokeB):
        B=1.5
    else:
        B=1
    dano = 0.01*B*E*V*((((0.2+1)*A*P)/(25*D))+2)
    if(hacerlo==True):
        print("******************IA*******************")
        print("Vida A",vidaActualA)
        print("Ataque del Pokemon B",A)
        print("Defensa del Pokemon A",D)
        print("Potencia del Ataq ",n,P)
        print("Precision del Atq ",n,V)
        print("Factor de tipos ",B)
        print("Efectividad del ataque",E)
        print("Daño:",dano)
        print("Daño real:",np.ceil(dano))
        efectuarDanoB_A(np.ceil(dano))
    else:
        return dano

class Battalla:
    i=0
    for i in range(12):
        ataquesA.append(random.randint(1,100))
        ataquesB.append(random.randint(1,100))

    def pokemonAAleatorio(self,n):
        r=random.randint(1, 152)
        pokemonesA.append(r)
        tiposA.append(pokedf.iloc[r,2])
        tiposA.append(pokedf.iloc[r,3])
        if(n==1):
            self.ImgA1Pokemon = tk.PhotoImage(file='pokemones/espalda/{}.png'.format(r))
            self.ImgA1Pokemon=self.ImgA1Pokemon.zoom(2,2)
            return self.ImgA1Pokemon
        if(n==2):
            self.ImgA2Pokemon = tk.PhotoImage(file='pokemones/espalda/{}.png'.format(r))
            return self.ImgA2Pokemon
        if(n==3):
            self.ImgA3Pokemon = tk.PhotoImage(file='pokemones/espalda/{}.png'.format(r))
            return self.ImgA3Pokemon

    def pokemonBAleatorio(self,n):
        r=random.randint(1, 152)
        pokemonesB.append(r)
        tiposB.append(pokedf.iloc[r,2])
        tiposB.append(pokedf.iloc[r,3])
        if(n==1):
            self.ImgB1Pokemon = tk.PhotoImage(file='pokemones/frente/{}.png'.format(r))
            self.ImgB1Pokemon=self.ImgB1Pokemon.zoom(2,2)
            return self.ImgB1Pokemon
        if(n==2):
            self.ImgB2Pokemon = tk.PhotoImage(file='pokemones/frente/{}.png'.format(r))
            return self.ImgB2Pokemon
        if(n==3):
            self.ImgB3Pokemon = tk.PhotoImage(file='pokemones/frente/{}.png'.format(r))
            return self.ImgB3Pokemon

    def __init__(self, top=None):
        global pokemonActualA
        top.geometry("650x450+388+135")
        top.title("Batalla Pokemon")
        global imgA1,imgA2,imgA3,imgB1,imgB2,imgB3
        imgA1=self.pokemonAAleatorio(1)
        imgA2=self.pokemonAAleatorio(2)
        imgA3=self.pokemonAAleatorio(3)
        imgB1=self.pokemonBAleatorio(1)
        imgB2=self.pokemonBAleatorio(2)
        imgB3=self.pokemonBAleatorio(3)

        self.Principal = tk.Canvas(top)
        self.Principal.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.Principal.configure(width=650,height=650)
        
        self.Bloque1 = tk.Frame(self.Principal)
        self.Bloque1.place(relx=0.015, rely=0.822, relheight=0.156, relwidth=0.923)
        self.Bloque1.configure(borderwidth="5")
        self.Bloque1.configure(relief="groove")
        self.Bloque1.configure(width=600)
        global A_Ataque1,A_Ataque2,A_Ataque3,A_Ataque4,A_Tipo1,A_Tipo2,A_Tipo3,A_Tipo4
        A_Ataque3 = tk.Button(self.Bloque1)
        A_Ataque3.place(relx=0.683, rely=0.143, height=24, width=110)
        A_Ataque3.config(command=lambda: Aataca(3+(pokemonActualA*4)))

        A_Ataque4 = tk.Button(self.Bloque1)
        A_Ataque4.place(relx=0.683, rely=0.571, height=24, width=110)
        A_Ataque4.config(command=lambda: Aataca(4+(pokemonActualA*4)))

        A_Ataque1 = tk.Button(self.Bloque1)
        A_Ataque1.place(relx=0.35, rely=0.143, height=24, width=110)
        A_Ataque1.config(command=lambda: Aataca(1+(pokemonActualA*4)))

        A_Ataque2 = tk.Button(self.Bloque1)
        A_Ataque2.place(relx=0.35, rely=0.571, height=24, width=110)
        A_Ataque2.config(command=lambda: Aataca(2+(pokemonActualA*4)))
        global NamePokemonA,VidaPokemonA
        NamePokemonA = tk.Label(self.Bloque1)
        NamePokemonA.place(relx=0.010, rely=0.143, height=21, width=124)
        NamePokemonA.configure(font='Helvetica 12 bold')

        VidaPokemonA = tk.Label(self.Bloque1)
        VidaPokemonA.place(relx=0.033, rely=0.48, height=21, width=88)
        VidaPokemonA.configure(font='Helvetica 12 bold')

        A_Tipo1 = tk.Label(self.Bloque1)
        A_Tipo1.place(relx=0.55, rely=0.143, height=21, width=74)

        A_Tipo2 = tk.Label(self.Bloque1)
        A_Tipo2.place(relx=0.55, rely=0.571, height=21, width=74)

        A_Tipo3 = tk.Label(self.Bloque1)
        A_Tipo3.place(relx=0.867, rely=0.143, height=21, width=74)

        A_Tipo4 = tk.Label(self.Bloque1)
        A_Tipo4.place(relx=0.867, rely=0.571, height=21, width=74)

        self.Bloque2 = tk.Frame(self.Principal)
        self.Bloque2.place(relx=0.062, rely=0.333, relheight=0.156, relwidth=0.923)
        self.Bloque2.configure(borderwidth="5")
        self.Bloque2.configure(relief='groove')
        self.Bloque2.configure(width=600)
        global B_Ataque1,B_Ataque2,B_Ataque3,B_Ataque4,B_Tipo1,B_Tipo2,B_Tipo3,B_Tipo4
        B_Ataque1 = tk.Label(self.Bloque2)
        B_Ataque1.place(relx=0.033, rely=0.143, height=24, width=110)
        B_Ataque1.configure(relief="groove")

        B_Ataque2 = tk.Label(self.Bloque2)
        B_Ataque2.place(relx=0.033, rely=0.571, height=24, width=110)
        B_Ataque2.configure(relief="groove")

        B_Ataque3 = tk.Label(self.Bloque2)
        B_Ataque3.place(relx=0.367, rely=0.143, height=24, width=110)
        B_Ataque3.configure(relief="groove")

        B_Ataque4 = tk.Label(self.Bloque2)
        B_Ataque4.place(relx=0.367, rely=0.571, height=24, width=110)
        B_Ataque4.configure(relief="groove")
        global NamePokemonB,VidaPokemonB
        NamePokemonB = tk.Label(self.Bloque2)
        NamePokemonB.place(relx=0.767, rely=0.143, height=21, width=124)
        NamePokemonB.configure(font='Helvetica 12 bold')

        VidaPokemonB = tk.Label(self.Bloque2)
        VidaPokemonB.place(relx=0.808, rely=0.5, height=21, width=88)
        VidaPokemonB.configure(font='Helvetica 12 bold')

        B_Tipo1 = tk.Label(self.Bloque2)
        B_Tipo1.place(relx=0.233, rely=0.143, height=21, width=74)

        B_Tipo2 = tk.Label(self.Bloque2)
        B_Tipo2.place(relx=0.233, rely=0.571, height=21, width=74)

        B_Tipo3 = tk.Label(self.Bloque2)
        B_Tipo3.place(relx=0.567, rely=0.143, height=21, width=74)

        B_Tipo4 = tk.Label(self.Bloque2)
        B_Tipo4.place(relx=0.567, rely=0.571, height=21, width=74)

        global PokemonA1,PokemonA2,PokemonA3,PokemonB1,PokemonB2,PokemonB3,PokemonTipoA1,PokemonTipoA2,PokemonTipoB1,PokemonTipoB2
        PokemonA1 = tk.Label(self.Principal)
        PokemonA1.place(relx=0.015, rely=0.489, height=150, width=150)

        PokemonA2 = tk.Label(self.Principal)
        PokemonA2.place(relx=0.785, rely=0.733, height=40, width=40)

        PokemonA3 = tk.Label(self.Principal)
        PokemonA3.place(relx=0.862, rely=0.733, height=40, width=40)

        PokemonB1 = tk.Label(self.Principal)
        PokemonB1.place(relx=0.738, rely=0.0, height=150, width=150)

        PokemonB2 = tk.Label(self.Principal)
        PokemonB2.place(relx=0.062, rely=0.244, height=40, width=40)

        PokemonB3 = tk.Label(self.Principal)
        PokemonB3.place(relx=0.138, rely=0.244, height=40, width=40)

        PokemonTipoA1 = tk.Label(self.Principal)
        PokemonTipoA1.place(relx=0.262, rely=0.756, height=21, width=74)

        PokemonTipoA2 = tk.Label(self.Principal)
        PokemonTipoA2.place(relx=0.431, rely=0.756, height=21, width=74)

        PokemonTipoB1 = tk.Label(self.Principal)
        PokemonTipoB1.place(relx=0.615, rely=0.267, height=21, width=74)

        PokemonTipoB2 = tk.Label(self.Principal)
        PokemonTipoB2.place(relx=0.462, rely=0.267, height=21, width=74)

        
        global DanoA,DanoB
        DanoB = tk.Label(self.Principal)
        DanoB.place(relx=0.01, rely=0.067, height=30, width=400)
        DanoB.configure(font='Helvetica 12 italic')
        DanoA = tk.Label(self.Principal)
        DanoA.place(relx=0.42, rely=0.578, height=30, width=400)
        DanoA.configure(font='Helvetica 12 italic')


        global vidaActualA,vidaActualB
        #### DEFINIENDO ####
        ### JUGADOR A ###
        PokemonA1.configure(image=imgA1)
        PokemonA2.configure(image=imgA2)
        PokemonA3.configure(image=imgA3)
        NamePokemonA.configure(text='{}'.format(pokedf.iloc[pokemonesA[0],1]))
        vida=pokedf.iloc[pokemonesA[0],4]
        vidaActualA=vida
        VidaPokemonA.configure(text='{}/{}'.format(vida,vida))
        PokemonTipoA1.configure(text='{}'.format(tipodf.iloc[tiposA[0],1]))
        if(tiposA[1]==0):
            PokemonTipoA2.configure(text='')
        else:
            PokemonTipoA2.configure(text='{}'.format(tipodf.iloc[tiposA[1],1]))
        ### ATAQUES
        ponerAtaquesDeA()

        ### JUGADOR B ###
        PokemonB1.configure(image=imgB1)
        PokemonB2.configure(image=imgB2)
        PokemonB3.configure(image=imgB3)
        NamePokemonB.configure(text='{}'.format(pokedf.iloc[pokemonesB[0],1]))
        vida=pokedf.iloc[pokemonesB[0],4]
        vidaActualB=vida
        VidaPokemonB.configure(text='{}/{}'.format(vida,vida))
        PokemonTipoB1.configure(text='{}'.format(tipodf.iloc[tiposB[0],1]))
        if(tiposB[1]==0):
            PokemonTipoB2.configure(text=' ')
        else:
            PokemonTipoB2.configure(text='{}'.format(tipodf.iloc[tiposB[1],1]))
        ### ATAQUES
        ponerAtaquesDeB()
        

if __name__ == '__main__':
    vp_start_gui()