import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

tormayslista=[]

class Model3d():
    def __init__(self, filename,index,text,tex_koko,vektori,koordinaatit):

        self.filename = filename
        self.tex_koko = tex_koko
        self.verticies = []
        self.surfaces = []
        self.normals = []
        self.index=index #indexi CallListia varten Ja TEX iideetä
        self.tex_koords = []
        self.imageID = self.lataa_text(text)
        self.pinta_kaikilla = []
        self.tex_koords_kerrotut=self.tex_koord_kerroin()
        self.vbo = []
        self.vektori = list(vektori)
        self.koordinaatit = list(koordinaatit)
        self.nopeus = math.sqrt((self.vektori[0] ** 2) + (self.vektori[1] ** 2))
        self.hidastuvuus = 0.0001

    def alustus(self):
        self.file = open(self.filename, "r")
        for rivi in self.file:
            rivi_lista = rivi.split()
            try:
                tyyppi = rivi_lista[0]
                data = rivi_lista[1:]

                if tyyppi == "v":
                    x, y, z = data
                    vertex = (float(x), float(y), float(z))
                    self.verticies.append(vertex)

                elif tyyppi == "vt":
                    x, y, z = data
                    tex_coords = (float(x), float(y))
                    self.tex_koords.append(tex_coords)

                elif tyyppi == "vn":
                    x, y, z = data
                    normal = (float(x), float(y), float(z))
                    self.normals.append(normal)


                elif tyyppi == "f":
                    for v_vt_vn in data:
                        vtn = list((v_vt_vn.split("/")))
                        self.pinta_kaikilla.append(vtn)

            except:
                ValueError

        self.file.close()
        for tex in self.tex_koords:
            self.tex_koords_kerrotut.append(((tex[0] / self.tex_koko), (tex[1] / self.tex_koko)))
        for alkio in self.pinta_kaikilla:
            v = (self.verticies[int(alkio[0]) - 1])
            vt = (self.tex_koords_kerrotut[int(alkio[1]) - 1])
            vn = (self.normals[int(alkio[2]) - 1])
            self.vbo.append([v,vt,vn])
    def lataa_text(self,text):

        image = pygame.image.load(text)
        width = image.get_width()
        height = image.get_height()
        image = pygame.image.tostring(image, "RGB", False)

        texture_ID = self.index

        ID = glGenTextures(1,texture_ID)
        glBindTexture(GL_TEXTURE_2D, texture_ID)      #tän hetken käytössä oleva text
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
        glGenerateMipmap(GL_TEXTURE_2D)

        return ID
    def piirra2(self):
        glNewList(self.index, GL_COMPILE)
        glBegin(GL_TRIANGLES)
        for osa in self.vbo:
            glTexCoord2f((osa[1][0]), (osa[1][1]))
            glVertex3fv(osa[0])
            glNormal3fv(osa[2])
        glEnd()
        glEndList()
    def tex_koord_kerroin(self):
        kerrotut = []
        for tex in self.tex_koords:
            kerrotut.append(((tex[0]/self.text_koko),(tex[1]/self.text_koko)))
        return kerrotut
class peli_arvoja():
    def __init__(self):
        self.turn = 0
        self.SCORE = 0
        self.GameOver = False
        self.win = False
        self.tarkastus = 0

