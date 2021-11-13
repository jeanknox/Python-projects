from xml.dom import minidom
import pandas as pd
import sys
import os
from threading import Thread

def getNodeText(node):
    nodelist = node.childNodes
    result = []
    for node in nodelist: 
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)
def xml_2xls(nota,*args, **kwargs):
    notas= [] 
    columns = ['Codigo produto', 'Descrição', 'Quantidade', 'Valor unitario', 'Valor total',
               'Valor icms-st', 'ipi', 'ncm']
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

def get_xml_files():
    xmls = [item for item in os.listdir() if '.xml' in item]
    return xmls

if __name__ =="__main__":
    print(get_xml_files())
    for element in get_xml_files():
        print(element)
        t = Thread(target=xml_2xls, args=element)
        t.start()
        t.join()
        
        

