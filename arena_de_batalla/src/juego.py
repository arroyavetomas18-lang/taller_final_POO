#Tomás Arroyave Celis - Jaleth Yaled Campuzano Gutierrez
from abc import ABC, abstractmethod
from typing import Optional
import random
import json
import os

#clase de item para la composicion
class Item:
    def __init__(self, nombre: str, tipo: str, valor: int) -> None:
        self.nombre: str = nombre
        self.tipo: str = tipo
        self.valor: int = valor

    def __str__(self) -> str:
        return self.tipo + " " + self.nombre + " (+" + str(self.valor) + ")"

    def __repr__(self) -> str:
        return "Item(nombre=" + repr(self.nombre) + ", tipo=" + repr(self.tipo) + ", valor=" + str(self.valor) + ")"

#clase de inventario para la composicion tambien
class Inventario:
    def __init__(self, capacidad: int = 3) -> None:
        self.__items: list = []
        self.__capacidad: int = capacidad

    def agregar(self, item: Item) -> bool:
        if len(self.__items) < self.__capacidad:
            self.__items.append(item)
            return True
        return False

    def usar(self, indice: int) -> Optional[Item]:
        if 0 <= indice < len(self.__items):
            return self.__items.pop(indice)
        return None

    def listar(self) -> list:
        return list(self.__items)

    def __len__(self) -> int:
        return len(self.__items)

    def __str__(self) -> str:
        if not self.__items:
            return "inventario vacio"
        return ", ".join(str(i) for i in self.__items)

    def __repr__(self) -> str:
        return "Inventario(items=" + repr(self.__items) + ")"

    def __contains__(self, nombre: str) -> bool:
        return any(i.nombre == nombre for i in self.__items)


#clase padre abstracta
class Personaje(ABC):
    __contador: int = 0

    def __init__(self, nombre: str, vida: int) -> None:
        Personaje.__contador += 1
        self.__nombre: str = nombre
        self.__vida: int = vida
        self.__vida_max: int = vida
        self.ataque_base: int = random.randint(10, 30)

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def vida(self) -> int:
        return self.__vida

#setter de vida para que no se vaya a negativo ni pase el limite
    @vida.setter
    def vida(self, valor: int) -> None:
        if valor < 0:
            valor = 0
        if valor > self.__vida_max:
            valor = self.__vida_max
        self.__vida = valor

#para acceder a la vida maxima
    @property
    def vida_max(self) -> int:
        return self.__vida_max

    @abstractmethod
    def atacar(self, objetivo: 'Personaje') -> int:
        pass

    @abstractmethod
    def habilidad_especial(self, objetivo: 'Personaje') -> None:
        pass

    @classmethod
    def total_personajes(cls) -> int:
        return cls.__contador

    @staticmethod
    def calcular_nivel_vida(vida: int, vida_max: int) -> str:
        porcentaje: float = (vida / vida_max) * 100
        if porcentaje > 60:
            return "bien"
        elif porcentaje > 30:
            return "moderado"
        else:
            return "critico"

    def esta_vivo(self) -> bool:
        return self.__vida > 0

    def recibir_daño(self, dmg: int) -> None:
        self.vida = self.__vida - dmg
        print(self.__nombre + " recibe " + str(dmg) + " de daño, vida restante: " + str(self.__vida) + " - " + str(self.__vida_max))

    def __str__(self) -> str:
        return self.__nombre + " (vida: " + str(self.__vida) + "/" + str(self.__vida_max) + ")"

    def __repr__(self) -> str:
        return type(self).__name__ + "(nombre=" + repr(self.__nombre) + ", vida=" + str(self.__vida) + ")"