def main():
    INIT()

    peli = peli_arvoja()

    maila = Model3d("maila.obj", 6, "jalka.png",1,[0.0,0.0],[20.0,300.0])
    maila.alustus()
    maila.piirra2()

    jalat = Model3d("jalat.obj", 2, "jalka.png",1,[0.0,0.0],[100,50.0])
    jalat.alustus()
    jalat.piirra2()

    pohjalevy = Model3d("pohjalevy.obj", 3,"kentta.png",1,[0.0,0.0],[70,150.0])
    pohjalevy.alustus()
    pohjalevy.piirra2()

    top = Model3d("top.obj", 4,"jalka.png",1,[0.0,0.0],[70,150.0])
    top.alustus()
    top.piirra2()

    Vpallo = Model3d("pallo.obj",1,"Vpallo.png",1,[0,0],[0.0,0.0])
    Vpallo.alustus()
    Vpallo.piirra2()

    lattia = Model3d("lattia.obj", 5, "lattia.png",8,[0.0,0.0],[70,150.0])
    lattia.alustus()
    lattia.piirra2()

    Kpallo = Model3d("pallo.obj", 7, "Kpallo.png",1,[0.0,0.0],[-30.0,-50.0])
    Kpallo.alustus()
    Kpallo.piirra2()

    Ppallo = Model3d("pallo.obj", 8, "Ppallo.png",1,[0.0,0.0],[20.0,20.0])
    Ppallo.alustus()
    Ppallo.piirra2()

    Pallot = [Vpallo,Kpallo,Ppallo]

    Oikea_laita = 83
    Vasen_laita = -83
    Yla_laita = 133
    Ala_laita = -136

    PALLON_SADE = 5

    zoom = 0
    ZOOM = 0
    y_rot = 0
    y_rotation = 100000
    x_move = 0
    y_move = 0
    right = 0
    left = 0

    tormayslista=[]

    display=(800,600)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    y_rot = +3
                if event.key == pygame.K_d:
                    y_rot = -3
                if event.key == pygame.K_q:
                    y_rot = +0.5
                if event.key == pygame.K_e:
                    y_rot = -0.5

                if event.key == pygame.K_w:
                    zoom = -3
                if event.key == pygame.K_s:
                    zoom = 3
            if event.type == pygame.KEYUP:
                right = 0
                left = 0
                y_rot = 0
                zoom = 0


        x_move += right
        y_move += left
        y_rotation += y_rot
        ZOOM += zoom


        if ZOOM <= -100:
            ZOOM = -100
        if ZOOM >= 200:
            ZOOM = 200

        x_kamera = -(350+ZOOM)*math.sin(math.radians(y_rotation))
        y_kamera = (350+ZOOM)*math.cos(math.radians(y_rotation))


        for i in range(0, 100):
            tormayslista=pallojen_aseman_paivitys(tormayslista,Pallot, Oikea_laita, Vasen_laita, PALLON_SADE, Yla_laita, Ala_laita)

        if Vpallo.nopeus == 0 and Kpallo.nopeus == 0 and Ppallo.nopeus == 0:
            if ([0, 1] in tormayslista) and ([0, 2] in tormayslista):
                peli.SCORE += 1
            if peli.turn > 10:
                peli.GameOver = True
            if peli.SCORE >= 5 and peli.turn <= 10:
                peli.win = True
            tormayslista = []


        if nopeus_check(Pallot) == False:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                Valkoinen_yksikko_vektori = V_Y_V(Vpallo, y_kamera, x_kamera)
                peli.turn +=1
                latauss = lataus()
                Vpallo.vektori = [-((Valkoinen_yksikko_vektori[0]) * latauss),
                                  -((Valkoinen_yksikko_vektori[1]) * latauss)]

        glClearColor(0.15, 0, 0.15, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)


        gluPerspective(45, (display[0] / display[1]), 0.1, 800.0)

                    #"kamera"           #"objekti"          #"entiedä"


        gluLookAt(0, 90, (350+ZOOM), -Pallot[0].koordinaatit[1]*(x_kamera/(350+ZOOM))+Pallot[0].koordinaatit[0]*\
                  (y_kamera/(350+ZOOM)), 0, Pallot[0].koordinaatit[0]*(x_kamera/(350+ZOOM))+Pallot[0].koordinaatit[1]*\
                  (y_kamera/(350+ZOOM)), 0, 1, 0)


        glRotatef(0 + y_rotation, 0, 0 + y_rotation, 0)

        glBindTexture(GL_TEXTURE_2D, 8)
        line(x_kamera, y_kamera, Pallot[0].koordinaatit[1], Pallot[0].koordinaatit[0])#TÄHTÄYSLINJA

        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, 5)
        glTranslatef(0, -70, 0)
        glCallList(5)
        glPopMatrix()

        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, 2)
        glCallList(2)
        glPopMatrix()

        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, 3)
        glCallList(3)
        glPopMatrix()

        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, 1)
        glTranslatef(Pallot[0].koordinaatit[0], 4.5, Pallot[0].koordinaatit[1])
        glCallList(1)
        glPopMatrix()

        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, 7)
        glTranslatef(Pallot[1].koordinaatit[0], 4.5, Pallot[1].koordinaatit[1])
        glCallList(7)
        glPopMatrix()

        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, 8)
        glTranslatef(Pallot[2].koordinaatit[0], 4.5, Pallot[2].koordinaatit[1])
        glCallList(8)
        glPopMatrix()

        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, 4)
        glCallList(4)
        glPopMatrix()

        #glPushMatrix()
        drawText((-300,90,-300),"NÄPPÄIMET: NUMBAD W, A, S, D, Q ja E")
        drawText((-300, 70, -300), "HIIREN VASEMMASTA lyödään palloa (pohjassa pitämällä kovempi lyönti)")
        drawText((-300, 50, -300), "IDEA: Osua valkoisella pallolla punaiseen ja keltaiseen palloon samalla lyönnillä = 1p")
        drawText((-300, 30, -300), "TAVOITE: 5 pistettä 10 lyöntivuoron aikana ")

        drawText((300, 50, 300), "SCORE:"+str(peli.SCORE))
        drawText((300, 30, 300), "LYÖTY:" + str(peli.turn))

        if peli.win:
            drawText((0, 30, 0), "!!!!VOITIT PELIN!!!!")
        if peli.GameOver:
            drawText((0, 30, 0), "HÄVISIT PELIN :(")

        pygame.display.flip()
        pygame.time.wait(10)
