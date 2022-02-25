from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
from urllib.request import Request, urlopen
import matplotlib.pyplot as plt
import streamlit as st


fintechs = ['Nubank', 'PicPay', 'XP']
twttes_ultimo_mes = []
seguidores_dia = []
total_seguidores = []
seguidores_ultimo_mes = []

#Inicio
def inicio():

    st.title("Fintechs - Estatísticas(Twitter) - Nubank | PicPay | XP Investimentos")

    vetora = [[],[],[]]
    nubank = []
    picpay = []
    xp = []
   
    i=0

    #passando a url dos sites onde os dados serão coletados
    urls = ["https://socialblade.com/twitter/user/nubank","https://socialblade.com/twitter/user/picpay","https://socialblade.com/twitter/user/xpinvestimentos"]
    
    #loop que realiza a coleta de dados em todos os sites passados
    for url in urls:
        teste = dadoaA(url)
        vetora[i] = teste
        i+=1
    #atribui os respectivos dados de cada fintech
    nubank = vetora[0]
    picpay = vetora[1]
    xp = vetora[2]

    graficoGanhoSeguidores(nubank,picpay,xp)

   
# gerando gráfico de ganho de seguidores nos ultimos 7 dias e calculando o crescimento em porcentagem no último mês
def graficoGanhoSeguidores(nubank, picpay, xp):
    st.text("----------------------------------------------------------------------------------------------------------------------------")

    #definindo os dados do gráfico de ganho de seguidores nos ultimos 7 dias em pizza
    plt.xlabel('Dias')
    plt.ylabel('Ganho Seguidores')
 
    plt.title("Gaanho de seguidores nos ultimos 7 dias")
    plt.plot(nubank, 'purple', label="nubank",)
    plt.plot(picpay, 'green', label="picpay")
    plt.plot(xp,'yellow', label="xp")
    plt.legend(fintechs)

    st.pyplot(plt)
    plt.close()

    st.text("----------------------------------------------------------------------------------------------------------------------------")

    #calculando o crecimento de seguidores em porcentagem do último mes
    crescimento_ultimo_mes = []
    tot_seguodores = 0
    ganho_mes = 0
    res = 0
    i = 0
    for a in range(3):
        tot_seguodores = float(total_seguidores[i])
        ganho_mes = float(seguidores_ultimo_mes[i])
        res = float((tot_seguodores - ganho_mes)/(ganho_mes * 100))
        crescimento_ultimo_mes.append(res)
        
        i+=1

    cresc_ultimo_mes = (f"Crescimento no ultimo mês\nNubank: {crescimento_ultimo_mes[0]:.2f}%\nPicPay: {crescimento_ultimo_mes[1]:.2f}%\nXP: {crescimento_ultimo_mes[2]:.2f}%\n")

    st.text(cresc_ultimo_mes)

    GraficoQquantidadeSeguidores()

#gerando o gráfico da quantidade de seguidores de cada Fintech
def GraficoQquantidadeSeguidores():
    st.text("----------------------------------------------------------------------------------------------------------------------------")
    #definindo os dados do gráfico em pizza
    plt.title("Maior quantidade de seguidores")
    colunas = ['purple', 'green', 'yellow']
    plt.xlabel('')
    plt.ylabel('')
    
    plt.pie(total_seguidores, labels = fintechs, colors = colunas, startangle = 90, autopct='%1.1f%%',shadow = True, explode = (0.1, 0, 0))
    plt.legend(fintechs)
    st.pyplot(plt)

    texto = (f"Fintechs com mais seguidores \nNubank: {total_seguidores[0]}\nPicPay: {total_seguidores[1]}\nXP: {total_seguidores[2]}\n")
    st.text(texto)


 

    

    graficoTweetsUltimoMes()
