#interfaz grafica de Arena de batalla
#Tomas Arroyave - Jaleth Campuzano

import tkinter as tk
import os
import sys
import json

#esto le dice a Python donde encontrar el archivo juego.py
sys.path.insert(0, os.path.dirname(__file__))

from juego import (
    Guerrero, Mago, Arquero, Item,
    crear_torre, aplicar_escalado,
    guardar_puntaje,
    ARCHIVO_PUNTAJES,
)
#se agrega la imagen de fondo
RUTA_FONDO = os.path.join(os.path.dirname(__file__), "fondo.png")

def cargar_puntajes():
    if not os.path.exists(ARCHIVO_PUNTAJES):
        return []
    with open(ARCHIVO_PUNTAJES) as f:
        return json.load(f)

def poner_fondo(contenedor):
    try:
        img = tk.PhotoImage(file=RUTA_FONDO)
        c = tk.Canvas(contenedor, width=980, height=680)
        c.place(x=0, y=0, relwidth=1, relheight=1)
        c.create_image(0, 0, anchor="nw", image=img)
        c._img = img
    except Exception:
        pass

#pantalla de inicio

class PantallaInicio:
    def __init__(self, ventana, al_iniciar):
        self.ventana = ventana
        self.al_iniciar = al_iniciar
        self.clase_elegida = tk.StringVar(value="guerrero")
        self.frame = tk.Frame(ventana, bg="#1b2233")
        self.construir()

    def construir(self):
        poner_fondo(self.frame)

        tk.Label(self.frame, text="ARENA DE BATALLA",
                 font=("Trebuchet MS", 28, "bold"),
                 bg="#1b2233", fg="#d4a017").pack(pady=(30, 0))

        tk.Label(self.frame, text="Tomas Arroyave  -  Jaleth Campuzano",
                 font=("Consolas", 9), bg="#1b2233", fg="#8892a4").pack(pady=(2, 0))

        cuerpo = tk.Frame(self.frame, bg="#1b2233")
        cuerpo.pack(fill="both", expand=True, padx=60)

        col_izq = tk.Frame(cuerpo, bg="#232e44", padx=20, pady=20)
        col_izq.pack(side="left", fill="y", padx=(0, 8))

        col_centro = tk.Frame(cuerpo, bg="#232e44")
        col_centro.pack(side="left", fill="both", expand=True, padx=8)

        col_der = tk.Frame(cuerpo, bg="#232e44", padx=16, pady=16)
        col_der.pack(side="left", fill="y", padx=(8, 0))

#tabla de nombre y clase
#se crea la columna donde se va a poner el nombre y la clase del jugador
        tk.Label(col_izq, text="NOMBRE DEL HEROE",
                 font=("Consolas", 9, "bold"), bg="#232e44", fg="#8892a4").pack(anchor="w")

        self.campo_nombre = tk.Entry(col_izq, font=("Trebuchet MS", 13), width=16,
                                     bg="#2a3750", fg="#e8eaf0",
                                     insertbackground="#d4a017", relief="flat", bd=6)
        self.campo_nombre.insert(0, "heroe")
        self.campo_nombre.pack(fill="x", pady=(6, 0))

        tk.Label(col_izq, text="\nELIGE TU CLASE",
                 font=("Consolas", 9, "bold"), bg="#232e44", fg="#8892a4").pack(anchor="w")

        clases = [
            ("Guerrero", "guerrero", "Furia al 30% de vida"),
            ("Mago",     "mago",     "Puede curarse"),
            ("Arquero",  "arquero",  "Doble disparo"),
        ]
        for nombre_c, val, desc in clases:
            f = tk.Frame(col_izq, bg="#232e44")
            f.pack(fill="x", pady=4)
            tk.Radiobutton(f, text=nombre_c, variable=self.clase_elegida, value=val,
                           font=("Trebuchet MS", 11), bg="#232e44", fg="#e8eaf0",
                           selectcolor="#2a3750", activebackground="#232e44",
                           activeforeground="#d4a017").pack(side="left")
            tk.Label(f, text=desc, font=("Consolas", 8),
                     bg="#232e44", fg="#8892a4").pack(side="left", padx=6)

        tk.Button(col_izq, text="COMENZAR PARTIDA", command=self.iniciar,
                  font=("Trebuchet MS", 11, "bold"),
                  bg="#2e4070", fg="#d4a017",
                  activebackground="#d4a017", activeforeground="#1b2233",
                  relief="flat", bd=0, padx=24, pady=10).pack(fill="x", pady=(20, 0))

