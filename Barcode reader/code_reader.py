from qrtools.qrtools import QR
import os
def get_files():
    files = [arquivo for arquivo in os.listdir() if arquivo.endswith(('.jpg', '.png'))]
    return files

def get_codebar(files):
    for arquivo in files:
        my_code = QR(filename=arquivo)
        if my_code.decode():
            with open('retorno.txt', 'w') as retorno:
                retorno.writelines(f'{arquivo}:{my_code.data_to_streing()}')


if __name__ =='__main__':
    files = get_files()
    get_codebar(files)
