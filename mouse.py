import pyautogui

def moveDown(timeBlink):
    pyautogui.moveRel(0, timeBlink * 10, duration = 0.5)

def moveUp(timeBlink):
    pyautogui.moveRel(0, timeBlink * -10, duration = 0.5)
    
def moveLeft(timeBlink):
    pyautogui.moveRel(timeBlink * -10, 0, duration = 0.5)
    
def moveRight(timeBlink):
    pyautogui.moveRel(timeBlink * 10, 0, duration = 0.5)
