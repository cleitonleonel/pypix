# _pypix_

PYPIX is a python library based on the GPIX project by Hiago Silva Souza [(https://github.com/hiagodotme/gpix.git)] that facilitates the generation of dynamic and static br-codes for transactions via PIX.
# Installing the pypix library

```pip install git+https://github.com/cleitonleonel/pypix.git```

# How to use

```
from pix import Pix


def normal_static():
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')  # Pode-se passar uma chave tipo cpf, telefone, e-mail ou aleatória
    pix.set_identificator('123')
    pix.set_zipcode_receiver('29148613')
    pix.set_description('Doação com valor fixo - PYPIX')
    pix.set_value(5.0)

    print('\nDoação com valor fixo - PYPIX >>>>\n', pix.get_br_code())


def simple_static():
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')    # Pode-se passar uma chave tipo cpf, telefone, e-mail ou aleatória
    pix.set_description('Doação Livre / QRCODE - PYPIX')

    print('Doação Livre - PYPIX >>>>\n', pix.get_br_code())


def dinamic():
    pix.set_name_receiver('MasterSystem LTDA')
    pix.set_city_receiver('Cariacica')
    pix.set_default_url_pix('url-location-instituicao')

    print('\nBRCODE dinâmico - PYPIX >>>>\n', pix.get_br_code())


if __name__ == '__main__':
    pix = Pix()

    simple_static()
    # normal_static()
    # dinamic()

    base64qr = pix.save_qrcode('./qrcode.png')

    if base64qr:
        print('sucesso ao salvar qr-code estático')
        print(base64qr)
    else:
        print('erro ao salvar qr-code')
```

# Did this lib help you?

If this lib lets you feel free to make a donation =), it can be R $ 0.50 hahahaha. To do so, just read the qrcode below, it was generated with the lib sample file.

![QRCode Doação](https://github.com/cleitonleonel/pypix/blob/master/qrcode.png?raw=true)

# Author

Cleiton Leonel Creton ==> cleiton.leonel@gmail.com