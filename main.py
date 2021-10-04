from Models import ClipboardPoller, QueueObject
from Views import Application
from Controllers import Controller


def main():
    clipboardQueue = QueueObject()
    clipboardPoller = ClipboardPoller(clipboardQueue)
    clipboardPoller.start()

    controller = Controller(clipboardQueue)
    controller.attachModel(clipboardPoller)
    controller.attachView(Application)
    controller.start()


if __name__ == "__main__":
    main()
