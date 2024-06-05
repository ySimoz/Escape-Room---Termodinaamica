import pygame
import sys

# screen dimensions
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Escape Room")

class EscapeRoom():
    def __init__(self):
        # setup
        self.init_pygame()
        self.clock = pygame.time.Clock()
        self.WIDTH, self.HEIGHT = screen.get_width(), screen.get_height()
        
        self.running = True
        self.general_setup()
        self.setup_states()
        self.timer_setup()
    
    # start and end game
    def init_pygame(self):
        pygame.init()
    
    def quit_game(self):
        pygame.quit()
        sys.exit()
        
    def clean(self):
        screen.fill((0,0,0))
    
    def timer_setup(self):
        self.active_timer = False
        self.timer_font = pygame.font.SysFont('Honeymoon', 70)
        self.initial_time = 900  # 10 minutes in seconds
        self.timer = self.initial_time
        self.timer_text = self.timer_font.render("{}".format(self.format_time(self.timer)), True, (255, 255, 255))
        self.timer_rect = self.timer_text.get_rect(topleft =(1480, 940))
        self.timer_interval = 1000  # 1000 milliseconds = 1 second
        self.last_time = pygame.time.get_ticks()
    
    
    # general setup
    def general_setup(self):
        self.introduction_surface = pygame.transform.scale(pygame.image.load('porta-escaperoom.png'), (self.WIDTH,self.HEIGHT))
        self.door_rect = pygame.Rect(485, 420, 533, 500)
        self.door_text = 'Premimi per iniziare'
        self.font2= pygame.font.SysFont('Honeymoon', 50)
        self.font1 = pygame.font.SysFont('Honeymoon', 70)
        self.font3 = pygame.font.SysFont('Honeymoon', 60)
        self.font4 = pygame.font.SysFont('Honeymoon', 80)
        self.font5 = pygame.font.SysFont('Honeymoon', 120)
        
        self.door_text_surface = self.font2.render(self.door_text, True, (255,255,255))
        self.max_scale = 1.0 #writing animation
        self.min_scale = 0.8
        self.scale_increment = 0.004
        self.current_scale = self.min_scale
        self.growing = True
        
        # caloriferi room
        self.calorifero_state = 0
        self.calorifero_rosso_surface = pygame.transform.scale(pygame.image.load('calorifero-rosso.png'), (self.WIDTH,self.HEIGHT))
        self.calorifero_verde_surface = pygame.transform.scale(pygame.image.load('calorifero-verde.png'), (self.WIDTH,self.HEIGHT))
        self.calorifero_fuoco_surface = pygame.transform.scale(pygame.image.load('calorifero-fuoco.png'), (self.WIDTH,self.HEIGHT))
        self.regolatore_rect = pygame.Rect(1266, 364, 90, 84)
        self.question_surface_1 = pygame.Surface((1100, 780))
        self.question_surface_inner_1 = pygame.Surface((1080, 760))
        self.question_surface_inner_1.fill((255,255,255))
        self.question_surface_1.blit(self.question_surface_inner_1, (10,10))
        self.question_box_state = False
        self.question_box_rect_1 = pygame.Rect(100,50,1100,780)
        self.vero_falso_writing_1 = 'ATTENZIONE'
        self.vero_falso_writing_2 = 'rispondi a questo vero falso per salvarti'
        self.vero_falso_surface_1 = self.font4.render(self.vero_falso_writing_1, True, (255,0,0))
        self.vero_falso_surface_2 = self.font2.render(self.vero_falso_writing_2, True, (255,0,0))
        self.question_surface_1_5 = pygame.Surface((1000, 700))
        self.question_surface_inner_1_5 = pygame.Surface((980, 680))
        self.question_surface_inner_1_5.fill((255,255,255))
        self.question_surface_1_5.blit(self.question_surface_inner_1_5, (10,10))
        self.question_surface_1_5.blit(self.vero_falso_surface_1, (self.question_surface_1_5.get_width() / 2 - self.vero_falso_surface_1.get_width() / 2, 70 ))
        self.question_surface_1_5.blit(self.vero_falso_surface_2, (self.question_surface_1_5.get_width() / 2 - self.vero_falso_surface_2.get_width() / 2, 180 ))
        self.question_box_rect_1_5 = pygame.Rect(100,50,1000,700)
        self.vero_writing = 'VERO'
        self.falso_writing = 'FALSO'
        self.vero_surface = self.font2.render(self.vero_writing, True, (0,0,0))
        self.falso_surface = self.font2.render(self.falso_writing, True, (0,0,0))
        self.question_surface_1_5.blit(self.vero_surface, (250, 450))
        self.question_surface_1_5.blit(self.falso_surface, (650, 450))
        self.vero_falso_question_state = False
        
        
        #cassaforti room
        self.cassaforti_1_surface = pygame.transform.scale(pygame.image.load('cassaforti-1.png'), (self.WIDTH,self.HEIGHT))
        self.cassaforti_2_surface = pygame.transform.scale(pygame.image.load('cassaforti-2.png'), (750, 582))
        self.cassaforti_rect_1 = pygame.Rect(300, 490, 270, 195)
        self.cassaforti_rect_2 = pygame.Rect(100, 210, 750, 582)
        self.cassaforte_zoom_state = False
        self.question_box_rect_2 = pygame.Rect(900,100,670,800)
        self.question_surface_2 = pygame.Surface((670, 800))
        self.question_surface_2_5 = pygame.Surface((670, 800))
        self.question_surface_inner_2 = pygame.Surface((650, 780))
        self.question_surface_inner_2.fill((255,255,255))
        self.question_surface_2.blit(self.question_surface_inner_2, (10,10))
        self.question_surface_2_5.blit(self.question_surface_inner_2, (10,10))
        
        self.second_question_state = False
        self.active_buttons = True
        self.codice = '5784'
        self.codice_inserito = ""
        self.codice_surface = pygame.Surface((235,120))
        self.codice_surface.fill((0,255,0))
        self.codice_state = False
        self.codice_writing1 = 'Digita il codice'
        self.codice_writing1_surface = self.font4.render(self.codice_writing1, True, (0,0,0))
        self.codice_writing2_surface = self.font5.render(self.codice, True, (0,255,0))
        
        #pugnetti room
        self.pugnetti_surface = pygame.transform.scale(pygame.image.load('pugnetti.png'), (self.WIDTH, self.HEIGHT))
        self.pugnetti_dialog_rect = pygame.Rect(1000, 75, 540, 315)
        
        # Text to be displayed on the dialog rectangle
        dialog_text_1 = "Buongiorno cari"
        dialog_text_2 = "studenti siete pronti a"
        dialog_text_3 = "rispondere alle mie domande?"
        self.dialog_font = pygame.font.SysFont('Honeymoon', 50)  # Adjust font and size as needed
        self.dialog_color = (0, 0, 0)  # Adjust color as needed
        
        
        # Render the text surfaces
        self.dialog_text_surface_1 = self.dialog_font.render(dialog_text_1, True, self.dialog_color)
        self.dialog_text_surface_2 = self.dialog_font.render(dialog_text_2, True, self.dialog_color)
        self.dialog_text_surface_3 = self.dialog_font.render(dialog_text_3, True, self.dialog_color)
        

        # Position the text surfaces within the dialog rectangle
        self.pugnetti_text_rect_1 = self.dialog_text_surface_1.get_rect(midtop=(self.pugnetti_dialog_rect.centerx, self.pugnetti_dialog_rect.top + 50))
        self.pugnetti_text_rect_2 = self.dialog_text_surface_2.get_rect(midtop=(self.pugnetti_dialog_rect.centerx, self.pugnetti_text_rect_1.bottom + 15))
        self.pugnetti_text_rect_3 = self.dialog_text_surface_3.get_rect(midtop=(self.pugnetti_dialog_rect.centerx, self.pugnetti_text_rect_2.bottom + 15))
        
        dialog_text_4 = "Pensavi fosse"
        dialog_text_5 = "solo una e invece!"
        self.dialog_font = pygame.font.SysFont('Honeymoon', 55)  # Adjust font and size as needed
        self.dialog_color = (0, 0, 0)  # Adjust color as needed
        
        # Render the text surfaces
        self.dialog_text_surface_4 = self.dialog_font.render(dialog_text_4, True, self.dialog_color)
        self.dialog_text_surface_5 = self.dialog_font.render(dialog_text_5, True, self.dialog_color)
        # Position the text surfaces within the dialog rectangle
        self.pugnetti_text_rect_4 = self.dialog_text_surface_4.get_rect(midtop=(self.pugnetti_dialog_rect.centerx, self.pugnetti_dialog_rect.top + 60))
        self.pugnetti_text_rect_5 = self.dialog_text_surface_5.get_rect(midtop=(self.pugnetti_dialog_rect.centerx, self.pugnetti_text_rect_4.bottom + 20))
        #
        self.question_surface_3 = pygame.Surface((580, 840))
        self.question_surface_inner_3 = pygame.Surface((560, 820))
        self.question_surface_inner_3.fill((255,255,255))
        self.question_surface_3.blit(self.question_surface_inner_3, (10,10))
        self.question_surface_3_5 = pygame.Surface((580, 840))
        self.question_surface_inner_3_5 = pygame.Surface((560, 820))
        self.question_surface_inner_3_5.fill((255,255,255))
        self.question_surface_3_5.blit(self.question_surface_inner_3, (10,10))
        self.question_box_rect_3 = pygame.Rect(60,100,580,840)
        
        #pistoni room
        self.entrance_animation_state = True
        self.pistoni1_surface = pygame.transform.scale(pygame.image.load('pistone-1.png'), (self.WIDTH, self.HEIGHT))
        self.pistoni2_surface = pygame.transform.scale(pygame.image.load('pistone-2.png'), (self.WIDTH, self.HEIGHT))
        self.pistoni_wiriting_1 = 'ATTENZIONE!'
        self.pistoni_wiriting_2 = 'GRAZIE!!'
        self.pistoni_wiriting_surface_1 = self.font5.render(self.pistoni_wiriting_1, True, ((255,0,0)))
        self.pistoni_wiriting_surface_2 = self.font5.render(self.pistoni_wiriting_2, True, ((0,255,0)))
        self.pannello_controllo_rect = pygame.Rect(740, 495, 200, 135)
        self.question_surface_4 = pygame.Surface((1150, 600))
        self.question_surface_inner_4 = pygame.Surface((1130, 580))
        self.question_surface_inner_4.fill((255,255,255))
        self.question_surface_4.blit(self.question_surface_inner_4, (10,10))
        self.question_box_rect_4 = pygame.Rect(250,70,1150,600)
        
        #ipad room
        self.ipad_zoom_state = False
        self.codice_sate = False
        self.lucchetto_zoom_state = False
        self.ipad_codice_state = True
        self.ipad_lucchetto_surface = pygame.transform.scale(pygame.image.load('ipad-lucchetto.png'), (self.WIDTH +2 , self.HEIGHT))
        self.ipad_surface = pygame.transform.scale(pygame.image.load('ipad.png'), (self.WIDTH + 2, self.HEIGHT))
        self.lucchetto_surface = pygame.transform.scale(pygame.image.load('lucchetto.png'), (self.WIDTH + 2, self.HEIGHT))
        self.ipad_rect = pygame.Rect(960, 460, 205, 265)
        self.ipad_zoomed_rect = pygame.Rect(650, 45, 680, 855)
        self.question_box_rect_5 = pygame.Rect(705,100,570,740)
        self.question_surface_5 = pygame.Surface((570, 740), pygame.SRCALPHA)
        self.question_surface_5_b = pygame.Surface((570, 740), pygame.SRCALPHA)
        self.ipad_codice = '3752'
        self.ipad_codice_surface = self.font5.render(self.ipad_codice, True, (0,255,0))
        self.ipad_codice_inserito = ''
        self.ipad_codice_surface_inserire = pygame.Surface((240,130))
        self.ipad_codice_surface_inserire.fill((0,255,0))
        self.lucchetto_surface.blit(self.ipad_codice_surface_inserire, (300, 300))
        self.lucchetto_rect = pygame.Rect(630, 710, 130, 90)
        
        #stanza freddo
        self.termostato_surface = pygame.transform.scale(pygame.image.load('termostato.png'), (self.WIDTH + 2, self.HEIGHT))
        self.sf_1_surface =  pygame.transform.scale(pygame.image.load('stanza-fredda-1.png'), (self.WIDTH + 2, self.HEIGHT))
        self.sf_2_surface =  pygame.transform.scale(pygame.image.load('stanza-fredda-2.png'), (self.WIDTH + 2, self.HEIGHT))
        self.termostato_rect = pygame.Rect(925, 660, 250, 210)
        self.question_box_rect_6 = pygame.Rect(80, 100, 720, 880)
        self.question_surface_6 = pygame.Surface((720, 880))
        self.question_surface_inner_6 = pygame.Surface((700, 860))
        self.question_surface_inner_6.fill((255,255,255))
        self.question_surface_6.blit(self.question_surface_inner_6, (10,10))
        
        #poli room
        self.poli_first_dialog_state = True
        self.poli_second_dialog_state = False
        self.poli_third_dialog_state = False
        self.poli_fourth_dialog_state = False
        self.poli_end_dialog_state = False
        self.poli_surface = pygame.transform.scale(pygame.image.load('poli.png'), (self.WIDTH + 2, self.HEIGHT))
        self.question_box_rect_7 = pygame.Rect(120, 70, 1430, 650)
        self.question_surface_7 = pygame.Surface((1430, 650))
        self.question_surface_inner_7 = pygame.Surface((1410, 630))
        self.question_surface_inner_7.fill((255,255,255))
        self.question_surface_7.blit(self.question_surface_inner_7, (10,10))
        self.question_box_rect_7_5 = pygame.Rect(120, 70, 1430, 650)
        self.question_surface_7_5 = pygame.Surface((1430, 650))
        self.question_surface_inner_7_5 = pygame.Surface((1410, 630))
        self.question_surface_inner_7_5.fill((255,255,255))
        self.question_surface_7_5.blit(self.question_surface_inner_7_5, (10,10))
        
        self.poli_dialog_rect = pygame.Rect(1000, 75, 540, 315)
        self.poli_dialog_rect2 = pygame.Rect(50, 60, 540, 315)
        dialog_text_1 = "Ciao bimbi"
        dialog_text_2 = "finalmente siete arrivati"
        dialog_text_3 = "siete pronti a soffrire?"
        dialog_text_4 = "Come dite..."
        dialog_text_5 = "non siete preparati"
        dialog_text_6 = "eh problemi vostri!"
        dialog_text_7 = "Col poco tempo che"
        dialog_text_8 = "vi rimane dovete rispondere"
        dialog_text_9 = "a due difficili quesiti!"
        dialog_text_10 = "AH AH AH AH AH"
        dialog_text_11 = "non rimane che sfidarti"
        dialog_text_12 = "von l'ultimo quesito!!"
        dialog_text_13 = "COMPLIMENTI!! Sei riuscito"
        dialog_text_14 = "a completare l'escape room!"
        dialog_text_15 = "Sii felice per la tua VITTORIA!"
        
        self.dialog_font = pygame.font.SysFont('Honeymoon', 50)  # Adjust font and size as needed
        self.dialog_color = (0, 0, 0)  # Adjust color as needed
        
        # Render the text surfaces
        self.poli_dialog_text_surface_1 = self.dialog_font.render(dialog_text_1, True, self.dialog_color)
        self.poli_dialog_text_surface_2 = self.dialog_font.render(dialog_text_2, True, self.dialog_color)
        self.poli_dialog_text_surface_3 = self.dialog_font.render(dialog_text_3, True, self.dialog_color)
        self.poli_dialog_text_surface_4 = self.dialog_font.render(dialog_text_4, True, self.dialog_color)
        self.poli_dialog_text_surface_5 = self.dialog_font.render(dialog_text_5, True, self.dialog_color)
        self.poli_dialog_text_surface_6 = self.dialog_font.render(dialog_text_6, True, self.dialog_color)
        self.poli_dialog_text_surface_7 = self.dialog_font.render(dialog_text_7, True, self.dialog_color)
        self.poli_dialog_text_surface_8 = self.dialog_font.render(dialog_text_8, True, self.dialog_color)
        self.poli_dialog_text_surface_9 = self.dialog_font.render(dialog_text_9, True, self.dialog_color)
        self.poli_dialog_text_surface_10 = self.dialog_font.render(dialog_text_10, True, self.dialog_color)
        self.poli_dialog_text_surface_11 = self.dialog_font.render(dialog_text_11, True, self.dialog_color)
        self.poli_dialog_text_surface_12 = self.dialog_font.render(dialog_text_12, True, self.dialog_color)
        self.poli_dialog_text_surface_13 = self.dialog_font.render(dialog_text_13, True, self.dialog_color)
        self.poli_dialog_text_surface_14 = self.dialog_font.render(dialog_text_14, True, self.dialog_color)
        self.poli_dialog_text_surface_15 = self.dialog_font.render(dialog_text_15, True, self.dialog_color)
        
        # Position the text surfaces within the dialog rectangle
        self.poli_text_rect_1 = self.poli_dialog_text_surface_1.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_dialog_rect.top + 50))
        self.poli_text_rect_2 = self.poli_dialog_text_surface_2.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_text_rect_1.bottom + 15))
        self.poli_text_rect_3 = self.poli_dialog_text_surface_3.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_text_rect_2.bottom + 15))
        self.poli_text_rect_4 = self.poli_dialog_text_surface_4.get_rect(midtop=(self.poli_dialog_rect2.centerx, self.poli_dialog_rect2.top + 50))
        self.poli_text_rect_5 = self.poli_dialog_text_surface_5.get_rect(midtop=(self.poli_dialog_rect2.centerx, self.poli_text_rect_4.bottom + 15))
        self.poli_text_rect_6 = self.poli_dialog_text_surface_6.get_rect(midtop=(self.poli_dialog_rect2.centerx, self.poli_text_rect_5.bottom + 15))
        self.poli_text_rect_7 = self.poli_dialog_text_surface_7.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_dialog_rect.top + 50))
        self.poli_text_rect_8 = self.poli_dialog_text_surface_8.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_text_rect_7.bottom + 15))
        self.poli_text_rect_9 = self.poli_dialog_text_surface_9.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_text_rect_8.bottom + 15))
        self.poli_text_rect_10 = self.poli_dialog_text_surface_10.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_dialog_rect.top + 50))
        self.poli_text_rect_11 = self.poli_dialog_text_surface_11.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_text_rect_10.bottom + 15))
        self.poli_text_rect_12 = self.poli_dialog_text_surface_12.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_text_rect_11.bottom + 15))
        self.poli_text_rect_13 = self.poli_dialog_text_surface_13.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_dialog_rect.top + 50))
        self.poli_text_rect_14 = self.poli_dialog_text_surface_14.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_text_rect_13.bottom + 15))
        self.poli_text_rect_15 = self.poli_dialog_text_surface_15.get_rect(midtop=(self.poli_dialog_rect.centerx, self.poli_text_rect_14.bottom + 15))

        #escaped room
        self.escaped_writing_1 = 'GRAZIE PER AVER GIOCATO'
        self.escaped_writing_2 = 'Structure Designer: Tommaso Faverio'
        self.escaped_writing_3 = 'Graphic designer: Anna Arcidiacono'
        self.escaped_writing_4 = 'Game designer: Simone Oliveri'
        self.escaped_writing_5 = 'Physics espert: Alex Filip'
        
        color = (255,255,255)
        font1 = self.dialog_font = pygame.font.SysFont('Honeymoon', 80) 
        font2 = self.dialog_font = pygame.font.SysFont('Honeymoon', 90) 
        self.escaped_writing_1_surface = font2.render(self.escaped_writing_1, True, (204,85,0))
        self.escaped_writing_2_surface = font1.render(self.escaped_writing_2, True, color)
        self.escaped_writing_3_surface = font1.render(self.escaped_writing_3, True, color)
        self.escaped_writing_4_surface = font1.render(self.escaped_writing_4, True, color)
        self.escaped_writing_5_surface = font1.render(self.escaped_writing_5, True, color)
        
        
        
        #question buttons and answers
        #room 1
        #first question box
        self.question_text_1_1 = "A temperatura costante se la"
        self.question_text_1_2 = "pressione si dimezza, il volume "
        self.question_text_1_3 = "di un gas perfetto:"
        self.q_text_1_1_surface = pygame.font.SysFont('Honeymoon', 60).render(self.question_text_1_1, True, (0,0,0))
        self.q_text_1_2_surface = pygame.font.SysFont('Honeymoon', 60).render(self.question_text_1_2, True, (0,0,0))
        self.q_text_1_3_surface = pygame.font.SysFont('Honeymoon', 60).render(self.question_text_1_3, True, (0,0,0))
        self.question_surface_1.blit(self.q_text_1_1_surface, (120, 40))
        self.question_surface_1.blit(self.q_text_1_2_surface, (120, 100))
        self.question_surface_1.blit(self.q_text_1_3_surface, (120, 160))
        #second question box
        self.question_text_1_1_5 = "La massa molare in alcuni casi"
        self.question_text_1_2_5 = "coincide con con la massa atomica, "
        self.question_text_1_3_5 = "in altri con la massa molecolare"
        self.q_text_1_1_5_surface = pygame.font.SysFont('Honeymoon', 50).render(self.question_text_1_1_5, True, (0,0,0))
        self.q_text_1_2_5_surface = pygame.font.SysFont('Honeymoon', 50).render(self.question_text_1_2_5, True, (0,0,0))
        self.q_text_1_3_5_surface = pygame.font.SysFont('Honeymoon', 50).render(self.question_text_1_3_5, True, (0,0,0))
        self.question_surface_1_5.blit(self.q_text_1_1_5_surface, (140, 280))
        self.question_surface_1_5.blit(self.q_text_1_2_5_surface, (140, 330))
        self.question_surface_1_5.blit(self.q_text_1_3_5_surface, (140, 380))
        
        self.q_button_1_width, self.q_button_1_height = 70, 70
        self.q_buttons_1_rects = []
        self.answer_1_1 = 'quadruplica'
        self.answer_1_2 = 'aumenta ma non raddoppia'
        self.answer_1_3 = 'raddoppia '
        self.answer_1_4 = 'nessuna delle precedenti'
        
        self.answers_1 = [self.answer_1_1, self.answer_1_2, self.answer_1_3, self.answer_1_4]
        for i in range(4):
            button_x = 100
            button_y = self.question_box_rect_1.y + i * 120 + 250
            button_surface = pygame.Surface((70,70))
            answer_surface = self.font1.render(self.answers_1[i], True, (0,0,0))
            self.question_surface_1.blit(button_surface, (button_x, button_y))
            self.question_surface_1.blit(answer_surface, (200 + self.question_box_rect_1.x, button_y + self.question_box_rect_1.y - 50 ))
            button_rect = pygame.Rect(button_x + self.question_box_rect_1.x, button_y + self.question_box_rect_1.y, self.q_button_1_width, self.q_button_1_height)
            self.q_buttons_1_rects.append(button_rect)  
        
        v_button_rect = pygame.Rect(355, 560, 70, 70)
        f_button_rect= pygame.Rect(755, 560, 70, 70)
        v_button_surface = pygame.Surface((70,70))
        v_button_surface.fill((0,255,0))
        f_button_surface = pygame.Surface((70,70))
        f_button_surface.fill((255,0,0))
        self.question_surface_1_5.blit(v_button_surface, (255,510))
        self.question_surface_1_5.blit(f_button_surface, (655, 510))
        self.vf_buttons_rects = [v_button_rect, f_button_rect]
        
        
        #room 2
        #question text
        self.question_text_2_1 = "Un sistema chiuso e' "
        self.question_text_2_2 = "definito tale "
        self.q_text_2_1_surface = pygame.font.SysFont('Honeymoon', 70).render(self.question_text_2_1, True, (0,0,0))
        self.q_text_2_2_surface = pygame.font.SysFont('Honeymoon', 70).render(self.question_text_2_2, True, (0,0,0))
        self.question_surface_2.blit(self.q_text_2_1_surface, (120, 100))
        self.question_surface_2.blit(self.q_text_2_2_surface, (120, 170))
        
        self.question_text_2_1_5 = "Due quantità di gas perfetti uguali si trovano allo stesso"
        self.question_text_2_2_5 = "stato. Uno si espande a pressione costante l'altro a temperatura"
        self.question_text_2_3_5 = "costante. Alla fine quale dei due avra' energia interna maggiore?"
        self.q_text_2_1_5_surface = pygame.font.SysFont('Honeymoon', 28).render(self.question_text_2_1_5, True, (0,0,0))
        self.q_text_2_2_5_surface = pygame.font.SysFont('Honeymoon', 28).render(self.question_text_2_2_5, True, (0,0,0))
        self.q_text_2_3_5_surface = pygame.font.SysFont('Honeymoon', 28).render(self.question_text_2_3_5, True, (0,0,0))
        self.question_surface_2_5.blit(self.q_text_2_1_5_surface, (25, 80))
        self.question_surface_2_5.blit(self.q_text_2_2_5_surface, (25, 110))
        self.question_surface_2_5.blit(self.q_text_2_3_5_surface, (25, 140))

        self.q_button_2_width, self.q_button_2_height = 60, 60
        self.q_buttons_2_rects = []
        self.q_buttons_2_5_rects = []
        self.answer_2_1 = "Non scambia ne energia ne materia con l'esterno"
        self.answer_2_2 = "Scambia materia ma non energia con l'esterno"
        self.answer_2_3 = "Scambia sia materia che energia con l'esterno"
        self.answer_2_4 = 'Nessuna delle precedenti'
        self.answer_2_5 = 'Il secondo'
        self.answer_2_6 = 'Il primo'
        self.answer_2_7 = 'Hanno la stessa energia interna'
        self.answer_2_8 = 'Nessuna delle precedenti'
        self.answers_2 = [self.answer_2_1, self.answer_2_2, self.answer_2_3, self.answer_2_4, self.answer_2_5, self.answer_2_6, self.answer_2_7, self.answer_2_8]
        for i in range(4):
            button_x = 70
            button_y = self.question_box_rect_2.y + 250 + (i * 100)
            button_surface = pygame.Surface((60,60))
            answer_surface = pygame.font.SysFont('Honeymoon', 28).render(self.answers_2[i], True, (0,0,0))
            self.question_surface_2.blit(button_surface, (button_x, button_y))
            self.question_surface_2.blit(answer_surface, (180, button_y + 15 ))
            button_rect = pygame.Rect(button_x + self.question_box_rect_2.x, button_y + 100, self.q_button_2_width, self.q_button_2_height)
            self.q_buttons_2_rects.append(button_rect)
        for i in range(4):
            button_x = 70
            button_y = self.question_box_rect_2.y + 250 + (i * 100)
            button_surface = pygame.Surface((60,60))
            answer_surface = pygame.font.SysFont('Honeymoon', 35).render(self.answers_2[i+4], True, (0,0,0))
            self.question_surface_2_5.blit(button_surface, (button_x, button_y))
            self.question_surface_2_5.blit(answer_surface, (200, button_y ))
            button_rect = pygame.Rect(button_x + self.question_box_rect_2.x, button_y + 100, self.q_button_2_width, self.q_button_2_height)
            self.q_buttons_2_5_rects.append(button_rect)
        
        #room3 
        #question text
        self.question_text_3_1 = "Un gas perfetti si espande isotermicamente"
        self.question_text_3_2 = "dallo stato A allo stato B."
        self.question_text_3_3 = "Quale affermazione è sbagliata? "
        self.q_text_3_1_surface = pygame.font.SysFont('Honeymoon', 34).render(self.question_text_3_1, True, (0,0,0))
        self.q_text_3_2_surface = pygame.font.SysFont('Honeymoon', 34).render(self.question_text_3_2, True, (0,0,0))
        self.q_text_3_3_surface = pygame.font.SysFont('Honeymoon', 34).render(self.question_text_3_3, True, (0,0,0))
        self.question_surface_3.blit(self.q_text_3_1_surface, (40, 120))
        self.question_surface_3.blit(self.q_text_3_2_surface, (40, 180))
        self.question_surface_3.blit(self.q_text_3_3_surface, (40, 240))
        #question text 2
        self.question_text_3_1_5 = "Se un gas passa dallo stato (p1,V1,T1)"
        self.question_text_3_2_5 = "allo stato (p2,V2,T2) mediante."
        self.question_text_3_3_5 = "una trasformazione isobara allora:"
        self.q_text_3_1_5_surface = pygame.font.SysFont('Honeymoon', 35).render(self.question_text_3_1_5, True, (0,0,0))
        self.q_text_3_2_5_surface = pygame.font.SysFont('Honeymoon', 35).render(self.question_text_3_2_5, True, (0,0,0))
        self.q_text_3_3_5_surface = pygame.font.SysFont('Honeymoon', 35 ).render(self.question_text_3_3_5, True, (0,0,0))
        self.question_surface_3_5.blit(self.q_text_3_1_5_surface, (45, 120))
        self.question_surface_3_5.blit(self.q_text_3_2_5_surface, (45, 180))
        self.question_surface_3_5.blit(self.q_text_3_3_5_surface, (45, 240))
        
        self.q_button_3_width, self.q_button_3_height = 60, 60
        self.q_buttons_3_rects = []
        self.q_buttons_3_5_rects = []
        self.answer_3_1 = "Il gas cede calore all'ambiente"
        self.answer_3_2 = 'La temperatura del gas rimane costante'
        self.answer_3_3 = "L'energia interna del gas rimane costante"
        self.answer_3_4 = 'Il lavoro che compie il gas è positivo'
        self.answer_3_5 = 'V1/p = V2/p'
        self.answer_3_6 = 'V1*T1 = V2*T2'
        self.answer_3_7 = 'V1*T2 = V2*T1'
        self.answer_3_8 = 'V1/T1 = V2/T1'
        
        self.answers_3 = [self.answer_3_1, self.answer_3_2, self.answer_3_3, self.answer_3_4, self.answer_3_5, self.answer_3_6, self.answer_3_7, self.answer_3_8]
        for i in range(4):
            button_x = 60
            button_y = self.question_box_rect_3.y + 250 + (i * 100)
            button_surface = pygame.Surface((60,60))
            answer_surface = pygame.font.SysFont('Honeymoon', 28).render(self.answers_3[i], True, (0,0,0))
            self.question_surface_3.blit(button_surface, (button_x, button_y))
            self.question_surface_3.blit(answer_surface, (155, button_y + 15 ))
            button_rect = pygame.Rect(button_x + self.question_box_rect_3.x, button_y + 100, self.q_button_3_width, self.q_button_3_height)
            self.q_buttons_3_rects.append(button_rect)
        for i in range(4):
            button_x = 70
            button_y = self.question_box_rect_3.y + 250 + (i * 100)
            button_surface = pygame.Surface((60,60))
            answer_surface = self.font3.render(self.answers_3[i+4], True, (0,0,0))
            self.question_surface_3_5.blit(button_surface, (button_x, button_y))
            self.question_surface_3_5.blit(answer_surface, (200, button_y ))
            button_rect = pygame.Rect(button_x + self.question_box_rect_3.x, button_y + 100, self.q_button_3_width, self.q_button_3_height)
            self.q_buttons_3_5_rects.append(button_rect)
        
        #room4
        #question text
        self.question_text_4_1 = "Cosa su intende per funzione di stato?"
        self.q_text_4_1_surface = pygame.font.SysFont('Honeymoon', 75).render(self.question_text_4_1, True, (0,0,0))
        self.question_surface_4.blit(self.q_text_4_1_surface, (100, 100))
        
        self.q_button_4_width, self.q_button_4_height = 60, 60
        self.q_buttons_4_rects = []
        self.answer_4_1 = "E' una proprietà che dipende solo dal modo in cui si è determinato un sistema"
        self.answer_4_2 = "E' una proprietà che dipende solo dallo stato in cui si trova il sistema e non dal modo in cui esso è si determinato"
        self.answer_4_3 = "E' una proprietà che non dipende dello stato in cui si trova il sistema"
        self.answer_4_4 = "E' una funzione di una reazione chimica"
        
        self.answers_4 = [self.answer_4_1, self.answer_4_2, self.answer_4_3, self.answer_4_4]
        for i in range(4):
            button_x = 50
            button_y = self.question_box_rect_4.y + i * 80 + 180
            button_surface = pygame.Surface((50,50))
            answer_surface = pygame.font.SysFont('Honeymoon', 26).render(self.answers_4[i], True, (0,0,0))
            self.question_surface_4.blit(button_surface, (button_x, button_y))
            self.question_surface_4.blit(answer_surface, (self.question_box_rect_4.x - 110, button_y + 15))
            button_rect = pygame.Rect(button_x + self.question_box_rect_4.x, button_y + self.question_box_rect_4.y, self.q_button_4_width, self.q_button_4_height)
            self.q_buttons_4_rects.append(button_rect)  
        
        #room 5
        #question text
        self.question_text_5_1 = "Il primo principio della "
        self.question_text_5_2 = "termodinamica afferma che: "
        self.q_text_5_1_surface = pygame.font.SysFont('Honeymoon', 50).render(self.question_text_5_1, True, (0,0,0))
        self.q_text_5_2_surface = pygame.font.SysFont('Honeymoon', 50).render(self.question_text_5_2, True, (0,0,0))
        self.question_surface_5.blit(self.q_text_5_1_surface, (50, 100))
        self.question_surface_5.blit(self.q_text_5_2_surface, (50, 170))
        
        self.q_button_5_width, self.q_button_5_height = 50, 50
        self.q_buttons_5_rects = []
        self.answer_5_1 = 'La variazione di calore di una' 
        self.answer_5_1_5 = 'reazione è costante nel tempo'
        self.answer_5_2 = 'Qualunque sistema isolato tende spontaneamente'
        self.answer_5_2_5 = 'ad aumentare il suo grado di disordine'
        self.answer_5_3 = 'La variazione di energia interna di un sistema e data'
        self.answer_5_3_5 = 'dalla somma delle quantità di calore e lavolo del sitema'
        self.answer_5_4 = 'Nessuna delle precedenti'
    
        self.answers_5_1 = [self.answer_5_1, self.answer_5_2,  self.answer_5_3, self.answer_5_4]
        self.answers_5_2 = [self.answer_5_1_5, self.answer_5_2_5,  self.answer_5_3_5]
        
        for i in range(4):
            button_x = 30
            button_y = self.question_box_rect_5.top + 200 + i*80
            answer_surface = pygame.font.SysFont('Honeymoon', 25).render(self.answers_5_1[i], True, (0,0,0))
            button_surface = pygame.Surface((50,50))
            self.question_surface_5.blit(button_surface, (button_x, button_y))
            button_rect = pygame.Rect(button_x + self.question_box_rect_5.x, button_y + 100, self.q_button_5_width, self.q_button_5_height)
            self.question_surface_5.blit(answer_surface, (90, button_y ))
            self.q_buttons_5_rects.append(button_rect)
            
        for i in range(3):
            button_x = 30
            button_y = self.question_box_rect_5.top + 230 + i*80
            answer_surface = pygame.font.SysFont('Honeymoon', 25).render(self.answers_5_2[i], True, (0,0,0))
            self.question_surface_5.blit(answer_surface, (90, button_y ))
            
        #room 6
        #first question box
        self.question_text_6_1 = "Un gas perfetto X e' costituito da particelle"
        self.question_text_6_2 = "di massa m ed energia cinetica media Ec. Un'altro"
        self.question_text_6_3 = "gas perfetto Y e' costituito da particelle di massa 4m ed"
        self.question_text_6_4 = "energia cinetica media 2Ec. Se la temperatura assoluta del gas"
        self.question_text_6_5 = "e' 200 K, qual e' la temperatura assoluta del gas Y?"

        self.q_text_6_1_surface = pygame.font.SysFont('Honeymoon', 30).render(self.question_text_6_1, True, (0,0,0))
        self.q_text_6_2_surface = pygame.font.SysFont('Honeymoon', 30).render(self.question_text_6_2, True, (0,0,0))
        self.q_text_6_3_surface = pygame.font.SysFont('Honeymoon', 30).render(self.question_text_6_3, True, (0,0,0))
        self.q_text_6_4_surface = pygame.font.SysFont('Honeymoon', 30).render(self.question_text_6_4, True, (0,0,0))
        self.q_text_6_5_surface = pygame.font.SysFont('Honeymoon', 30).render(self.question_text_6_5, True, (0,0,0))

        self.question_surface_6.blit(self.q_text_6_1_surface, (30, 90))
        self.question_surface_6.blit(self.q_text_6_2_surface, (30, 130))
        self.question_surface_6.blit(self.q_text_6_3_surface, (30, 170))
        self.question_surface_6.blit(self.q_text_6_4_surface, (30, 210))
        self.question_surface_6.blit(self.q_text_6_5_surface, (30, 250))
        
        self.q_button_6_width, self.q_button_6_height = 60, 60
        self.q_buttons_6_rects = []
        self.answer_6_1 = '800K'
        self.answer_6_2 = '100K'
        self.answer_6_3 = '50K'
        self.answer_6_4 = '400K'
    
        self.answers_6 = [self.answer_6_1, self.answer_6_2, self.answer_6_3, self.answer_6_4]
        for i in range(4):
            button_x = 70
            button_y = self.question_box_rect_6.y + 350 + (i * 100)
            button_surface = pygame.Surface((60,60))
            answer_surface = self.font3.render(self.answers_6[i], True, (0,0,0))
            self.question_surface_6.blit(button_surface, (button_x, button_y))
            self.question_surface_6.blit(answer_surface, (200, button_y ))
            button_rect = pygame.Rect(button_x + self.question_box_rect_6.x, button_y + 100, self.q_button_6_width, self.q_button_6_height)
            self.q_buttons_6_rects.append(button_rect)
        
        #room 7
        #question text
        self.question_text_7_1 = "Una data quantita' di gas perfetto, a partire da uno stato di equilibrio, subisce una trasformazione"
        self.question_text_7_2 = "sino a raggiungere un nuovo stato di equilibrio in cui csia il volume sia la temperatura sono il doppio"
        self.question_text_7_3 = "di quelle iniziali. Quale affermazione è corretta?"
        self.q_text_7_1_surface = pygame.font.SysFont('Honeymoon', 32).render(self.question_text_7_1, True, (0,0,0))
        self.q_text_7_2_surface = pygame.font.SysFont('Honeymoon', 32).render(self.question_text_7_2, True, (0,0,0))
        self.q_text_7_3_surface = pygame.font.SysFont('Honeymoon', 32).render(self.question_text_7_3, True, (0,0,0))
        self.question_surface_7.blit(self.q_text_7_1_surface, (70, 100))
        self.question_surface_7.blit(self.q_text_7_2_surface, (70, 150))
        self.question_surface_7.blit(self.q_text_7_3_surface, (70, 200))
        #question text 2
        self.question_text_7_1_5 = "L'aria (y = 1,4) al termine di una trasformazione adiabatica occupa un volume di 350cm^3"
        self.question_text_7_2_5 = "con una pressione di 2,80 bar. Se inizialmente la pressione valeva 1.25*10^5 Pa, qual e'"
        self.question_text_7_3_5 = "il volume iniziale, considerando l'aria  come se fosse un gas perfetto ?"
        self.q_text_7_1_5_surface = pygame.font.SysFont('Honeymoon', 33).render(self.question_text_7_1_5, True, (0,0,0))
        self.q_text_7_2_5_surface = pygame.font.SysFont('Honeymoon', 33).render(self.question_text_7_2_5, True, (0,0,0))
        self.q_text_7_3_5_surface = pygame.font.SysFont('Honeymoon', 33).render(self.question_text_7_3_5, True, (0,0,0))
        self.question_surface_7_5.blit(self.q_text_7_1_5_surface, (90, 100))
        self.question_surface_7_5.blit(self.q_text_7_2_5_surface, (90, 150))
        self.question_surface_7_5.blit(self.q_text_7_3_5_surface, (90, 200))
        
        self.question_text_7_1 = "Il primo principio della "
        self.question_text_7_2 = "termodinamica afferma che: "
        self.q_text_5_1_surface = pygame.font.SysFont('Honeymoon', 50).render(self.question_text_5_1, True, (0,0,0))
        self.q_text_5_2_surface = pygame.font.SysFont('Honeymoon', 50).render(self.question_text_5_2, True, (0,0,0))
        self.question_surface_5.blit(self.q_text_5_1_surface, (50, 100))
        self.question_surface_5.blit(self.q_text_5_2_surface, (50, 170))
        
        self.q_button_7_width, self.q_button_7_height = 50, 50
        self.q_buttons_7_rects = []
        self.answer_7_1 = "Nessuna delle altre affermazioni e' corretta" 
        self.answer_7_2 = "Dato che il volume e' raddoppiato, la pressione"
        self.answer_7_2_b = "finale e' la meta' di quella iniziale"
        self.answer_7_3 = "Dato che la temperatura del gas e' raddoppiata,"
        self.answer_7_3_b = "la pressione finale e' il doppio di quella iniziale"
        self.answer_7_4 = "Sono necessari ulteriori dati sulla trasformazione"
        self.answer_7_4_b = "per poter rispondere"
        
        self.answers_7_1 = [self.answer_7_1, self.answer_7_2,  self.answer_7_3, self.answer_7_4]
        self.answers_7_1_b = [self.answer_7_2_b, self.answer_7_3_b,  self.answer_7_4_b]
        
        for i in range(4):
            button_x = 50
            button_y = self.question_box_rect_7.top + 200 + i*85
            answer_surface = pygame.font.SysFont('Honeymoon', 35).render(self.answers_7_1[i], True, (0,0,0))
            button_surface = pygame.Surface((50,50))
            self.question_surface_7.blit(button_surface, (button_x, button_y))
            button_rect = pygame.Rect(button_x + self.question_box_rect_7.x, button_y + 70, self.q_button_7_width, self.q_button_7_height)
            self.question_surface_7.blit(answer_surface, (120, button_y ))
            self.q_buttons_7_rects.append(button_rect)
            
        for i in range(1,4):
            button_x = 50
            button_y = self.question_box_rect_7.top + 240 + i*85
            answer_surface = pygame.font.SysFont('Honeymoon', 35).render(self.answers_7_1_b[i-1], True, (0,0,0))
            self.question_surface_7.blit(answer_surface, (120, button_y ))
        
        self.q_button_7_5_width, self.q_button_7_5_height = 50, 50
        self.q_buttons_7_5_rects = []
        self.answer_7_1_5 = "784 cm^3" 
        self.answer_7_2_5 = "197 cm^3"
        self.answer_7_3_5 = "156 cm^3 "
        self.answer_7_4_5 = "623 cm^3"
        
        self.answers_7_1_5 = [self.answer_7_1_5, self.answer_7_2_5,  self.answer_7_3_5, self.answer_7_4_5]
        
        for i in range(4):
            button_x = 50
            button_y = self.question_box_rect_7.top + 200 + i*85
            answer_surface = pygame.font.SysFont('Honeymoon', 35).render(self.answers_7_1_5[i], True, (0,0,0))
            button_surface = pygame.Surface((50,50))
            self.question_surface_7_5.blit(button_surface, (button_x, button_y))
            button_rect = pygame.Rect(button_x + self.question_box_rect_7.x, button_y + 70, self.q_button_7_5_width, self.q_button_7_5_height)
            self.question_surface_7_5.blit(answer_surface, (120, button_y ))
            self.q_buttons_7_5_rects.append(button_rect)
        
        # Animation variables
        self.fade_animation_running = True
        self.fade_alpha = 0
        self.fade_alpha_increment = 1

    # set up states and update screen
    def setup_states(self):
        self.STATE_INTRODUCTION = 0
        self.STATE_FIRSTROOM = 1
        self.STATE_SECONDROOM = 2
        self.STATE_THIRDROOM = 3
        self.STATE_FOURTHROOM = 4
        self.STATE_FIFTHROOM = 5
        self.STATE_SIXTHROOM = 6
        self.STATE_SEVENTHROOM = 7
        self.STATE_ESCAPED = 8
        self.current_state = self.STATE_SEVENTHROOM
    
    def update_state(self, state):
        self.current_state = state
        self.active_buttons = True
        self.fade_animation_running = True
        self.question_box_state = False
        self.second_question_state = False
        self.fade_out_animation()
            


    def update_screen(self):
        #draw rooms
        if self.current_state == self.STATE_INTRODUCTION:
            self.draw_introduction()
        elif self.current_state == self.STATE_FIRSTROOM:
            self.draw_first_room()
        elif self.current_state == self.STATE_SECONDROOM:
            self.draw_second_room()
        elif self.current_state == self.STATE_THIRDROOM:
            self.draw_third_room()
        elif self.current_state == self.STATE_FOURTHROOM:
            self.draw_fourth_room()
        elif self.current_state == self.STATE_FIFTHROOM:
            self.draw_fifth_room()
        elif self.current_state == self.STATE_SIXTHROOM:
            self.draw_sixth_room()
        elif self.current_state == self.STATE_SEVENTHROOM:
            self.draw_seventh_room()
        elif self.current_state == self.STATE_ESCAPED:
            self.draw_escaped()
            
        #update timer
        self.update_timer()
            
        
        
    # handle events, keys and mouse click
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_press(event)

    def handle_mouse_click(self, event):
        if self.current_state == self.STATE_INTRODUCTION:
            self.handle_mouse_click_introduction(event)
        elif self.current_state == self.STATE_FIRSTROOM:
            self.handle_mouse_click_firstroom(event)
        elif self.current_state == self.STATE_SECONDROOM:
            self.handle_mouse_click_secondroom(event)
        elif self.current_state == self.STATE_THIRDROOM:
            self.handle_mouse_click_thirdroom(event)
        elif self.current_state == self.STATE_FOURTHROOM:
            self.handle_mouse_click_fourthroom(event)
        elif self.current_state == self.STATE_FIFTHROOM:
            self.handle_mouse_click_fifthroom(event)
        elif self.current_state == self.STATE_SIXTHROOM:
            self.handle_mouse_click_sixthroom(event)
        elif self.current_state == self.STATE_SEVENTHROOM:
            self.handle_mouse_click_seventhroom(event)
    
    def handle_key_press(self, event):
        if self.current_state == self.STATE_SECONDROOM and self.codice_state == True and self.cassaforte_zoom_state:
            if event.key == pygame.K_RETURN:
                self.check_code()
            elif event.key == pygame.K_BACKSPACE:
                self.codice_inserito = self.codice_inserito[:-1]
            else:
                self.codice_inserito += event.unicode
        
        if self.current_state == self.STATE_THIRDROOM and self.question_box_state == False:
            if event.key == pygame.K_SPACE:
                self.question_box_state = True
        
        if self.current_state == self.STATE_FIFTHROOM and self.ipad_codice_state and self.lucchetto_zoom_state:
            if event.key == pygame.K_RETURN:
                self.ipad_check_code()
            elif event.key == pygame.K_BACKSPACE:
                self.ipad_codice_inserito = self.ipad_codice_inserito[:-1]
            else:
                self.ipad_codice_inserito += event.unicode
        
        if self.current_state == self.STATE_SEVENTHROOM:
            if event.key == pygame.K_SPACE:
                if self.poli_first_dialog_state:
                    self.poli_first_dialog_state = False
                    self.poli_second_dialog_state = True
                elif self.poli_second_dialog_state:
                    self.poli_second_dialog_state = False
                    self.poli_third_dialog_state = True
                elif self.poli_third_dialog_state:
                    self.poli_third_dialog_state = False
                    self.question_box_state = True
                elif self.poli_fourth_dialog_state:
                    self.poli_fourth_dialog_state = False
                    self.question_box_state = True
                
        
        if event.key == pygame.K_f:
            pygame.display.toggle_fullscreen()
        if event.key == pygame.K_k:
            self.quit_game()
        
            

    def handle_mouse_click_introduction(self, event):
        if event.button == 1: #left click mouse
            if self.door_rect.collidepoint(event.pos):
                self.update_state(self.STATE_FIRSTROOM)
                self.active_timer = True
    
    def handle_mouse_click_firstroom(self, event):
        if event.button == 1:
            if self.calorifero_state == 0:
                if self.regolatore_rect.collidepoint(event.pos):
                    self.question_box_state = True
                elif self.question_box_state:
                    if not self.question_box_rect_1.collidepoint(event.pos):
                        self.question_box_state = False
                    else:
                        self.buttons_collision(self.q_buttons_1_rects, event)
            elif self.calorifero_state == 2:
                if self.question_box_state == True:
                    self.buttons_collision(self.vf_buttons_rects, event)
                    
                        
    def handle_mouse_click_secondroom(self, event):
        if event.button == 1:
            if self.cassaforti_rect_1.collidepoint(event.pos):
                self.cassaforte_zoom_state = True
                self.question_box_state = True
            elif self.question_box_state:
                    if not self.question_box_rect_2.collidepoint(event.pos) and not self.cassaforti_rect_2.collidepoint(event.pos):
                        self.question_box_state = False
                        self.cassaforte_zoom_state = False
                    else:
                        self.buttons_collision(self.q_buttons_2_rects, event)
    
    def handle_mouse_click_thirdroom(self, event):
        if event.button == 1:
            if self.question_box_state:
                    if not self.question_box_rect_3.collidepoint(event.pos):
                        self.question_box_state = False
                    else:
                        self.buttons_collision(self.q_buttons_3_rects, event)
    
    def handle_mouse_click_fourthroom(self, event):
        if event.button == 1:
            if self.pannello_controllo_rect.collidepoint(event.pos):
                self.question_box_state = True
            elif self.question_box_state:
                if not self.question_box_rect_4.collidepoint(event.pos):
                    self.question_box_state = False
                else:
                    self.buttons_collision(self.q_buttons_4_rects, event)
        
    def handle_mouse_click_fifthroom(self, event):
        if event.button == 1:
            if self.ipad_rect.collidepoint(event.pos) and not self.lucchetto_zoom_state:
                self.ipad_zoom_state = True
                self.question_box_state = True
            elif self.question_box_state and self.ipad_zoom_state:
                    if not self.ipad_zoomed_rect.collidepoint(event.pos):
                        self.question_box_state = False
                        self.ipad_zoom_state = False
                    else:
                        self.buttons_collision(self.q_buttons_5_rects, event)
            elif self.ipad_codice_state and not self.ipad_zoom_state:
                if not self.lucchetto_zoom_state and self.lucchetto_rect.collidepoint(event.pos):
                    self.lucchetto_zoom_state = True
                else:
                    self.lucchetto_zoom_state = False
    
    def handle_mouse_click_sixthroom(self, event):
        if event.button == 1:
            if self.termostato_rect.collidepoint(event.pos):
                self.question_box_state = True
            elif self.question_box_state:
                if not self.question_box_rect_6.collidepoint(event.pos):
                    self.question_box_state = False
                else:
                    self.buttons_collision(self.q_buttons_6_rects, event)
    
    def handle_mouse_click_seventhroom(self, event):
        if event.button == 1:
            if not self.question_box_rect_7.collidepoint(event.pos):
                    if not self.second_question_state:
                        self.question_box_state = False
                        self.poli_third_dialog_state = True
                    else:
                        self.question_box_state = False
                        self.poli_fourth_dialog_state = True
            else:
                self.buttons_collision(self.q_buttons_7_rects, event)
                    

    def inserisci_codice(self):
        self.codice_state = True
        self.active_buttons = False
        self.question_surface_inner_2.fill((255,255,255))
        self.question_surface_2_5.blit(self.question_surface_inner_2, (10,10))
        self.question_surface_2_5.blit(self.codice_writing1_surface, (self.question_surface_2_5.get_width()/2 - self.codice_writing1_surface.get_width()/2, 300))
        self.question_surface_2_5.blit(self.codice_writing2_surface, (self.question_surface_2_5.get_width()/2 - self.codice_writing2_surface.get_width()/2, 500))
        self.cassaforti_2_surface.blit(self.codice_surface, (120,130)) 
    
    def inserisci_codice_ipad(self):
        self.ipad_codice_state = True
        self.active_buttons = False
        self.question_surface_5.fill((0,0,0,0))
        self.question_surface_5.blit(self.ipad_codice_surface, (self.question_surface_5.get_width()/2 - self.ipad_codice_surface.get_width()/2, 300))
        
    
    def check_code(self):
        if self.codice_inserito == self.codice:
            self.second_room_end_transition()
        else:
            self.codice_surface.fill((255,0,0))
            screen.blit(self.codice_surface, (220,340)) 
            pygame.display.update()
            pygame.time.delay(800)
            self.codice_surface.fill((0,255,0))
            
            
    
    def ipad_check_code(self):
        if self.ipad_codice_inserito == self.ipad_codice:
            self.fifth_room_end_transition()
        else:
            self.ipad_codice_surface_inserire.fill((255,0,0))
            screen.blit(self.ipad_codice_surface_inserire, (300,300))
            pygame.display.update()
            pygame.time.delay(800)
            self.ipad_codice_surface_inserire.fill((0,255,0))
    
    def buttons_collision(self, buttons_rects, event):
        if self.active_buttons:
            for j,button_rect in enumerate(buttons_rects):
                if self.current_state == self.STATE_FIRSTROOM:
                    if self.calorifero_state == 0:
                        if button_rect.collidepoint(event.pos):
                            if j == 2:
                                self.calorifero_transition_1(0)
                            else:
                                self.calorifero_transition_2()
                    elif self.calorifero_state == 2:
                        if button_rect.collidepoint(event.pos):
                            if j == 0:
                                self.calorifero_transition_1(1)
                            elif j == 1:
                                self.timer -= 180
                                self.calorifero_transition_1(1)
                                
                elif self.current_state == self.STATE_SECONDROOM:
                    if self.second_question_state == False:
                        if button_rect.collidepoint(event.pos):
                            if j == 3:
                                self.second_question_state = True
                                self.second_room_q_transition(0)
                            else:
                                self.second_question_state = False
                                self.timer -= 30
                                self.second_room_q_transition(1)
                    elif self.second_question_state == True:
                        if button_rect.collidepoint(event.pos):
                            if j == 1:
                                self.second_room_q_transition(0)
                                self.inserisci_codice()
                            else:
                                self.timer -= 30
                                self.second_room_q_transition(1)
                
                elif self.current_state == self.STATE_THIRDROOM:
                    if self.second_question_state == False:
                        if button_rect.collidepoint(event.pos):
                            if j == 0:
                                self.second_question_state = True 
                                self.third_room_transition(0)
                            else:
                                self.second_question_state = False
                                self.timer -= 30
                                self.third_room_transition(1)
                    else:
                        if button_rect.collidepoint(event.pos):
                            if j == 2:
                                self.second_question_state = False
                                self.third_room_transition(0)
                                self.third_room_end_transition()
                            else:
                                self.timer -= 30
                                self.second_question_state = True
                                self.third_room_transition(1)
                
                elif self.current_state == self.STATE_FOURTHROOM:
                    if button_rect.collidepoint(event.pos):
                        if j == 1:
                            self.fourth_room_transition(0)
                            self.fourth_room_end_transition()
                        else:
                            self.timer -= 60
                            self.fourth_room_transition(1)
                        
                elif self.current_state == self.STATE_FIFTHROOM:
                    if button_rect.collidepoint(event.pos):
                        if j == 3:
                            self.fifth_room_transition(0)
                            self.inserisci_codice_ipad()
                        else:
                            self.timer -= 60
                            self.fifth_room_transition(1)
                            
                elif self.current_state == self.STATE_SIXTHROOM:
                    if button_rect.collidepoint(event.pos):
                        if j == 3:
                            self.sixth_room_transition(0)
                            self.sixth_room_end_transition()
                        else:
                            self.timer -= 60
                            self.sixth_room_transition(1)
                
                elif self.current_state == self.STATE_SEVENTHROOM:
                    if button_rect.collidepoint(event.pos):
                        if not self.second_question_state:
                            if j ==0:
                                self.seventh_room_transition(0)
                                self.second_question_state = True
                                self.question_box_state = False
                                self.poli_third_dialog_state = False
                                self.poli_fourth_dialog_state = True
                            else:
                                self.timer -= 60
                                self.seventh_room_transition(1)
                        else:
                            if j == 3:
                                self.seventh_room_transition(0)
                                self.poli_third_dialog_state = False
                                self.poli_end_dialog_state = True
                                self.seventh_room_end_transition()
                            else:
                                self.timer -= 75
                                self.seventh_room_transition(1)
                
            
                            
                            

    # drawing room


    def fade_out_animation(self):
        while self.fade_animation_running:
            if self.fade_alpha <= 255:
                fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
                fade_surface.fill((0, 0, 0, self.fade_alpha))
                screen.blit(fade_surface, (0, 0))
                self.fade_alpha += self.fade_alpha_increment
                pygame.display.flip()
            else:
                self.fade_animation_running = False
                self.fade_alpha = 0

    def draw_introduction(self):
        screen.blit(self.introduction_surface, (0,0)) 

        # Render text with the current scale
        font = self.font2
        text_surface = pygame.transform.rotozoom(font.render(self.door_text, True, (204,85,0)), 0, self.current_scale)
        text_rect = text_surface.get_rect(center=(765, 500))  # Centering text on the door
        screen.blit(text_surface, text_rect)

        # Adjust scale for the next frame
        if self.growing:
            self.current_scale += self.scale_increment
            if self.current_scale >= self.max_scale:
                self.growing = False
        else:
            self.current_scale -= self.scale_increment
            if self.current_scale <= self.min_scale:
                self.growing = True

    def draw_first_room(self):
        if self.calorifero_state == 0:
            screen.blit(self.calorifero_rosso_surface, (0,0))
            if self.question_box_state:
                screen.blit(self.question_surface_1, (100,50))
        elif self.calorifero_state == 1:
            screen.blit(self.calorifero_verde_surface, (0,0))
            pygame.display.flip()
            pygame.time.delay(1400)
            self.update_state(self.STATE_SECONDROOM)
        elif self.calorifero_state == 2:
            screen.blit(self.calorifero_fuoco_surface, (0,0))
            if self.question_box_state == True:
                screen.blit(self.question_surface_1_5, (100,50))
            
            
    def calorifero_transition_1(self, type):
        self.question_box_state = False
        if type == 0:
            self.question_surface_inner_1.fill((0,255,0))
            screen.blit(self.question_surface_inner_1, (110,60))
        elif type == 1:
            self.question_surface_inner_1_5.fill((0,255,0))
            screen.blit(self.question_surface_inner_1_5, (110,60))
        pygame.display.flip()
        pygame.time.delay(1000)
        screen.blit(self.calorifero_rosso_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(1400)
        self.calorifero_state = 1
        
    
    def calorifero_transition_2(self):
        self.question_box_state = False
        self.question_surface_inner_1.fill((255,0,0))
        screen.blit(self.question_surface_inner_1, (110,60))
        pygame.display.flip()
        pygame.time.delay(1000)
        screen.blit(self.calorifero_rosso_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(1400)
        screen.blit(self.calorifero_fuoco_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(2000)
        self.question_box_state = True
        self.calorifero_state = 2
    
        
    
    def draw_second_room(self):
        screen.blit(self.cassaforti_1_surface, (0,0))
        if self.cassaforte_zoom_state and self.question_box_state:
            screen.blit(self.cassaforti_2_surface, (100,210))
            codice_inserito = self.font3.render(self.codice_inserito,True, (0,0,0))
            screen.blit(codice_inserito, (225, 345))
            if not self.second_question_state: 
                screen.blit(self.question_surface_2, (900,100))
            else:
                screen.blit(self.question_surface_2_5, (900, 100))
                
    def second_room_q_transition(self, answer):
        if answer == 0:
            self.question_surface_inner_2.fill((0,255,0))
            screen.blit(self.question_surface_inner_2, (910, 110))
            pygame.display.flip()
            pygame.time.delay(1000)
        elif answer == 1:
            self.question_surface_inner_2.fill((255,0,0))
            screen.blit(self.question_surface_inner_2, (910, 110))
            pygame.display.flip()
            pygame.time.delay(700)
        
    def second_room_end_transition(self):
        screen.blit(self.cassaforti_1_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(1000)
        self.update_state(self.STATE_THIRDROOM)
        
    
    def draw_third_room(self):
        screen.blit(self.pugnetti_surface, (0,0))
        if self.question_box_state == True:
            if not self.second_question_state:
                screen.blit(self.question_surface_3, (60, 100))
            else:
                screen.blit(self.question_surface_3_5, (60, 100))
        
        self.draw_third_room_dialog()
        
    def draw_third_room_dialog(self):
        if self.question_box_state == False:
            pygame.draw.rect(screen, (255,255,255), self.pugnetti_dialog_rect, border_radius= 20)
            screen.blit(self.dialog_text_surface_1, self.pugnetti_text_rect_1)
            screen.blit(self.dialog_text_surface_2, self.pugnetti_text_rect_2)
            screen.blit(self.dialog_text_surface_3, self.pugnetti_text_rect_3)
        if self.second_question_state == True:
            pygame.draw.rect(screen, (255,255,255), self.pugnetti_dialog_rect, border_radius= 20)
            screen.blit(self.dialog_text_surface_4, self.pugnetti_text_rect_4)
            screen.blit(self.dialog_text_surface_5, self.pugnetti_text_rect_5)

    def third_room_transition(self, answer):
        if answer == 0:
            self.question_surface_inner_3.fill((0,255,0))
            screen.blit(self.question_surface_inner_3, (70, 110))
            pygame.display.flip()
            pygame.time.delay(1000)
        elif answer == 1:
            self.question_surface_inner_3.fill((255,0,0))
            screen.blit(self.question_surface_inner_3, (70, 110))
            pygame.display.flip()
            pygame.time.delay(700)
    
    def third_room_end_transition(self):
        screen.blit(self.pugnetti_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(1400)
        self.update_state(self.STATE_FOURTHROOM)
    
    def draw_fourth_room(self):
        if self.entrance_animation_state:
            self.fourth_room_entrance_animation()
            self.entrance_animation_state = False
        screen.blit(self.pistoni1_surface, (0,0))
        screen.blit(self.pistoni_wiriting_surface_1, (620, 810))
        if self.question_box_state:
            screen.blit(self.question_surface_4, (250, 70))
        
    def fourth_room_entrance_animation(self):
        screen.blit(self.pistoni1_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(1000)
    
    def fourth_room_transition(self, answer):
        if answer == 0:
            self.question_surface_inner_4.fill((0,255,0))
            screen.blit(self.question_surface_inner_4, (260, 80))
            pygame.display.flip()
            pygame.time.delay(1000)
        elif answer == 1:
            self.question_surface_inner_4.fill((255,0,0))
            screen.blit(self.question_surface_inner_4, (260, 80))
            pygame.display.flip()
            pygame.time.delay(700)
    
    def fourth_room_end_transition(self):
        screen.blit(self.pistoni2_surface, (0,0))
        screen.blit(self.pistoni_wiriting_surface_2, (640, 810))
        pygame.display.flip()
        pygame.time.delay(1500)
        self.update_state(self.STATE_FIFTHROOM)

    def draw_fifth_room(self):
        if not self.ipad_zoom_state:
            if not self.lucchetto_zoom_state:
                screen.blit(self.ipad_lucchetto_surface, (0,0))
            elif self.ipad_codice_state:
                screen.blit(self.lucchetto_surface, (0,0))
                codice_inserito = self.font4.render(self.ipad_codice_inserito,True, (0,0,0))
                screen.blit(codice_inserito, (320, 320))
        elif self.ipad_zoom_state and self.question_box_state:
            screen.blit(self.ipad_surface, (0,0))
            screen.blit(self.question_surface_5, (705,100))
    
       
    def fifth_room_transition(self, answer):
        if answer == 0:
            self.question_surface_5_b.fill((0,255,0))
            screen.blit(self.question_surface_5_b, (703, 98))
            pygame.display.flip()
            pygame.time.delay(1000)
            self.question_surface_5_b.fill((0,0,0,0)) 
        elif answer == 1:
            self.question_surface_5_b.fill((255,0,0))
            screen.blit(self.question_surface_5_b, (703, 98))
            pygame.display.flip()
            pygame.time.delay(700)
            self.question_surface_5_b.fill((0,0,0,0)) 
        
    def fifth_room_end_transition(self):
        screen.blit(self.ipad_lucchetto_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(1400)
        self.update_state(self.STATE_SIXTHROOM)
        
    def draw_sixth_room(self):
        screen.blit(self.sf_2_surface, (0,0))
        if self.question_box_state:
            screen.blit(self.question_surface_6, (80, 100))
    
    def sixth_room_transition(self, answer):
        if answer == 0:
            self.question_surface_inner_6.fill((0,255,0))
            screen.blit(self.question_surface_inner_6, (90, 110))
            pygame.display.flip()
            pygame.time.delay(1000)
           
        elif answer == 1:
            self.question_surface_inner_6.fill((255,0,0))
            screen.blit(self.question_surface_inner_6, (90, 110))
            pygame.display.flip()
            pygame.time.delay(700)
    
    def sixth_room_end_transition(self):
        screen.blit(self.sf_2_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(1500)
        screen.blit(self.sf_1_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(1500)
        screen.blit(self.termostato_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(1500)
        self.update_state(self.STATE_SEVENTHROOM)
        
    def draw_seventh_room(self):
        screen.blit(self.poli_surface,(0,0))
        self.draw_seventh_room_dialog()
        if self.question_box_state:
            if not self.second_question_state:
                screen.blit(self.question_surface_7, (120, 70))
            else:
                screen.blit(self.question_surface_7_5, (120,70))
        
            
    
    def draw_seventh_room_dialog(self):
        if self.poli_first_dialog_state:
            pygame.draw.rect(screen, (255,255,255), self.poli_dialog_rect, border_radius= 20)
            screen.blit(self.poli_dialog_text_surface_1, self.poli_text_rect_1)
            screen.blit(self.poli_dialog_text_surface_2, self.poli_text_rect_2)
            screen.blit(self.poli_dialog_text_surface_3, self.poli_text_rect_3)
        elif self.poli_second_dialog_state:
            pygame.draw.rect(screen, (255,255,255), self.poli_dialog_rect2, border_radius= 20)
            screen.blit(self.poli_dialog_text_surface_4, self.poli_text_rect_4)
            screen.blit(self.poli_dialog_text_surface_5, self.poli_text_rect_5)
            screen.blit(self.poli_dialog_text_surface_6, self.poli_text_rect_6)
        elif self.poli_third_dialog_state:
            pygame.draw.rect(screen, (255,255,255), self.poli_dialog_rect, border_radius= 20)
            screen.blit(self.poli_dialog_text_surface_7, self.poli_text_rect_7)
            screen.blit(self.poli_dialog_text_surface_8, self.poli_text_rect_8)
            screen.blit(self.poli_dialog_text_surface_9, self.poli_text_rect_9)
        elif self.poli_fourth_dialog_state:
            pygame.draw.rect(screen, (255,255,255), self.poli_dialog_rect, border_radius= 20)
            screen.blit(self.poli_dialog_text_surface_10, self.poli_text_rect_10)
            screen.blit(self.poli_dialog_text_surface_11, self.poli_text_rect_11)
            screen.blit(self.poli_dialog_text_surface_12, self.poli_text_rect_12)
        elif self.poli_end_dialog_state:
            pygame.draw.rect(screen, (255,255,255), self.poli_dialog_rect, border_radius= 20)
            screen.blit(self.poli_dialog_text_surface_13, self.poli_text_rect_13)
            screen.blit(self.poli_dialog_text_surface_14, self.poli_text_rect_14)
            screen.blit(self.poli_dialog_text_surface_15, self.poli_text_rect_15)
            
            
            
            
    def seventh_room_transition(self, answer):
        if answer == 0:
            self.question_surface_inner_7.fill((0,255,0))
            screen.blit(self.question_surface_inner_7, (130, 80))
            pygame.display.flip()
            pygame.time.delay(1000)
           
        elif answer == 1:
            self.question_surface_inner_7.fill((255,0,0))
            screen.blit(self.question_surface_inner_7, (130, 80))
            pygame.display.flip()
            pygame.time.delay(700)
        
    def seventh_room_end_transition(self):
        self.active_timer = False
        screen.blit(self.poli_surface, (0,0))
        pygame.display.flip()
        pygame.time.delay(800)
        self.draw_seventh_room_dialog()
        pygame.display.flip()
        pygame.time.delay(4000)
        self.update_state(self.STATE_ESCAPED)
        
    #time control
    def update_timer(self):
        if self.timer > 300:
            color = (255,255,255)
        else:
            color = (255,0,0)
        if self.active_timer:
            if self.timer <= 0:
                self.game_over_animation()
                self.running = False
            current_time = pygame.time.get_ticks()
            if current_time - self.last_time >= self.timer_interval:
                self.timer -= 1
                if self.timer < 0:
                    self.timer = 0
                self.last_time = current_time
                self.timer_text = self.timer_font.render("{}".format(self.format_time(self.timer)), True, color)

            # Blit timer onto the screen
        screen.blit(self.timer_text, self.timer_rect)

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds %= 60
        return '{:02d}:{:02d}'.format(minutes, seconds)
    
    def game_over_animation(self):
        # Define colors
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)

        # Define font
        font_bold = pygame.font.SysFont('Honeymoon', 250)
        font_bold.set_bold(True)

        # Create text surfaces
        game_text = font_bold.render("Game", True, RED)
        over_text = font_bold.render("Over", True, WHITE)

        # Initial positions
        game_x, game_y = -game_text.get_width(), 400
        over_x, over_y = self.WIDTH, 400

        game_end_x, over_end_x = 350 , 900

        speed = 1.5  # Adjust the speed as needed

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.quit_game()

            # Move the "Game" text
            if game_x < game_end_x:
                game_x += speed

            # Move the "Over" text from the right
            if over_x > over_end_x:
                over_x -= speed

            # Draw
            screen.fill((0, 0, 0))
            screen.blit(game_text, (game_x, game_y))
            screen.blit(over_text, (over_x, over_y))
            pygame.display.flip()

            # Check if both texts have reached their destinations
            if game_x >= game_end_x and over_x <= over_end_x:
                running = False

            self.clock.tick(300)  # Adjust the frame rate

    def draw_escaped(self):
        screen.blit(self.escaped_writing_1_surface, (100,100))
        screen.blit(self.escaped_writing_2_surface, (100,350))
        screen.blit(self.escaped_writing_3_surface, (100,460))
        screen.blit(self.escaped_writing_4_surface, (100,570))
        screen.blit(self.escaped_writing_5_surface, (100,680))
        
    
    def main(self):
        while self.running: 
            self.clock.tick(60)
            self.handle_events()
            self.update_screen()
            pygame.display.flip()
        
        while not self.running:
            self.handle_events()
    
    


escape_room = EscapeRoom()   
if __name__ == '__main__':  
    escape_room.main()
