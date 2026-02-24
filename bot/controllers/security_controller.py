from models.model import ToolReport
from tools.conn_loc import Buscar_CEP, Buscar_ip
from tools.bf import bf_on


class SecurityController:
    def run_cep_lookup(self, cep: str) -> ToolReport:
        result = Buscar_CEP(cep)
        success = not isinstance(result, str) or "Erro" not in result
        return ToolReport("buscar_cep", success, str(result))

    def run_ip_lookup(self, ip: str) -> ToolReport:
        result = Buscar_ip(ip)
        success = not isinstance(result, str) or "Erro" not in result
        return ToolReport("buscar_ip", success, str(result))

    def run_lockout_test(self, url: str, email: str, attempts: int) -> ToolReport:
        result = bf_on(url=url, email=email, max_attempts=attempts)
        success = "LOCKOUT detectado" in result
        return ToolReport("lockout_tester", success, result)