def INIT():
    pygame.init()
    display = (1280, 960)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("pilis peli :----D")
    pygame.font.init()

    glEnable(GL_TEXTURE_2D)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT)
    glMatrixMode(GL_PROJECTION)

    # Valoa_ EN TIEDA MITEN TOIMII
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glLight(GL_LIGHT0, GL_DIFFUSE, (15, 15, 15, 45))
    glLight(GL_LIGHT1, GL_AMBIENT, (0.3, 0.3, 0.3, 0))
    glLightfv(GL_LIGHT0, GL_POSITION, (5, 1, 1, 1))
    glLightfv(GL_LIGHT1, GL_POSITION, (0, 20, 20, 1))
def line(x_kamera,y_kamera,y_move,x_move):

    glBegin(GL_LINES)
    glVertex3fv([x_kamera, 30, y_kamera])
    glVertex3fv([x_move, 4.5, y_move])
    glEnd()
def drawText(position, textString):
    font = pygame.font.SysFont("Arial", 18)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
###FYSIIKAT#############################
def seina_peruutus(Pallot,Oikea_laita,PALLON_SADE,Vasen_laita,Yla_laita,Ala_laita):
    pakki_vauhti = 0.0001
    osuma = [1, 1, 1]
    while True:
        for x in range(len(Pallot)):
            Pallot[x].koordinaatit[0] = Pallot[x].koordinaatit[0] - (Pallot[x].vektori[0] * pakki_vauhti)
            Pallot[x].koordinaatit[1] = Pallot[x].koordinaatit[1] - (Pallot[x].vektori[1] * pakki_vauhti)

            Pallot[x].vektori[0] = Pallot[x].vektori[0] + (Pallot[x].vektori[0]) * (pakki_vauhti)
            Pallot[x].vektori[1] = Pallot[x].vektori[1] + (Pallot[x].vektori[1]) * (pakki_vauhti)

            if Pallot[x].koordinaatit[0] >= (Oikea_laita - PALLON_SADE) or\
                            Pallot[x].koordinaatit[0] <= (Vasen_laita + PALLON_SADE)\
                    or Pallot[x].koordinaatit[1] >= (Yla_laita - PALLON_SADE) or\
                            Pallot[x].koordinaatit[1] <= (Ala_laita + PALLON_SADE):
                osuma[x]=1
            else:
                osuma[x]=0
        if not 1 in osuma:
            return
