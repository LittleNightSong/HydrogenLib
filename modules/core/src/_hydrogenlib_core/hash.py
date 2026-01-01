import collections.abc
import enum
import hashlib
import typing


class Hash(enum.Enum):
    sha1 = 'sha1'
    sha224 = 'sha224'
    sha256 = 'sha256'
    sha384 = 'sha384'
    sha512 = 'sha512'

    sha3_224 = 'sha3_224'
    sha3_256 = 'sha3_256'
    sha3_384 = 'sha3_384'
    sha3_512 = 'sha3_512'

    shake_128 = 'shake_128'
    shake_256 = 'shake_256'

    blake2b = 'blake2b'
    blake2s = 'blake2s'

    md5 = 'md5'

    def new_object(self, data: collections.abc.Buffer = b'', used_for_security=True):
        return hashlib.new(self.value(), data, usedforsecurity=used_for_security)

    def is_variable_length(self):
        return self in [Hash.shake_128, Hash.shake_256]

    def compute_str(self, data: str, encoding='utf-8'):
        obj = self.new_object(data.encode(encoding))
        return obj

    def compute_bytes(self, data: bytes | bytearray | memoryview[bytes | bytearray]):
        obj = self.new_object(data)
        return obj

    def compute_from_stream(self, stream: typing.IO[bytes], chunk_size=65536, use_hashlib_method=False):
        if use_hashlib_method:
            return hashlib.file_digest(
                stream, self.value(), _bufsize=chunk_size
            )

        # Custom Method
        obj = self.new_object()
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            obj.update(chunk)
        return obj

    def compute_from_file(self, file_path: str, chunk_size=65536):
        with open(file_path, 'rb') as stream:
            return self.compute_from_stream(stream, chunk_size)

    def compute_from_iterable(self, iterable: typing.Iterable[bytes]):
        obj = self.new_object()
        for chunk in iterable:
            obj.update(chunk)
        return obj

    async def compute_from_aiterable(self, aiterable: typing.AsyncIterable[bytes]):
        obj = self.new_object()
        async for chunk in aiterable:
            obj.update(chunk)
        return obj
