import time
import os
import pygame
import numpy as np
from mss import mss


MAX_FPS = 30
SKIP = 20 # Skip pixels

class Screen:
    def __init__(self):
        self.instance = pygame.display.set_mode((200, 200))
        pygame.display.set_caption('Average Color Viewer')
        pygame.display.flip()

    def update(self, r, g, b):
        self.instance.fill((r*255, g*255, b*255))
        pygame.display.update()

def getMean_numpy(image):
    # arr = np.array(image)
    skipped_arr = image[::SKIP, 0::SKIP]
    mean = np.mean(skipped_arr, axis=(0, 1)) / 255.0
    return mean

# def getMean_naive(image):
#     red = 0
#     green = 0
#     blue = 0
#     for y in range(0, image.size[1], SKIP):  #loop over the height
#         for x in range(0, image.size[0], SKIP):  #loop over the width
#             color = image.getpixel((x, y))  #grab a pixel
#             red = red + color[0]
#             green = green + color[1]
#             blue = blue + color[2]
#     red = (( red / ( (image.size[1]/SKIP) * (image.size[0]/SKIP) ) ) )/255.0
#     green = ((green / ( (image.size[1]/SKIP) * (image.size[0]/SKIP) ) ) )/255.0
#     blue = ((blue / ( (image.size[1]/SKIP) * (image.size[0]/SKIP) ) ) )/255.0
#     return (red, green, blue)

# def getMean_cython(image):
#     image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#     return (0, 0, 0)

def loop():
    viewer = Screen()
    sct = mss()
    while True:
        t0 = time.time()
        # Take screenshot
        # image = ImageGrab.grab()
        sct_img = sct.grab(sct.monitors[0])
        image = np.array(sct_img)#Image.new("RGB", sct_img.size)
            # image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        t1 = time.time()
        mean = getMean_numpy(image)
        t2 = time.time()
        viewer.update(mean[0], mean[1], mean[2])
        t3 = time.time()
        dt_screenshot = t1-t0
        dt_loop = t3 - t0
        dt_math = t2 - t1
        dt_viewer = t3-t2
        PERIOD = 1.0/MAX_FPS
        if dt_loop < PERIOD:
            time.sleep(PERIOD-dt_loop)
        else:
            print(f"Slow loop: {dt_loop*1000}ms {f'{int((dt_loop - PERIOD)*100000)/100}ms excess'}")
            print(f"Screenshot: {int(dt_screenshot*100000)/100}ms")
            print(f"Computation: {int(dt_math*100000)/100}ms")
            print(f"Viewer update: {int(dt_viewer*100000)/100}ms\n")



def main():
    print("Starting screen color detection")
    loop()
    

if __name__ == "__main__":
    main()