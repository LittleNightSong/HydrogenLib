import logging

func_logger = logging.getLogger("SzQlib.zencrypt.func")


# module end


def _pkcs7_pad(data: bytes, block_size: int) -> bytes:
    if len(data) >= block_size:
        return data
    padding_length = block_size - len(data) % block_size
    padding = bytes([padding_length]) * padding_length
    return data + padding


def _pkcs7_unpad(padded_data: bytes, block_size: int = 16) -> bytes:
    if not (len(padded_data) % block_size == 0 and 1 <= padded_data[-1] <= block_size):
        return padded_data  # 不需要解填充，直接返回原字节串

    last_byte = padded_data[-1]
    if last_byte > block_size:
        func_logger.error("Invalid padding byte value", last_byte)
        raise ValueError("Invalid padding byte value", last_byte)

    padding_length = last_byte
    if padded_data[-padding_length:] != bytes([last_byte]) * padding_length:
        func_logger.error("Invalid padding pattern")
        raise ValueError("Invalid padding pattern")

    return padded_data[:-padding_length]


def split(text, size=16):
    if len(text) % size == 0:
        return [text[i:i + size] for i in range(0, len(text), size)]
    res_lenght = ((len(text) // size) + 1) * size
    add_lenght = res_lenght - len(text)
    text = pad(text, res_lenght)
    ls = split(text, size)
    ls[-1] = ls[-1][:add_lenght]
    # print(ls)
    return ls


def pad(text: bytes, size=16):
    return _pkcs7_pad(text, size)


def unpad(text: bytes, size=16):
    return _pkcs7_unpad(text, size)
