import re
from io import BytesIO
from unicodedata import normalize
import base64


def get_value(identify, value):
    """Formata o valor de acordo com o identificador.
    :param identify: Identificador do tipo de valor (ex: '00', '01', etc.).
    :param value: Valor a ser formatado.
    :return: Valor formatado como string, com o identificador e o tamanho do valor.
    """
    return f"{identify}{str(len(value)).zfill(2)}{value}"


def formatted_text(value):
    """Formata o texto removendo caracteres especiais e normalizando.
    :param value: Texto a ser formatado.
    :return: Texto formatado, contendo apenas caracteres alfanuméricos e alguns símbolos permitidos.
    """
    return re.sub(
        r'[^A-Za-z0-9$@%*+\-./:_ ]', '',
        normalize('NFD', value).encode('ascii', 'ignore').decode('ascii')
    )


def base64_qrcode(img, output, frames=None, duration=None):
    """
    Converte uma imagem para uma string codificada em base64, adequada para incorporação em HTML ou outros formatos.
    Se frames forem fornecidos, cria um GIF; caso contrário, salva uma imagem PNG única.
    Esta função utiliza um buffer BytesIO para manipular os dados da imagem em memória, evitando operações de I/O em disco.
    A string base64 resultante pode ser usada diretamente numa tag <img> HTML ou contextos similares.
    :param img: Objeto PIL Image a ser convertido.
    :param output: Caminho do arquivo de saída para a imagem (não utilizado nesta função, mantido por compatibilidade).
    :param frames: Lista de objetos PIL Image para criar um GIF animado (opcional).
    :param duration: Duração de cada frame no GIF (em milissegundos, opcional).
    :return: String codificada em base64 dos dados da imagem, prefixada com o esquema de URI de dados apropriado.
    """
    img_buffer = BytesIO()
    extension = "png"

    if frames:
        extension = "gif"
        for mode in [img_buffer, output]:
            frames[0].save(
                mode,
                save_all=True,
                format=extension.upper(),
                append_images=frames[1:],
                duration=duration,
                loop=0
            )
    else:
        img.save(img_buffer, format=extension.upper())
        img.save(output, format=extension.upper())

    img_buffer.seek(0)
    res = img_buffer.read()
    img_buffer.close()

    data_string = base64.b64encode(res).decode()
    return f"data:image/{extension};base64,{data_string}"
