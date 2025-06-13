from pypix.pix import Pix
from pypix.core.utils.pix_parser import parse_br_code
from pypix.core.styles.qr_styler import GradientMode
from pypix.core.styles.marker_styles import MarkerStyle
from pypix.core.styles.border_styles import BorderStyle
from pypix.core.styles.line_styles import LineStyle
from pypix.core.styles.frame_styles import FrameStyle
import logging
import json

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def normal_static():  # Testado e funcionando para Nubank, Inter, Caixa
    """Gera um BRCODE estático com valores definidos, como nome do recebedor,
    cidade, chave PIX, identificação, CEP e descrição.
    O valor é definido como 5.00, mas pode ser alterado conforme necessário."""

    pix.set_name_receiver('Teste')
    pix.set_city_receiver('Cariacica')
    # pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_key('27995772291')
    pix.set_identification('PIXMP0001')
    pix.set_zipcode_receiver('29148613')
    pix.set_description('Doação Livre / QRCODE - PYPIX')
    pix.set_amount(5.00)

    print('\nDonation with defined amount - PYPIX >>>>\n', pix.get_br_code())


def simple_static():  # Banco Inter exige valores acima de 1 R$, Nubank e Caixa aceitam valores livres
    """Gera um BRCODE estático para doação livre, sem valor definido.
    O nome do recebedor, cidade, chave PIX e descrição são definidos, mas o valor é deixado como 0.0."""

    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_description('Doação Livre / QRCODE - PYPIX')
    pix.set_amount(0.0)  # Valor definido como 0.0 para doação livre

    print('Donation without defined amount - PYPIX >>>>\n', pix.get_br_code())


def dynamic():  # Não Testado
    """Gera um BRCODE dinâmico com valores definidos, como nome do recebedor, cidade, chave PIX,
    URL padrão e transação única.
    O valor é definido como 0.0, indicando que o valor será determinado na hora do pagamento."""

    pix.set_name_receiver('TESOURO NACIONAL')
    pix.set_city_receiver('BRASILIA')
    pix.set_default_url_pix('meupsp.com.br/fatura/123456')
    pix.is_single_transaction(True)

    print('\nBRCODE dinamic - PYPIX >>>>\n', pix.get_br_code())


if __name__ == '__main__':
    pix = Pix()
    normal_static()
    # simple_static()
    # dynamic()

    br_code = pix.get_br_code()
    decoded_data = parse_br_code(br_code)  # Converte o BRCODE em dicionário
    print(json.dumps(decoded_data, indent=4, ensure_ascii=False))

    # base64qr = pix.save_qrcode('./qrcode.png')
    """Método para gerar qrcode, com ou sem logo"""
    base64qr = pix.save_qrcode(
        data=br_code, # Optional: data pode ser o BRCODE ou uma string de dados
        output='qrcode.png',
        box_size=7,
        border=1,
        custom_logo="pix.png",  # Pode ser um gif ou uma imagem png
        marker_style=MarkerStyle.QUARTER_CIRCLE,
        border_style=BorderStyle.ROUNDED,
        line_style=LineStyle.ROUNDED,
        gradient_color="purple",
        gradient_mode=GradientMode.NORMAL,
        frame_style=FrameStyle.SCAN_ME_PURPLE,
        style_mode="Full"  # Normal
    )

    if base64qr:  # Imprime qrcode em fomato base64
        logger.info("QR Code saved successfully.")
        # print(base64qr)
        # pix.qr_ascii()  # Imprime qrcode no terminal
    else:
        logger.error('Error saving QR-code.')
