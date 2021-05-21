from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
from PIL import Image
import random

from Asteroide import Asteroide
from Particula import Particula

T = 0
T2 = 0
T3 = 0
XMove = 0
COUNT = 0.5
XMoveFlag = 0.1
width = 600
height = 600

light_position = [0.0, 5.0, 5.0, 1.0]
light_position2 = [0.0, 6.0, -5.0, 1.0]

amb_light = [0.3, 0.3, 0.3, 1.0]
diffuse = [0.9, 0.9, 0.9, 1.0]
specular = [1.0, 1.0, 1.0, 1.0]
attenuation_quad = 0.0001
attenuation_linear = 0.01

ouro_amb = [0.24725, 0.1995, 0.0745, 1.0]
ouro_dif = [0.75164, 0.60648, 0.22648, 1.0]
ouro_spe = [0.628281, 0.555802, 0.366065, 1.0]
ouro_shi = 0.4*128.0

chrome_amb = [0.25, 0.25, 0.25, 1.0]
chrome_dif = [0.4, 0.4, 0.4, 1.0]
chrome_spe = [0.774597, 0.774597, 0.774597, 1.0]
chrome_shi = 0.6*128.0

rubi_amb = [0.1745, 0.01175, 0.01175, 1.0]
rubi_dif = [0.61424, 0.04136, 0.04136, 1.0]
rubi_spe = [0.727811, 0.626959, 0.626959, 1.0]
rubi_shi = 0.6*128.0

silver_amb = [0.19225, 0.19225, 0.19225, 1.0]
silver_dif = [0.50754, 0.50754, 0.50754, 1.0]
silver_spe = [0.508273, 0.508273, 0.508273, 1.0]
silver_shi = 0.4*128.0

obsidian_amb = [0.05375, 0.05, 0.06625, 1.0]
obsidian_dif = [0.18275, 0.17, 0.22525, 1.0]
obsidian_spe = [0.332741, 0.328634, 0.346435, 1.0]
obsidian_shi = 0.3*128.0

pneu_ID = 0
asteroides = []
particulas = []
bullets = []


class MyParticulas(Particula):
    def __init__(self, x, z, radius=0.1):

        nx = random.randint(round(x-3), round(x+3))
        nz = random.randint(round(z-3), round(z+3))

        super().__init__(nx, nz, radius, altura=random.randint(-3, 4), pt=False)
        self.yaw = random.randint(0, 360)
        if(random.randint(1, 2) % 2 == 0):
            self.down = 1
        else:
            self.up = 1

        self.space = 1


def createExplosion(bola):
    for i in range(300):
        pt = MyParticulas(bola.px, bola.pz,
                          round(random.uniform(0.01, 0.2), 2))
        particulas.append(pt)


def genAsteroide():
    flag = True
    flagGen = False

    minx = -14
    maxx = 14

    minz = -36
    maxz = -8

    x = round(random.uniform(minx, maxx), 2)
    z = round(random.uniform(minz, maxz), 2)
    newAsteroide = Asteroide(x, z, 1.9, velocidade=0.01)

    while(flag):
        flag = False

        for aste in asteroides:
            if(newAsteroide.doesItCollide(aste)):
                flagGen = True

        if(not flagGen):
            return newAsteroide

        x = round(random.uniform(minx, maxx), 2)
        z = round(random.uniform(minz, maxz), 2)
        newAsteroide = Asteroide(x, z, 1.9, velocidade=0.01)
        flag = True
        flagGen = False


def checkAsteroides():
    amountAste = len(asteroides)
    if(amountAste < 3):
        for i in range(3 - amountAste):
            asteroides.append(genAsteroide())


def drawLines():
    # x
    # red
    glPushMatrix()
    glEnable(GL_COLOR_MATERIAL)
    glPushMatrix()
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    glEnd()
    glPopMatrix()

    # y
    # green
    glPushMatrix()
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    glEnd()
    glPopMatrix()

    # z
    # blue
    glPushMatrix()
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 10.0)
    glEnd()
    glPopMatrix()
    glDisable(GL_COLOR_MATERIAL)
    glPopMatrix()


