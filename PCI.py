#! python3

from bs4 import BeautifulSoup
import requests, re, os, time, ctypes
import pandas as pd
from datetime import date
import filecmp

# Date
today = date.today()
d1 = today.strftime("%d%m%Y")

# Get HTML from site
link = "https://www.pciconcursos.com.br/concursos/"
r  = requests.get(link)
data = r.text
pattern = re.compile(r'\.val\("([^@]+@[^@]+\.[^@]+)"\);', re.MULTILINE | re.DOTALL)
soup = BeautifulSoup(data, "html.parser") # complete html source code

# ---------- CONCURSOS NACIONAIS --------------------------------
source_nacional=str(soup)
nacional=source_nacional[source_nacional.find('<h2>NACIONAL</h2>')+len('<h2>NACIONAL</h2>'):source_nacional.find('<h2>REGIÃO SUDESTE</h2>')+len('<h2>REGIÃO SUDESTE</h2>')]
extract_nacional=BeautifulSoup(nacional,"html.parser")

name=['Concurso']
vagas=['Vagas']
nivel=['Nível']
salario=['Salário Até']
inscricao=['Inscrição Até']
link=['Link']
combinacao_nacional=[]

for line in extract_nacional.findAll(class_='ca'):
    name.append(line.find('a').text.strip()) # get name of institution
    link.append(line.find('a', href=True)['href']) # More information
    vagas.append(re.findall('(\d*) vaga', str(line.find(class_='cd')))[0]) # get number of available job's
    nivel.append('/'.join(re.findall('Superior|Médio', str(line.find(class_='cd'))))) # level
    salario.append(''.join(re.findall('R\$ *\d*\.*\d*\,*\d*', str(line.find(class_='cd'))))) # salary
    inscricao.append(''.join(re.findall('\d+/\d+/\d+', str(line.find(class_='ce')))))
    
# ---------- CONCURSOS CEARÁ --------------------------------
ceara=source_nacional[source_nacional.find('<div class="uf">CEARÁ</div>')+len('<div class="uf">CEARÁ</div>'):source_nacional.find('<div class="uf">MARANHÃO</div>')+len('<div class="uf">MARANHÃO</div>')]
extract_ceara=BeautifulSoup(ceara,"html.parser")

for line in extract_ceara.findAll(class_='ca'):
    name.append(line.find('a').text.strip()) # get name of institution
    link.append(line.find('a', href=True)['href']) # More information
    vagas.append(''.join(re.findall('(\d*) vaga', str(line.find(class_='cd'))))) # get number of available job's
    nivel.append('/'.join(re.findall('Superior|Médio', str(line.find(class_='cd'))))) # level
    salario.append(''.join(re.findall('R\$ *\d*\.*\d*\,*\d*', str(line.find(class_='cd'))))) # salary
    inscricao.append(''.join(re.findall('\d+/\d+/\d+', str(line.find(class_='ce')))))

for i in range(0,len(name)):
    combinacao_nacional=[name[i],vagas[i],nivel[i],salario[i],inscricao[i],link[i]]
    df=pd.DataFrame(combinacao_nacional)
    with open('ConcursosAtivos'+d1+'.csv', 'a', encoding='utf-16', newline='') as f:
        df.transpose().to_csv(f, encoding='utf-16', header=False, sep = "\t", index=False)

# Checar se há concursos novos
novos_concursos=['Concursos novos disponíveis: ']
if os.path.isfile('ConcursosAtivos.csv')==False:
    os.rename('ConcursosAtivos'+d1+'.csv','ConcursosAtivos.csv')
else:
    if filecmp.cmp('ConcursosAtivos.csv', 'ConcursosAtivos'+d1+'.csv') == False:
        antigo = pd.read_csv('ConcursosAtivos.csv', encoding='utf-16', header=None, sep = "\t")
        novo = pd.read_csv('ConcursosAtivos'+d1+'.csv', encoding='utf-16', header=None, sep = "\t")
        for contador in range(1,novo.shape[0]):
            encontrou=0
            for contador2 in range(1,antigo.shape[0]):
                if novo.iloc[contador,0]==antigo.iloc[contador2,0] and novo.iloc[contador,1]==antigo.iloc[contador2,1]:
                    encontrou=1
            if encontrou==0:
                print(novo.iloc[contador,0])
                novos_concursos.append(novo.iloc[contador,0]+' - '+novo.iloc[contador,2])

    os.remove('ConcursosAtivos.csv')
    os.rename('ConcursosAtivos'+d1+'.csv','ConcursosAtivos.csv')

# Avisa se houver concursos novos
if len(novos_concursos)>1:
    ctypes.windll.user32.MessageBoxW(0, '\n'.join(novos_concursos), "Novo Concurso", 1)
