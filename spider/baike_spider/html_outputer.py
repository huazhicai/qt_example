#!/usr/bin/env python
# coding=utf-8


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = open("output.html", "w")
        fout.write("<html>")
        fout.write("<meta charset='utf-8'>")
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td width='25%%'>%s</td>" % data["url"])
            fout.write("<td width='5%%'>%s</td>" % data["title"].encode("utf-8"))
            fout.write("<td width='70%%'>%s</td>" % data["summary"].encode("utf-8"))
            fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")