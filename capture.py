import time
import cv2
import numpy as np
import mss
from screeninfo import get_monitors
import pyautogui

screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height
height = 600
width = 800
bounding_box = {'top': int(screen_height/2-height/2), 'left': int(screen_width/2-width/2), 'width': width, 'height': height}

pole_img = cv2.imread('pole.png')
w = pole_img.shape[1]
h = pole_img.shape[0]

threshold = 0.55

timer = time.time()
with mss.mss() as sct:
    while True:
        start_time = time.time()
        screen = np.array(sct.grab(bounding_box))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

        # Find pole
        result = cv2.matchTemplate(screen, pole_img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > threshold:
            cv2.rectangle(screen, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
            # Do a right click
            pyautogui.rightClick(x=max_loc[0] + w/2, y=max_loc[1] + h/2)
            # Sleep random time between 0.5 and 1.5 seconds
            time.sleep(np.random.uniform(1, 2))
            pyautogui.rightClick(x=max_loc[0] + w/2, y=max_loc[1] + h/2)
            time.sleep(np.random.uniform(1, 2))

        cv2.imshow('screen', screen)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        end_time = time.time()
        if time.time() - timer > 1:
            print('FPS: ', 1 / (end_time - start_time))
            timer = time.time()