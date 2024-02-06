from ultra_type.controller import Controller
from ultra_type.model import Model
from ultra_type.view_main import ViewMain

def main():
    model = Model()
    controller = Controller(model)
    view = ViewMain(controller = controller)
    view .run()

if __name__ == "__main__":
    main()