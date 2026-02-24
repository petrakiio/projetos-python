import secrets
import string
import time
import requests


def _random_password(size: int = 14) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(size))


def bf_on(
    url: str,
    email: str,
    max_attempts: int = 15,
    login_field: str = "gmail",
    password_field: str = "password",
    lockout_marker: str = "Muitas tentativas",
    invalid_marker: str = "Credenciais inválidas",
    sleep_seconds: float = 0.15,
    timeout: float = 8.0,
) -> str:
    if not url or not email:
        return "URL e email sao obrigatorios."

    lines = [f"Lockout tester em {url}", f"conta={email}"]
    for i in range(1, max_attempts + 1):
        payload = {login_field: email, password_field: _random_password()}
        try:
            response = requests.post(url, data=payload, timeout=timeout)
            body = response.text
            if lockout_marker in body:
                lines.append(f"[{i}] LOCKOUT detectado")
                return "\n".join(lines)
            if invalid_marker in body:
                lines.append(f"[{i}] credencial invalida")
            else:
                lines.append(f"[{i}] resposta nao mapeada (HTTP {response.status_code})")
        except requests.RequestException as err:
            lines.append(f"[{i}] erro: {err}")

        time.sleep(sleep_seconds)

    lines.append("Lockout nao detectado dentro do limite informado.")
    return "\n".join(lines)