def display():
    global XMove

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    luz()

    # drawLines()

    glPushMatrix()

    nave.mesh_list[0].materials[0].ambient = ouro_amb
    nave.mesh_list[0].materials[0].diffuse = ouro_dif
    nave.mesh_list[0].materials[0].specular = ouro_spe
    nave.mesh_list[0].materials[0].shininess = ouro_shi

    glPushMatrix()
    glRotatef(T3, T, 0, 11)
    glTranslatef(T, 0, 11)
    visualization.draw(nave)
    glPopMatrix()

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glBindTexture(GL_TEXTURE_2D, pneu_ID)

    for aste in asteroides:

        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT, rubi_amb)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, rubi_dif)
        glMaterialfv(GL_FRONT, GL_SPECULAR, rubi_spe)
        glMaterialf(GL_FRONT, GL_SHININESS, rubi_shi)

        # glScalef(2, 2, 2)
        glRotatef(T2, aste.px, aste.py, aste.pz)
        glColor3f(0.1, 0.1, 0.1)
        glTranslatef(aste.px, aste.py, aste.pz)
        # visualization.draw(ast)
        glutSolidSphere(aste.radius, 50, 50)
        glPopMatrix()

    glMaterialfv(GL_FRONT, GL_AMBIENT, chrome_amb)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, chrome_dif)
    glMaterialfv(GL_FRONT, GL_SPECULAR, chrome_spe)
    glMaterialf(GL_FRONT, GL_SHININESS, chrome_shi)

    for bullet in bullets:

        glPushMatrix()
        glTranslatef(bullet.px, bullet.py, bullet.pz)
        glRotatef(bullet.yaw, 0.0, 1.0, 0.0)
        glTranslatef(0.0, 0.8, 0.0)
        glRotatef(bullet.pitch, 1.0, 0.0, 0.0)
        glutSolidSphere(bullet.radius, 8, 8)
        glPopMatrix()

    for particula in particulas:

        alpha = 1-(particula.life/50)

        glPushMatrix()

        glMaterialfv(GL_FRONT, GL_AMBIENT, rubi_amb)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, rubi_dif)
        glMaterialfv(GL_FRONT, GL_SPECULAR, rubi_spe)
        glMaterialf(GL_FRONT, GL_SHININESS, rubi_shi)

        glEnable(GL_COLOR_MATERIAL)

        glColor4f(1.0, 0.0, 0.0, alpha)

        glTranslatef(particula.px, particula.py, particula.pz)
        glRotatef(particula.yaw, 0.0, 1.0, 0.0)
        glTranslatef(0.0, 0.8, 0.0)
        glRotatef(particula.pitch, 1.0, 0.0, 0.0)
        glutSolidSphere(particula.radius, 8, 8)
        glDisable(GL_COLOR_MATERIAL)
        glPopMatrix()

    glPopMatrix()
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)

    glutSwapBuffers()


def Keys(key, x, y):
    global T
    global T2
    global T3

    if(key == GLUT_KEY_LEFT):
        # tentativa de detectar saida da tela
        # if(T > (width//100) * -1):
        T -= 0.5

    elif(key == GLUT_KEY_RIGHT):
        # tentativa de detectar saida da tela
        # asteroides[0].volta()
        # if(T < (width//100)):
        T += 0.5

    elif(key == GLUT_KEY_UP):
        T2 -= 1
    elif(key == GLUT_KEY_DOWN):
        T2 += 1
    elif(key == GLUT_KEY_PAGE_UP):
        T3 -= 1
    elif(key == GLUT_KEY_PAGE_DOWN):
        T3 += 1


