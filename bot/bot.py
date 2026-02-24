from controllers.security_controller import SecurityController
from views.terminal_view import TerminalView


def run() -> None:
    controller = SecurityController()
    view = TerminalView(controller)
    view.loop()


if __name__ == "__main__":
    run()
