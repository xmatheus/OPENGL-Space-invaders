from Particula import Particula


class Asteroide(Particula):
    def __init__(self, x=0, z=0, radius=0.8, velocidade=0.1):
        super().__init__(x, z, radius, 25, True, velocidade)

    def anda(self):
        self.up = 1

    def volta(self):
        self.down = 1

    def minus(self, v2):
        rx = self.px - v2.px
        ry = self.py - v2.py
        rz = self.pz - v2.pz
        return rx, ry, rz

    def distanceSquared(self, v2):
        rx, ry, rz = self.minus(v2)
        return self.dotProduct(rx, ry, rz)

    def dotProduct(self, rx, ry, rz):
        return rx * rx + ry * ry + rz * rz

    def doesItCollide(self, s2):
        rr = (self.radius * self.radius) * 8
        return self.distanceSquared(s2) < rr
