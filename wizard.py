from Modules.camera import Camera
import Modules.handsigns as hs
from multiprocessing import Process, Manager
import time
import math
import pyautogui as pag
from tkinter import *
from tkinter.ttk import *


if __name__ == "__main__":
    root = Tk()
    loop = True
    screen_w, screen_l = (root.winfo_screenwidth(), root.winfo_screenheight())

    def move(ldm):
        try:
            point1 = ldm[hs.fin_marks["thumb"][0]]
            point2 = ldm[hs.fin_marks["pointer"][0]]
            point3 = ldm[hs.fin_marks["middle"][0]]

            if point1 == [] or point2 == [] or point3 == []:
                return False

            midpoint_x = (point1[0] + point2[0]) / 2
            midpoint_y = (point1[1] + point2[1]) / 2
            scale = 1.75
            midpoint = ((midpoint_x*scale - (scale/6))*screen_w,
                        (midpoint_y*scale - (scale/6))*screen_l)

            # Lock
            if point3[1] > point1[1]:
                pag.moveTo(midpoint)

            # Clicks
            pointt = ldm[hs.fin_marks["thumb"][1]]
            if pointt != []:
                pag.mouseDown() if math.dist(point1, point2) < math.dist(
                    point1, pointt) else pag.mouseUp()
            else:
                pag.mouseUp()

            return True
        except:
            return False

    # return success
    def slide_window(ldm):
        try:
            center = ldm[hs.fin_marks["middle"][-1]]
            swap = True
            dist = 0.045
            if center == None:
                return False
            while True:

                if len(hs.fingers_pointing_up(ldm, ["middle"])) == 0:
                    return False

                center_point = ldm[hs.fin_marks["middle"][-1]]
                if swap and abs(center[0] - center_point[0]) > dist:
                    swap = False
                    direction = 'right' if center[0] < center_point[0] else 'left'
                    pag.hotkey('ctrl', direction)
                elif abs(center[0] - center_point[0]) < dist:
                    swap = True

        except:
            return False

    def destroy():
        global loop
        loop = False
        root.destroy()
    btn = Button(root, text='Stop Process',
                 command=destroy)
    btn.pack(side='top')

    manager = Manager()

    ldm = manager.list(range(21))

    cam = Camera(ldm)

    cam.start()
    print("testing")

    stage = "roaming"
    stages = {
        "pointer": lambda: len(fingers_up) == 2 and "pointer" in fingers_up and "thumb" in fingers_up,
        "palm": lambda: len(fingers_up) >= 4
    }
    wait = False
    starttime = 0

    while loop:
        fingers_up = []
        match (stage):
            case "roaming":
                fingers_up = hs.fingers_pointing_up(ldm)

            case "pointer":
                while move(ldm) and not hs.fist(ldm):
                    pass
                stage = "roaming"

            case "palm":
                success = slide_window(ldm)
                if not success or hs.fist(ldm):
                    stage = "roaming"

        for s in stages:
            if stages[s]():
                stage = s
                if not wait:
                    starttime = time.time()
                wait = True
                break

        if wait:
            if stage[-1] != '.':
                stage += "."
            if (time.time() - starttime) > 1:
                stage = stage[:-1]
                wait = False

        root.update()
        pass
    cam.shutdown()
    time.sleep(3)
    print("Done")
