import pyautogui
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\howar\AppData\Local\Tesseract-OCR\tesseract.exe'
from PIL import Image
from pyzbar.pyzbar import decode
import time
import webbrowser
from datetime import datetime


while(True):
    pos = pyautogui.locateOnScreen('qr2.png')
    if pos != None:
        flag = True
        break
    else:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('not found ', current_time)
        
    time.sleep(7)

if flag == True:
    qrscreenshot = pyautogui.screenshot()
    qrscreenshot.save(r'myscreenshot.png')

    img = Image.open('myscreenshot.png')
    d = decode(img)
    if len(d) > 0:
        attcode= d[0].data.decode('ascii')
    else:
        print('no qr found')
    print(attcode)

    webbrowser.open('https://apspace.apu.edu.my/attendix/update', autoraise=True)

    eachattcode = list(attcode)
    time.sleep(10)
    for x in eachattcode:
        print(x)
        pyautogui.press(x)