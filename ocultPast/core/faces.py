import cv2
import questionary
import face_recognition


def capturar_foto(nome_arquivo):
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Não foi possível abrir a câmera")
        return False

    print("Pressione ESPAÇO para tirar a foto")

    while True:
        ret, frame = camera.read()

        if not ret:
            break

        cv2.imshow("Captura", frame)

        tecla = cv2.waitKey(1)

        if tecla == 32:  # espaço
            cv2.imwrite(nome_arquivo, frame)
            print("Foto salva!")
            break

        elif tecla == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    return True


def cadastrar_rosto():
    print("Cadastro iniciado")

    capturar_foto("rosto_cadastrado.jpg")

    print("Cadastro concluído!")


def validar_rosto(imagem_teste, imagem_cadastrada):
    try:
        rosto_cadastrado = face_recognition.load_image_file(
            imagem_cadastrada
        )

        rosto_teste = face_recognition.load_image_file(
            imagem_teste
        )

        encoding_cadastrado = face_recognition.face_encodings(
            rosto_cadastrado
        )

        encoding_teste = face_recognition.face_encodings(
            rosto_teste
        )

        # Verifica se encontrou rosto nas imagens
        if not encoding_cadastrado or not encoding_teste:
            return False


        resultado = face_recognition.compare_faces(
            [encoding_cadastrado[0]],
            encoding_teste[0]
        )

        return resultado[0]


    except Exception as erro:
        print("Erro:", erro)
        return False
