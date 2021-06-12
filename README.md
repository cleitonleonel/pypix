# _pypix_

<img src="https://github.com/cleitonleonel/pypix/blob/master/pypix.png?raw=true" alt="pypix" width="450"/>

PYPIX is a python library based on the GPIX project by Hiago Silva Souza [(https://github.com/hiagodotme/gpix.git)] that facilitates the generation of dynamic and static br-codes for transactions via PIX.
# Installing the pypix library

```pip install git+https://github.com/cleitonleonel/pypix.git```

# How to use

```python
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

    """Método para gerar qrcode, com ou sem logo"""
    base64qr = pix.save_qrcode('./qrcode.png', color="green", box_size=7,
                               border=1, custom_logo='/home/cleiton/PyJobs/ScriptsPython/qrcodes/g4g.jpg'
                               )
    pix.qr_ascii()  # Imprime qrcode no terminal

    if base64qr:  # Imprime qrcode em fomato base64
        print('Success in saving static QR-code.')
        print(base64qr)
    else:
        print('Error saving QR-code.')

    """Método para gerar qrcode estilizado, colorido ou não e animado"""
    pix.get_qrcode_artistic('./py.gif', version=3, output='./artistic.gif',
                            fill={'contrast': 10.0, 'brightness': 1.0}
                            )

```

# Did this lib help you?

If this lib lets you feel free to make a donation =), it can be R $ 0.50 hahahaha. To do so, just read the qrcode below, it was generated with the lib sample file.

<img src="https://github.com/cleitonleonel/pypix/blob/master/qrcode.png?raw=true" alt="QRCode Doação" width="250"/>


# Author

Cleiton Leonel Creton ==> cleiton.leonel@gmail.com