import pyautogui
# import pytesseract as tess
# tess.pytesseract.tesseract_cmd = r'C:\Users\howar\AppData\Local\Tesseract-OCR\tesseract.exe'
from PIL import Image
from pyzbar.pyzbar import decode
import time
import webbrowser
from datetime import datetime
from pushbullet import Pushbullet
import os

API_KEY_File = "API_KEY.txt"
if os.path.isfile(API_KEY_File):
    with open(API_KEY_File, mode='r') as f:
        API_KEY = f.read()
else:
    API_KEY = input("Please enter your API key:")
    with open(API_KEY_File, mode='w') as f:
        f.write(API_KEY)
pb = Pushbullet(API_KEY)
screenshot_folderPath = 'screenshots/'
screenshot_fileName = 'stage_screenshot.png'
statusScreenshot_folderPath = 'status_screenshots/'
statusScreenshot_fileNameSuffix = '_attendanceStatus.png'
noqr = True

while(True):
    qrscreenshot = pyautogui.screenshot()
    qrscreenshot.save(r'' + screenshot_folderPath + screenshot_fileName + '') #take an initial screenshot, save it
    img = Image.open(screenshot_folderPath + screenshot_fileName ) #open the screenshot
    d = decode(img)

    #if there is qr code, then it will be a list with more than 0 
    if len(d) > 0:
        attcode = d[0].data.decode('ascii')
        #if found a qr but it is not an attendance code then still not found

        if len(attcode) == 3: #attendance code found!
            now = datetime.now()
            current_dateTime = now.strftime("%y%m%d_%H%M%S")
            img.save(screenshot_folderPath+ 'ScreenshotGotten'+current_dateTime+'_'+attcode+'.png')
            print('Attendance code: ', attcode)
            attendanceCodeReady = True
            break
        
    if noqr:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('no qr found ', current_time)   
        
    time.sleep(10) #if no qr found, wait for 10 seconds


if attendanceCodeReady: #if you know how to communicate with apu api, go ahead
    webbrowser.open('https://apspace.apu.edu.my/attendix/update', new=1, autoraise=True)

    eachattcode = list(attcode)
    time.sleep(6) #wait 6 seconds for slow connection to load the website
    for x in eachattcode:
        print(x)
        pyautogui.press(x)
        time.sleep(1)
        
    qrscreenshot = pyautogui.screenshot()
    qrscreenshot.save(r''+statusScreenshot_folderPath+attcode+statusScreenshot_fileNameSuffix)

    push = pb.push_note('AttendanceAuto Completed at:', current_dateTime +
        '\nPlease check your image at:\n' + os.path.abspath(statusScreenshot_folderPath+attcode+statusScreenshot_fileNameSuffix))

    print('Status saved, exiting application...')
    input('Press any key to close...')