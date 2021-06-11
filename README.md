# _pypix_

<img src="https://github.com/cleitonleonel/pypix/blob/master/pypix.png?raw=true" alt="pypix" width="450"/>

PYPIX is a python library based on the GPIX project by Hiago Silva Souza [(https://github.com/hiagodotme/gpix.git)] that facilitates the generation of dynamic and static br-codes for transactions via PIX.
# Installing the pypix library

```pip install git+https://github.com/cleitonleonel/pypix.git```

# How to use

```python
from pypix.pix import Pix


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
    simple_static()

    # normal_static()
    # dynamic()

    base64qr = pix.save_qrcode('./qrcode.png')

    if base64qr:
        print('Success in saving static QR-code.')
        print(base64qr)
    else:
        print('Error saving QR-code.')

```

# Did this lib help you?

If this lib lets you feel free to make a donation =), it can be R $ 0.50 hahahaha. To do so, just read the qrcode below, it was generated with the lib sample file.

<img src="https://github.com/cleitonleonel/pypix/blob/master/qrcode.png?raw=true" alt="QRCode Doação" width="250"/>


# Author

Cleiton Leonel Creton ==> cleiton.leonel@gmail.com