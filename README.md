# PCI Concursos - Web-Scraping
Extrair os concursos disponíveis do site [PCI Concursos](https://www.pciconcursos.com.br/) em nível nacional e estadual, salvando-os em um arquivo *.CSV* e avisando quando estiver um novo concurso disponível. 

# Requisitos
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Pandas](https://pandas.pydata.org/)
* [Requests](https://pypi.org/project/requests/)

# Utilização
Extraem as informações dos concursos disponíveis tanto a nível nacional quanto a nível estadual obtidas pelo site [PCI Concursos](https://www.pciconcursos.com.br/). Essas informações são salvas na mesma pasta do *script* como um arquivo nomeado *ConcursosAtivos.csv*, em que contém o nome do concurso, quantitativo de vagas, nível de escolaridade, salário até, período máximo de inscrições e o link com mais informações do concurso. 

Para extrair a informação do estado, basta colocar a sigla do estado em:
```Python
state = exam_region(soup, 'SIGLA DO ESTADO AQUI')
```

Exemplo:
```Python
state = exam_region(soup, 'SP')
```

# Captura de Tela
![concurso-atis](https://user-images.githubusercontent.com/56649205/73771040-4b0e1980-475c-11ea-9458-8b957cdeb212.PNG)
![image](https://user-images.githubusercontent.com/56649205/74050703-5445f300-49b5-11ea-9425-72c40b700926.png)
