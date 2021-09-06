'''
from lib.cv import cv2, CaptureInput
cap = CaptureInput(0, 640, 480, 30)
'''
import cv2
from lib.display_fps import DisplayFPS

class CaptureInput(cv2.VideoCapture):
    display_fps = True
    flip = 1

    def __init__(self, var, width=640, height=480, fps=30, info=True) -> None:
        super().__init__(var)
        self.setSize(width, height)
        self.setFps(fps)
        if info is True:
            self.info()
        self.rate = DisplayFPS(fps)

    def info(self):
        print(f'Resolution = {self.width}x{self.height}, FPS = {self.fps}')
    
    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.shape = width, height
        self.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    def setFps(self, fps):
        self.fps = fps
        self.set(cv2.CAP_PROP_FPS, fps)

    def read(self):
        ret, frame = super().read()
        frame = cv2.flip(frame, self.flip)
        self.rate.count()
        self.real_fps = self.rate.fps
        if self.display_fps is True:
            self.rate.print(frame)
        return ret, frame

    def setDisplayFps(self, bool):
        self.display_fps = bool

    def setFlip(self, var):
        self.flip = var

if __name__ == '__main__':
    cap = CaptureInput(0, 640, 480, 30)
    cap.setDisplayFps(True)
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()