#tabla de lista de enemigos
        #la tabla donde va a estar toda la lista con los enemigos de la torre
        tk.Label(col_centro, text="ENEMIGOS DE LA TORRE",
                 font=("Consolas", 9, "bold"), bg="#232e44", fg="#d4a017").pack(pady=(16, 6))

        lista_enemigos = [
            ("Orco Gigante",      "piel gruesa que absorbe el daño"),
            ("Duende Maldito",    "tiene maldiciones que potencian sus ataques"),
            ("Troll",             "envenena con su hedor"),
            ("Esqueleto Gigante", "se debilita con cada golpe"),
            ("Vampiro",           "roba vida con cada ataque"),
            ("Dragon Pequeño",    "escupe fuego en cargas"),
            ("Brujo Maldito",     "hace hechizos oscuros"),
            ("Lobo Gigante",      "puede atacar dos veces"),
            ("Demonio del Fuego", "aura de calor constante"),
            ("Caballero Oscuro",  "bloquea parte del daño"),
            ("Golem de Piedra",   "dureza que se va degradando"),
        ]
        for nom, desc in lista_enemigos:
            fila = tk.Frame(col_centro, bg="#2a3750")
            fila.pack(fill="x", padx=12, pady=2)
            tk.Label(fila, text=f"  {nom}", font=("Trebuchet MS", 9, "bold"),
                     bg="#2a3750", fg="#e8eaf0", width=20, anchor="w").pack(side="left", pady=3)
            tk.Label(fila, text=desc, font=("Consolas", 8),
                     bg="#2a3750", fg="#8892a4").pack(side="left", padx=8)

#tabla top 5
        #y la ultima columna que es donde se van a guardar todos los puntajes de los jugadores
        tk.Label(col_der, text="TOP 5", font=("Consolas", 10, "bold"),
                 bg="#232e44", fg="#d4a017").pack(pady=(0, 10))

        puntajes = cargar_puntajes()
        if not puntajes:
            tk.Label(col_der, text="sin registros todavia",
                     font=("Consolas", 9), bg="#232e44", fg="#8892a4").pack()
        else:
            numeros = ["1.", "2.", "3.", "4.", "5."]
            i = 0
            for p in puntajes[:5]:
                fila = tk.Frame(col_der, bg="#2a3750")
                fila.pack(fill="x", pady=2)
                tk.Label(fila, text=f" {numeros[i]}", font=("Consolas", 11),
                         bg="#2a3750", fg="#d4a017").pack(side="left", pady=4)
                tk.Label(fila, text=p["nombre"], font=("Trebuchet MS", 9),
                         bg="#2a3750", fg="#e8eaf0").pack(side="left", padx=4)
                tk.Label(fila, text=f"{p['puntos']} pts", font=("Consolas", 9, "bold"),
                         bg="#2a3750", fg="#d4a017").pack(side="right", padx=6)
                i += 1

    def iniciar(self):
        nombre = self.campo_nombre.get().strip()
        if nombre == "":
            nombre = "heroe"
        clase = self.clase_elegida.get()
        if clase == "guerrero":
            jugador = Guerrero.crear_guerrero_base(nombre)
        elif clase == "mago":
            jugador = Mago.crear_mago_base(nombre)
        else:
            jugador = Arquero.crear_arquero_base(nombre)
        pocion_inicial = Item("pocion", "curacion", 70)
        jugador.inventario.agregar(pocion_inicial)
        self.al_iniciar(jugador)

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def destruir(self):
        self.frame.destroy()

#pantalla de juego

class PantallaJuego:
    def __init__(self, ventana, jugador, al_terminar):
        self.ventana = ventana
        self.jugador = jugador
        self.al_terminar = al_terminar
        self.torre = crear_torre()
        self.numero_enemigo = 0
        self.enemigo = None
        self.puntos = 0
        self.turno = 1
        self.botones = []
        self.frame = tk.Frame(ventana, bg="#1b2233")
        self.construir()
        self.cargar_enemigo()

    def construir(self):
        poner_fondo(self.frame)

