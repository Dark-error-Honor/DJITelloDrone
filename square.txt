from tello import Tello

me = Tello()
me.connect()

dist = 100  # afstand die de drone moet afleggen voor 1 zijde
min_height = 90
max_height = 140

me.takeoff()  # opstijgen
while min_height > me.get_height() or max_height < me.get_height():  # 2 keer proberen om op de juiste hoogte te komen
    if me.get_height() < min_height:
        me.move_up(20)
    else:
        me.move_down(20)

if min_height <= me.get_height() < max_height:  # als de drone tussen 90 en 140 cm is
    me.move_forward(dist)  # 100cm vooruit
    me.move_right(dist)  # 100cm naar rechts
    me.move_back(dist)  # 100cm naar achter
    me.move_left(dist)  # 100cm naar links


me.land()
