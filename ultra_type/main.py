from ultra_type.controller import Controller
from ultra_type.view import View
from ultra_type.model import Model

def main():
    model = Model()
    model.set_user("default")
    model.set_language("English")
    view = View()
    controller = Controller(model, view)
    controller.run()

if __name__ == "__main__":
    main()
