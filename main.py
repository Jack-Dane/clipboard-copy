from Models import ClipboardPoller
from Views import StaticViewCreator
from Controllers import Controller


def main():
    clipboardPoller = ClipboardPoller()
    clipboardPoller.start()

    controller = Controller()
    controller.start()
    controller.attachModel(clipboardPoller)
    controller.attachView(StaticViewCreator)


if __name__ == "__main__":
    main()
