def crc_compute(data: str) -> str:
    """
    Calcula o CRC16-CCITT-FALSE para a string de dados do PIX.
    """
    crc = 0xFFFF
    data_bytes = data.encode('utf-8')

    for byte in data_bytes:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1

    return f'{crc & 0xFFFF:04X}'


def parse_tlv(data_string: str) -> dict:
    """
    Analisa uma string no formato TLV (Tag-Length-Value) e a retorna como um dicionário.
    Esta função é recursiva para lidar com campos aninhados.
    """
    data = {}
    i = 0
    while i < len(data_string):
        tag = data_string[i:i + 2]
        if len(data_string[i + 2:i + 4]) != 2:
            raise ValueError(f"Formato TLV inválido próximo à tag {tag}. Comprimento malformado.")

        length = int(data_string[i + 2:i + 4])
        value = data_string[i + 4:i + 4 + length]

        # Se for um campo que pode conter outros TLVs, chama a função recursivamente
        if tag in ['26', '62']:
            data[tag] = parse_tlv(value)
        else:
            data[tag] = value

        i += 4 + length

    return data


def parse_br_code(br_code_string: str) -> dict:
    """
    Função principal para analisar a string completa do BR Code PIX.

    Ela separa a carga útil do CRC, valida o checksum e formata a saída
    num dicionário legível.
    """

    crc_field_index = br_code_string.rfind('6304')
    if crc_field_index == -1 or len(br_code_string[crc_field_index:]) != 8:
        raise ValueError("String PIX inválida: campo CRC (ID 63) não encontrado ou malformado.")

    payload_for_crc_calc = br_code_string[:-4]
    payload_for_parsing = br_code_string[:crc_field_index] # Parse somente até antes do campo do CRC
    provided_crc = br_code_string[-4:]

    calculated_crc = crc_compute(payload_for_crc_calc)
    is_crc_valid = (calculated_crc == provided_crc)

    parsed_data = parse_tlv(payload_for_parsing)

    merchant_info = parsed_data.get('26', {})
    additional_data = parsed_data.get('62', {})

    result = {
        'dados_gerais': {
            'payload_format_indicator': parsed_data.get('00'),
            'point_of_initiation_method': 'Estático' if parsed_data.get('01') == '11' else 'Dinâmico',
            'merchant_category_code': parsed_data.get('52'),
            'transaction_currency': parsed_data.get('53'),
            'country_code': parsed_data.get('58'),
        },
        'recebedor': {
            'nome': parsed_data.get('59'),
            'cidade': parsed_data.get('60'),
            'cep': parsed_data.get('61'),
        },
        'info_pix': {
            'gui': merchant_info.get('00'),
            'chave_pix': merchant_info.get('01'),
            'descricao': merchant_info.get('02'),
            'txid': additional_data.get('05'),
        },
        'valor_transacao': float(parsed_data['54']) if '54' in parsed_data else 'Não especificado',
        'validacao': {
            'crc16_fornecido': provided_crc,
            'crc16_calculado': calculated_crc,
            'valido': is_crc_valid
        }
    }
    return result