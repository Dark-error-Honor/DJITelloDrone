from djitellopy.tello import Tello
from time import sleep

tello = Tello()
sleep(1)
tello.connect()  # verbinden met de drone
print(f'Drone is {tello.get_battery()}%')  # Batterijpercentage

tello.takeoff()  # drone stijgt op
height_1 = 50  # gewenste hoogte in cm omlaag
height_2 = 130  # gewenste hoogte in cm omhoog
print(f"Height after takeoff: {tello.get_height()}cm")

for i in range(3):  # 2 keer herhalen
    height_drone = tello.get_height()  # geeft de hoogte van de drone in cm
    # Als drone op 120cm vliegt: 110cm naar beneden
    # => 120 - 10 = height_drone - height_1
    down = height_drone - height_1
    print(down)
    if down > 0:
        tello.move_down(down)  # naar beneden
    sleep(1)  # 1 seconde wachten
    height_drone = tello.get_height()  # nieuwe hoogte
    tello.move_up(height_2-height_drone)  # naar boven vliegen

tello.land()