def peruutus(Pallot,PALLON_SADE):
    pakki_vauhti = 0.0001
    while True:
        for q in range(len(Pallot)):
            Pallot[q].koordinaatit[0] = Pallot[q].koordinaatit[0] - (Pallot[q].vektori[0] * pakki_vauhti)
            Pallot[q].koordinaatit[1] = Pallot[q].koordinaatit[1] - (Pallot[q].vektori[1] * pakki_vauhti)

            Pallot[q].vektori[0] = Pallot[q].vektori[0] + (Pallot[q].vektori[0]) * (pakki_vauhti)
            Pallot[q].vektori[1] = Pallot[q].vektori[1] + (Pallot[q].vektori[1]) * (pakki_vauhti)
        for t in range(len(Pallot)):
            for g in range(len(Pallot)):
                valimatka = math.sqrt(
                    ((Pallot[t].koordinaatit[0] - Pallot[g].koordinaatit[0]) ** 2) + \
                    ((Pallot[t].koordinaatit[1] - Pallot[g].koordinaatit[1]) ** 2))
                if (round(valimatka, 0) == (PALLON_SADE* 2)):
                    return
def collision_check(Pallot,PALLON_SADE):
    for y in range(len(Pallot)):
        for z in range(len(Pallot)):
            valimatka = math.sqrt(((Pallot[y].koordinaatit[0] - Pallot[z].koordinaatit[0]) ** 2) + \
                                  ((Pallot[y].koordinaatit[1] - Pallot[z].koordinaatit[1]) ** 2))
            if (valimatka > 0) and (valimatka <= (PALLON_SADE * 2)):
                tormaavat_pallot=[y,z]
                return tormaavat_pallot
def collision(tormaavat_pallot,Pallot):
    vali_vektori = [(Pallot[tormaavat_pallot[0]].koordinaatit[0]) - \
                    (Pallot[tormaavat_pallot[1]].koordinaatit[0]), \
                    (Pallot[tormaavat_pallot[0]].koordinaatit[1]) - \
                    (Pallot[tormaavat_pallot[1]].koordinaatit[1])
                    ]

    pituus = math.sqrt((vali_vektori[0] ** 2) + (vali_vektori[1] ** 2))

    yksikkovektori = [(vali_vektori[0] / pituus), (vali_vektori[1] / pituus)]

    normaali_vektori_0_kerroin = (((Pallot[tormaavat_pallot[0]].vektori[0]) * \
                                   (-yksikkovektori[0])) + \
                                  ((Pallot[tormaavat_pallot[0]].vektori[1]) * \
                                   (-yksikkovektori[1])))

    normaali_vektori_1_kerroin = (((Pallot[tormaavat_pallot[1]].vektori[0]) * \
                                   (yksikkovektori[0])) + \
                                  ((Pallot[tormaavat_pallot[1]].vektori[1]) * \
                                   (yksikkovektori[1])))

    normaali_vektori_0 = [((-yksikkovektori[0]) * normaali_vektori_0_kerroin), \
                          ((-yksikkovektori[1]) * normaali_vektori_0_kerroin)]
    normaali_vektori_1 = [((yksikkovektori[0]) * normaali_vektori_1_kerroin), \
                          ((yksikkovektori[1]) * normaali_vektori_1_kerroin)]

    tangentti_vektori_0 = [(normaali_vektori_0[0]) - (Pallot[tormaavat_pallot[0]].vektori[0]), \
                           (normaali_vektori_0[1]) - (Pallot[tormaavat_pallot[0]].vektori[1])]

    tangentti_vektori_1 = [(normaali_vektori_1[0]) - (Pallot[tormaavat_pallot[1]].vektori[0]), \
                           (normaali_vektori_1[1]) - (Pallot[tormaavat_pallot[1]].vektori[1])]

    #print(Pallot[tormaavat_pallot[0]].vektori)
    #print(Pallot[tormaavat_pallot[1]].vektori)

    Pallot[tormaavat_pallot[0]].vektori[0] = -(tangentti_vektori_0[0] - normaali_vektori_1[0])
    Pallot[tormaavat_pallot[0]].vektori[1] = -(tangentti_vektori_0[1] - normaali_vektori_1[1])

    Pallot[tormaavat_pallot[1]].vektori[0] = -(tangentti_vektori_1[0] - normaali_vektori_0[0])
    Pallot[tormaavat_pallot[1]].vektori[1] = -(tangentti_vektori_1[1] - normaali_vektori_0[1])

    #print(Pallot[tormaavat_pallot[0]].vektori)
    #print(Pallot[tormaavat_pallot[1]].vektori)

    return
