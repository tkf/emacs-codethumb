import base64
import io

from PIL import Image
from pygments import highlight
from pygments import lexers
from pygments.formatters import ImageFormatter


def crop_image(png, center_pos_ratio, height_px):
    im = Image.open(io.BytesIO(png))
    (im_w, im_h) = im.size
    center_px = im_h * center_pos_ratio
    lower = min(center_px + height_px / 2, im_h)
    upper = max(lower - height_px, 0)
    box = [0, int(upper), im_w, int(lower)]
    out = io.BytesIO()
    im.crop(box).save(out, 'PNG')
    return out.getvalue()


class CodeThumb(object):

    def __init__(self):
        self.font_name = None
        self.style = 'monokai'

    def set_font_name(self, name):
        self.font_name = name

    def make_thumb(self, code, filename, hl_line_min, hl_line_max,
                   height_px):
        if filename:
            lx = lexers.guess_lexer_for_filename(filename, code)
        else:
            lx = lexers.guess_lexer(code)
        png = highlight(
            code,
            lx,
            ImageFormatter(style=self.style,
                           line_numbers=False,
                           hl_lines=range(hl_line_min, hl_line_max + 1),
                           font_size=3,
                           font_name=self.font_name))

        lines = sum(1 for _ in code.splitlines())
        center_pos_ratio = ((hl_line_max + hl_line_min) / 2.0) / lines
        cropped = crop_image(png, center_pos_ratio, height_px)

        return base64.encodestring(cropped)


def codethumb_epc_server(address, port):
    import epc.server
    codethumb = CodeThumb()
    server = epc.server.EPCServer((address, port))
    server.register_function(codethumb.make_thumb)
    server.register_function(codethumb.set_font_name)
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
