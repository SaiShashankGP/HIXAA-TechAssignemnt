# Import useful libraries

import cv2 as cv
import numpy as np
import concurrent.futures

# We need to have two processes
# 1. to capture the image
# 2. to display the image

class captureimgProcess():
    filename = ''
    def __init__(self, videoAddr):
        self.videoAddr = videoAddr
    def captureimg(self):
        '''
        This function performs the task of capturing webcam screenshot
        When 's' is pressed, the screenshot is captured and stored as Screenshot-{ss_count}.png
        When 'q' is pressed, the video is closed
        '''
        video = cv.VideoCapture(self.videoAddr)
        ss_count = 0
        print('Starting video...')
        while True:
            isTrue, frame = video.read()
            if not isTrue:
                print('Video failed to load!')
                break
            cv.imshow('Video', frame)
            if cv.waitKey(1) & 0xFF == ord('s'):
                print('Taking screenshot...')
                name = 'Screenshot-{}.png'.format(ss_count)
                cv.imwrite(name, frame)
                captureimgProcess.filename = name
                ss_count += 1
            if cv.waitKey(1) & 0xFF == ord('q'):
                print('Closing video...')
                break
                
        video.release()
        cv.destroyWindow('Video')
        
class showimgProcess(captureimgProcess):
    def __init__(self):
        print('Showing Screenshot...')
        print('{}'.format(captureimgProcess.filename))
    def showimg(self):
        '''
        This function performs the task of showing the latest captured image
        
        When any key is pressed, the image is closed
        '''
        img = cv.imread(captureimgProcess.filename)
        cv.imshow('Screenshot', img)
        cv.waitKey(0)

with concurrent.futures.ProcessPoolExecutor() as executor:
    List = [captureimgProcess(0).captureimg(), showimgProcess().showimg()]
    for process in List:
        executor.map(process)
        

print('----END OF PROGRAM----')
    
