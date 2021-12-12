import sys

from Models import ClipboardPoller, QueueObject
from Views import Application
from Controllers import Controller


def main():
    clipboardQueue = QueueObject()
    clipboardPoller = ClipboardPoller(clipboardQueue)
    clipboardPoller.daemon = True
    clipboardPoller.start()

    controller = Controller(clipboardQueue)
    controller.attachModel(clipboardPoller)
    controller.attachView(Application)
    controller.daemon = True
    controller.start()

    clipboardPoller.join()
    controller.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Terminating Clipboard-Copy Application")
