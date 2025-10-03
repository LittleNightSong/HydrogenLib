import builtins
import os


class OSError(builtins.OSError):
    @classmethod
    def from_errorcode(cls, errorcode):
        return cls(
            f"Error({errorcode}): {os.strerror(errorcode)}"
        )
