"""Core module for the package. It holds the main object to be used."""

from string import Template
from urllib.parse import quote as urllib_quote

from .utils import bool_js, read


class Base:
    def __init__(self, data, width, height, chart, view_box):
        self.data = data
        self.width = width
        self.height = height
        self.view_box = bool_js(view_box)
        self.canvas = bool_js(False)
        self.main_js = read("main.js")
        self.chart_js = Template(read("code.js", chart)).safe_substitute(
            main=self.main_js
        )
        self.style_css = f'<style>\n{read("style.css", chart)}\n</style>'

    def export(self, path):
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.get_html())

    def get_html(self):
        html = read("main.html")
        style_css = self.style_css
        chart_js = Template(self.chart_js).safe_substitute(**self.__dict__)
        return Template(html).safe_substitute(style=style_css, code=chart_js)

    def _repr_html_(self):
        html = urllib_quote(self.get_html())
        onload = (
            "this.contentDocument.open();"
            "this.contentDocument.write("
            "    decodeURIComponent(this.getAttribute('data-html'))"
            ");"
            "this.contentDocument.close();"
        )
        iframe = (
            f'<iframe src="about:blank" width="{self.width + 50}" height="{self.height + 50}"'
            'style="border:none !important;" '
            f'data-html={html} onload="{onload}" '
            '"allowfullscreen" "webkitallowfullscreen" "mozallowfullscreen">'
            "</iframe>"
        )
        return iframe


class ForceGraph(Base):
    def __init__(
        self,
        data,
        width,
        height,
        radio=20,
        tooltip="null",
        bounding_box=True,
        view_box=False,
        force_link=100,
        force_simulation=-50,
        force_collision=30,
        canvas=False,
    ):
        super().__init__(data, width, height, "force graph", view_box)
        self.tooltip = tooltip
        self.radio = radio
        self.bounding_box = bool_js(bounding_box)
        self.force_link = force_link
        self.force_simulation = force_simulation
        self.force_collision = force_collision
        self.canvas = bool_js(canvas)

    def get_html(self):
        filename = "code-canvas.js" if self.canvas == bool_js(True) else "code-svg.js"
        code = read(filename, "force graph")
        html = super().get_html()
        return Template(html).safe_substitute(code=code)


class ArcDiagram(Base):
    def __init__(self, data, width, height=None, radio=20, tooltip="null", view_box=False):
        if height is None:
            height = width/2

        super().__init__(data, width, height, "arc diagram", view_box)
        self.tooltip = tooltip
        self.radio = radio


class RadialDiagram(Base):
    def __init__(self, data, size, tooltip="null", view_box=False):
        super().__init__(data, size, size, "radial diagram", view_box)
        self.tooltip = tooltip


class AdjacencyMatrix(Base):
    def __init__(
        self, data, size, tooltip="null", view_box=False, bidirrectional=False
    ):
        super().__init__(data, size, size, "adjacency matrix", view_box)
        self.tooltip = tooltip
        self.bidirrectional = bool_js(bidirrectional)
