#Projekt POiGK 2022 - Wizualizacja ramienia robota - Nowak, Nowogrodzki
from vpython import *

class Visualization():
    def __init__(self):
        self.scene = canvas(title='Wizualizacja ramienia robota typu "cylindrical arm"', width=1200, height=800, center=vector(0,0,0)) 

        #tworzenie obiektow widocznych na scenie
        ground = box(length=10, height=0.01, width=10, texture=textures.stucco)             
        self.base_obj = cylinder(axis=vector(0,3,0), radius=0.2, visible=True, texture=textures.metal)
        self.arm_obj = box(pos=vector(0.6,2.5,0), length=2, height=0.4, width=0.8, visible=True, texture=textures.rough)
        self.ext_obj = cylinder(pos=vector(0.8, 2.5, 0), axis=vector(1.5,0,0), radius=0.1, visible=True, texture=textures.metal)
        self.grapple_obj1 = cylinder(pos = vector(2.1, 2.5, 0), axis=vector(0.4, 0, -0.3), radius=0.05, visible=True, texture=textures.metal)
        self.grapple_obj2 = cylinder(pos = vector(2.1, 2.5, 0), axis=vector(0.4, 0, 0.3), radius=0.05, visible=True, texture=textures.metal)
        self.ext_v = vector(1, 0 , 0)

        self.recording = False
        self.playing = False
        self.record_list = []
        self.prev_pos = [0]*16

        self.to_point = False
        #domyslne wartosci punktu docelowego kinematyki odwrotnej
        self.number_x=0.45
        self.number_y=2
        self.number_z=0.5

        self.makeCaption()
        self.defaultCamera()

    def run(self):
        
        while True:
            k = keysdown()
            if self.recording:
                self.record_list.append(k)      #zapisywanie wejsc klawiatury do listy, w trakcie trybu nagrywania; z tej listy zostana odtworzone ruchy ramienia robota
                
            if not self.playing and not self.to_point:
                self.control(k)

    def control(self, k, rate_val=5000):
        i=0
        rate(rate_val)
        if 'left' in k:
                i = 0.001
        if 'right' in k:
                i = -0.001
        self.rotate(i) 
        i = 0
        if 'up' in k:
            i = 0.0001
        if 'down' in k:
            i = -0.0001
        self.move(i)
        i = 0
        if 'm' in k:
            i = 0.0001    
        if 'n' in k:
            i = -0.0001
        self.extend(i)

    def rotate(self, i=0):
        self.base_obj.rotate(angle=i/10, axis=vector(0,1,0))
        self.arm_obj.rotate(angle=i/10, axis=vector(0,1,0), origin=self.base_obj.pos)
        self.ext_obj.rotate(angle=i/10, axis=vector(0,1,0), origin=self.base_obj.pos)
        self.grapple_obj1.rotate(angle=i/10, axis=vector(0,1,0), origin=self.base_obj.pos)
        self.grapple_obj2.rotate(angle=i/10, axis=vector(0,1,0), origin=self.base_obj.pos)
        self.ext_v = rotate(self.ext_v, angle=i/10, axis=vector(0,1,0))
        
    def move(self, i=0):
        self.arm_obj.pos = self.arm_obj.pos + vector(0,i,0)
        self.ext_obj.pos = self.ext_obj.pos + vector(0,i,0)
        self.grapple_obj1.pos = self.grapple_obj1.pos + vector(0,i,0)
        self.grapple_obj2.pos = self.grapple_obj2.pos + vector(0,i,0)
        if self.arm_obj.pos.y >= 2.8 or self.arm_obj.pos.y <= 0.2:
            i=-i
            self.arm_obj.pos = self.arm_obj.pos + vector(0,i,0)
            self.ext_obj.pos = self.ext_obj.pos + vector(0,i,0)
            self.grapple_obj1.pos = self.grapple_obj1.pos + vector(0,i,0)
            self.grapple_obj2.pos = self.grapple_obj2.pos + vector(0,i,0)
            return True
        return False
            
    def extend(self, i=0):
        self.ext_obj.pos = self.ext_obj.pos + i*self.ext_v
        self.grapple_obj1.pos = self.grapple_obj1.pos + i*self.ext_v
        self.grapple_obj2.pos = self.grapple_obj2.pos + i*self.ext_v
        if mag(self.ext_obj.pos - self.arm_obj.pos) > 0.4:
            i=-i
            self.ext_obj.pos = self.ext_obj.pos + i*self.ext_v
            self.grapple_obj1.pos = self.grapple_obj1.pos + i*self.ext_v
            self.grapple_obj2.pos = self.grapple_obj2.pos + i*self.ext_v
            
    def defaultCamera(self, b=''):
        self.scene.camera.axis = vector(-5, -6.7, -5.7)
        self.scene.camera.pos = -self.scene.camera.axis

    def record(self, b=''):
        self.recording=True
        self.record_list=[]
        self.makeCaption('Nagrywanie')
        self.btn_point.disabled = True

        #zapisanie poczatkowej pozycji ramienia robota na poczatku nagrywania ruchu
        self.prev_pos[0] = vector(self.base_obj.axis)           
        self.prev_pos[1] = vector(self.arm_obj.axis)
        self.prev_pos[2] = vector(self.ext_obj.axis)
        self.prev_pos[3] = vector(self.grapple_obj1.axis)
        self.prev_pos[4] = vector(self.grapple_obj2.axis)
        self.prev_pos[5] = vector(self.ext_v)
        self.prev_pos[6] = vector(self.base_obj.up)
        self.prev_pos[7] = vector(self.arm_obj.up)
        self.prev_pos[8] = vector(self.ext_obj.up)
        self.prev_pos[9] = vector(self.grapple_obj1.up)
        self.prev_pos[10] = vector(self.grapple_obj2.up)
        self.prev_pos[11] = vector(self.base_obj.pos)
        self.prev_pos[12] = vector(self.arm_obj.pos)
        self.prev_pos[13] = vector(self.ext_obj.pos)
        self.prev_pos[14] = vector(self.grapple_obj1.pos)
        self.prev_pos[15] = vector(self.grapple_obj2.pos)
        
    def play(self, b=''):
        if not self.record_list: return
        self.recording = False
        self.playing = True
        self.makeCaption('Odtwarzanie')
        self.btn_rec.disabled = True
        self.btn_play.disabled = True
        self.btn_point.disabled = True

        #ustawienie ramienia robota do pozycji poczatkowej z nagranego ruchu
        self.base_obj.axis = self.prev_pos[0] 
        self.arm_obj.axis = self.prev_pos[1] 
        self.ext_obj.axis = self.prev_pos[2]  
        self.grapple_obj1.axis = self.prev_pos[3] 
        self.grapple_obj2.axis = self.prev_pos[4] 
        self.ext_v = self.prev_pos[5]
        self.base_obj.up = self.prev_pos[6] 
        self.arm_obj.up = self.prev_pos[7] 
        self.ext_obj.up = self.prev_pos[8]  
        self.grapple_obj1.up = self.prev_pos[9] 
        self.grapple_obj2.up = self.prev_pos[10]
        self.base_obj.pos = self.prev_pos[11] 
        self.arm_obj.pos = self.prev_pos[12] 
        self.ext_obj.pos = self.prev_pos[13]  
        self.grapple_obj1.pos = self.prev_pos[14] 
        self.grapple_obj2.pos = self.prev_pos[15]

        #odtworzenie ruchow robota
        for k in self.record_list:
            self.control(k)

        self.playing = False
        self.makeCaption()
        self.btn_rec.disabled = False
        self.btn_play.disabled = False
        self.btn_point.disabled = False
    
    def kinOdw(self):
        self.to_point = True
        self.makeCaption('W trakcie ruchu do punktu')
        self.btn_rec.disabled = True
        self.btn_play.disabled = True
        self.btn_point.disabled = True
        
        ang_to = atan2(self.number_z, self.number_x)
        mag_to = sqrt(self.number_x**2 + self.number_z**2)

        #sprawdzenie czy punkt nie jest poza zakresem ramienia
        if self.number_y > 2.7999: self.number_y = 2.7999
        elif self.number_y < 0.2001: self.number_y = 0.2001
        if mag_to > 0.99: mag_to = 0.99
        elif mag_to < 0.2: mag_to = 0.2

        #ustawienie ramienia robota do docelowego punktu
        while self.ext_obj.pos.y < self.number_y:
            self.control(['up'])
        while self.ext_obj.pos.y > self.number_y:
            self.control(['down'])
        while atan2(self.ext_obj.pos.z, self.ext_obj.pos.x) > ang_to:
            self.control(['left'])
        while atan2(self.ext_obj.pos.z, self.ext_obj.pos.x) < ang_to:
            self.control(['right'])
        while sqrt(self.ext_obj.pos.x**2 + self.ext_obj.pos.z**2) > mag_to:
            self.control(['n'])
        while sqrt(self.ext_obj.pos.x**2 + self.ext_obj.pos.z**2) < mag_to:
            self.control(['m'])

        self.number_x = round(self.ext_obj.pos.x, 3)
        self.number_z = round(self.ext_obj.pos.z, 3)

        self.to_point = False
        self.makeCaption()
        self.btn_rec.disabled = False
        self.btn_play.disabled = False
        self.btn_point.disabled = False

    def inp_x(self, s):
        if not s.number == None: 
            self.number_x = s.number
    
    def inp_y(self, s):
        if not s.number == None: 
            self.number_y = s.number

    def inp_z(self, s):
        if not s.number == None: 
            self.number_z = s.number
                 
    def makeCaption(self, capt=''):
        self.scene.caption = '\n' + capt
        self.scene.append_to_caption('\n\n')
        button(bind=self.defaultCamera, text='Domyslny widok')
        self.scene.append_to_caption('   ')
        self.btn_rec = button(bind=self.record, text='Nagrywanie ruchu')
        self.scene.append_to_caption('   ')
        self.btn_play = button(bind=self.play, text='Odtwarzanie ruchu')
        self.scene.append_to_caption('   ')
        self.btn_point = button(bind=self.kinOdw, text='Do punktu')
        self.scene.append_to_caption('\n\nx:')
        winput(bind=self.inp_x, text=self.number_x)
        self.scene.append_to_caption('    y:')
        winput(bind=self.inp_y, text=self.number_y)
        self.scene.append_to_caption('    z:')
        winput(bind=self.inp_z, text=self.number_z)
        self.scene.append_to_caption('\n\nSterowanie robotem odbywa sie za pomoca strzalek i klawiszy "n" oraz "m"\nSterowanie kamera: ctrl+lewy przycisk mysz lub prawy przycisk myszy\nAby zakonczyc nagrywanie ruchu nalezy wcisnac przycisk "Odtwarzanie ruchu"\nPrzycisk "Do punktu" ustawia położenie robota we wprowadzonych przez użytkownika wspólrzędnych, w przypadku braku zakresu robota ustawia go jak najbliżej tego punktu')

visualization = Visualization()
visualization.run()         #uruchomienie glownej petli programu
