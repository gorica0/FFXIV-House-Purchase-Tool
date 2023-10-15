from threading import Thread, Lock

import win32gui
import win32con
import win32api
from time import sleep

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLineEdit, QFormLayout

# Hook into the process
hwndMain = win32gui.FindWindow("FINAL FANTASY XIV", "FINAL FANTASY XIV")
hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)

# delays array, in ms
global delays
delays = [500, 800, 400, 400, 1000]


def functionality(y: Lock):

    # lock is acquired before the thread calling this function is started. If the state of lock (y) changes
    # while running, then the loop ends and end of functionality(), thread dies naturally.
    while y.locked():

        # 0x44 = D
        temp1 = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x44, 0)
        sleep(delays[0]/1000)

        # 0x60 = numeric 0
        temp2 = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x30, 0)
        sleep(delays[1]/1000)

        # 0x60 = numeric 0
        temp3 = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x30, 0)
        sleep(delays[2]/1000)

        # 0x64 = numeric 4
        temp4 = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x34, 0)
        sleep(delays[3]/1000)

        # 0x60 = numeric 0
        temp5 = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x30, 0)
        sleep(delays[4]/1000)


# Implements mutex + threading to toggle the inputs on a single button, updates button text
def toggle(button: QPushButton, y: Lock):

    # Setup a new thread, but only run it if the lock is currently in unlocked state
    x = Thread(group=None, target=lambda: functionality(y))

    # if in locked state, a Thread is already running and entering keys. Unlock and let the thread die.
    if y.locked():
        button.setText("Start")
        y.release()

    # if in an unlocked state, acquire the lock and run the Thread.
    else:
        button.setText("Stop")
        y.acquire()
        x.start()


# update the delays list with user entered data
def update_handler(e1, e2, e3, e4, e5):
    args_list = [e1, e2, e3, e4, e5]
    global delays
    for i in range(5):
        delays[i] = int(args_list[i].text())


def main():

    # mutex lock - singleton
    y = Lock()

    # UI
    app = QApplication([])
    app.setStyle('Fusion')
    window = QWidget()
    layout = QFormLayout()

    # text inputs
    e1 = QLineEdit()
    e1.setText(str(delays[0]))
    e1.setValidator(QDoubleValidator(0, 10, 0))

    e2 = QLineEdit()
    e2.setText(str(delays[1]))
    e2.setValidator(QDoubleValidator(0, 10, 0))

    e3 = QLineEdit()
    e3.setText(str(delays[2]))
    e3.setValidator(QDoubleValidator(0, 10, 0))

    e4 = QLineEdit()
    e4.setText(str(delays[3]))
    e4.setValidator(QDoubleValidator(0, 10, 0))

    e5 = QLineEdit()
    e5.setText(str(delays[4]))
    e5.setValidator(QDoubleValidator(0, 10, 0))

    # add to layout
    layout.addRow('Delay of 1st keypress:', e1)
    layout.addRow('Delay of 2nd keypress:', e2)
    layout.addRow('Delay of 3rd keypress:', e3)
    layout.addRow('Delay of 4th keypress:', e4)
    layout.addRow('Delay of 5th keypress:', e5)

    # Toggle button
    button = QPushButton('Start')
    button.clicked.connect(lambda: toggle(button, y))

    # Update button
    update_button = QPushButton('Update Delays')
    update_button.clicked.connect(lambda: update_handler(e1, e2, e3, e4, e5))

    layout.addWidget(button)
    layout.addWidget(update_button)

    window.setLayout(layout)
    window.show()

    window.setWindowTitle('FF14 Land Purchaser')
    app.exec_()


if __name__ == "__main__":
    main()