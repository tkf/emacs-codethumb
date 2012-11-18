import base64

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter


class CodeThumb(object):

    def __init__(self):
        self.font_name = 'VL Gothic'
        self.style = 'monokai'

    def make_thumb(self, code, hl_line_min, hl_line_max):
        png = highlight(
            code,
            PythonLexer(),
            ImageFormatter(style=self.style,
                           line_numbers=False,
                           hl_lines=range(hl_line_min, hl_line_max + 1),
                           font_size=3,
                           font_name=self.font_name))

        return base64.encodestring(png)


def codethumb_epc_server(address, port):
    import epc.server
    codethumb = CodeThumb()
    server = epc.server.EPCServer((address, port))
    server.register_function(codethumb.make_thumb)
    server.print_port()
    server.serve_forever()


def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=__doc__)
    parser.add_argument(
        '--address', default='localhost')
    parser.add_argument(
        '--port', default=0, type=int)
    ns = parser.parse_args(args)
    codethumb_epc_server(**vars(ns))


if __name__ == '__main__':
    main()
