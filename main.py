from pix import Pix


def normal_static():
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_identificator('123')
    pix.set_zipcode_receiver('29148613')
    pix.set_description('Doaçao com valor fixo - PYPIX')
    pix.set_value(5.0)

    print('\nDoação com valor fixo - PYPIX >>>>\n', pix.get_br_code())


def simple_static():
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_description('Doaçao Livre / QRCODE - PYPIX')

    print('Doação Livre - PYPIX >>>>\n', pix.get_br_code())


def dinamic():
    pix.set_name_receiver('MasterSystem LTDA')
    pix.set_city_receiver('Cariacica')
    pix.set_default_url_pix('url-location-instituicao')

    print('\nBRCODE dinâmico - PYPIX >>>>\n', pix.get_br_code())


if __name__ == '__main__':
    pix = Pix()

    # normal_static()
    simple_static()
    # dinamic()

    if pix.save_qrcode('./qrcode.png'):
        print('sucesso ao salvar qr-code estático')
    else:
        print('erro ao salvar qr-code')
