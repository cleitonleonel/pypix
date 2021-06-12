import re
import os
import sys
import crc16
import base64
import qrcode
from unicodedata import normalize
from amzqr import amzqr
from PIL import Image
from io import BytesIO


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
    rule = re.compile(r'\?\b([0-9]{2,3}|0((x|[0-9]){2,3}[0-9]{2}))\?\s*[0-9]{4,5}[- ]*[0-9]{4}\b')
    if rule.search(value):
        return False

    return True


def validate_number(phone_number):
    return all([x.isdigit() for x in phone_number.split("-")])


def get_value(identify, value):
    return f"{identify}{str(len(value)).zfill(2)}{value}"


def formatted_text(value):
    return re.sub(r'[^A-a-Z-z\[\]0-9$@%*+-\./:_]', ' ',
                  normalize('NFD', value).encode('ascii', 'ignore').decode('ascii')
                  )


def crc_compute(hex_string):
    msg = bytes(hex_string, 'utf-8')
    crc = crc16.crc16xmodem(msg, 0xffff)
    return '{:04X}'.format(crc & 0xffff)


def get_qrcode(**kwargs):
    if not kwargs.get('box_size'):
        kwargs['box_size'] = 5
    qr = qrcode.QRCode(**kwargs)
    return qr


def base64_qrcode(img):
    img_buffer = BytesIO()
    img.save(img_buffer, 'png')
    res = img_buffer.getvalue()
    img_buffer.close()
    data_string = base64.b64encode(res).decode()
    return f'data:image/png;base64,{data_string}'


def qr_logo(logo, qr_code, out):
    custom_name = os.path.join(out, 'custom_qr.png')
    lg = Image.open(logo)
    width = 100
    wpercent = (width / float(lg.size[0]))
    hsize = int((float(lg.size[1]) * float(wpercent)))
    logo_qr = lg.resize((width, hsize), Image.ANTIALIAS)
    pos = ((qr_code.size[0] - logo_qr.size[0]) // 2,
           (qr_code.size[1] - logo_qr.size[1]) // 2)
    qr_code.paste(logo_qr, pos)
    qr_code.save(custom_name)
    return Image.open(custom_name)


class Pix(object):

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
        self.default_url_pix = default_url_pix.replace('https://', '')

    def set_key(self, key=None):
        self.key = key

    def set_zipcode_receiver(self, zipcode=None):
        self.zipcode_receiver = zipcode

    def set_name_receiver(self, name=None):
        if len(name) > 25:
            print('The maximum number of characters for the receiver name is 25')
            sys.exit()

        self.name_receiver = name

    def set_identification(self, identification=None):
        self.identification = identification

    def set_description(self, description=None):
        self.description = description

    def set_city_receiver(self, city=None):
        if len(city) > 15:
            print('The maximum number of characters for the receiver city is 15.')
            sys.exit()

        self.city_receiver = city

    def set_amount(self, value=None):
        if len(str("{0:.2f}".format(value))) > 13:
            print('The maximum number of characters for the value is 13.')
            sys.exit()

        self.amount = "{0:.2f}".format(value)

    def is_single_transaction(self, single_transaction=None):
        self.single_transaction = single_transaction

    def get_br_code(self):
        result_string = f"{get_value('00', '01')}" \
                        f"{get_value('01', '12' if self.single_transaction else '11')}" \
                        f"{self.get_account_information()}" \
                        f"{get_value('52', '0000')}" \
                        f"{get_value('53', '986')}" \
                        f"{get_value('54', str(self.amount))}" \
                        f"{get_value('58', 'BR')}" \
                        f"{get_value('59', formatted_text(self.name_receiver))}" \
                        f"{get_value('60', formatted_text(self.city_receiver))}" \
                        f"{get_value('61', formatted_text(self.zipcode_receiver)) if self.zipcode_receiver else ''}" \
                        f"{self.get_additional_data_field()}" \
                        f"6304"

        return result_string + crc_compute(result_string)

    def get_account_information(self):
        base_pix = get_value('00', 'br.gov.bcb.pix')
        info_string = ''
        if self.key:
            if len(self.key) == 11:
                if validate_cpf(self.key):
                    self.key = self.key
                elif validate_phone(self.key):
                    self.key = f'+55{self.key}'
            info_string += get_value('01', self.key)
        elif self.default_url_pix:
            info_string += get_value('25', self.default_url_pix)
        else:
            print('You must enter a URL or a pix key.')
            sys.exit()
        if self.description:
            info_string += get_value('02', formatted_text(self.description))

        return get_value('26', f'{base_pix}{info_string}')

    def get_additional_data_field(self):
        if self.identification:
            return get_value('62', get_value('05', formatted_text(self.identification)))
        else:
            return get_value('62', get_value('05', '***'))

    def save_qrcode(self, output='./qrcode.png', color='black', custom_logo=None, **kwargs):
        try:
            self.qr = get_qrcode(**kwargs)
            self.qr.add_data(self.get_br_code())
            self.qr.make(fit=True)
            img = self.qr.make_image(fill_color=color, back_color='white').convert("RGB")
            img.save(output)
            if custom_logo:
                img = qr_logo(custom_logo, qr_code=img, out='/'.join(output.split('/')[:-1]))
            return base64_qrcode(img)
        except ValueError:
            return False

    def get_qrcode_artistic(self, picture, version=None, colorized=True, output=None, fill=None):
        try:
            version, level, qr_name = amzqr.run(
                self.get_br_code(),
                version=version if version else 1,
                level='H',
                picture=picture,
                colorized=colorized,
                contrast=fill['contrast'] if fill else 1.0,
                brightness=fill['brightness'] if fill else 1.0,
                save_name=output if output else './artistic.gif',
                save_dir=os.getcwd()
            )
            print(f"Success in saving artistic QR-code.")
            print(version, level, qr_name)
        except ValueError:
            print('Error saving QR-code.')

        sys.exit()

    def qr_ascii(self):
        return self.qr.print_ascii()
