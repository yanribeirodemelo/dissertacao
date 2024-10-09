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

# import streamlit.report_thread as ReportThread
# st.report_thread.add_report_ctx(thread)

def main():
    #criando 3 colunas
    col1, col2, col3 = st.columns(3)
    foto = Image.open('foto.png')
    #inserindo na coluna 2
    col2.image(foto, use_column_width=True)
    
    st.title('Quasi-periodic opportunistic replacement policy')

    menu = ["Application", "Information", "Website"]
    
    choice = st.sidebar.selectbox("Select here", menu)
    
    if choice == menu[0]:
        
        st.header(menu[0])

        st.subheader("Insert the parameter values below:")
        
        n2=st.number_input("Insert the characteristic life parameter of component - {}" .format(chr(945)), min_value = 0.0, value = 10.0) #escala fraca
        b2=st.number_input("Insert the weibull shape parameter of component - {}" .format(chr(946)), min_value = 1.0, max_value = 6.0, value = 3.0) #forma fraca
        
        cp=st.number_input("Insert the cost of preventive replacement parameter", min_value = 0.0, value = 1.0) #custo da preventiva
        cd=st.number_input("Insert the cost of downtime per unit of time parameter", min_value = 0.0, value = 0.5) #custo de downtime por unidade de tempo
        cm=st.number_input("Insert the aditional (unit) cost for replacement at preventive age", min_value = 0.0, value = 1.00) #custo de inspeção
        cf=st.number_input("Insert the cost of corrective replacement parameter", min_value = 0.0, value = 1.0) #custo de falha
        
        q=st.number_input("Insert the proability of opportunity", min_value = 0.0, max_value = 1.0, value = 0.2) #taxa de chegada de oportunidades
        s=st.number_input("Insert the scheduled time between visits parameter", min_value = 0.0, value = 1.0) #intervalo entre visitas
        
        st.subheader("Insert the decision variable values below:")
        
        W=int(st.number_input("Insert the initial threshold of opportunities variable", min_value = 0, max_value = 50, step = 1, value = 6)) #Limite inferior da janela de oportunidades
        M=int(st.number_input("Insert the total number of visits variable", min_value = 0, max_value = 50, step = 1, value = 14)) #Limite inferior da janela de oportunidades
        
        st.subheader("Click on botton below to run this application:")
        
        botao = st.button("Get cost-rate")

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
              
              mu = ve/(p11+p12+p31+p32)
            
              if pe < 0.999 or pe > 1.001:
                print("Algum erro ocorreu!")
            
              return tx, ce, ve, pe, dx, mu

            taxadecusto = otm()
            st.write("Cost-rate result: {}" .format(taxadecusto[0]))
            st.write("Downtime-rate result: {}" .format(taxadecusto[4]))

    if choice == menu[1]:
        
        st.header(menu[1])
        
        st.write('''This prototype was created by members of the RANDOM research group, which aims to assist in the application of a quasi-periodic opportunistic replacement policy.''')
        st.write('''This prototype has restrictions regarding the solution search space. If it is in the user's interest to use a wider range of solution combinations or if there is any question about the study and/or this prototype can be directed to any of the email addresses below. Also, this application is still in the development stage. Finally, if this application is used for any purpose, all authors should be informed.''')
        st.write('''y.r.melo@random.org.br''')
        st.write('''a.j.s.rodrigues@random.org.br''')
        st.write('''c.a.v.cavalcante@random.org.br''')
        
    if choice == menu[2]:
        
        st.header(menu[2])
        
        st.write("The Research Group on Risk and Decision Analysis in Operations and Maintenance was created in 2012 in order to bring together different researchers who work in the following areas: risk, maintenance and operation modelling. Learn more about it through our website.")
        st.markdown('[Click here to be redirected to our website](https://random.org.br)',False)

if st._is_running_with_streamlit:
    main()
else:
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())
