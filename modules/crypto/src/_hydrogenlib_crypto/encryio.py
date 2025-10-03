# from .encrypt.aes import decrypt as aes_decode, encode as aes_encode
# from .._hycore.json_file import *
# from .._hycore.utils import null
#
#
# module not end
# TODO: 完成模块
#
# class _EncryptJsonFile:
#     """
#     entrypt the value , not key and value
#     """
#
#     def __init__(self, filename, key, iv):
#         self.iostream = pickle_safe_open(filename, dict)
#         self.key, self.iv = key, iv
#
#     def __getitem__(self, item):
#         cry_text = self.iostream[item]
#         plain_text = aes_decode(cry_text, self.key, self.iv)
#         return Pickle.decode(plain_text)
#
#     def __setitem__(self, key, value):
#         value = Pickle.encode(value)
#         cry_text = aes_encode(value, self.key, self.iv)
#         self.iostream[key] = cry_text
#
#     def __delitem__(self, key):
#         del self.iostream[key]
#
#     def get(self, key, default=null):
#         try:
#             x = self.iostream.peek(key, default)
#             return aes_decode(x, self.key, self.iv)
#         except KeyError as e:
#             if default is not null:
#                 return default
#             raise e
#
#     def clear(self):
#         self.iostream.clear()
#
#     def set(self, key, value):
#         self[key] = value
#
#     def keys(self):
#         return self.iostream.keys()
#
#     def values(self):
#         return self.iostream.values()
#
#     def items(self):
#         return self.iostream._instances()
#
#     def __iter__(self):
#         return self.iostream.__iter__()
#
#     def save(self):
#         self.iostream.save()
#
#     def flush(self):
#         self.iostream.flush()
#
#     def close(self):
#         self.iostream.close()
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.close()
#
#
# def EncryptJsonOpen(filename, key, iv):
#     return _EncryptJsonFile(filename, key, iv)
#
# # TODO: finish this class
# # class EncryptSyncSocket(SyncSocket):
# #     def __init__(self, s: socket.socket | object | None, aes_key=None, aes_iv=None, rsa_pubkey=None, rsa_prikey=None):
# #         super().__init__(s)
# #         self._encry_mode = None
# #
# #         if not any([aes_key, aes_iv, rsa_pubkey, rsa_prikey]):
# #             raise ValueError("必须指定aes_key, aes_iv, rsa_pubkey, rsa_prikey")
# #
# #         if aes_key is not None and aes_iv is not None:
# #             self._encry_mode = 'aes'
# #             self.key1 = aes_key
# #             self.key2 = aes_iv
# #
# #         elif rsa_pubkey is not None and rsa_prikey is not None:
# #             self._encry_mode = 'rsa'
# #             self.key1 = rsa_pubkey
# #             self.key2 = rsa_prikey
# #
# #         else:
# #             args = [
# #                 k for k, v in
# #                 {'aes_key': aes_key, 'aes_iv': aes_iv, 'rsa_pubkey': rsa_pubkey, 'rsa_prikey': rsa_prikey}.items() if
# #                 v is not None
# #             ]
# #             raise ValueError(
# #                 f"无法确定加密方式(Args: {tuple(args)}"
# #             )
# #
# #     def write(self, data):
# #         data = Pickle.encode(data).encode()  # <------------- encode() return bytes
# #         if self._encry_mode:
# #             if self._encry_mode == 'aes':
# #                 encry_data = aes_encode(data, self.key1, self.key2)
# #             elif self._encry_mode == 'rsa':
# #                 encry_data = rsa_encrypt(data, self.key1)
# #             else:
# #                 raise ValueError("无效的加密模式")
# #             super().write(encry_data)
# #
# #     def read(self, timeout=None):
# #         if self._encry_mode:
# #             if self._encry_mode == 'aes':
# #                 encry_data = super().read(timeout)
# #                 decry_data = aes_decode(encry_data, self.key1, self.key2)
# #             elif self._encry_mode == 'rsa':
# #                 encry_data = super().read(timeout)
# #                 decry_data = rsa_decrypt(encry_data, self.key2)
# #             else:
# #                 raise ValueError("无效的加密模式")
# #
# #             return Pickle.decode(decry_data.decode())
