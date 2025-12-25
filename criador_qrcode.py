import qrcode

url = input("Me diga a url!:")
image = qrcode.make(url)
image.save("Qrcode.png")
print("Qrcode criado com sucesso!\nSalvo como Qrcode.png")
opn = int(input("Quer visualizar o seu Qrcode?\n1-Sim/2-Não:"))
if opn == 1:
    image.show()
else:
    pass

