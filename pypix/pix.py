import base64
import re
import sys
import crc16
import qrcode
from PIL import Image
from unicodedata import normalize
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


def right_pad(value):
    return f'0{value}' if value < 10 else value


def formatted_text(value):
    text = value.upper().replace('Ç', 'C')
    return re.sub(r'[^A-Z0-9$@%*+-\./:]', '\n', normalize('NFD', text).encode('ASCII', 'ignore').decode('ASCII'))


def crc_compute(hex_string):
    msg = bytes(hex_string, 'utf-8')
    crc = crc16.crc16xmodem(msg, 0xffff)
    return '{:04X}'.format(crc & 0xffff)


class Pix(object):

    def __init__(self):
        self.single_transaction = False
        self.key = ''
        self.name_receiver = ''
        self.city_receiver = ''
        self.value = 0
        self.zipcode_receiver = ''
        self.identification = ''
        self.description = ''
        self.default_url_pix = ''
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

    def set_value(self, value=None):
        if len(str("{0:.2f}".format(value))) > 13:
            print('The maximum number of characters for the value is 13.')
            sys.exit()

        self.value = value

    def is_single_transaction(self, single_transaction=None):
        self.single_transaction = single_transaction

    def get_br_code(self):
        lines = []
        lines.append('0002 01')

        if self.single_transaction:
            lines.append('0102 12')

        description = formatted_text(self.description or '')

        extra = 14 + 8
        if description:
            extra += 4 + len(description)

        if self.key:
            if len(self.key) == 11:
                if validate_cpf(self.key):
                    self.key = self.key
                elif validate_phone(self.key):
                    self.key = f'+55{self.key}'

            content = formatted_text(self.key)
            lines.append(f'26{len(content) + extra}')
            lines.append('\t0014 br.gov.bcb.pix')
            lines.append(f'\t01{right_pad(len(content))} {content}')
        elif self.default_url_pix:
            default_url = self.default_url_pix
            lines.append(f'26{len(default_url) + extra}')
            lines.append('\f0014 br.gov.bcb.pix')
            lines.append(f'\t25{right_pad(len(default_url))} {default_url}')
        else:
            print('You must enter a URL or a pix key.')
            sys.exit()

        if self.description:
            lines.append(f'\t02{right_pad(len(description))} {description}')

        lines.append('5204 0000')
        lines.append('5303 986')

        if self.value:
            value = formatted_text(str(self.value))
            if self.value > 0:
                lines.append(f'54{right_pad(len(value))} {value}')

        lines.append('5802 BR')
        name = formatted_text(self.name_receiver)
        lines.append(f'59{right_pad(len(name))} {name}')

        city = formatted_text(self.city_receiver)
        lines.append(f'60{right_pad(len(city))} {city}')

        if self.zipcode_receiver:
            zipcode = formatted_text(self.zipcode_receiver)
            lines.append(f'61{right_pad(len(zipcode))} {zipcode}')

        if self.identification:
            identification = formatted_text(self.identification)
            lines.append(f'62{len(identification) + 38}')
            lines.append(f'\t05{right_pad(len(identification))} {identification}')
            lines.append('\t5030')
            lines.append('\t\t0017 br.gov.bcb.brcode')
            lines.append('\t\t0105 1.0.0')

        if self.default_url_pix:
            lines.append('6207')
            lines.append('\t0503 ***')

        lines.append('6304')

        lines = map(lambda item: item.replace(' ', ''), lines)
        result_string = ''.join(lines).replace('\t', '').replace('\n', ' ')

        return result_string + crc_compute(result_string)

    @staticmethod
    def get_qrcode(version=1, size=2, border=5):
        qr = qrcode.QRCode(
            version=version,
            box_size=size,
            border=border)
        return qr

    def save_qrcode(self, output='.', custom_logo=None, size=None):
        size = 8 if custom_logo else size
        try:
            self.qr = self.get_qrcode(size=size)
            self.qr.add_data(self.get_br_code())
            self.qr.make(fit=True)
            img = self.qr.make_image(fill='black', back_color='white').convert("RGB")
            img.save(f'{output}')
            if custom_logo:
                return self.qr_logo(custom_logo, qr_code=img)
            return self.base64_qrcode(img)
        except ValueError:
            return False

    @staticmethod
    def base64_qrcode(img):
        img_buffer = BytesIO()
        img.save(img_buffer, 'png')
        res = img_buffer.getvalue()
        img_buffer.close()
        data_string = base64.b64encode(res).decode()
        return f'data:image/png;base64,{data_string}'

    def qr_ascii(self):
        return self.qr.print_ascii()

    @staticmethod
    def qr_logo(logo, qr_code):
        lg = Image.open(logo)
        width = 100
        wpercent = (width / float(lg.size[0]))
        hsize = int((float(lg.size[1]) * float(wpercent)))
        logo_qr = lg.resize((width, hsize), Image.ANTIALIAS)
        pos = ((qr_code.size[0] - logo_qr.size[0]) // 2,
               (qr_code.size[1] - logo_qr.size[1]) // 2)
        qr_code.paste(logo_qr, pos)
        return qr_code.save('custom_qr.png')
