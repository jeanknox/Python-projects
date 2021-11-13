from xml.dom import minidom
import os
import pandas as pd
from threading import Thread


def get_files(extension='.xml'):
    arquivos = [file for file in os.listdir() if file.endswith(extension)]
    return arquivos

def getNodeText(node):
    nodelist = node.childNodes
    result = []
    for node in nodelist: 
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)

def get_from_xml(nota):
    notas= []
    columns = ['Codigo produto', 'Descrição', 'Quantidade', 'Valor unitario', 'Valor total', 'Valor icms-st', 'ipi', 'ncm']
    document = minidom.parse(nota)
    produtos = document.getElementsByTagName('det')
    for produto in produtos:
        codigo_prod = getNodeText(produto.getElementsByTagName("cProd")[0])
        descricao_prod = getNodeText(produto.getElementsByTagName("xProd")[0])
        quantidade_prod = getNodeText(produto.getElementsByTagName("qCom")[0]).replace('.',',')
        valorunitario_prod = getNodeText(produto.getElementsByTagName("vUnCom")[0]).replace('.',',')
        valortotal_prod = getNodeText(produto.getElementsByTagName("vProd")[0]).replace('.',',')
        ncm_prod = getNodeText(produto.getElementsByTagName("NCM")[0])

        try:
            st_prod = getNodeText(produto.getElementsByTagName("vICMSST")[0]).replace('.',',')
        except IndexError:
            st_prod = 0
        try:    
            ipi_prod = getNodeText(produto.getElementsByTagName("vIPI")[0]).replace('.',',')
        except IndexError:
            ipi_prod = 0
        data = {columns[0]:codigo_prod, columns[1]:descricao_prod, columns[2]:quantidade_prod,
                columns[3]:valorunitario_prod, columns[4]:valortotal_prod,
                columns[5]:st_prod, columns[6]:ipi_prod, columns[7]:ncm_prod}
        notas.append(data)
    df = pd.DataFrame(notas)
    df.to_excel('{}.xlsx'.format(nota.replace('.xml','')),header=columns)

if __name__ == "__main__":
    threads = []
    files = get_files()
    for nota in files:
        t = Thread(target=get_from_xml, args=(nota,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
