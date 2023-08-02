import pyautogui

def moveDown(timeBlink):
    pyautogui.moveRel(0, timeBlink * 50, duration = 0.5)

def moveUp(timeBlink):
    pyautogui.moveRel(0, timeBlink * -50, duration = 0.5)
    
def moveLeft(timeBlink):
    pyautogui.moveRel(timeBlink * -50, 0, duration = 0.5)
    
def moveRight(timeBlink):
    pyautogui.moveRel(timeBlink * 50, 0, duration = 0.5)

def click(timeBlink):
    pyautogui.click(100, 100)

def click():
    pyautogui.click()

def doubleClick():
    pyautogui.click()
    pyautogui.click()