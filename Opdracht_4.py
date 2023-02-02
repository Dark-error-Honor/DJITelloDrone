from tello import Tello
import pygame
import cv2
from PIL import Image

def init():  # PyGame initializeren
    pygame.init()
    window = pygame.display.set_mode((400, 400))  # window met 400x400 pixels


def get_key(key_name):
    pressed = False
    for event in pygame.event.get(): pass
    key_input = pygame.key.get_pressed()  # welke toets er ingedrukt is
    my_key = getattr(pygame, 'K_{}'.format(key_name))  # naam van ingedrukte knop
    if key_input[my_key]:  # als toets wordt ingedrukt
        pressed = True
    pygame.display.update()  # update de display
    return pressed


def control():
    lr, fb, ud, yaw = 0, 0, 0, 0  # waarden voor lr(links, rechts), fb(forward, backward), ud(up, down) en yaw
    speed = 50  # snelheid van drone
    if get_key('LEFT'): lr = -speed  # links pijltje
    if get_key('RIGHT'): lr = speed  # rechts pijltje

    if get_key('UP'): fb = speed  # pijltje omhoog
    if get_key('DOWN'): fb = -speed  # pijltje omlaag

    if get_key('z'): ud = speed  # z toets
    if get_key('s'): ud = -speed  # s toets

    if get_key('a'): yaw = -speed  # a toets
    if get_key('e'): yaw = speed  # e toets

    if get_key('l'): me.land()  # l toets = landen
    if get_key('t'): me.takeoff()  # t toets = takeoff

    if get_key('c'):
        pic = me.get_frame_read().frame
        pic = Image.fromarray(pic)
        pic.save("foto.jpeg")

    return [lr, fb, ud, yaw]


if __name__ == '__main__':
    init()
    me = Tello()
    me.connect()
    me.streamon()

while True:
    vals = control()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    img = cv2.resize(img, (400, 400))
    cv2.imshow('Drone', img)
    cv2.waitKey(1)
