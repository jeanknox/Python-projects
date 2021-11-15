from xml.dom import minidom
import os
import pandas as pd
from threading import Thread


class MinidomXml:
    def __init__(self, arquivo) -> None:
        self.arquivo = arquivo

    def get_clear_text(self, nodelist):
        try:
            nodelist = nodelist.childNodes
            result = []
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    result.append(node.data)
            return ''.join(result)
        except:
            print("Erro ao limpar o texto")

    def get_by_tagname(self, tag_name, replace_comma=False):
        try:
            if replace_comma:
                return self.get_clear_text((self.arquivo.getElementsByTagName(tag_name)[0])).replace(".", ",")
            return self.get_clear_text(self.arquivo.getElementsByTagName(tag_name)[0])
        except IndexError:
            return 0


def get_files(extension='.xml'):
    arquivos = [file for file in os.listdir() if file.endswith(extension)]
    return arquivos


def get_from_xml(nota):
    columns = ['Codigo produto', 'Descrição', 'Quantidade',
               'Valor unitario', 'Valor total', 'Valor icms-st', 'ipi', 'ncm']
    dados = []
    document = minidom.parse(nota)
    produtos = document.getElementsByTagName('det')
    for produto in produtos:
        produto = MinidomXml(produto)
        data = {columns[0]: produto.get_by_tagname("cProd"),
                columns[1]: produto.get_by_tagname("xProd"),
                columns[2]: produto.get_by_tagname("qCom", replace_comma=True),
                columns[3]: produto.get_by_tagname("vUnCom", replace_comma=True),
                columns[4]: produto.get_by_tagname("vProd", replace_comma=True),
                columns[5]: produto.get_by_tagname("vICMSST", replace_comma=True),
                columns[6]: produto.get_by_tagname("vIPI", replace_comma=True),
                columns[7]: produto.get_by_tagname("NCM")}
        dados.append(data)
    df = pd.DataFrame(dados)
    df.to_excel('{}.xlsx'.format(nota.replace('.xml', '')), header=columns)


if __name__ == "__main__":
    threads = []
    files = get_files()
    for nota in files:
        t = Thread(target=get_from_xml, args=(nota,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
