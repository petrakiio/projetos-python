from controllers.security_controller import SecurityController
from models.model import ToolReport


class TerminalView:
    def __init__(self, controller: SecurityController):
        self.controller = controller

    @staticmethod
    def _read_int(prompt: str, default: int) -> int:
        raw = input(f"{prompt} [{default}]: ").strip()
        if not raw:
            return default
        try:
            return int(raw)
        except ValueError:
            print("Valor invalido. Usando padrao.")
            return default

    @staticmethod
    def _render_report(report: ToolReport) -> None:
        status = "SUCESSO" if report.success else "ATENCAO"
        print(f"\n[{status}] tool={report.tool_name}")
        print(report.output)

    @staticmethod
    def _menu() -> str:
        print("\n=== Bot MVC (Defensivo) ===")
        print("1. Buscar CEP")
        print("2. Buscar IP")
        print("3. Teste de lockout (anti brute-force)")
        print("0. Sair")
        return input("Escolha: ").strip()

    def loop(self) -> None:
        while True:
            option = self._menu()

            if option == "0":
                print("Encerrando.")
                return

            if option == "1":
                cep = input("CEP: ").strip()
                self._render_report(self.controller.run_cep_lookup(cep))
                continue

            if option == "2":
                ip = input("IP: ").strip()
                self._render_report(self.controller.run_ip_lookup(ip))
                continue

            if option == "3":
                url = input("URL login (ex: http://127.0.0.1:5000/login): ").strip()
                email = input("Email de teste: ").strip()
                attempts = self._read_int("Tentativas maximas", 15)
                self._render_report(
                    self.controller.run_lockout_test(url=url, email=email, attempts=attempts)
                )
                continue

            print("Opcao invalida.")