#barra de arriba
        barra = tk.Frame(self.frame, bg="#232e44")
        barra.pack(fill="x", pady=6)

        self.progreso = tk.Label(barra, text="", font=("Consolas", 10),
                                     bg="#232e44", fg="#8892a4")
        self.progreso.pack(side="left", padx=16)

        self.turno_lbl = tk.Label(barra, text="Turno 1", font=("Consolas", 10),
                                  bg="#232e44", fg="#8892a4")
        self.turno_lbl.pack(side="left", padx=16)

        self.puntos_lbl = tk.Label(barra, text="Puntos: 0",
                                   font=("Trebuchet MS", 11, "bold"),
                                   bg="#232e44", fg="#d4a017")
        self.puntos_lbl.pack(side="right", padx=16)

#area principal
        area = tk.Frame(self.frame, bg="#1b2233")
        area.pack(fill="both", expand=True, padx=10, pady=8)

#panel izquierdo
        panel_izq = tk.Frame(area, bg="#1b2233")
        panel_izq.pack(side="left", fill="y", padx=(0, 8))

#stats jugador
        frame_jugador = tk.LabelFrame(panel_izq, text=" HEROE ",
                                      font=("Consolas", 8, "bold"),
                                      bg="#232e44", fg="#3dbf7a",
                                      relief="flat", bd=3, padx=10, pady=8)
        frame_jugador.pack(fill="x", pady=(0, 6))

        self.j_nombre = tk.Label(frame_jugador, text="",
                                     font=("Trebuchet MS", 12, "bold"),
                                     bg="#232e44", fg="#e8eaf0")
        self.j_nombre.pack(anchor="w")

        self.j_barra = tk.Label(frame_jugador, text="",
                                    font=("Consolas", 8), bg="#232e44", fg="#3dbf7a")
        self.j_barra.pack(anchor="w", pady=2)

        self.j_vida = tk.Label(frame_jugador, text="",
                                   font=("Consolas", 9), bg="#232e44", fg="#e8eaf0")
        self.j_vida.pack(anchor="w")

        self.j_estadisticas = tk.Label(frame_jugador, text="",
                                    font=("Consolas", 8), bg="#232e44", fg="#d4a017")
        self.j_estadisticas.pack(anchor="w")

        self.j_inv = tk.Label(frame_jugador, text="",
                                  font=("Consolas", 8), bg="#232e44", fg="#8892a4")
        self.j_inv.pack(anchor="w")

#stats enemigo
        frame_enemigo = tk.LabelFrame(panel_izq, text=" ENEMIGO ",
                                      font=("Consolas", 8, "bold"),
                                      bg="#232e44", fg="#e84040",
                                      relief="flat", bd=3, padx=10, pady=8)
        frame_enemigo.pack(fill="x")

        self.e_nombre = tk.Label(frame_enemigo, text="",
                                     font=("Trebuchet MS", 12, "bold"),
                                     bg="#232e44", fg="#e8eaf0")
        self.e_nombre.pack(anchor="w")

        self.e_barra = tk.Label(frame_enemigo, text="",
                                    font=("Consolas", 8), bg="#232e44", fg="#e84040")
        self.e_barra.pack(anchor="w", pady=2)

        self.e_vida = tk.Label(frame_enemigo, text="",
                                   font=("Consolas", 9), bg="#232e44", fg="#e8eaf0")
        self.e_vida.pack(anchor="w")

        self.e_estadisticas = tk.Label(frame_enemigo, text="",
                                   font=("Consolas", 8), bg="#232e44", fg="#8892a4")
        self.e_estadisticas.pack(anchor="w")

#botones de accion
        contenedor_botones = tk.Frame(panel_izq, bg="#232e44")
        contenedor_botones.pack(fill="x", pady=(10, 0))

        tk.Label(contenedor_botones, text="ACCIONES",
                 font=("Consolas", 9, "bold"), bg="#232e44", fg="#8892a4").pack(pady=(10, 6))

        self.area_botones = tk.Frame(contenedor_botones, bg="#232e44")
        self.area_botones.pack(fill="x", padx=12, pady=(0, 12))

