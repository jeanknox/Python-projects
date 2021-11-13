from bs4 import BeautifulSoup
import os, keyboard, time, pyperclip

codigos = []
arquivos =[item for item in os.listdir() if item.endswith('.html')]
for item in arquivos:
    with open(item, 'r') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        for tr in soup.find_all('tr'):
            if((element := tr.find('td', align='right')) and element != '' and element!= None):
                codigos.append(element.get_text())
print(codigos)

for codigo in codigos:
    pyperclip.copy(codigo)
    print(f'Codigo {codigo}, da posição {codigos.index(codigo)}')
    keyboard.wait('backspace')
