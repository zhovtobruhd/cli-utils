import cbor


class CBORViewApp:
    def __init__(self, **kwargs):
        self.path = None
        self.raw = None
        self._data = None

    @property
    def data(self):
        return self._data

    def run(self, stdscr, **kwargs):
        self.path = kwargs.get('path')

        if self.path is None and self.data is None:
            raise ValueError('No data to work with')

        with open(self.path, 'rb') as f:
            self.raw = f.read()

        self._parse_data()

        print(self.data)

    def _parse_data(self):
        if self.raw is None:
            raise ValueError('Nothing to parse')

        self._data = CBORViewApp._parse(cbor.loads(self.raw))

    @staticmethod
    def _parse(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, bytes):
                    res = cbor.loads(v)
                    if res is not None:
                        obj[k] = CBORViewApp._parse(res)
        elif isinstance(obj, bytes):
            res = cbor.loads(obj)
            if res is not None:
                return CBORViewApp._parse(res)

        return obj
