from pydocx import PyDocX
from sys import argv
import os

from pydocx import constants
from pydocx.export import PyDocXHTMLExporter
from pydocx.export.html import HtmlTag
from pydocx.util.xml import convert_dictionary_to_style_fragment


class MyPyDocXHTMLExporter(PyDocXHTMLExporter):
    def __init__(self, path):
        # Handle dstrike the same as italic
        super(MyPyDocXHTMLExporter, self).__init__(path=path)

    def style(self):
        styles = {
            'body': {
                'margin': '0px auto',
            },
            'img': {
                'width': '100%',
                'height': 'auto'
            }
        }

        if self.page_width:
            width = self.page_width / constants.POINTS_PER_EM
            styles['body']['width'] = '%.2fem' % width

        result = []
        for name, definition in sorted(constants.PYDOCX_STYLES.items()):
            result.append('.pydocx-%s {%s}' % (
                name,
                convert_dictionary_to_style_fragment(definition),
            ))

        for name, definition in sorted(styles.items()):
            result.append('%s {%s}' % (
                name,
                convert_dictionary_to_style_fragment(definition),
            ))

        tag = HtmlTag('style')
        return tag.apply(''.join(result))


print (os.path.basename(argv[1]))
def handle_image():
    filename = os.path.basename(argv[1])
    html = MyPyDocXHTMLExporter(argv[1]).export()
    # html = PyDocX.to_html(argv[1])
    f = open("/tmp/"+os.path.splitext(filename)[0]+".html", 'w', encoding="utf-8")
    f.write(html)
    f.close()
    os.system("scp -P 22233 /tmp/" + os.path.splitext(filename)[0] + ".html hawk@laoqi.welikev.com:/opt/files/laoqi")
    print("http://laoqi.welikev.com/"+os.path.splitext(filename)[0] + ".html")

handle_image()