#Gera o grafico das fintechs que mais tweetaram nos últimos 
def graficoTweetsUltimoMes():
    st.text("----------------------------------------------------------------------------------------------------------------------------")
    plt.close()
    plt.title("Mais tweets no último mês")
    width = 0.5
    plt.bar(fintechs[0],twttes_ultimo_mes[0], width, color='purple') 
    plt.bar(fintechs[1],twttes_ultimo_mes[1],width,color='green') 
    plt.bar(fintechs[2],twttes_ultimo_mes[2],width,color='yellow') 
    plt.xlabel("Fintechs") 
    plt.ylabel("seguidores ganhos") 
    plt.legend(fintechs)
    st.pyplot(plt)

    texto = (f"Fintechs com mais tweets nos últimos 30 dias \nNubank: {twttes_ultimo_mes[0]}\nPicPay: {twttes_ultimo_mes[1]}\nXP: {twttes_ultimo_mes[2]}\n")
    st.text(texto)

    dadosFinais()

def dadosFinais():
    #últimos dados da página
    st.text("----------------------------------------------------------------------------------------------------------------------------")
    texto = (f"Média - Ganho de seguidores por dia \nNubank: {seguidores_dia[0]}\nPicPay: {seguidores_dia[1]}\nXP: {seguidores_dia[2]}\n")
    st.text(texto)
    texto = (f"\nprevisão de ganho de seguidores nos próximo 12 meses \nNubank: {total_seguidores[0] + (seguidores_dia[0] * 30) * 12}\nPicPay: {total_seguidores[1] + (seguidores_dia[1] * 30) * 12}\nXP: {total_seguidores[2] + (seguidores_dia[2] * 30) *12}\n") 
    st.text(texto)
    st.text("----------------------------------------------------------------------------------------------------------------------------")
    texto = ("Dados coletados via Scraping no site Social Blade") 
    st.text(texto)
def dadoaA(url):
    content = ''
    #cabeçalho definido para evitar que a aplicação seja identificada como robô
    cabecalho = {'user-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers = cabecalho)
    #Chaca se a requiseção foi bem sucedida
    if response.status_code == 200:
        content = response.content

    posicao = 0

    #utilizando o BeautifulSoup para realizar o scraping na página
    soup = BeautifulSoup(content, 'html.parser')
    dados = soup.find_all('span')

    #lista que armazana a quantidade de seguidores ganhas nos útimos 7 dias
    crescimento_semana = []
   
    crescimento_semana.append(0)

    #organizando os dados coletados
    for dados_coletados in dados:

        if(posicao == 47 or posicao == 50 or posicao == 53 or posicao == 56 or posicao == 59 or posicao == 62 or posicao == 65):
            dados_coletados = dados_coletados.text.replace(',','')
            dados_coletados = dados_coletados.replace('--','0')
            crescimento_semana.append(int(dados_coletados))
        elif(posicao == 70):
            dados_coletados = dados_coletados.text.replace(',','')
            dados_coletados = dados_coletados.replace('--','0')
            seguidores_dia.append(int(dados_coletados))
        elif(posicao ==8):
            dados_coletados = dados_coletados.text.replace(',','')
            dados_coletados = dados_coletados.replace('--','0')
            total_seguidores.append(int(dados_coletados))
        elif(posicao == 74):
            dados_coletados = dados_coletados.text.replace(',','')
            dados_coletados = dados_coletados.replace('--','0')
            seguidores_ultimo_mes.append(int(dados_coletados))
        elif(posicao == 76):
            dados_coletados = dados_coletados.text.replace(',','')
            dados_coletados = dados_coletados.replace('--','0')
            twttes_ultimo_mes.append(int(dados_coletados))
        posicao +=1


    return crescimento_semana

inicio()




#padrão utulizado para contabilizar os spans da página, pois não tinha id e nem classe e no perfil de todas fintechs o padrão era o mesmo
#segudores ultimos 7 dias: spans - 47,50,53,56,59,62,65
#seguidores no dia - span 70
#seguidores ultimos 30 dias: span - 74
#twittes ultimos 30 dias: span 76
#total de seguidores: span - 8

