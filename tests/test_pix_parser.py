import pytest
from pypix.core.utils.pix_parser import parse_br_code

# Cada tupla contém: (id_do_teste, br_code_string, resultados_esperados)
VALID_BR_CODES_DATA = [
    (
        "celular_com_valor",
        "00020101021126690014br.gov.bcb.pix0114+55279957722910229Doacao Livre / QRCODE - PYPIX52040000530398654045.005802BR5905Teste6009Cariacica61082914861362130509PIXMP00016304325F",
        {"nome": "Teste", "cidade": "Cariacica", "valor": 5.00, "chave": "+5527995772291", "txid": "PIXMP0001"}
    ),
    (
        "aleatoria_com_valor_zero",
        "00020101021126910014br.gov.bcb.pix0136b5fe1edc-d108-410f-b966-eccaaca75e4f0229Doacao Livre / QRCODE - PYPIX52040000530398654030.05802BR5921Cleiton Leonel Creton6009Cariacica62070503***63049182",
        {"nome": "Cleiton Leonel Creton", "cidade": "Cariacica", "valor": 0.0,
         "chave": "b5fe1edc-d108-410f-b966-eccaaca75e4f", "txid": "***"}
    ),
    (
        "aleatoria_com_valor_baixo",
        "00020101021126910014br.gov.bcb.pix0136b5fe1edc-d108-410f-b966-eccaaca75e4f0229Doacao Livre / QRCODE - PYPIX52040000530398654040.015802BR5921Cleiton Leonel Creton6009Cariacica62070503***63045A49",
        {"nome": "Cleiton Leonel Creton", "cidade": "Cariacica", "valor": 0.01,
         "chave": "b5fe1edc-d108-410f-b966-eccaaca75e4f", "txid": "***"}
    ),
    (
        "aleatoria_com_valor_zero_ponto_zero",
        "00020101021126910014br.gov.bcb.pix0136b5fe1edc-d108-410f-b966-eccaaca75e4f0229Doacao Livre / QRCODE - PYPIX52040000530398654040.005802BR5921Cleiton Leonel Creton6009Cariacica62070503***6304E106",
        {"nome": "Cleiton Leonel Creton", "cidade": "Cariacica", "valor": 0.0,
         "chave": "b5fe1edc-d108-410f-b966-eccaaca75e4f", "txid": "***"}
    ),
    (
        "dinamico_sem_valor",
        "00020101021226450014br.gov.bcb.pix2523bitsorbyte.com.br/login5204000053039865802BR5916TESOURO NACIONAL6008BRASILIA62070503***63042D75",
        {"nome": "TESOURO NACIONAL", "cidade": "BRASILIA", "valor": "Não especificado", "chave": None, "txid": "***"}
    ),
]


@pytest.mark.parametrize("test_id, br_code, expected", VALID_BR_CODES_DATA, ids=[data[0] for data in VALID_BR_CODES_DATA])
def test_parse_br_code_com_dados_validos(test_id, br_code, expected):
    """
    Testa o parse de BR Codes válidos, verificando campos-chave e a validade do CRC.
    """
    result = parse_br_code(br_code)

    # Validações principais
    assert result['validacao']['valido'] is True
    assert result['validacao']['crc16_calculado'] == result['validacao']['crc16_fornecido']
    assert result['recebedor']['nome'] == expected['nome']
    assert result['recebedor']['cidade'] == expected['cidade']
    assert result['valor_transacao'] == expected['valor']
    assert result['info_pix']['chave_pix'] == expected['chave']
    assert result['info_pix']['txid'] == expected['txid']


def test_parse_br_code_com_crc_invalido():
    """
    Testa se a função identifica corretamente um CRC inválido.
    """
    # Pega um código válido e adultera o CRC no final (325F -> 325E)
    invalid_br_code = "00020101021126690014br.gov.bcb.pix0114+55279957722910229Doacao Livre / QRCODE - PYPIX52040000530398654045.005802BR5905Teste6009Cariacica61082914861362130509PIXMP00016304325E"

    result = parse_br_code(invalid_br_code)

    assert result['validacao']['valido'] is False
    assert result['validacao']['crc16_calculado'] == "325F"
    assert result['validacao']['crc16_fornecido'] == "325E"


def test_parse_br_code_malformado_sem_crc():
    """
    Testa se a função levanta um erro (ValueError) para uma string sem o campo CRC.
    """
    # String sem o campo '6304...' no final
    malformed_br_code = "00020101021126690014br.gov.bcb.pix0114+5527995772291"

    with pytest.raises(ValueError, match="String PIX inválida: campo CRC .* não encontrado"):
        parse_br_code(malformed_br_code)
