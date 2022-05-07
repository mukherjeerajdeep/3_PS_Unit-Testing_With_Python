
import html as html_converter


class HtmlPagesConverter:

    def __init__(self, file):
        self._file = file
        self._find_page_breaks()

    def _find_page_breaks(self):
        """Read the file and note the positions of the page breaks,
        so we can access them quickly"""
        self.breaks = [0]

        while True:
            line = self._file.readline()
            if not line:
                break
            if "PAGE_BREAK" in line:
                self.breaks.append(self._file.tell())
        self.breaks.append(self._file.tell())

    def get_html_page(self, page):
        """Return html page with the given number (zero indexed)"""
        page_start = self.breaks[page]
        page_end = self.breaks[page+1]
        html = ""
        self._file.seek(page_start)
        while self._file.tell() != page_end:
            line = self._file.readline()
            if "PAGE_BREAK" in line:
                continue
            line = line.rstrip()
            html += html_converter.escape(line, quote=True)
            html += "<br />"
        return html
