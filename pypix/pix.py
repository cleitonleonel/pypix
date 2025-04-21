import re
import base64
from io import BytesIO
from binascii import crc_hqx
from unicodedata import normalize
from pypix.core.qrgen import Generator


def validate_cpf(numbers):
    cpf = [int(char) for char in numbers if char.isdigit()]
    if len(cpf) != 11:
        return False
    if cpf == cpf[::-1]:
        return False
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


def validate_phone(value):
    rule = re.compile(r'^\+?[1-9]\d{1,14}$')
    return bool(rule.match(value))


def get_value(identify, value):
    return f"{identify}{str(len(value)).zfill(2)}{value}"


def formatted_text(value):
    return re.sub(
        r'[^A-Za-z0-9$@%*+\-./:_ ]', '',
        normalize('NFD', value).encode('ascii', 'ignore').decode('ascii')
    )


def crc_compute(hex_string):
    msg = bytes(hex_string, 'utf-8')
    crc = crc_hqx(msg, 0xffff)
    return '{:04X}'.format(crc & 0xffff)


def get_qrcode():
    qr_generator = Generator()
    return qr_generator


def base64_qrcode(img):
    img_buffer = BytesIO()
    img.save(img_buffer, 'png')
    res = img_buffer.getvalue()
    img_buffer.close()
    data_string = base64.b64encode(res).decode()
    return f'data:image/png;base64,{data_string}'


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
        self.qr = None

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
            output='./qrcode.png',
            box_size=7,
            border=1,
            custom_logo=None,
            **kwargs
    ):
        try:
            self.qr = get_qrcode()

            qr_img = self.qr.create_custom_qr(
                self.get_br_code(),
                size=box_size,
                border=border,
                center_image=custom_logo,
                **kwargs
            )
            qr_img.save(output)
            return base64_qrcode(qr_img)
        except ValueError as e:
            print(f"Error saving QR Code: {e}")
            return False

    def qr_ascii(self):
        return self.qr.print_ascii()
