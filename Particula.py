import uuid
import numpy as np
import random

GRAVIDADE = 0.1
VOLANTE = 20.0
PULO = 1.5
RESISTENCIA = 1.4
F_RESISTENCIA = 0.2
F_RESISTENCIA_AR = 0.05


class Particula:

    vx = vy = vz = 0.0
    px = py = pz = 0.0
    yaw = pitch = roll = 0.0
    dir_y = rx = rz = 0.0
    altura = space = pulo = up = down = life = radius = frente = 0
    id = ''

    def __init__(self, x=0, z=0, radius=0.05, altura=25, pt=True, velocidade=0.1):
        self.id = uuid.uuid4()
        self.altura = altura
        self.px = x
        self.pz = z
        self.radius = radius
        self.pt = pt
        self.VELOCIDADE = velocidade

    def atualiza_bola(self):
        self.life += 0.5
        self.px += self.vx
        self.py += self.vy
        self.pz += self.vz

        if(not (abs(self.px) <= 25.0)):
            self.px -= self.vx

        if(not (abs(self.pz) <= 65.0)):
            self.pz -= self.vz

        if(self.py > self.altura):
            self.py = self.altura
            # self.space = 0
            self.down = 0
            self.up = 0
        elif(self.pt and self.py < 0.0):
            self.py = 0.0
            self.vy = 0.0
            self.down = 0
            self.up = 0

    def calcula_velocidade(self):
        if(self.py == 0.0):
            if(self.up):
                self.vx += np.sin(self.yaw * 3.14159/180.0)*self.VELOCIDADE
                self.vz += np.cos(self.yaw * 3.14159/180.0)*self.VELOCIDADE
                self.frente = 1
            elif(self.down or self.down):
                self.vx += - np.sin(self.yaw * 3.14159/180.0)*self.VELOCIDADE
                self.vz += - np.cos(self.yaw * 3.14159/180.0)*self.VELOCIDADE
                self.frente = 0

            self.rx = (pow(RESISTENCIA, abs(self.vx))-1.0)*F_RESISTENCIA
            self.rz = (pow(RESISTENCIA, abs(self.vz))-1.0)*F_RESISTENCIA
        else:
            self.rx = (pow(RESISTENCIA, abs(self.vx))-1.0)*F_RESISTENCIA_AR
            self.rz = (pow(RESISTENCIA, abs(self.vz))-1.0)*F_RESISTENCIA_AR

        if(self.vx > self.rx):
            self.vx -= self.rx
        elif(self.vx < -self.rx):
            self.vx += self.rx
        elif(abs(self.vz) < self.rx):
            if(abs(self.vx) > 0):
                printf("Parou\n")
                self.vx = 0.0
                self.vz = 0.0

        if(self.vz > self.rz):
            self.vz -= self.rz
        elif(self.vz < -self.rz):
            self.vz += self.rz
        elif(abs(self.vx) < self.rz):
            if(abs(self.vz) > 0):
                printf("Parou\n")
                self.vz = 0.0
                self.vx = 0.0

        if(self.frente):
            self.pitch += 10*np.sqrt(pow(self.vx, 2)+pow(self.vz, 2))
        else:
            self.pitch -= 10*np.sqrt(pow(self.vx, 2)+pow(self.vz, 2))

        if((self.space) and not (self.pulo)):
            self.vy = PULO
            self.pulo = 1
        elif((not self.space) and (self.pulo)):
            if(self.vy > PULO/2):
                self.vy = PULO/2
                self.pulo = 0
            else:
                self.pulo = 0

        self.vy -= GRAVIDADE
