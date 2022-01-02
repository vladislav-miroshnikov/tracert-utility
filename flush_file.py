import io

_all__ = "flush_file"


class flush_file(io.FileIO):
    def __init__(self, f):
        self.f = f

    def write(self, x):
        self.f.write(x)
        self.f.flush()