def asteroideMove():
    global XMove, XMoveFlag
    global width, T2

    T2 += 1

    value = (width//100) * 0.5

    if (XMove < value * -1 and XMoveFlag < 0):
        XMoveFlag *= -1
    if (XMove > value and XMoveFlag > 0):
        XMoveFlag *= -1
    XMove += XMoveFlag


def naveRotate():
    global T3
    global COUNT

    if(T3 > 10 or T3 < -10):
        COUNT *= -1
    T3 += COUNT


def updateAsteroide():
    for aste in asteroides:
        aste.anda()
        aste.calcula_velocidade()
        aste.atualiza_bola()

        if(aste.life > 150):
            asteroides.remove(aste)
            checkAsteroides()


def updateParticula():
    for particula in particulas:
        particula.calcula_velocidade()
        particula.atualiza_bola()
        if(particula.life >= 30):
            particulas.remove(particula)


def updateBullet():
    for bullet in bullets:

        bullet.volta()
        bullet.calcula_velocidade()
        bullet.atualiza_bola()

        for aste in asteroides:
            if(bullet.doesItCollide(aste)):
                createExplosion(aste)
                asteroides.remove(aste)
                bullets.remove(bullet)
                checkAsteroides()

        if(bullet.life > 140):
            bullets.remove(bullet)


def animacao(value):

    updateAsteroide()
    updateParticula()
    updateBullet()

    naveRotate()
    asteroideMove()

    glutPostRedisplay()
    glutTimerFunc(30, animacao, 1)


def resize(w, h):
    global width, height

    width = w
    height = h

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # jogavel
    # gluLookAt(0, 11.0, 15.0,
    #           0.0, 0.0, 1.0,
    #           0.0, 1.0, 0.0)

    # chao
    # gluLookAt(6, 0.0, 13.0,
    #           0.0, 0.0, 1.0,
    #           0.0, 1.0, 0.0)

    # chao alto
    gluLookAt(0, 20, 13,
              0.0, 0.0, 1.0,
              0.0, 1.0, 0.0)


def Keys_letras(key, x, y):

    if(key == b' '):  # Espaço
        bullet = Asteroide(T, 9, 0.8, 0.2)
        bullets.append(bullet)

    glutPostRedisplay()


def luz():
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, amb_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, attenuation_quad)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, attenuation_linear)

    glLightfv(GL_LIGHT0, GL_POSITION, light_position2)
    glLightfv(GL_LIGHT0, GL_AMBIENT, amb_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, attenuation_quad)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, attenuation_linear)


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # glEnable( GL_COLOR_MATERIAL ) # Transforma cores em materiais
    glShadeModel(GL_SMOOTH)  # Suaviza normais
    glEnable(GL_NORMALIZE)
    #glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE )

    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)

    global pneu_ID
    pneu_img = Image.open('aste-2.jpeg')
    pneu_img = pneu_img.resize((512, 512), resample=Image.LANCZOS)
    w, h, pneu_img = pneu_img.size[0], pneu_img.size[1], pneu_img.tobytes(
        "raw", "RGB", 0, -1)
    pneu_ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, pneu_ID)

    #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, pneu_img)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, w, h, GL_RGB,
                      GL_UNSIGNED_BYTE, pneu_img)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                    GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_NEAREST)
    #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glEnable(GL_BLEND)
    glBlendFuncSeparate(GL_SRC_ALPHA, GL_SRC_COLOR, GL_SRC_ALPHA, GL_DST_COLOR)
    glBlendEquationSeparate(GL_FUNC_ADD, GL_FUNC_REVERSE_SUBTRACT)


glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Asteroide 0")
init()
luz()
nave = pywavefront.Wavefront("nave.obj", create_materials=True)
ast = pywavefront.Wavefront("pneu_text.obj", create_materials=True)

glutDisplayFunc(display)
checkAsteroides()
glutReshapeFunc(resize)
glutTimerFunc(30, animacao, 1)
glutSpecialFunc(Keys)
glutKeyboardFunc(Keys_letras)
glutMainLoop()
