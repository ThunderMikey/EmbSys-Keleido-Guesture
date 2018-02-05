import pyautogui

#pyautogui.FAILSAFE = True

#get the screen size

#pyautogui.size()
#2560,1440

width, height = pyautogui.size()

pyautogui.PAUSE = 2

#pyautogui.click(601,527)
#pyautogui.typewrite('Hello world!', 0.25)

pyautogui.keyDown('altleft');
pyautogui.press('f4');
pyautogui.keyUp('altleft')

pyautogui.PAUSE = 1.5
#pyautogui.typewrite('Hello world!', 0.25)
#pyautogui.typewrite('Hello world!', 0.25)
