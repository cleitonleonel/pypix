from pypix.pix import Pix


def normal_static():  # Testado e funcionando para Nubank, Inter, Caixa
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_identification('123')
    pix.set_zipcode_receiver('29148613')
    pix.set_description('Doação com valor fixo - PYPIX')
    pix.set_amount(5.0)

    print('\nDonation with defined amount - PYPIX >>>>\n', pix.get_br_code())


def simple_static():  # Banco Inter exige valores acima de 1 R$, Nubank e Caixa aceitam valores livres
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_description('Doação Livre / QRCODE - PYPIX')

    print('Donation without defined amount - PYPIX >>>>\n', pix.get_br_code())


def dynamic():  # Não Testado
    pix.set_name_receiver('MasterSystem LTDA')
    pix.set_city_receiver('Cariacica')
    pix.set_default_url_pix('url-location-psp')
    pix.set_amount(10.5)

    print('\nBRCODE dinamic - PYPIX >>>>\n', pix.get_br_code())


if __name__ == '__main__':
    pix = Pix()

    normal_static()
    # simple_static()
    # dynamic()

    base64qr = pix.save_qrcode('./qrcode.png', color="green", box_size=7,
                               border=1, custom_logo='/home/cleiton/PyJobs/ScriptsPython/qrcodes/g4g.jpg')
    pix.qr_ascii()

    if base64qr:
        print('Success in saving static QR-code.')
        print(base64qr)
    else:
        print('Error saving QR-code.')