#log derecho
        panel_der = tk.Frame(area, bg="#1b2233")
        panel_der.pack(side="right", fill="both", expand=True)

        tk.Label(panel_der, text="ARENA DE BATALLA",
                 font=("Consolas", 9, "bold"), bg="#1b2233", fg="#d4a017").pack(anchor="w")

        fondo_log = tk.Frame(panel_der, bg="#161e2e", bd=1, relief="flat")
        fondo_log.pack(fill="both", expand=True, pady=(4, 0))

        self.log = tk.Text(fondo_log, font=("Consolas", 9),
                           bg="#161e2e", fg="#e8eaf0",
                           state="disabled", relief="flat", wrap="word", bd=6)
        self.log.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(fondo_log, command=self.log.yview,
                              bg="#161e2e", troughcolor="#161e2e")
        scroll.pack(side="right", fill="y")
        self.log["yscrollcommand"] = scroll.set

    def cargar_enemigo(self):
        if self.numero_enemigo >= len(self.torre):
            guardar_puntaje(self.jugador.nombre, self.puntos)
            self.al_terminar(self.jugador, self.puntos, gano=True)
            return
        self.enemigo = aplicar_escalado(self.torre[self.numero_enemigo], self.numero_enemigo)
        self.turno = 1
        self.actualizar_pantalla()
        num = self.numero_enemigo + 1
        total = len(self.torre)
        nombre_enemigo = self.enemigo.nombre.upper()
        self.escribir_titulo(f"ENCUENTRO {num}/{total}: {nombre_enemigo}")
        self.escribir_log(f"Nivel {self.enemigo.nivel} - Recompensa: {self.enemigo.recompensa} pts", "#8892a4")
        if self.numero_enemigo > 0:
            self.escribir_log(f"(estadisticas +{self.numero_enemigo * 3}%)", "#8892a4")
        self.dibujar_botones()

    def dibujar_botones(self):
        for boton in self.botones:
            boton.destroy()
        self.botones = []

        if isinstance(self.jugador, Guerrero):
            textos = [("atacar con espada", self.accion_atacar),
                      ("activar Furia",     self.accion_especial)]
        elif isinstance(self.jugador, Mago):
            textos = [("lanzar hechizo", self.accion_atacar),
                      ("curarse",        self.accion_especial)]
        else:
            textos = [("disparar flecha", self.accion_atacar),
                      ("doble disparo",   self.accion_especial)]

#boton de atacar
        boton_atacar = tk.Button(self.area_botones, text=textos[0][0], command=textos[0][1],
                                  font=("Consolas", 10), bg="#2a3750", fg="#e8eaf0",
                                  activebackground="#d4a017", activeforeground="#1b2233",
                                  relief="flat", bd=0, padx=10, pady=8)
        boton_atacar.pack(fill="x", padx=4, pady=3)
        self.botones.append(boton_atacar)

#boton de habilidad especial
        boton_especial = tk.Button(self.area_botones, text=textos[1][0], command=textos[1][1],
                                    font=("Consolas", 10), bg="#2a3750", fg="#e8eaf0",
                                    activebackground="#d4a017", activeforeground="#1b2233",
                                    relief="flat", bd=0, padx=10, pady=8)
        boton_especial.pack(fill="x", padx=4, pady=3)
        self.botones.append(boton_especial)