def pallojen_aseman_paivitys(tormayslista,Pallot,Oikea_laita,Vasen_laita,PALLON_SADE,Yla_laita,Ala_laita):
    for x in range(len(Pallot)):
        if (round((Pallot[x].vektori[0]/7),0) == 0) and (round((Pallot[x].vektori[1]/7),0) == 0):
            Pallot[x].vektori = [0.0,0.0]

        Pallot[x].koordinaatit[0]=Pallot[x].koordinaatit[0]+(Pallot[x].vektori[0]*0.001)
        Pallot[x].koordinaatit[1] = Pallot[x].koordinaatit[1] + (Pallot[x].vektori[1] * 0.001)


        #taitaapi olla noissa vektoreissa pikku bugi
        Pallot[x].vektori[0]=Pallot[x].vektori[0]-(Pallot[x].vektori[0])*(Pallot[x].hidastuvuus)
        Pallot[x].vektori[1] = Pallot[x].vektori[1] - (Pallot[x].vektori[1]) * (Pallot[x].hidastuvuus)

        #collision check palauttaa pallojen indeksit jotka törmää

        tormaavat_pallot = collision_check(Pallot,PALLON_SADE)
        if collision_check(Pallot,PALLON_SADE) != None:
            tormayslista.append(tormaavat_pallot)



            peruutus(Pallot,PALLON_SADE)

            collision(tormaavat_pallot,Pallot)


        if Pallot[x].koordinaatit[0] >= (Oikea_laita - PALLON_SADE) or\
                        Pallot[x].koordinaatit[0] <= (Vasen_laita + PALLON_SADE):
            seina_peruutus(Pallot,Oikea_laita,Vasen_laita,PALLON_SADE,Yla_laita,Ala_laita)
            Pallot[x].vektori[0]=-(Pallot[x].vektori[0])

        if Pallot[x].koordinaatit[1] >= (Yla_laita - PALLON_SADE) or\
                            Pallot[x].koordinaatit[1] <= (Ala_laita + PALLON_SADE):
            seina_peruutus(Pallot, Oikea_laita, PALLON_SADE, Vasen_laita, Yla_laita, Ala_laita)
            Pallot[x].vektori[1] = -(Pallot[x].vektori[1])

    return tormayslista
def nopeus_check(Pallot):
    nopeus_lista = []
    for x in range(len(Pallot)):
        Pallot[x].nopeus = math.sqrt((Pallot[x].vektori[0] ** 2) + (Pallot[x].vektori[1] ** 2))
        nopeus_lista.append(Pallot[x].nopeus)
    for x in range(len(nopeus_lista)):
        if nopeus_lista[x] != 0:
            return True
        else:
            return False
def lataus():
    mouse = 1
    lataus = 0
    while mouse == 1:
        pygame.event.get()
        lataus += 10
        if lataus > 300:
            lataus = 300
        pygame.time.wait(200)
        pygame.display.flip()
        if pygame.mouse.get_pressed() == (0, 0, 0):
            mouse = 0


    return lataus
def V_Y_V(Vpallo,y_kamera,x_kamera):
    Valkoinen_vali_vektori = [(Vpallo.koordinaatit[0] + 10) - (x_kamera),\
                              (Vpallo.koordinaatit[1] + 10) - (y_kamera)
                            ]

    V_V_V_pituus = math.sqrt((Valkoinen_vali_vektori[0] ** 2) + (Valkoinen_vali_vektori[1] ** 2))

    V_V_V_yksikko_vektori = [-(Valkoinen_vali_vektori[0] / V_V_V_pituus), -(Valkoinen_vali_vektori[1] / V_V_V_pituus)]

    #print(Valkoinen_vali_vektori)
    #print(V_V_V_pituus)
    #print(V_V_V_yksikko_vektori)
    return V_V_V_yksikko_vektori
########################################

if __name__ == "__main__":
    main()
