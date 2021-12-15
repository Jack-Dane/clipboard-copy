import sys
import threading
import time

from Models import ClipboardPoller, QueueObject
from Views import Application
from Controllers import Controller

threads = []
stoppingEvent = threading.Event()


def main():
    clipboardQueue = QueueObject()
    clipboardPoller = ClipboardPoller(stoppingEvent, clipboardQueue)
    threads.append(clipboardPoller)
    clipboardPoller.start()

    controller = Controller(clipboardQueue)
    controller.attachModel(clipboardPoller)
    controller.attachView(Application)
    controller.daemon = True
    controller.start()

    checkForInterrupt()


def checkForInterrupt():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stoppingEvent.set()
        for thread in threads:
            thread.join()
        print("Stopped Clipboard-Copy Application")


if __name__ == "__main__":
    main()