#boton de usar objeto
        boton_item = tk.Button(self.area_botones, text="Usar objeto", command=self.accion_item,
                                font=("Consolas", 10), bg="#2a3750", fg="#e8eaf0",
                                activebackground="#d4a017", activeforeground="#1b2233",
                                relief="flat", bd=0, padx=10, pady=8)
        boton_item.pack(fill="x", padx=4, pady=3)
        self.botones.append(boton_item)

    def deshabilitar_botones(self):
        for boton in self.botones:
            boton.config(state="disabled")

    def accion_atacar(self):
        self.deshabilitar_botones()
        if isinstance(self.jugador, Guerrero):
            if self.jugador.vida <= self.jugador.vida_max * 0.3:
                self.jugador.furia = True
        self.escribir_log(f"{self.jugador.nombre} ataca a {self.enemigo.nombre}")
        self.jugador.atacar(self.enemigo)
        self.actualizar_pantalla()
        if not self.enemigo.esta_vivo():
            self.on_enemigo_muerto()
            return
        self.ventana.after(650, self.turno_enemigo)

    def accion_especial(self):
        self.deshabilitar_botones()
        if isinstance(self.jugador, Guerrero):
            if self.jugador.vida <= self.jugador.vida_max * 0.3:
                self.jugador.furia = True
        self.escribir_log(f"{self.jugador.nombre} usa su habilidad especial")
        self.jugador.habilidad_especial(self.enemigo)
        self.actualizar_pantalla()
        if not self.enemigo.esta_vivo():
            self.on_enemigo_muerto()
            return
        self.ventana.after(650, self.turno_enemigo)

    def usar_item(self, indice):
        obj = self.jugador.inventario.usar(indice)
        if obj:
            self.jugador.vida += obj.valor
            self.escribir_log(f"Usaste {obj} - Vida: {self.jugador.vida}/{self.jugador.vida_max}", "#3dbf7a")
        self.actualizar_pantalla()
        self.ventana.after(650, self.turno_enemigo)

    def accion_item(self):
        self.deshabilitar_botones()
        items_disponibles = self.jugador.inventario.listar()
        if not items_disponibles:
            self.escribir_log("no tienes objetos, turno perdido", "#8892a4")
            self.ventana.after(650, self.turno_enemigo)
            return
        self.usar_item(0)

    def turno_enemigo(self):
        vida_antes = self.jugador.vida
        self.escribir_log(f"{self.enemigo.nombre} ataca a {self.jugador.nombre}", "#e84040")
        self.enemigo.atacar(self.jugador)
        dano = vida_antes - self.jugador.vida
        if dano > 0:
            self.escribir_log(f"recibes {dano} de daño", "#e84040")
        self.turno += 1
        self.turno_lbl.config(text=f"Turno {self.turno}")
        self.actualizar_pantalla()
        if not self.jugador.esta_vivo():
            guardar_puntaje(self.jugador.nombre, self.puntos)
            self.al_terminar(self.jugador, self.puntos, gano=False)
            return
        self.dibujar_botones()

    def on_enemigo_muerto(self):
        recompensa = self.enemigo.recompensa
        self.puntos += recompensa
        self.puntos_lbl.config(text=f"Puntos: {self.puntos}")
        self.escribir_log(f"derrotaste a {self.enemigo.nombre}  +{recompensa} pts", "#3dbf7a")
        if (self.numero_enemigo + 1) % 2 == 0:
            nueva_pocion = Item("pocion", "curacion", 70)
            ok = self.jugador.inventario.agregar(nueva_pocion)
            if ok:
                self.escribir_log("obtienes una pocion de curacion (+70)", "#3dbf7a")
            else:
                self.escribir_log("inventario lleno, la pocion se perdio", "#8892a4")
        self.numero_enemigo += 1
        self.ventana.after(900, self.cargar_enemigo)

    def actualizar_pantalla(self):
        j = self.jugador
        e = self.enemigo

        self.j_nombre.config(text=j.nombre)
        self.j_vida.config(text=f"Vida: {j.vida} / {j.vida_max}")

        if isinstance(j, Guerrero):
            if j.furia:
                self.j_estadisticas.config(text=f"Armadura: {j.armadura}  Furia: SI")
            else:
                self.j_estadisticas.config(text=f"Armadura: {j.armadura}  Furia: no")
        elif isinstance(j, Mago):
            self.j_estadisticas.config(text=f"Mana: {j.mana}")
        else:
            self.j_estadisticas.config(text=f"Flechas: {j.flechas}")

        inv = str(j.inventario)
        if inv == "inventario vacio":
            self.j_inv.config(text="")
        else:
            self.j_inv.config(text=f"Inv: {inv}")

        self.e_nombre.config(text=e.nombre)
        self.e_vida.config(text=f"Vida: {e.vida} / {e.vida_max}")
        self.e_estadisticas.config(text=f"Nivel {e.nivel} - Recompensa: {e.recompensa} pts")
        self.progreso.config(text=f"Enemigo {self.numero_enemigo + 1} / {len(self.torre)}")

#barra de vida jugador
        bloques_j = int((j.vida / j.vida_max) * 20)
        if j.vida > j.vida_max * 0.6:
            color_j = "#3dbf7a" #verde
        elif j.vida > j.vida_max * 0.3:
            color_j = "#e8a020" #naranja
        else:
            color_j = "#e84040" #rojo
        self.j_barra.config(text="█" * bloques_j + "░" * (20 - bloques_j), fg=color_j)

