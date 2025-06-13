import logging
from pathlib import Path
from typing import Optional, Union
from pypix.core.qrgen import GeneratorQR
from pypix.core.utils.validators import (
    validate_cpf,
    validate_phone
)
from pypix.core.services import (
    base64_qrcode,
    get_value,
    formatted_text
)
from pypix.core.utils.pix_parser import crc_compute

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Pix:

    def __init__(self):
        self.single_transaction = False
        self.key = None
        self.name_receiver = None
        self.city_receiver = None
        self.amount = 0.0
        self.zipcode_receiver = None
        self.identification = None
        self.description = None
        self.default_url_pix = None
        self.qr = GeneratorQR()

    def set_default_url_pix(self, default_url_pix=None):
        self.default_url_pix = default_url_pix.replace('https://', '') if default_url_pix else None

    def set_key(self, key=None):
        self.key = key

    def set_zipcode_receiver(self, zipcode=None):
        self.zipcode_receiver = zipcode

    def set_name_receiver(self, name=None):
        if len(name) > 25:
            raise ValueError('The maximum number of characters for the receiver name is 25.')
        self.name_receiver = name

    def set_identification(self, identification=None):
        self.identification = identification

    def set_description(self, description=None):
        self.description = description

    def set_city_receiver(self, city=None):
        if len(city) > 15:
            raise ValueError('The maximum number of characters for the receiver city is 15.')
        self.city_receiver = city

    def set_amount(self, value=None):
        if len(str("{0:.2f}".format(value))) > 13:
            raise ValueError('The maximum number of characters for the value is 13.')
        self.amount = "{0:.2f}".format(value)

    def is_single_transaction(self, single_transaction=None):
        self.single_transaction = single_transaction

    def get_br_code(self):
        result_string = (
            f"{get_value('00', '01')}"
            f"{get_value('01', '12' if self.single_transaction else '11')}"
            f"{self.get_account_information()}"
            f"{get_value('52', '0000')}"
            f"{get_value('53', '986')}"
            f"{get_value('54', str(self.amount)) if self.key else ''}"
            f"{get_value('58', 'BR')}"
            f"{get_value('59', formatted_text(self.name_receiver))}"
            f"{get_value('60', formatted_text(self.city_receiver))}"
            f"{get_value('61', formatted_text(self.zipcode_receiver)) if self.zipcode_receiver else ''}"
            f"{self.get_additional_data_field()}"
            f"6304"
        )
        return result_string + crc_compute(result_string)

    def get_account_information(self):
        base_pix = get_value('00', 'br.gov.bcb.pix')
        info_string = ''
        if self.key:
            if len(self.key) == 11 and validate_cpf(self.key):
                self.key = self.key
            elif validate_phone(self.key):
                self.key = (
                    f'+55{self.key}' if not self.key.startswith("+55")
                    else self.key
                )
            info_string += get_value('01', self.key)
        elif self.default_url_pix:
            info_string += get_value('25', self.default_url_pix)
        else:
            raise ValueError('You must enter a URL or a pix key.')
        if self.description:
            info_string += get_value(
                '02', formatted_text(self.description)
            )
        return get_value(
            '26', f'{base_pix}{info_string}'
        )

    def get_additional_data_field(self):
        if self.identification:
            return get_value(
                '62',
                get_value('05', formatted_text(self.identification))
            )
        return get_value(
            '62', get_value('05', '***')
        )

    def save_qrcode(
            self,
            data: Optional[str] = None,
            output: str = "./qrcode.png",
            box_size: int = 7,
            border: int = 1,
            custom_logo: Optional[str] = None,
            **kwargs
    ) -> Union[str, bool]:
        output_path = Path(output)
        is_gif_logo = custom_logo and custom_logo.endswith(".gif")
        try:
            frames, duration = [], 100

            if not data:
                data = self.get_br_code()

            qr_img = self.qr.create_custom_qr(
                data=data,
                size=box_size,
                border=border,
                center_image=custom_logo if not is_gif_logo else None,
                **kwargs,
            )

            if is_gif_logo:
                output_path = output_path.with_suffix(".gif")
                frames, duration = self.qr.add_center_animation(
                    qr_img,
                    custom_logo,
                    gif_len_percent=0.85,
                    radius=2
                )

            qrcode_str = base64_qrcode(
                qr_img,
                output_path,
                frames=frames,
                duration=duration
            )
            return qrcode_str
        except ValueError as e:
            logger.error(f"Error saving QR Code: {e}")
            return False

    def qr_ascii(self):
        return self.qr.print_ascii()
