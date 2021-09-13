from Models import ClipboardPoller
from Views import Application
from Controllers import Controller


def main():
    clipboardPoller = ClipboardPoller()
    clipboardPoller.start()

    controller = Controller()
    controller.attachModel(clipboardPoller)
    controller.attachView(Application)
    controller.start()


if __name__ == "__main__":
    main()
