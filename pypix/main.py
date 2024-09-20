from pypix.pix import Pix


def normal_static():  # Testado e funcionando para Nubank, Inter, Caixa
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_identification('PIXMP0001')
    pix.set_zipcode_receiver('29148613')
    pix.set_description('Doação Livre / QRCODE - PYPIX')
    pix.set_amount(0.10)

    print('\nDonation with defined amount - PYPIX >>>>\n', pix.get_br_code())


def simple_static():  # Banco Inter exige valores acima de 1 R$, Nubank e Caixa aceitam valores livres
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_description('Doação Livre / QRCODE - PYPIX')

    print('Donation without defined amount - PYPIX >>>>\n', pix.get_br_code())


def dynamic():  # Não Testado
    pix.set_name_receiver('PAGSMILE')
    pix.set_city_receiver('Belo Horizonte')
    pix.set_default_url_pix('api-pix.bancobs2.com.br/spi/v2/a737c1c0-71c0-4939-9436-e03706047c74')
    pix.set_amount(120)
    print('\nBRCODE dinamic - PYPIX >>>>\n', pix.get_br_code())


if __name__ == '__main__':
    pix = Pix()
    normal_static()
    # simple_static()
    # dynamic()

    # base64qr = pix.save_qrcode('./qrcode.png')
    """Método para gerar qrcode, com ou sem logo"""
    base64qr = pix.save_qrcode(
        './qrcode.png',
        color="black",
        box_size=7,
        border=1,
        custom_logo={
            "logo": "pix.png",
            "border_radius": 25,
            "shape": "circle",
        }
    )
    # pix.qr_ascii()  # Imprime qrcode no terminal

    if base64qr:  # Imprime qrcode em fomato base64
        print('Success in saving static QR-code.')
        # print(base64qr)
    else:
        print('Error saving QR-code.')