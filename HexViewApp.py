import curses
import sys
import time

import logging
logging.basicConfig(filename='log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('two-wins')


ADDRESS_WIN_WIDTH = 12
ASCII_WIN_WIDTH = 18

BYTES_PER_ROW = 16


class HexViewApp:
    def __init__(self, **kwargs):
        self.start_row = 0
        self.rows = 0
        self.columns = 0
        self.render = True
        self.data = None
        self.path = None

    def run(self, stdscr, **kwargs):
        self.path = kwargs.get('path')

        if self.path is None and self.data is None:
            raise ValueError('No data to work with') 

        with open(self.path, 'rb') as f:
            self.data = f.read()
        
        a, b, c = self._parse_data(self.data)

        self.start_row = 0

        self.a = a
        self.render = True 
        stdscr.clear()
        stdscr.refresh()

        while True:
            
            if True:
                self.render = False

                height, width = stdscr.getmaxyx()

                self.columns = width
                self.rows = height

                win1 = curses.newwin(self.rows, ADDRESS_WIN_WIDTH, 0, 0)
                win2 = curses.newwin(
                    self.rows,
                    self.columns - ADDRESS_WIN_WIDTH - ASCII_WIN_WIDTH,
                    0,
                    ADDRESS_WIN_WIDTH
                )
                win3 = curses.newwin(self.rows, ASCII_WIN_WIDTH, 0, self.columns - ASCII_WIN_WIDTH)
                
                lth = self.columns - ADDRESS_WIN_WIDTH - ASCII_WIN_WIDTH - 2

                win1.border(0)
                win2.border(0)
                win3.border(0)

                win1.addstr(0, 2, "Address")
                win2.addstr(0, 2, "HEX")
                win3.addstr(0, 2, "ASCII")

                for i, v in enumerate(
                    a[self.start_row:self.start_row + self.rows - 2]
                ):
                    if i + 3 > self.rows:
                        break
                    win1.addstr(i + 1, 1, v)

                for i, v in enumerate(
                    b[self.start_row:self.start_row + self.rows - 2]
                ):
                    if i + 3 > self.rows:
                        break
                    
                    if lth <= BYTES_PER_ROW * 2 + 1:
                        srow = ' '
                    elif lth <= BYTES_PER_ROW * 2 + BYTES_PER_ROW // 4:
                        srow = ''.join(v).strip()
                    elif lth <= BYTES_PER_ROW * 3:
                        srow = ' '.join(
                            [''.join(v[i:i+4]) for i in range(0, len(v), 4)]
                        )
                    else:
                        srow = ' '.join(v).strip()
                    win2.addstr(i + 1, 1, ' ' + srow)

                for i, v in enumerate(
                    c[self.start_row: self.start_row + self.rows - 2]
                ):
                    if i + 3 > self.rows:
                        break
                    win3.addstr(i + 1, 1, v)

                win1.refresh()
                win2.refresh()
                win3.refresh()
                logger.info('REFRESHED')

            self.process_keys(stdscr)
            time.sleep(.02)

    def process_keys(self, stdscr):
        k = stdscr.getch()

        if k == ord('s') or k == curses.KEY_DOWN:
            self.start_row = self.start_row if self.start_row + self.rows - 2 >= len(self.a) else self.start_row + 1
            self.render = True
        elif k == ord('w') or k == curses.KEY_UP:
            self.start_row = 0 if self.start_row <= 0 else self.start_row - 1
            self.render = True
        elif k == ord('q'):
            sys.exit(0)
        elif k == curses.KEY_RESIZE or k == curses.KEY_MAX:
            self.render = True

        logger.debug('Pressed key %s', k)

    @staticmethod
    def _parse_data(data, start_addr=0):
        address_view = []
        hex_view = []
        ascii_view = []

        hex_row = []
        ascii_row = ''

        for i, v in enumerate(data):
            hex_row.append(f'{v:02x}')
            ascii_row += chr(v) if 32 <= v <= 126 else '.'

            if i % 16 == 0:
                address_view.append(f'{start_addr + i:#010x}')

            if (i + 1) % 16 == 0:
                hex_view.append(hex_row)
                ascii_view.append(ascii_row)
                hex_row = []
                ascii_row = ''

        if len(hex_row) > 0:
            hex_view.append(hex_row)
            ascii_view.append(ascii_row)

        return address_view, hex_view, ascii_view


if __name__ == "__main__":
    app = HexViewApp()
    curses.wrapper(app.run)

