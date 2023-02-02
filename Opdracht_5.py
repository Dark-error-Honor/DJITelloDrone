from tello import Tello
import numpy as np
import cv2

me = Tello()
me.connect()
me.streamon()
me.takeoff()
me.move_up(90)
w, h = 600, 400  # breedte en hoogte van frame


class Face:
    def __init__(self, center_x, center_y, width, height, area):
        self.x = center_x
        self.y = center_y
        self.width = width
        self.height = height
        self.area = area


def get_face(frame):
    casc_path = './haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(casc_path)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # kleur frame naar grijstinten
    faces = face_cascade.detectMultiScale(gray, 1.2, 8)  # detecteer gezichten

    faces_area = []
    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)  # teken een rechthoek rond gezicht
        center_x = x + w//2  # midden x
        center_y = y + w//2  # midden y
        cv2.circle(gray, (center_x, center_y), 5, (0, 255, 0), cv2.FILLED)  # teken een cirkel in het midden
        area = w*h  # oppervlakte van rechthoek om het dichtse te vinden
        faces_area.append(Face(center_x, center_y, w, h, area))

    if len(faces) != 0:
        aface = max(face.area for face in faces_area)  # geeft de oppervlakte van het grootste gezicht
        face = next((face for face in faces_area if face.area == aface))  # geeft het object met grootste oppervlakte
        return gray, face
    else:
        return gray, Face(0, 0, 0, 0, 0)


def track_face(face, w, pid, p_error):
    # pid = proportioneel, integrerend, deferentiërend
    # pid wordt gebruikt om overshoot tegen te gaan, als de drone naar een exacte positie wil
    # moet die als hij er bijna is vertragen omdat hij anders te ver doordraait.
    x, y = face.x, face.y
    error = x - w//2  # positie van midden - midden van frame
    speed = pid[0]*error + pid[1]*(error - p_error)
    speed = int(np.clip(speed, -100, 100))

    b_range = 6200  # oppervlakte van rechthoek voor correcte afstand ver
    f_range = 6800  # oppervlakte van rechthoek voor correcte afstand dicht

    if b_range < face.area < f_range:
        fb = 0
    elif face.area > f_range:
        fb = -20  # 20 achteruit gaan
    elif face.area < b_range and face.area != 0:
        fb = 20  # 20 vooruit gaan
    else:
        fb = 0

    if x == 0:
        speed = 0
        error = 0

    me.send_rc_control(0, fb, 0, speed)
    return error


while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, face = get_face(img)
    p_error = 0
    p_error = track_face(face, w, [0.2, 0.2, 0], p_error)
    cv2.imshow('Drone', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