#barra de vida enemigo
        bloques_e = int((e.vida / e.vida_max) * 20)
        if e.vida > e.vida_max * 0.6:
            color_e = "#3dbf7a" #verde
        elif e.vida > e.vida_max * 0.3:
            color_e = "#e8a020" #naranja
        else:
            color_e = "#e84040" #rojo
        self.e_barra.config(text="█" * bloques_e + "░" * (20 - bloques_e), fg=color_e)

    def escribir_titulo(self, texto):
        color = "#d4a017" #dorado
        self.log.tag_config(color, foreground=color, font=("Consolas", 9, "bold"))
        self.log.config(state="normal")
        self.log.insert("end", f"\n{'─' * 42}\n{texto}\n{'─' * 42}\n", color)
        self.log.see("end")
        self.log.config(state="disabled")

    def escribir_log(self, texto, color="#e8eaf0"):
        self.log.tag_config(color, foreground=color)
        self.log.config(state="normal")
        self.log.insert("end", texto + "\n", color)
        self.log.see("end")
        self.log.config(state="disabled")

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def destruir(self):
        self.frame.destroy()

#pantalla de fin

class PantallaFin:
    def __init__(self, ventana, jugador, puntos, gano, al_reiniciar):
        self.ventana = ventana
        self.frame = tk.Frame(ventana, bg="#1b2233")
        self.construir(jugador, puntos, gano, al_reiniciar)

    def construir(self, jugador, puntos, gano, al_reiniciar):
        poner_fondo(self.frame)

        if gano:
            titulo = "VICTORIA"
            sub = "ganaste toda la torre"
            color = "#3dbf7a"
        else:
            titulo = "DERROTA"
            sub = "la torre quedo sin conquistar"
            color = "#e84040"

        tk.Label(self.frame, text=titulo, font=("Trebuchet MS", 30, "bold"),
                 bg="#1b2233", fg=color).pack(pady=(50, 0))

        tk.Label(self.frame, text=sub, font=("Consolas", 10),
                 bg="#1b2233", fg="#8892a4").pack(pady=2)

        tk.Label(self.frame, text=f"{jugador.nombre}   -   {puntos} puntos",
                 font=("Trebuchet MS", 14), bg="#1b2233", fg="#e8eaf0").pack(pady=20)

        tk.Label(self.frame, text="TOP 5", font=("Consolas", 11, "bold"),
                 bg="#1b2233", fg="#d4a017").pack()

        cont = tk.Frame(self.frame, bg="#232e44")
        cont.pack(padx=200, pady=10, fill="x")

        puntajes = cargar_puntajes()
        if not puntajes:
            tk.Label(cont, text="sin registros todavia", font=("Consolas", 9),
                     bg="#232e44", fg="#8892a4").pack(pady=10)
        else:
            i = 0
            for p in puntajes[:5]:
                fila = tk.Frame(cont, bg="#2a3750")
                fila.pack(fill="x", padx=16, pady=3)
                tk.Label(fila, text=f" {i+1}.", font=("Consolas", 12),
                         bg="#2a3750", fg="#d4a017").pack(side="left", pady=5)
                tk.Label(fila, text=p["nombre"], font=("Trebuchet MS", 11),
                         bg="#2a3750", fg="#e8eaf0").pack(side="left", padx=8)
                tk.Label(fila, text=f"{p['puntos']} pts",
                         font=("Consolas", 10, "bold"),
                         bg="#2a3750", fg="#d4a017").pack(side="right", padx=12)
                i += 1

        tk.Button(self.frame, text="JUGAR OTRA VEZ", command=al_reiniciar,
                  font=("Trebuchet MS", 11, "bold"),
                  bg="#2e4070", fg="#d4a017",
                  activebackground="#d4a017", activeforeground="#1b2233",
                  relief="flat", bd=0, padx=24, pady=10).pack()

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def destruir(self):
        self.frame.destroy()

#ventana principal

ventana = tk.Tk()
ventana.title("Arena de Batalla")
ventana.resizable(False, False)
ventana.configure(bg="#1b2233")
ventana.geometry("980x680")

pantalla_actual = None

def ir_inicio():
    global pantalla_actual
    if pantalla_actual:
        pantalla_actual.destruir()
    pantalla_actual = PantallaInicio(ventana, ir_juego)
    pantalla_actual.mostrar()

def ir_juego(jugador):
    global pantalla_actual
    if pantalla_actual:
        pantalla_actual.destruir()
    pantalla_actual = PantallaJuego(ventana, jugador, ir_fin)
    pantalla_actual.mostrar()

def ir_fin(jugador, puntos, gano):
    global pantalla_actual
    if pantalla_actual:
        pantalla_actual.destruir()
    pantalla_actual = PantallaFin(ventana, jugador, puntos, gano, ir_inicio)
    pantalla_actual.mostrar()

ir_inicio()
ventana.mainloop()
