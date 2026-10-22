import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# Obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    print(df_ocorrencias)

    df_cvli = df_ocorrencias[['aisp', 'cvli']]
    print(df_cvli)

    cvli_total = df_ocorrencias.groupby('aisp', as_index=False)['cvli'].sum() #nesse caso está somando o CVLI. nao soma o AISP
    print(cvli_total)

    ranking = cvli_total.sort_values(by='cvli', ascending=False)
    print('Batalhoes com mais CVLI: ')
    print(ranking.head(5))
    print('Batalhoes com menos CVLI: ')
    print(ranking.tail(5))

    valores = np.array(cvli_total['cvli'])
    media = np.mean(valores)
    mediana = np.median(valores)
    distancia_pct = abs(media - mediana) / mediana * 100

    print(f'Media: {media:.2f}')
    print(f'Mediana: {mediana:.2f}')
    print(f'Diferenca Relativa: {distancia_pct:.2f} %')

    q1 = np.quantile(valores, 0.25)
    q2 = np.quantile(valores, 0.50)
    q3 = np.quantile(valores, 0.75)
    print(f'quartis: {q1}, {q2}, {q3}')

    baixos= cvli_total[cvli_total['cvli'] < q1]
    altos= cvli_total[cvli_total['cvli'] > q3]
    print(f'valores maiores que Q3: ')
    print(altos)
    print(f'valores menores que Q1: ')
    print(baixos)

    iqr = q3 - q1
    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)

    outliers_baixos = cvli_total[cvli_total['cvli'] < limite_inferior]
    outliers_altos = cvli_total[cvli_total['cvli'] > limite_superior]
    print('outliers altos: ')
    print(outliers_altos)
    print('outliers baixos: ')
    print(outliers_baixos)

    if len(outliers_baixos) ==0:
        print('nenhum outlier inferior pelo criterio do IQR')

    maximo = np.max(valores) 
    minimo = np.min(valores) 
    amplitude = maximo - minimo 

    variancia = np.var(valores)

    distancia_var_media = variancia / (media ** 2) * 100

    desvio_padrao = np.std(valores)

    coef_variacao = (desvio_padrao / media) * 100

    print(f'Amplitude: {amplitude}')   
    print(f'Variância: {variancia:.2f}') 
    print(f'Distancia variância e Média: {distancia_var_media:.2f}')
    print(f'Desvio padrão: {desvio_padrao:.2f}')
    print(f'Coeficiente de variação: {coef_variacao:.2f}%')


    fig, ax = plt.subplots(2, 1, figsize=(14, 9))

    # GRÁFICO 1 - Todos os AISPs
    ax[0].bar(
    cvli_total["aisp"].astype(str),
    cvli_total["cvli"]
 )

    ax[0].axhline(
    cvli_total["cvli"].mean(),
    color="red",
    linestyle="--",
    label="Média"
 )

    ax[0].set_title("Total de CVLI por AISP")
    ax[0].set_xlabel("AISP")
    ax[0].set_ylabel("Quantidade de CVLI")
    ax[0].legend()

   # GRÁFICO 2 - Outliers
    ax[1].bar(
    outliers_altos["aisp"].astype(str),
    outliers_altos["cvli"],
    color="orange"
  )

    ax[1].set_title("AISPs com CVLI muito elevado")
    ax[1].set_xlabel("AISP")
    ax[1].set_ylabel("Quantidade de CVLI")

    # Ajustar os espaços
    plt.tight_layout()

    # Mostrar os dois juntos
    plt.show()



except Exception as e:
    print(f'Erro ao obter os dados - {e}')





    # A análise dos registros de Crimes Violentos Letais Intencionais (CVLI) por Área Integrada de Segurança Pública (AISP) 
    # demonstrou uma elevada variação na quantidade de ocorrências entre as áreas analisadas.

    # A média registrada foi de 2.751,76 ocorrências, enquanto a mediana foi de 2.362,50, 
    # indicando que os valores mais elevados influenciam a média geral.

    # O desvio padrão de 2.549,15 e o coeficiente de variação de 92,64% evidenciam uma alta dispersão dos dados. Portanto, 
    # embora exista uma média calculada, ela não representa de maneira uniforme o comportamento das diferentes AISPs.

    # Além disso, foram identificados dois outliers superiores: a AISP 15, com 9.166 ocorrências, e a AISP 20, com 11.549 ocorrências. 
    # Não foram identificados outliers inferiores pelo critério do intervalo interquartil (IQR).

    # Conclui-se que as ocorrências de CVLI apresentam uma distribuição bastante desigual entre as AISPs, com destaque para as áreas 15 e 20,
    # que registraram quantidades excepcionalmente elevadas em relação às demais.