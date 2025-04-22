# _pypix_

<img src="https://github.com/cleitonleonel/pypix/blob/master/pypix.png?raw=true" alt="pypix" width="450"/>

PYPIX is a python library based on the [GPIX](https://github.com/hiagodotme/gpix.git) project by Hiago Silva Souza that facilitates the generation of dynamic and static br-codes for transactions via PIX.
# Installing the pypix library

```shell
pip install git+https://github.com/cleitonleonel/pypix.git
cd pypix
pip install poetry
poetry install
```

# How to use

```python
from pypix.pix import Pix
from pypix.core.styles.qr_styler import GradientMode
from pypix.core.styles.marker_styles import MarkerStyle
from pypix.core.styles.border_styles import BorderStyle
from pypix.core.styles.line_styles import LineStyle
from pypix.core.styles.frame_styles import FrameStyler


def normal_static():  # Testado e funcionando para Nubank, Inter, Caixa, Mercadopago
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

    base64qr = pix.save_qrcode(
        'qrcode.png',
        box_size=7,
        border=1,
        custom_logo="pix.png",
        marker_style=MarkerStyle.QUARTER_CIRCLE,
        border_style=BorderStyle.ROUNDED,
        line_style=LineStyle.ROUNDED,
        gradient_color="green",
        gradient_mode=GradientMode.MULTI,
        frame_style=FrameStyler.SCAN_ME_PURPLE,
        style_mode="Full"  # Normal
    )

    pix.qr_ascii()  # Imprime qrcode no terminal

    if base64qr:  # Imprime qrcode em fomato base64
        print('Success in saving static QR-code.')
        print(base64qr)
    else:
        print('Error saving QR-code.')
```

# Did this lib help you?

If this lib lets you feel free to make a donation =), it can be R $ 0.50 hahahaha. To do so, just read the qrcode below, it was generated with the lib sample file.

<img src="https://github.com/cleitonleonel/pypix/blob/master/qrcode.png?raw=true" alt="QRCode Doação" width="250"/>


<img src="https://github.com/cleitonleonel/pypix/blob/master/artistic.gif?raw=true" alt="QRCode Doação" width="250"/>

# Author

Cleiton Leonel Creton ==> cleiton.leonel@gmail.com
