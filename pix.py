import re
import crc16
import qrcode
from unicodedata import normalize


def right_pad(value):
    return f'0{value}' if value < 10 else value


def formated_text(value):
    text = value.upper().replace('Ç', 'C')
    return re.sub('[^A-Z0-9$%*+-/:]', '\n', normalize('NFD', text))


def crc_compute(hex_string):
    msg = bytes(hex_string, 'utf-8')
    crc = crc16.crc16xmodem(msg, 0xffff)
    return '{:04X}'.format(crc & 0xffff)


class Pix(object):

    def __init__(self):
        self.single_transation = False
        self.key = ''
        self.name_receiver = ''
        self.city_receiver = ''
        self.value = 0
        self.zipcode_receiver = ''
        self.identificator = ''
        self.description = ''
        self.default_url_pix = ''

    def set_default_url_pix(self, default_url_pix=None):
        self.default_url_pix = default_url_pix.replace('https://', '')

    def set_key(self, key=None):
        self.key = key

    def set_zipcode_receiver(self, zipcode=None):
        self.zipcode_receiver = zipcode

    def set_name_receiver(self, name=None):
        if len(name) > 25:
            return 'A quantidade máxima de caracteres para o nome do recebedor é 25'

        self.name_receiver = name

    def set_identificator(self, identificator=None):
        self.identificator = identificator

    def set_description(self, description=None):
        self.description = description

    def set_city_receiver(self, city=None):
        if len(city) > 15:
            return 'A quantidade máxima de caracteres para a cidade do recebedor é 15'

        self.city_receiver = city

    def set_value(self, value=None):
        if len(str("{0:.2f}".format(value))) > 13:
            return 'A quantidade máxima de caracteres para o valor é 13'

        self.value = value

    def is_single_transation(self, single_transation=None):
        self.single_transation = single_transation

    def get_br_code(self):
        lines = []
        lines.append('0002 01')

        if self.single_transation:
            lines.append('0102 12')

        description = formated_text(self.description or '')

        extra = 14 + 8
        if description:
            extra += 4 + len(description)

        if self.key:
            content = formated_text(self.key)
            print(content)
            lines.append(f'26{len(content) + extra}')
            lines.append('\t0014 br.gov.bcb.pix')
            lines.append(f'\t01{right_pad(len(content))} {content}')
        elif self.default_url_pix:
            default_url = self.default_url_pix
            lines.append(f'26{len(default_url) + extra}')
            lines.append('\f0014 br.gov.bcb.pix')
            lines.append(f'\t25{right_pad(len(default_url))} {default_url}')
        else:
            return 'É necessário informar uma URL ou então uma chave pix.'

        if self.description:
            lines.append(f'\t02{right_pad(len(description))} {description}')

        lines.append('5204 0000')
        lines.append('5303 986')

        if self.value:
            value = formated_text(str(self.value))
            if self.value > 0:
                lines.append(f'54{right_pad(len(value))} {value}')

        lines.append('5802 BR')
        name = formated_text(self.name_receiver)
        lines.append(f'59{right_pad(len(name))} {name}')

        city = formated_text(self.city_receiver)
        lines.append(f'60{right_pad(len(city))} {city}')

        if self.zipcode_receiver:
            zipcode = formated_text(self.zipcode_receiver)
            lines.append(f'61{right_pad(len(zipcode))} {zipcode}')

        if self.identificator:
            identificator = formated_text(self.identificator)
            lines.append(f'62{len(identificator) + 38}')
            lines.append(f'\t05{right_pad(len(identificator))} {identificator}')
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

    def get_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)

        return qr

    def save_qrcode(self, output='.'):
        try:
            qr = self.get_qrcode()
            qr.add_data(self.get_br_code())
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img.save(f'{output}')
            return True
        except:
            return False
