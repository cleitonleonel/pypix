# _pypix_

PYPIX é um biblioteca python que facilita a geração de br-codes dinâmicos e estáticos para o transações via PIX.

# Instalação

```pip install git+https://github.com/cleitonleonel/pypix.git```

# Como utilizar

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

# Essa lib te ajudou?

Se essa lib te ajudou fique a vontade para fazer uma doação =), pode ser R$ 0.50 hahahaha. Para isso basta ler o qrcode abaixo, ele foi gerado com o arquivo de exemplo da lib.

![QRCode Doação](https://github.com/cleitonleonel/pypix/blob/master/qrcode.png?raw=true)

# Autor

Cleiton Leonel Creton ==> cleiton.leonel@gmail.com