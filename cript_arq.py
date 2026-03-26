import os
import tkinter as tk
from tkinter import filedialog, messagebox
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ========================
# CONFIGURAÇÕES
# ========================
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32  # AES-256

# ========================
# DERIVAR CHAVE (ARGON2)
# ========================
def derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=1,
        hash_len=KEY_SIZE,
        type=Type.ID
    )

# ========================
# CRIPTOGRAFAR
# ========================
def encrypt_file(filepath, password):
    try:
        with open(filepath, "rb") as f:
            data = f.read()

        salt = os.urandom(SALT_SIZE)
        key = derive_key(password, salt)

        aes = AESGCM(key)
        nonce = os.urandom(NONCE_SIZE)

        encrypted = aes.encrypt(nonce, data, None)

        new_path = filepath + ".enc"
        with open(new_path, "wb") as f:
            f.write(salt + nonce + encrypted)

        messagebox.showinfo("Sucesso", f"Arquivo criptografado:\n{new_path}")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# ========================
# DESCRIPTOGRAFAR
# ========================
def decrypt_file(filepath, password):
    try:
        with open(filepath, "rb") as f:
            content = f.read()

        salt = content[:SALT_SIZE]
        nonce = content[SALT_SIZE:SALT_SIZE+NONCE_SIZE]
        encrypted = content[SALT_SIZE+NONCE_SIZE:]

        key = derive_key(password, salt)

        aes = AESGCM(key)
        decrypted = aes.decrypt(nonce, encrypted, None)

        new_path = filepath.replace(".enc", "_decrypted.txt")
        with open(new_path, "wb") as f:
            f.write(decrypted)

        messagebox.showinfo("Sucesso", f"Arquivo descriptografado:\n{new_path}")

    except Exception:
        messagebox.showerror("Erro", "Senha incorreta ou arquivo corrompido!")

# ========================
# INTERFACE
# ========================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Criptografia AES-256")
        self.root.geometry("400x250")

        self.filepath = None

        tk.Label(root, text="Arquivo:").pack(pady=5)

        self.file_label = tk.Label(root, text="Nenhum arquivo selecionado")
        self.file_label.pack()

        tk.Button(root, text="Selecionar arquivo", command=self.select_file).pack(pady=5)

        tk.Label(root, text="Senha:").pack(pady=5)

        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.pack()

        tk.Button(root, text="Criptografar", command=self.encrypt).pack(pady=10)
        tk.Button(root, text="Descriptografar", command=self.decrypt).pack()

    def select_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt *.enc")])
        if self.filepath:
            self.file_label.config(text=self.filepath)

    def encrypt(self):
        if not self.filepath:
            messagebox.showwarning("Aviso", "Selecione um arquivo!")
            return

        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Aviso", "Digite uma senha!")
            return

        encrypt_file(self.filepath, password)

    def decrypt(self):
        if not self.filepath:
            messagebox.showwarning("Aviso", "Selecione um arquivo!")
            return

        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Aviso", "Digite uma senha!")
            return

        decrypt_file(self.filepath, password)

# ========================
# EXECUTAR
# ========================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()