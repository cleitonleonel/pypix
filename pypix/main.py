from .pix import Pix


def normal_static():
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_identification('123')
    pix.set_zipcode_receiver('29148613')
    pix.set_description('Doação com valor fixo - PYPIX')
    pix.set_value(5.0)

    print('\nDonation with defined amount - PYPIX >>>>\n', pix.get_br_code())


def simple_static():
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_description('Doação Livre / QRCODE - PYPIX')

    print('Donation without defined amount - PYPIX >>>>\n', pix.get_br_code())


def dynamic():
    pix.set_name_receiver('MasterSystem LTDA')
    pix.set_city_receiver('Cariacica')
    pix.set_default_url_pix('url-location-psp')
    pix.set_value(10.5)

    print('\nBRCODE dinamic - PYPIX >>>>\n', pix.get_br_code())


if __name__ == '__main__':
    pix = Pix()
    #simple_static()

    normal_static()
    # dynamic()

    base64qr = pix.save_qrcode('./qrcode.png')

    if base64qr:
        print('Success in saving static QR-code.')
        print(base64qr)
    else:
        print('Error saving QR-code.')
