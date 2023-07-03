# CLI utils by zhovtobruhd

## Requirements

### Windows

```bash
pip install cbor click windows-curses
```

### Linux

```bash
pip install cbor click curses
```

## Usage

### Hex View

```bash
python3 main.py hexview -p file.bin
```

### CBOR View

Note: if you do not want parser to parse specific dict fields, you can specify 
in `do_not_parse.py`

Example:
```python
DO_NOT_PARSE = [
    0x10000000,
    0x10000001
]
```
If 0x10000000 or 0x10000001 key is found during parsing, its value will be left
as string and not be parsed


```bash
python3 main.py cborview -p file.bin
```

