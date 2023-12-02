from ultra_type.controller import Controller
from ultra_type.view import View
from ultra_type.model import Model


def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        print("Error: UltraType has crashed")
        exit(1)