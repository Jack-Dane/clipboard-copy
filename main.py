from Models import ClipboardPoller
from Views import Application
from Controllers import Controller


def main():
    clipboardPoller = ClipboardPoller()
    clipboardPoller.start()

    controller = Controller()
    controller.start()
    controller.attachModel(clipboardPoller)
    controller.attachView(Application)


if __name__ == "__main__":
    main()
