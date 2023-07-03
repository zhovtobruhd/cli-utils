import cbor
from cbor import Tag

from do_not_parse import DO_NOT_PARSE


class CBORViewApp:
    def __init__(self, **kwargs):
        self.path = None
        self.raw = None
        self.skip_raw_bytes = None
        self._data = None

    @property
    def data(self):
        return self._data

    def run(self, stdscr, **kwargs):
        self.path = kwargs.get('path')
        self.skip_raw_bytes = kwargs.get('skip_raw_bytes', 0)

        if self.path is None and self.data is None:
            raise ValueError('No data to work with')

        with open(self.path, 'rb') as f:
            self.raw = f.read()

        self._parse_data()

        CBORViewApp._print(self.data)

    def _parse_data(self):
        if self.raw is None:
            raise ValueError('Nothing to parse')

        self._data = CBORViewApp._parse(
            cbor.loads(self.raw[self.skip_raw_bytes:])
        )

    @staticmethod
    def _parse(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                obj[k] = CBORViewApp._parse(v) if k not in DO_NOT_PARSE else v.hex()
        elif isinstance(obj, bytes):
            try:
                res = cbor.loads(obj)
            except Exception:
                return obj
            if res is not None:
                return CBORViewApp._parse(res)
            else:
                return obj.hex()
        elif isinstance(obj, Tag):
            return Tag(obj.tag, CBORViewApp._parse(obj.value))
        elif isinstance(obj, (list, tuple)):
            return [CBORViewApp._parse(v) for v in obj]
        return obj

    @staticmethod
    def _print(obj, level=0, spacer='    '):
        if isinstance(obj, dict):
            print(spacer * level + '{')
            for i, (k, v) in enumerate(obj.items()):
                if i > 0:
                    print(',')
                print(spacer * (level + 1) + f'{k:#010x} : ', end='')
                if isinstance(v, (str, bool, float)):
                    print(f'{v}', end='')
                elif isinstance(v, int):
                    print(f'{v:#010x}', end='')
                else:
                    print('')
                    CBORViewApp._print(v, level + 1, spacer)
                if i + 1 == len(obj):
                    print('')
            print(spacer * level + '}', end='')

        elif isinstance(obj, (list, tuple)):
            print(spacer * level + '[')
            for i, v in enumerate(obj):
                if i > 0:
                    print(',')
                if isinstance(v, (str, bool, float)):
                    print(spacer * (level + 1) + f'{v}', end='')
                elif isinstance(v, int):
                    print(f'{v:#010x}', end='')
                else:
                    CBORViewApp._print(v, level + 1, spacer)
                if i > 0 and i + 1 == len(obj):
                    print('')
            print(spacer * level + ']', end='')

        elif isinstance(obj, Tag):
            print(spacer * (level + 1) + f'TAG({obj.tag}) : ', end='')
            if isinstance(obj.value, (str, bool, float)):
                print(f'{obj.value}')
            elif isinstance(obj.value, int):
                print(f'{obj.value:#010x}', end='')
            else:
                print('')
                CBORViewApp._print(obj.value, level + 1, spacer)
