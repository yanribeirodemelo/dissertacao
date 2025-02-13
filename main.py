# -*- coding: utf-8 -*-
"""
Código de Análise de Sensibilidade

@author: yanri
"""
import streamlit as st
import numpy as np
import sys
from streamlit import cli as stcli
from scipy.integrate import quad
from PIL import Image

st.set_page_config(
    page_title="Política de Manutenção",
    page_icon="foto2.png",
    layout="wide"
)

# import streamlit.report_thread as ReportThread
# st.report_thread.add_report_ctx(thread)

def main():
    #criando 3 colunas
    col1, col2, col3 = st.columns(3)
    foto = Image.open('foto.png')
    #inserindo na coluna 2
    col2.image(foto, use_column_width=True)
    
    st.title('Modelo de Manutenção para Sistemas de Difícil Acesso')

    menu = ["Aplicação Analítica", "Aplicação Otimizadora", "Informações", "Grupo de Pesquisa"]
    
    choice = st.sidebar.selectbox("Selecione aqui", menu)
    
    if choice == menu[0]:
        
        st.header(menu[0])

        st.subheader("Insira os valores dos parâmetros de entrada abaixo:")

        n2 = st.number_input("Insira o parâmetro de escala - {}".format(chr(945)), min_value = 0.0, value = 10.0) # escala fraca
        b2 = st.number_input("Insira o parâmetro de forma - {}".format(chr(946)), min_value = 1.0, max_value = 6.0, value = 3.0) # forma fraca

        cp = st.number_input("Insira o parâmetro de custo de substituição preventiva", min_value = 0.0, value = 1.0) # custo da preventiva
        cd = st.number_input("Insira o parâmetro de custo de tempo de inatividade por unidade de tempo", min_value = 0.0, value = 0.5) # custo de downtime por unidade de tempo
        cm = st.number_input("Insira o parâmetro de custo adicional para ação de manutenção garantida", min_value = 0.0, value = 1.00) # custo de inspeção
        cf = st.number_input("Insira o parâmetro de custo de substituição corretiva", min_value = 0.0, value = 1.0) # custo de falha
        
        q = st.number_input("Insira o parâmetro de probabilidade de oportunidade em uma visita", min_value = 0.0, max_value = 1.0, value = 0.2) # taxa de chegada de oportunidades
        s = st.number_input("Insira o parâmetro de intervalo de tempo entre visitas", min_value = 0.0, value = 1.0) # intervalo entre visitas
        
        st.subheader("Insira os valores das variáveis de decisão abaixo:")
        
        W = int(st.number_input("Insira o limite inferior das ações de manutenção preventivas por oportunidades", min_value = 0, max_value = 50, step = 1, value = 6)) # Limite inferior da janela de oportunidades
        M = int(st.number_input("Insira a idade de ação de manutenção garantida", min_value = 0, max_value = 50, step = 1, value = 14)) # Limite inferior da janela de oportunidades
        
        st.subheader("Clique no botão abaixo para executar esta aplicação:")
        botao = st.button("Executar")

        if botao:
        
            def otm():
              def fx(x):#weibull density func (for strong comp) for arrival of fails
                  return (b2/n2)*((x/n2)**(b2-1))*np.exp(-(x/n2)**b2)
            
              #%% VARIÁVEIS E CONSTANTES
            
              # #Parâmetros
              # b2 = b2[i] #Forma do componente forte
              # n2 = n2[i] #Escala do componente forte     
              # cd = cd[i] #custo de downtime
              # cm = cm[i] #custo logístico
              # cp = cp[i] #custo de manutenção preventiva
              # cf = cf[i] #custo de manutenção corretiva
                 
              # s = s[i] #Intervalo entre visitas
              # q = q[i] #Oportunidade de manutenção
            
              #%%Variáveis auxiliares
              p11 = p12 = p2 = p31 = p32 = p4 = 0
              c11 = c12 = c2 = c31 = c32 = c4 = 0
              t11 = t12 = t2 = t31 = t32 = t4 = 0
              d11 = d12 = d2 = d31 = d32 = d4 = 0 
            
              #%%CASO 1
              
              def fprob1(x):
                  return ((fx(x)))
              def fcusto1(x):
                  return ((cf+cd*(j*s-x))*(fx(x)))
              def fvida1(x):
                  return ((j*s)*(fx(x)))
              def fdown1(x):
                  return ((j*s-x)*(fx(x)))
            
              for i in range(1, W):
                  for j in range(i, M):
                      fp11 = quad(fprob1, (i-1)*s, i*s)[0]*((1-q)**(j-i))*(q)
                      p11 = p11 + fp11
                      
                      fc11 = quad(fcusto1, (i-1)*s, i*s)[0]*((1-q)**(j-i))*(q)
                      c11 = c11 + fc11
                      
                      ft11 = quad(fvida1, (i-1)*s, i*s)[0]*((1-q)**(j-i))*(q)
                      t11 = t11 + ft11
                      
                      fd11 = quad(fdown1, (i-1)*s, i*s)[0]*((1-q)**(j-i))*(q)
                      d11 = d11 + fd11
                      
              for i in range(W, M):
                  for j in range(i, M):
                      fp12 = quad(fprob1, (i-1)*s, i*s)[0]*((1-q)**(j-W))*(q)
                      p12 = p12 + fp12
                      
                      fc12 = quad(fcusto1, (i-1)*s, i*s)[0]*((1-q)**(j-W))*(q)
                      c12 = c12 + fc12
                      
                      ft12 = quad(fvida1, (i-1)*s, i*s)[0]*((1-q)**(j-W))*(q)
                      t12 = t12 + ft12
                      
                      fd12 = quad(fdown1, (i-1)*s, i*s)[0]*((1-q)**(j-W))*(q)
                      d12 = d12 + fd12
                
              #%%CASO 2
            
              def fprob2(x):
                  return ((fx(x)))
              def fcusto2(x):
                  return ((cp)*(fx(x)))
              def fvida2(x):
                  return ((j*s)*(fx(x)))
              def fdown2(x):
                  return ((0)*(fx(x)))
            
              for j in range(W, M):
                fp2 = quad(fprob2, j*s, np.inf)[0]*(((1-q)**(j-W))*q)
                p2 = p2 + fp2
                  
                fc2 = quad(fcusto2, j*s, np.inf)[0]*(((1-q)**(j-W))*q)
                c2 = c2 + fc2
                
                ft2 = quad(fvida2, j*s, np.inf)[0]*(((1-q)**(j-W))*q)
                t2 = t2 + ft2
                
                fd2 = quad(fdown2, j*s, np.inf)[0]*(((1-q)**(j-W))*q)
                d2 = d2 + fd2 
                
              #%%CASO 3
              
              def fprob3(x):
                  return ((fx(x)))
              def fcusto3(x):
                  return ((cf+cd*(M*s-x)+cm)*(fx(x)))
              def fvida3(x):
                  return ((M*s)*(fx(x)))
              def fdown3(x):
                  return ((M*s-x)*(fx(x)))
            
              for i in range(1, W):
                  fp31 = quad(fprob3, (i-1)*s, i*s)[0]*((1-q)**(M-i))
                  p31 = p31 + fp31
                  
                  fc31 = quad(fcusto3, (i-1)*s, i*s)[0]*((1-q)**(M-i))
                  c31 = c31 + fc31
                  
                  ft31 = quad(fvida3, (i-1)*s, i*s)[0]*((1-q)**(M-i))
                  t31 = t31 + ft31
                  
                  fd31 = quad(fdown3, (i-1)*s, i*s)[0]*((1-q)**(M-i))
                  d31 = d31 + fd31   
                  
            
              for i in range(W, M+1):
                  fp32 = quad(fprob3, (i-1)*s, i*s)[0]*((1-q)**(M-W))
                  p32 = p32 + fp32
                  
                  fc32 = quad(fcusto3, (i-1)*s, i*s)[0]*((1-q)**(M-W))
                  c32 = c32 + fc32
                  
                  ft32 = quad(fvida3, (i-1)*s, i*s)[0]*((1-q)**(M-W))
                  t32= t32 + ft32
                  
                  fd32 = quad(fdown3, (i-1)*s, i*s)[0]*((1-q)**(M-W))
                  d32 = d32 + fd32  
            
              #%%CASO 4
              
              def fprob4(x):
                  return ((fx(x)))
              def fcusto4(x):
                  return ((cp+cm)*(fx(x)))
              def fvida4(x):
                  return ((M*s)*(fx(x)))
              def fdown4(x):
                  return ((0)*(fx(x)))
              
              fp4 = quad(fprob4, M*s, np.inf)[0]*(((1-q)**(M-W)))
              p4 = p4 + fp4
              
              fc4 = quad(fcusto4, M*s, np.inf)[0]*(((1-q)**(M-W)))
              c4 = c4 + fc4
              
              ft4 = quad(fvida4, M*s, np.inf)[0]*(((1-q)**(M-W)))
              t4= t4 + ft4
              
              fd4 = quad(fdown4, M*s, np.inf)[0]*(((1-q)**(M-W)))
              d4 = d4 + fd4  
            
              #%%RESULTADOS

                
              pe = p11+p12+p2+p31+p32+p4 #probabilidade total
              ce = c11+c12+c2+c31+c32+c4 #custo total
              ve = t11+t12+t2+t31+t32+t4 #tamanho total
              de = d11+d12+d2+d31+d32+d4 #downtime total
              
              tx = ce/ve #taxa de custo
              dx = de/ve #taxa de downtime
              mu = ve/(p11+p12+p31+p32) #mtbof
            
              if pe < 0.999 or pe > 1.001:
                print("Algum erro ocorreu!")
            
              return tx, ce, ve, pe, dx, mu

            taxadecusto = otm()
            st.write("Resultado de taxa de custo: {}" .format(taxadecusto[0]))
            st.write("Resultado de tempo de indisponibilidade médio: {}" .format(taxadecusto[4]))
            st.write("Resultado de tempo médio entre falhas operacionais: {}" .format(taxadecusto[5]))
    
    if choice == menu[1]:
        
        st.header(menu[1])

        st.subheader("Insira os valores dos parâmetros de entrada abaixo:")

        n2 = st.number_input("Insira o parâmetro de escala - {}".format(chr(945)), min_value = 0.0, value = 10.0) # escala fraca
        b2 = st.number_input("Insira o parâmetro de forma - {}".format(chr(946)), min_value = 1.0, max_value = 6.0, value = 3.0) # forma fraca

        cp = st.number_input("Insira o parâmetro de custo de substituição preventiva", min_value = 0.0, value = 1.0) # custo da preventiva
        cd = st.number_input("Insira o parâmetro de custo de tempo de inatividade por unidade de tempo", min_value = 0.0, value = 0.5) # custo de downtime por unidade de tempo
        cm = st.number_input("Insira o parâmetro de custo adicional para ação de manutenção garantida", min_value = 0.0, value = 1.00) # custo de inspeção
        cf = st.number_input("Insira o parâmetro de custo de substituição corretiva", min_value = 0.0, value = 1.0) # custo de falha
        
        q = st.number_input("Insira o parâmetro de probabilidade de oportunidade em uma visita", min_value = 0.0, max_value = 1.0, value = 0.2) # taxa de chegada de oportunidades
        s = st.number_input("Insira o parâmetro de intervalo de tempo entre visitas", min_value = 0.0, value = 1.0) # intervalo entre visitas

        opcoes = ["Taxa de custo", "Taxa de indisponibilidade", "Confiabilidade operacional"]
        st.subheader(st.selectbox("Qual medida de desempenho você deseja otimizar?", opcoes))
        
        st.subheader("Clique no botão abaixo para executar esta aplicação:")
        botao = st.button("Executar")

        if botao:
        
            def otm():
              def fx(x):#weibull density func (for strong comp) for arrival of fails
                  return (b2/n2)*((x/n2)**(b2-1))*np.exp(-(x/n2)**b2)
            
              #%% VARIÁVEIS E CONSTANTES
            
              # #Parâmetros
              # b2 = b2[i] #Forma do componente forte
              # n2 = n2[i] #Escala do componente forte     
              # cd = cd[i] #custo de downtime
              # cm = cm[i] #custo logístico
              # cp = cp[i] #custo de manutenção preventiva
              # cf = cf[i] #custo de manutenção corretiva
                 
              # s = s[i] #Intervalo entre visitas
              # q = q[i] #Oportunidade de manutenção
            
              #%%Variáveis auxiliares
              p11 = p12 = p2 = p31 = p32 = p4 = 0
              c11 = c12 = c2 = c31 = c32 = c4 = 0
              t11 = t12 = t2 = t31 = t32 = t4 = 0
              d11 = d12 = d2 = d31 = d32 = d4 = 0 
            
              #%%CASO 1
              
              def fprob1(x):
                  return ((fx(x)))
              def fcusto1(x):
                  return ((cf+cd*(j*s-x))*(fx(x)))
              def fvida1(x):
                  return ((j*s)*(fx(x)))
              def fdown1(x):
                  return ((j*s-x)*(fx(x)))
            
              for i in range(1, W):
                  for j in range(i, M):
                      fp11 = quad(fprob1, (i-1)*s, i*s)[0]*((1-q)**(j-i))*(q)
                      p11 = p11 + fp11
                      
                      fc11 = quad(fcusto1, (i-1)*s, i*s)[0]*((1-q)**(j-i))*(q)
                      c11 = c11 + fc11
                      
                      ft11 = quad(fvida1, (i-1)*s, i*s)[0]*((1-q)**(j-i))*(q)
                      t11 = t11 + ft11
                      
                      fd11 = quad(fdown1, (i-1)*s, i*s)[0]*((1-q)**(j-i))*(q)
                      d11 = d11 + fd11
                      
              for i in range(W, M):
                  for j in range(i, M):
                      fp12 = quad(fprob1, (i-1)*s, i*s)[0]*((1-q)**(j-W))*(q)
                      p12 = p12 + fp12
                      
                      fc12 = quad(fcusto1, (i-1)*s, i*s)[0]*((1-q)**(j-W))*(q)
                      c12 = c12 + fc12
                      
                      ft12 = quad(fvida1, (i-1)*s, i*s)[0]*((1-q)**(j-W))*(q)
                      t12 = t12 + ft12
                      
                      fd12 = quad(fdown1, (i-1)*s, i*s)[0]*((1-q)**(j-W))*(q)
                      d12 = d12 + fd12
                
              #%%CASO 2
            
              def fprob2(x):
                  return ((fx(x)))
              def fcusto2(x):
                  return ((cp)*(fx(x)))
              def fvida2(x):
                  return ((j*s)*(fx(x)))
              def fdown2(x):
                  return ((0)*(fx(x)))
            
              for j in range(W, M):
                fp2 = quad(fprob2, j*s, np.inf)[0]*(((1-q)**(j-W))*q)
                p2 = p2 + fp2
                  
                fc2 = quad(fcusto2, j*s, np.inf)[0]*(((1-q)**(j-W))*q)
                c2 = c2 + fc2
                
                ft2 = quad(fvida2, j*s, np.inf)[0]*(((1-q)**(j-W))*q)
                t2 = t2 + ft2
                
                fd2 = quad(fdown2, j*s, np.inf)[0]*(((1-q)**(j-W))*q)
                d2 = d2 + fd2 
                
              #%%CASO 3
              
              def fprob3(x):
                  return ((fx(x)))
              def fcusto3(x):
                  return ((cf+cd*(M*s-x)+cm)*(fx(x)))
              def fvida3(x):
                  return ((M*s)*(fx(x)))
              def fdown3(x):
                  return ((M*s-x)*(fx(x)))
            
              for i in range(1, W):
                  fp31 = quad(fprob3, (i-1)*s, i*s)[0]*((1-q)**(M-i))
                  p31 = p31 + fp31
                  
                  fc31 = quad(fcusto3, (i-1)*s, i*s)[0]*((1-q)**(M-i))
                  c31 = c31 + fc31
                  
                  ft31 = quad(fvida3, (i-1)*s, i*s)[0]*((1-q)**(M-i))
                  t31 = t31 + ft31
                  
                  fd31 = quad(fdown3, (i-1)*s, i*s)[0]*((1-q)**(M-i))
                  d31 = d31 + fd31   
                  
            
              for i in range(W, M+1):
                  fp32 = quad(fprob3, (i-1)*s, i*s)[0]*((1-q)**(M-W))
                  p32 = p32 + fp32
                  
                  fc32 = quad(fcusto3, (i-1)*s, i*s)[0]*((1-q)**(M-W))
                  c32 = c32 + fc32
                  
                  ft32 = quad(fvida3, (i-1)*s, i*s)[0]*((1-q)**(M-W))
                  t32= t32 + ft32
                  
                  fd32 = quad(fdown3, (i-1)*s, i*s)[0]*((1-q)**(M-W))
                  d32 = d32 + fd32  
            
              #%%CASO 4
              
              def fprob4(x):
                  return ((fx(x)))
              def fcusto4(x):
                  return ((cp+cm)*(fx(x)))
              def fvida4(x):
                  return ((M*s)*(fx(x)))
              def fdown4(x):
                  return ((0)*(fx(x)))
              
              fp4 = quad(fprob4, M*s, np.inf)[0]*(((1-q)**(M-W)))
              p4 = p4 + fp4
              
              fc4 = quad(fcusto4, M*s, np.inf)[0]*(((1-q)**(M-W)))
              c4 = c4 + fc4
              
              ft4 = quad(fvida4, M*s, np.inf)[0]*(((1-q)**(M-W)))
              t4= t4 + ft4
              
              fd4 = quad(fdown4, M*s, np.inf)[0]*(((1-q)**(M-W)))
              d4 = d4 + fd4  
            
              #%%RESULTADOS

                
              pe = p11+p12+p2+p31+p32+p4 #probabilidade total
              ce = c11+c12+c2+c31+c32+c4 #custo total
              ve = t11+t12+t2+t31+t32+t4 #tamanho total
              de = d11+d12+d2+d31+d32+d4 #downtime total
              
              tx = ce/ve #taxa de custo
              dx = de/ve #taxa de downtime
              mu = ve/(p11+p12+p31+p32) #mtbof
            
              if pe < 0.999 or pe > 1.001:
                print("Algum erro ocorreu!")
            
              return tx, ce, ve, pe, dx, mu

            menortaxa = 10000000000
            for W in range(1, 50+1):
                for M in range(W, 50+1):
                    resultado = otm()
                    if resultado[0] < menortaxa:
                        Wotm = W
                        Motm = M
                        menortaxa = resultado[0]
                        indisponibilidade = resultado[4]
                        confiabilidade = resultado[5]

            st.write("A política de manutenção ótima é a política [{},{}]" .format(Wotm, Motm)
            st.write("Resultado de taxa de custo: {}" .format(taxadecusto[0]))
            st.write("Resultado de tempo de indisponibilidade médio: {}" .format(taxadecusto[4]))
            st.write("Resultado de tempo médio entre falhas operacionais: {}" .format(taxadecusto[5]))
            
            st.write('''Este protótipo possui restrições quanto ao espaço de busca de soluções ≤. Se for do interesse do usuário utilizar uma gama maior de combinações de soluções ou se houver alguma dúvida sobre o estudo e/ou este protótipo, elas podem ser direcionadas para qualquer um dos endereços de e-mail abaixo. Por fim, se esta aplicação for utilizada para qualquer propósito, todos os autores devem ser informados.''')
            st.write('''y.r.melo@random.org.br''')
            st.write('''c.a.v.cavalcante@random.org.br''')
    
    if choice == menu[2]:
        
        st.header(menu[2])

        st.write('''Este protótipo foi criado por membros do grupo de pesquisa RANDOM, que tem como objetivo auxiliar na aplicação de uma política de manutenção periódica oportuna para sistemas de difícil acesso''')
        st.write('''Este protótipo possui restrições quanto ao espaço de busca de soluções. Se for do interesse do usuário utilizar uma gama maior de combinações de soluções ou se houver alguma dúvida sobre o estudo e/ou este protótipo, elas podem ser direcionadas para qualquer um dos endereços de e-mail abaixo. Por fim, se esta aplicação for utilizada para qualquer propósito, todos os autores devem ser informados.''')
        st.write('''y.r.melo@random.org.br''')
        st.write('''c.a.v.cavalcante@random.org.br''')

    if choice == menu[4]:
        
        st.header(menu[4])
        
        st.write("O Grupo de Pesquisa em Risco e Análise da Decisão em Operações e Manutenção foi criado em 2012 com o objetivo de reunir diferentes pesquisadores que atuam nas seguintes áreas: risco, modelagem de manutenção e operação. Saiba mais sobre o grupo através do nosso site.")
        st.markdown('[Clique aqui para ser redirecionado ao nosso site](https://sites.ufpe.br/random/#page-top)', False)
        
if st._is_running_with_streamlit:
    main()
else:
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())