class Guerrero(Personaje):
    def __init__(self, nombre: str, vida: int) -> None:
        super().__init__(nombre, vida)
        self.armadura: int = random.randint(10, 30)
        self.furia: bool = False
        self.inventario: Inventario = Inventario()

    def atacar(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + random.randint(10, 30)
        if self.furia:
            daño = daño * 2
            print(self.nombre + " ataca con el efecto de Furia usando la espada")
        else:
            print(self.nombre + " ataca con la espada")
        objetivo.recibir_daño(daño)
        return daño

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.furia = True
        print(self.nombre + " activa la furia manualmente")
        self.atacar(objetivo)

    def estado(self) -> None:
        print(self.nombre + " tiene " + str(self.vida) + " de vida y " + str(self.armadura) + " de armadura")

    def __repr__(self) -> str:
        return "Guerrero(nombre=" + repr(self.nombre) + ", vida=" + str(self.vida) + ", armadura=" + str(self.armadura) + ")"

    @classmethod
    def crear_guerrero_base(cls, nombre: str) -> 'Guerrero':
        return cls(nombre, 100)


class Mago(Personaje):
    def __init__(self, nombre: str, vida: int) -> None:
        super().__init__(nombre, vida)
        self.mana: int = random.randint(10, 30)
        self.hechizo: str = "bola de Fuego"
        self.inventario: Inventario = Inventario()

    def atacar(self, objetivo: Personaje) -> int:
        if self.mana >= 20:
            daño: int = self.ataque_base + random.randint(10, 30)
            self.mana -= 20
            print(self.nombre + " tira una " + self.hechizo + " (mana restante: " + str(self.mana) + ")")
            objetivo.recibir_daño(daño)
            return daño
        else:
            daño = self.ataque_base
            print(self.nombre + " no le queda mana, hizo un golpe debil")
            objetivo.recibir_daño(daño)
            return daño

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.curar()

    def curar(self) -> int:
        curacion: int = random.randint(50, 60)
        self.vida = self.vida + curacion
        print(self.nombre + " se cura " + str(curacion) + " puntos de vida, vida: " + str(self.vida) + " - " + str(self.vida_max))
        return curacion

    def __repr__(self) -> str:
        return "Mago(nombre=" + repr(self.nombre) + ", vida=" + str(self.vida) + ", mana=" + str(self.mana) + ")"

    @classmethod
    def crear_mago_base(cls, nombre: str) -> 'Mago':
        return cls(nombre, 100)


class Arquero(Personaje):
    def __init__(self, nombre: str, vida: int) -> None:
        super().__init__(nombre, vida)
        self.flechas: int = random.randint(10, 30)
        self.inventario: Inventario = Inventario()

    def atacar(self, objetivo: Personaje) -> int:
        if self.flechas <= 0:
            daño: int = self.ataque_base
            print(self.nombre + " no tiene flechas, ataca con su arco en mano")
            objetivo.recibir_daño(daño)
            return daño
        daño = self.ataque_base + random.randint(10, 30)
        self.flechas -= 1
        print(self.nombre + " disparo una flecha (flechas restantes: " + str(self.flechas) + ")")
        objetivo.recibir_daño(daño)
        return daño

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.doble_tiro(objetivo)

    def doble_tiro(self, objetivo: Personaje) -> int:
        print(self.nombre + " uso doble tiro")
        daño1: int = self.atacar(objetivo)
        daño2: int = self.atacar(objetivo)
        return daño1 + daño2

    def __repr__(self) -> str:
        return "Arquero(nombre=" + repr(self.nombre) + ", vida=" + str(self.vida) + ", flechas=" + str(self.flechas) + ")"

    @classmethod
    def crear_arquero_base(cls, nombre: str) -> 'Arquero':
        return cls(nombre, 100)


class Enemigo(Personaje):
    def __init__(self, nombre: str, nivel: int, vida: int) -> None:
        super().__init__(nombre, vida)
        self.nivel: int = nivel
        self.recompensa: int = random.randint(10, 30)

    def atacar(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + random.randint(5, 15)
        print(self.nombre + " ataca salvajemente")
        objetivo.recibir_daño(daño)
        return daño

    def habilidad_especial(self, objetivo: Personaje) -> None:
        print(self.nombre + " usa su habilidad especial")
        self.atacar(objetivo)
        self.atacar(objetivo)

    def estado(self) -> None:
        print(self.nombre + " es nivel " + str(self.nivel) + " y tiene " + str(self.vida) + " de vida")

    def __repr__(self) -> str:
        return "Enemigo(nombre=" + repr(self.nombre) + ", nivel=" + str(self.nivel) + ", vida=" + str(self.vida) + ")"


class OrcoGigante(Enemigo):
    def __init__(self) -> None:
        super().__init__("orco gigante", random.randint(10, 30), 100)
        self.fuerza_bruta: int = random.randint(10, 30)
        self.piel_gruesa: int = random.randint(5, 15)

    def golpe_brutal(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + self.fuerza_bruta
        print(self.nombre + " lanza un golpe con toda su fuerza")
        objetivo.recibir_daño(daño)
        return daño

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.golpe_brutal(objetivo)

    def recibir_daño(self, dmg: int) -> None:
        dmg_reducido: int = max(0, dmg - self.piel_gruesa)
        print(self.nombre + " absorbe " + str(dmg - dmg_reducido) + " de daño con su piel gruesa")
        super().recibir_daño(dmg_reducido)

    def estado(self) -> None:
        super().estado()
        print("  fuerza bruta: " + str(self.fuerza_bruta) + " | piel gruesa: " + str(self.piel_gruesa))

    def __repr__(self) -> str:
        return "OrcoGigante(vida=" + str(self.vida) + ", fuerza_bruta=" + str(self.fuerza_bruta) + ")"


class DuendeMaldito(Enemigo):
    def __init__(self) -> None:
        super().__init__("duende maldito", random.randint(10, 30), 100)
        self.maldicion_activa: bool = False
        self.cargas_maldicion: int = random.randint(1, 3)

    def maldecir(self, objetivo: Personaje) -> None:
        if self.cargas_maldicion > 0:
            self.cargas_maldicion -= 1
            self.maldicion_activa = True
            print(self.nombre + " lanza una maldicion sobre " + objetivo.nombre + " (cargas restantes: " + str(self.cargas_maldicion) + ")")
        else:
            print(self.nombre + " intenta maldecir pero no tiene mas cargas")

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.maldecir(objetivo)

    def atacar(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + random.randint(5, 15)
        if self.maldicion_activa:
            daño = int(daño * 1.5)
            print(self.nombre + " ataca aprovechando la maldicion activa")
        else:
            print(self.nombre + " ataca con sus garras")
        objetivo.recibir_daño(daño)
        return daño

    def estado(self) -> None:
        super().estado()
        print("  maldicion activa: " + str(self.maldicion_activa) + " | cargas: " + str(self.cargas_maldicion))

    def __repr__(self) -> str:
        return "DuendeMaldito(vida=" + str(self.vida) + ", cargas=" + str(self.cargas_maldicion) + ")"


class Troll(Enemigo):
    def __init__(self) -> None:
        super().__init__("troll", random.randint(10, 30), 100)
        self.olor_putrefacto: int = random.randint(5, 15)

    def envenenar(self, objetivo: Personaje) -> None:
        print(self.nombre + " saca un olor putrefacto que envenena a " + objetivo.nombre)
        objetivo.recibir_daño(self.olor_putrefacto)

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.envenenar(objetivo)

    def atacar(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + random.randint(5, 15)
        print(self.nombre + " golpea con su maza")
        objetivo.recibir_daño(daño)
        self.envenenar(objetivo)
        return daño + self.olor_putrefacto

    def estado(self) -> None:
        super().estado()
        print("  olor putrefacto: " + str(self.olor_putrefacto))

    def __repr__(self) -> str:
        return "Troll(vida=" + str(self.vida) + ", olor_putrefacto=" + str(self.olor_putrefacto) + ")"


class EsqueletoGigante(Enemigo):
    def __init__(self) -> None:
        super().__init__("esqueleto gigante", random.randint(10, 30), 100)
        self.huesos_rotos: int = 0
        self.resistencia_magica: int = random.randint(5, 15)

    def atacar(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + random.randint(5, 15)
        print(self.nombre + " lanza su lanza de hueso")
        objetivo.recibir_daño(daño)
        return daño

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.atacar(objetivo)
        self.atacar(objetivo)

    def recibir_daño(self, dmg: int) -> None:
        self.huesos_rotos += 1
        if self.huesos_rotos > 3:
            print(self.nombre + " tiene varios huesos rotos, esta debilitado")
        super().recibir_daño(dmg)

    def estado(self) -> None:
        super().estado()
        print("  huesos rotos: " + str(self.huesos_rotos) + " | resistencia magica: " + str(self.resistencia_magica))

    def __repr__(self) -> str:
        return "EsqueletoGigante(vida=" + str(self.vida) + ", huesos_rotos=" + str(self.huesos_rotos) + ")"


class Vampiro(Enemigo):
    def __init__(self) -> None:
        super().__init__("vampiro", random.randint(10, 30), 100)
        self.sed_de_sangre: int = random.randint(5, 15)
        self.forma_murcielago: bool = False

    def drenar_vida(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + random.randint(5, 15)
        objetivo.recibir_daño(daño)
        self.vida = self.vida + self.sed_de_sangre
        print(self.nombre + " drena " + str(self.sed_de_sangre) + " de vida, vida propia: " + str(self.vida))
        return daño

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.drenar_vida(objetivo)

    def atacar(self, objetivo: Personaje) -> int:
        print(self.nombre + " ataca con sus colmillos")
        return self.drenar_vida(objetivo)

    def estado(self) -> None:
        super().estado()
        print("  sed de sangre: " + str(self.sed_de_sangre) + " | forma murcielago: " + str(self.forma_murcielago))

    def __repr__(self) -> str:
        return "Vampiro(vida=" + str(self.vida) + ", sed_de_sangre=" + str(self.sed_de_sangre) + ")"


class DragonPequeño(Enemigo):
    def __init__(self) -> None:
        super().__init__("dragon pequeño", random.randint(10, 30), 100)
        self.cargas_fuego: int = random.randint(2, 5)
        self.escamas: int = random.randint(5, 15)

    def escupir_fuego(self, objetivo: Personaje) -> int:
        if self.cargas_fuego > 0:
            daño: int = self.ataque_base + random.randint(15, 35)
            self.cargas_fuego -= 1
            print(self.nombre + " escupe fuego (cargas restantes: " + str(self.cargas_fuego) + ")")
            objetivo.recibir_daño(daño)
            return daño
        else:
            print(self.nombre + " intenta escupir fuego pero no tiene mas cargas")
            return self.atacar(objetivo)

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.escupir_fuego(objetivo)

    def atacar(self, objetivo: Personaje) -> int:
        if self.cargas_fuego > 0:
            return self.escupir_fuego(objetivo)
        daño: int = self.ataque_base + random.randint(5, 15)
        print(self.nombre + " ataca con sus garras")
        objetivo.recibir_daño(daño)
        return daño

    def estado(self) -> None:
        super().estado()
        print("  cargas de fuego: " + str(self.cargas_fuego) + " | escamas: " + str(self.escamas))

    def __repr__(self) -> str:
        return "DragonPequeño(vida=" + str(self.vida) + ", cargas_fuego=" + str(self.cargas_fuego) + ")"


class BrujoMaldito(Enemigo):
    def __init__(self) -> None:
        super().__init__("brujo maldito", random.randint(10, 30), 100)
        self.mana_oscuro: int = random.randint(10, 30)
        self.hechizo_activo: Optional[str] = None

    def preparar_hechizo(self) -> None:
        if self.mana_oscuro >= 10:
            self.hechizo_activo = "maldicion oscura"
            self.mana_oscuro -= 10
            print(self.nombre + " prepara una " + self.hechizo_activo + " (mana: " + str(self.mana_oscuro) + ")")
        else:
            print(self.nombre + " no tiene mana suficiente para preparar un hechizo")

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.preparar_hechizo()

    def atacar(self, objetivo: Personaje) -> int:
        if self.hechizo_activo:
            daño: int = self.ataque_base + random.randint(15, 35)
            print(self.nombre + " lanza su " + self.hechizo_activo)
            self.hechizo_activo = None
            objetivo.recibir_daño(daño)
            return daño
        else:
            self.preparar_hechizo()
            daño = self.ataque_base
            print(self.nombre + " ataca con su baculo mientras prepara hechizos")
            objetivo.recibir_daño(daño)
            return daño

    def estado(self) -> None:
        super().estado()
        print("  mana oscuro: " + str(self.mana_oscuro) + " | hechizo activo: " + str(self.hechizo_activo))

    def __repr__(self) -> str:
        return "BrujoMaldito(vida=" + str(self.vida) + ", mana_oscuro=" + str(self.mana_oscuro) + ")"


class LoboGigante(Enemigo):
    def __init__(self) -> None:
        super().__init__("lobo gigante", random.randint(10, 30), 100)
        self.velocidad: int = random.randint(5, 15)
        self.manada: int = random.randint(1, 3)

    def aullar(self) -> None:
        bonus: int = random.randint(5, 10)
        self.ataque_base += bonus
        print(self.nombre + " aulla convocando a su manada, ataque aumentado en " + str(bonus))

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.aullar()

    def atacar(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + random.randint(5, 15)
        print(self.nombre + " ataca con sus fauces")
        objetivo.recibir_daño(daño)
        if random.randint(1, 30) <= self.velocidad:
            daño2: int = self.ataque_base + random.randint(5, 15)
            print(self.nombre + " es tan rapido que ataca de nuevo")
            objetivo.recibir_daño(daño2)
            return daño + daño2
        return daño

    def estado(self) -> None:
        super().estado()
        print("  velocidad: " + str(self.velocidad) + " | manada: " + str(self.manada) + " lobos")

    def __repr__(self) -> str:
        return "LoboGigante(vida=" + str(self.vida) + ", velocidad=" + str(self.velocidad) + ")"


class DemonioDelFuego(Enemigo):
    def __init__(self) -> None:
        super().__init__("demonio del fuego", random.randint(10, 30), 100)
        self.calor_infernal: int = random.randint(5, 20)
        self.inmunidad_fuego: bool = True

    def aura_fuego(self, objetivo: Personaje) -> None:
        print(self.nombre + " irradia un calor infernal de " + str(self.calor_infernal))
        objetivo.recibir_daño(self.calor_infernal)

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.aura_fuego(objetivo)

    def atacar(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + random.randint(5, 15)
        print(self.nombre + " golpea con su puño de fuego")
        objetivo.recibir_daño(daño)
        self.aura_fuego(objetivo)
        return daño + self.calor_infernal

    def estado(self) -> None:
        super().estado()
        print("  calor infernal: " + str(self.calor_infernal) + " | inmune al fuego: " + str(self.inmunidad_fuego))

    def __repr__(self) -> str:
        return "DemonioDelFuego(vida=" + str(self.vida) + ", calor_infernal=" + str(self.calor_infernal) + ")"


class CaballeroOscuro(Enemigo):
    def __init__(self) -> None:
        super().__init__("caballero oscuro", random.randint(10, 30), 100)
        self.escudo_oscuro: int = random.randint(5, 20)
        self.golpes_bloqueados: int = 0

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.atacar(objetivo)

    def recibir_daño(self, dmg: int) -> None:
        if self.escudo_oscuro > 0:
            bloqueado: int = min(dmg, self.escudo_oscuro)
            self.golpes_bloqueados += 1
            dmg -= bloqueado
            print(self.nombre + " bloquea " + str(bloqueado) + " de daño con su escudo oscuro (bloqueados: " + str(self.golpes_bloqueados) + ")")
        super().recibir_daño(dmg)

    def atacar(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + random.randint(5, 15)
        print(self.nombre + " ataca con su espada oscura")
        objetivo.recibir_daño(daño)
        return daño

    def estado(self) -> None:
        super().estado()
        print("  escudo oscuro: " + str(self.escudo_oscuro) + " | golpes bloqueados: " + str(self.golpes_bloqueados))

    def __repr__(self) -> str:
        return "CaballeroOscuro(vida=" + str(self.vida) + ", escudo_oscuro=" + str(self.escudo_oscuro) + ")"


class GolemDePiedra(Enemigo):
    def __init__(self) -> None:
        super().__init__("golem de piedra", random.randint(10, 30), 100)
        self.dureza: int = random.randint(5, 20)
        self.grietas: int = 0

    def golpe_tierra(self, objetivo: Personaje) -> int:
        daño: int = self.ataque_base + random.randint(15, 35)
        print(self.nombre + " golpea el suelo causando un temblor")
        objetivo.recibir_daño(daño)
        return daño

    def habilidad_especial(self, objetivo: Personaje) -> None:
        self.golpe_tierra(objetivo)

    def recibir_daño(self, dmg: int) -> None:
        defensa_actual: int = max(0, self.dureza - self.grietas * 2)
        dmg_reducido: int = max(0, dmg - defensa_actual)
        self.grietas += 1
        print(self.nombre + " acumula una grieta (grietas: " + str(self.grietas) + "), defensa actual: " + str(defensa_actual))
        super().recibir_daño(dmg_reducido)

    def estado(self) -> None:
        super().estado()
        print("  dureza: " + str(self.dureza) + " | grietas: " + str(self.grietas))

    def __repr__(self) -> str:
        return "GolemDePiedra(vida=" + str(self.vida) + ", dureza=" + str(self.dureza) + ")"


def crear_torre() -> list:
#coloca los 11 enemigos en orden aleatorio
    enemigos_disponibles: list = [
        OrcoGigante(),
        DuendeMaldito(),
        Troll(),
        EsqueletoGigante(),
        Vampiro(),
        DragonPequeño(),
        BrujoMaldito(),
        LoboGigante(),
        DemonioDelFuego(),
        CaballeroOscuro(),
        GolemDePiedra(),
    ]
    random.shuffle(enemigos_disponibles)
    return enemigos_disponibles


def aplicar_escalado(enemigo: Enemigo, numero_enemigo: int) -> Enemigo:
#va subiendo un 3% las estadisticas del enemigo cada que vaya matando 1
    factor: float = 1.03 ** numero_enemigo
    enemigo.ataque_base = int(enemigo.ataque_base * factor)
#sube los atributos propios de todas las clases
    if isinstance(enemigo, OrcoGigante):
        enemigo.fuerza_bruta = int(enemigo.fuerza_bruta * factor)
        enemigo.piel_gruesa = int(enemigo.piel_gruesa * factor)
    elif isinstance(enemigo, DuendeMaldito):
        enemigo.cargas_maldicion = int(enemigo.cargas_maldicion * factor)
    elif isinstance(enemigo, Troll):
        enemigo.olor_putrefacto = int(enemigo.olor_putrefacto * factor)
    elif isinstance(enemigo, EsqueletoGigante):
        enemigo.resistencia_magica = int(enemigo.resistencia_magica * factor)
    elif isinstance(enemigo, Vampiro):
        enemigo.sed_de_sangre = int(enemigo.sed_de_sangre * factor)
    elif isinstance(enemigo, DragonPequeño):
        enemigo.escamas = int(enemigo.escamas * factor)
    elif isinstance(enemigo, BrujoMaldito):
        enemigo.mana_oscuro = int(enemigo.mana_oscuro * factor)
    elif isinstance(enemigo, LoboGigante):
        enemigo.velocidad = int(enemigo.velocidad * factor)
    elif isinstance(enemigo, DemonioDelFuego):
        enemigo.calor_infernal = int(enemigo.calor_infernal * factor)
    elif isinstance(enemigo, CaballeroOscuro):
        enemigo.escudo_oscuro = int(enemigo.escudo_oscuro * factor)
    elif isinstance(enemigo, GolemDePiedra):
        enemigo.dureza = int(enemigo.dureza * factor)
    return enemigo


ARCHIVO_PUNTAJES: str = "puntajes.json"

def guardar_puntaje(nombre: str, puntos: int) -> None:
    if os.path.exists(ARCHIVO_PUNTAJES):
        with open(ARCHIVO_PUNTAJES, "r") as f:
            puntajes: list = json.load(f)
    else:
        puntajes = []
    puntajes.append({"nombre": nombre, "puntos": puntos})
    puntajes = sorted(puntajes, key=lambda x: x["puntos"], reverse=True)
    with open(ARCHIVO_PUNTAJES, "w") as f:
        json.dump(puntajes, f, indent=2)


def mostrar_top5() -> None:
    if not os.path.exists(ARCHIVO_PUNTAJES):
        print("aun no hay puntajes guardados")
        return
    with open(ARCHIVO_PUNTAJES, "r") as f:
        puntajes: list = json.load(f)
    if not puntajes:
        print("aun no hay puntajes guardados")
        return
    top5: list = puntajes[:5]
    puntaje_max: int = top5[0]["puntos"] if top5[0]["puntos"] > 0 else 1
    print("-----------")
    print("top 5 mejores puntajes")
    print("-----------")
    for i, entrada in enumerate(top5):
        porcentaje: int = round((entrada["puntos"] / puntaje_max) * 100)
        print(str(i + 1) + ". " + entrada["nombre"] + " - " + str(entrada["puntos"]) + " pts  " + str(porcentaje) + "%")
    print("-----------")
