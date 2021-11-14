from pyzbar.pyzbar import decode
from cv2 import imread
import os


def get_files(file_etxtension=".jpg,.png"):
    files = [arquivo for arquivo in os.listdir()
             if arquivo.endswith((tuple(file_etxtension.split(","))))]
    return files


def get_codebar(files):
    for arquivo in files:
        try:
            code_bar = decode(imread(arquivo))
            with open('retorno.txt', 'w') as retorno:
                retorno.writelines(f'{arquivo}: {code_bar[0][0]}')
        except:
            print("Erro ao ler a imagem:{arquivo}")


if __name__ == '__main__':
    get_codebar(get_files())
