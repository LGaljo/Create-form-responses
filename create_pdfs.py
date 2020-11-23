import os
import pdfkit
import re
import pandas as pd

# TODO before running make sure that you have wkhtmltopdf installed and in path
# https://wkhtmltopdf.org/downloads.html

template = 'prijavnica.html'
source_data = 'podatki.csv'


class StringConverter(dict):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return str

    def get(self, default=None):
        return str


def replace_fields(data, index):
    html_file = open(template, 'r', encoding='utf-8')

    filename_html = "htmls/" + "Prijavnica " + data["Ime"].strip() + " " + data["Priimek"].strip() + ".html"
    filename_pdf = "pdfs/" + "Prijavnica " + data["Ime"].strip() + " " + data["Priimek"].strip() + ".pdf"

    output_file = open(filename_html, 'w', encoding='utf-8')

    page = html_file.read()
    x = re.findall("({%((\w* *)+)%})+", page)
    for match in x:
        to_replace = data[match[1]] if str(data[match[1]]) != "nan" else "/"
        page = page.replace(str(match[0]), str(to_replace), 1)

    output_file.write(page)
    html_file.close()
    output_file.close()
    pdfkit.from_file(filename_html, filename_pdf)


if __name__ == '__main__':
    if not os.path.exists('pdfs'):
        os.makedirs('pdfs')
    if not os.path.exists('htmls'):
        os.makedirs('htmls')

    data_file = pd.DataFrame(pd.read_csv(source_data, converters=StringConverter()))

    for i, row in data_file.iterrows():
        replace_fields(row, i)
