# pypix

<img src="https://github.com/cleitonleonel/pypix/blob/master/pypix.png?raw=true" alt="pypix" width="450"/>

**pypix** é uma biblioteca Python baseada no projeto [GPIX](https://github.com/hiagodotme/gpix.git) de Hiago Silva Souza.  
Ela facilita a geração de códigos BR-Code estáticos e dinâmicos para transações via PIX, além de permitir personalização avançada de QR Codes com estilos visuais.

---

## 🛠️ Instalação

Clone o repositório e instale as dependências usando o Poetry:

```bash
git clone https://github.com/cleitonleonel/pypix.git
cd pypix
pip install poetry
poetry install
```

---

## 🚀 Como usar

```python
from pypix.pix import Pix
from pypix.core.utils.pix_parser import parse_br_code
from pypix.core.styles.qr_styler import GradientMode
from pypix.core.styles.marker_styles import MarkerStyle
from pypix.core.styles.border_styles import BorderStyle
from pypix.core.styles.line_styles import LineStyle
from pypix.core.styles.frame_styles import FrameStyle
import logging
import json

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def normal_static():
    """PIX Estático com valor fixo (Testado com Nubank, Inter, Caixa, MercadoPago)"""
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_identification('123')
    pix.set_zipcode_receiver('29148613')
    pix.set_description('Doação com valor fixo - PYPIX')
    pix.set_amount(5.0)

    print('\nDoação com valor definido - PYPIX >>>>\n', pix.get_br_code())


def simple_static():
    """PIX Estático com valor livre (Inter exige valor mínimo de R$ 1, Nubank/Caixa aceitam qualquer valor)"""
    pix.set_name_receiver('Cleiton Leonel Creton')
    pix.set_city_receiver('Cariacica')
    pix.set_key('b5fe1edc-d108-410f-b966-eccaaca75e4f')
    pix.set_description('Doação Livre / QRCODE - PYPIX')

    print('Doação sem valor definido - PYPIX >>>>\n', pix.get_br_code())


def dynamic():
    """PIX Dinâmico - requer URL de payload (não testado)"""
    pix.set_name_receiver('MasterSystem LTDA')
    pix.set_city_receiver('Cariacica')
    pix.set_default_url_pix('url-location-psp')
    pix.is_single_transaction(True)

    print('\nBR-Code dinâmico - PYPIX >>>>\n', pix.get_br_code())


if __name__ == '__main__':
    pix = Pix()

    normal_static()
    # simple_static()
    # dynamic()

    # Converte o BR-Code em dicionário (útil para debugging)
    br_code = pix.get_br_code()
    decoded_data = parse_br_code(br_code)
    print(json.dumps(decoded_data, indent=4, ensure_ascii=False))

    # Gera e salva QR Code estilizado com ou sem logo
    base64qr = pix.save_qrcode(
        data=br_code,
        output='qrcode.png',
        box_size=7,
        border=1,
        custom_logo="pix.png",  # Pode ser PNG ou GIF
        marker_style=MarkerStyle.QUARTER_CIRCLE,
        border_style=BorderStyle.ROUNDED,
        line_style=LineStyle.ROUNDED,
        gradient_color="purple",
        gradient_mode=GradientMode.NORMAL,
        frame_style=FrameStyle.SCAN_ME_PURPLE,
        style_mode="Full"
    )

    if base64qr:
        logger.info("QR Code salvo com sucesso!")
        # print(base64qr)  # Base64 do QR Code (caso necessário)
        # pix.qr_ascii()  # Imprime QR Code no terminal
    else:
        logger.error("Erro ao salvar o QR Code.")
```

---

## 🙌 Essa lib foi útil pra você?

Se sim, considere fazer uma doação — pode ser até R$ 0,50 😄  
Para isso, é só escanear o QR Code abaixo, gerado com o próprio pypix:

<img src="https://github.com/cleitonleonel/pypix/blob/master/qrcode.png?raw=true" alt="QRCode Doação" width="250"/>

<img src="https://github.com/cleitonleonel/pypix/blob/master/artistic.gif?raw=true" alt="QRCode Doação" width="250"/>

---

## 👨‍💻 Autor

**Cleiton Leonel Creton**  
📧 cleiton.leonel@gmail.com  
🔗 [GitHub](https://github.com/cleitonleonel)  
🔗 [LinkedIn](https://www.linkedin.com/in/cleiton-leonel-creton-331138167/)