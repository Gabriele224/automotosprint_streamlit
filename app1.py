import sys,os
from fastapi import FastAPI
import streamlit as st
import requests
from datetime import date
import pandas as pd

# url per le fastapi

BASE_URL= "http://127.0.0.1:8000"

#funzioni per le api

def get_simple(Query):
    response=requests.get(f"{BASE_URL}/{Query}")
    return response.json()
    

def clienti_total(clienti_box):
    response=requests.get(f"{BASE_URL}/{clienti_box}")
    return response.json()

def nomi_or_id(query_nome,nome_query_nome_id):
    response=requests.get(f"{BASE_URL}/{query_nome}/{nome_query_nome_id}")
    return response.json()

def get_ordine_total(ordine_box,serie_box):
    response=requests.get(f"{BASE_URL}/{ordine_box}/{serie_box}")
    return response.json()

def simple_ordine(ord_box):
    response=requests.get(f"{BASE_URL}/{ord_box}")
    return response.json()

def prodotto_get(proquery):
    response=requests.get(f"{BASE_URL}/{proquery}")
    return response.json()

def single_c_o_f_p(cofp,single):
    response=requests.get(f"{BASE_URL}/{cofp}/{single}")
    return response.json()

def post_c_o_f_p(pcofp,data):
    if "data" in data and isinstance(data["data"], date):
        data["data"] = data["data"].isoformat()
    response=requests.post(f"{BASE_URL}/{pcofp}",json=data)
    return response

def put_c_o_f_p(putcofp,identificativo,data):
    if "data" in data and isinstance(data["data"], date):
        data["data"] = data["data"].isoformat()
    response=requests.put(f"{BASE_URL}/{putcofp}/{identificativo}",json=data)
    return response

def delete_c_o_f_p(deletecofp,iden):
    response=requests.delete(f"{BASE_URL}/{deletecofp}/{iden}")
    return response.json()
#main con tutte le interfacce streamlit
def main():
    #get single ottenimento tutti i dati
    st.title("Ottenimento tutti clienti,ordine,fornitura,prodotti,digitando tra 3 elementi\n")
    query_operazione=['clienti','ordine','fornitura','prodotti']
    Query=st.selectbox("Segli tra queste operazioni:\n",query_operazione)
    if st.button("Esequi la scelta"):
        s=get_simple(Query)
        if isinstance(s,list):
            simple=pd.DataFrame(s)
            st.write(simple)
        else:
            st.info("Nessun  trovato!!")

    st.title("Query Clienti 3),4),7)")
    st.header('3)Elenca i clienti indicando quanti ordini hanno effettuato(ordine_clienti)')
    st.header('4)Elenca i clienti indicando il quantitativo di pezzi acquistato(clienti_acquisto)')
    st.header('7)Elenco dei clienti che hanno speso di più in totale(cliente_spesa)')
    c_box=['ordine_clienti','clienti_acquisto','cliente_spesa']
    clienti_box=st.selectbox("scegli tra queste operazioni sui i clienti:\n",c_box)
    if st.button("Esegui ope_clienti"):
            cb=clienti_total(clienti_box)
            if isinstance(cb,list):
                cbox=pd.DataFrame(cb)
                st.write(cbox)
            else:
                st.info("Operazioni non trovate!!")

    st.title("Query dei clienti 2),6)")
    st.header('2)Elenco dei clienti che comprano uno specifico prodotto(clienti_with_prodotto)')
    st.header('6)Elenco dei prodotti acquistati da un cliente specifico e la quantità acquistata(cliente_prodotto)')
    query_nome_box=['clienti_with_prodotto','cliente_prodotto']
    nome_query_nome_id_1=["Cliente(cliente_prodotto):\n",'fiat','nissan','volvo','mercedes','volkswagen','peugeut','lancia','land rover','tesla',
                            'renaut','dacia','mg','jeep','\n\n',
                            "Prodotto(clienti_with_prodotto):\n",'ruote','pistone','bulloni','cerchioni','volante','motore','radiatori','servosterzo',
                            'olio','radio','chiaveinglese','acqua','porte']
    query_nome=st.selectbox("Scegli tra clienti_with_prodotto(prodotto),cliente_prodotto(nome_cliente):\n",query_nome_box)
    nome_query_nome_id=st.selectbox("Scegli tra nome_cliente,product,clientiId:\n",nome_query_nome_id_1)
    if st.button("Esegui query"):
        g=nomi_or_id(query_nome,nome_query_nome_id)
        if isinstance(g,list):
            ni=pd.DataFrame(g)
            st.write(ni)
        else:
            st.info("Nessun cliente trovato!!")

    st.title("Ottenimento singolo cliente ,ordine, fornitura, prodotti")
    cofp1=['cliente_singolo','ordine_singolo','fornitura','prodotto_single']
    single1=["clientiId:\n",1,2,3,4,5,6,7,8,9,10,12,14,18,'\n',
             "singolo ordine:\n",1,2,3,4,5,6,7,10,11,12,13,14,15,16,17,'\n',
             "singola fornitura:\n",1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,'\n',
             "singolo prodotto:\n",1,2,3,4,5,6,7,8,9,10,11,12,13]
    #single2=["singolo ordine:\n",1,2,3,4,5,6,7,10,11,12,13,14,15,16,17]
    #single3=["singola fornitura:\n",1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20]
    #single4=["singolo prodotto:\n",1,2,3,4,5,6,7,8,9,10,11,12,13]
    #singl=single1+single2+single3+single4
    cofp=st.selectbox("scegli tra i singoli 1)clienti,2)ordine,3)fornitura,4)prodotti:\n",cofp1)
    single=st.selectbox("scegli l'id giusto per te:\n",single1)
    if st.button("Esegui singolo"):
        c=single_c_o_f_p(cofp,single)
        if isinstance(c,list):
            co=pd.DataFrame(c)
            st.write(co)
        else:
            st.info("Nessuna infomarzione singola ottenuta!!")

    st.title("Query ordini ")
    st.header('1)Elenco degli ordini effettuati da uno specifico cliente(ordini)')
    st.header('4)indica il numero e la data di tutti gli ordini dove è stato venduto'+'\n'+' uno specifico prodotto e il numero di pezzi di quel prodotto venduti(ordini_venduti)')
    ordine_selectbox=['ordini','ordine_venduti']
    serie2=["prodotto:\n",'ruote','pistone','bulloni','cerchioni','volante','motore','radiatori','servosterzo',
                          'olio','radio','chiaveinglese','acqua','porte','\n',
                          "Cliente(macchina):\n",'fiat','nissan','volvo','mercedes','volkswagen','peugeut','lancia','land rover','tesla',
                          'renaut','dacia','mg','jeep']
    ordine_box=st.selectbox("Scegli tra 1)ordini da specifico cliente(nome_cliente),2)ordini totale(prodotto):\n",ordine_selectbox)
    serie_box=st.selectbox("Scegli ordini o ordine_venduti:\n",serie2)
    if st.button("Esegui ordini",key="buttonfirst"):
        ord=get_ordine_total(ordine_box,serie_box)
        if isinstance(ord,list):
            ob=pd.DataFrame(ord)
            st.write(ob)
        else:
            st.info("ordine non trovato per nessuna seguente query!!")

    st.title("Query ordini\n")
    st.header('3)Elenco degli ordini dei rispettivi clienti con importo complessivo organizzato per importo(ordine_clienti)')
    st.header('7)quali sono gli ordini che hanno più di un prodotto')
    ord_select=['ordine_clienti','ordine_with_prodotto']
    ord_box=st.selectbox("Query ordini 3),7):\n",ord_select)
    if st.button("Esegui ordini",key="buttonseconds"):
        o=simple_ordine(ord_box)
        if isinstance(o,list):
            ordbox=pd.DataFrame(o)
            st.write(ordbox)
        else:
            st.info("Nessun operazione effettuata!!")
    
    st.title("Query prodotti\n")
    st.header('1)Elenco dei prodotti più venduti in base alla quantità totale venduta(prodotti_qt)')
    st.header('2)prodotti non ancora ordinati da nessun cliente(prodotti_no_ordinati)')
    p=['prodotti_qt','prodotti_no_ordinati']
    proquery=st.selectbox("1)(prodotti_qt),2)(prodotti_no_ordinati):\n",p)
    if st.button("Esequi prodotti"):
        pr=prodotto_get(proquery)
        if isinstance(pr,list):
            pro=pd.DataFrame(pr)
            st.write(pro)
        else:
            st.info("Nessuna operazione sui prodotti!!")
    
    st.title("Post clienti,ordini,fornitura,prodotti")
    pcofp1=['clienti','ordini','fornitura','prodotti']
    pcofp=st.selectbox("Scegli la post che vuoi fare:\n",pcofp1,key="post1")

    if pcofp == 'clienti':
        nome=st.text_input("Nome:\n",key="nome_cliente")
        data={"nome":nome}
        st.success(f"Cliente aggiunto con successo: {nome}")
    elif pcofp == 'ordini':
        cliente =st.text_input("cliente:\n",key="chiave_cliente")
        data =st.date_input("data:\n",key="postdata")
        try:
            cliente=int(cliente)
            data={"cliente":cliente,"data":data}
            st.success(f"ordine aggiunto con successo :{cliente} e {data}")
        except ValueError:
            st.error("inserisci numero valido")
    elif pcofp == 'fornitura':
        codordine=st.text_input("codordine:\n",key="chiavesternaordine")
        codiceprod=st.text_input("codiceprod:\n",key="chiavesternaporodotto")
        qt=st.text_input("qt:\n",key="quantitàfornitura")
        try:
            codordine=int(codordine)
            codiceprod=int(codiceprod)
            qt=int(qt)
            data={"codordine":codordine,"codiceprod":codiceprod,"qt":qt}
            st.success(f"fornitura aggiunta con successo :{codordine}, {codiceprod}, {qt}")
        except ValueError:
            st.error("inserisci numeri validi")
    elif pcofp == 'prodotti':
        nomeprod=st.text_input("nomeprod:\n",key="nomeprodotto")
        prezzoprod=st.text_input("prezzoprod:\n",key="prezzoprodotto")
        giacenza=st.text_input("giacenza:\n",key="giacenzaprodotto")
        try:
            prezzoprod=int(prezzoprod)
            giacenza=int(giacenza)
            data={"nomeprod":nomeprod,"prezzoprod":prezzoprod,"giacenza":giacenza}
            st.success(f"prodotto aggiunto con successo :{nomeprod} , {prezzoprod}, {giacenza}")
        except ValueError:
            st.error("dati validi")
    if st.button("Invia post"):
        response=post_c_o_f_p(pcofp,data)
        if response.status_code == 200:
            st.success(f"Dati inviati con successo: {response.json()}")
        else:
            st.error(f"Errore nell'invio dei dati: {response.status_code}")
    else:
        st.info("Compila i campi e clicca su 'Invia post' per inviare i dati")

    st.title("Put clienti,ordini,fornitura,prodotti")
    putcofp1=['clienti','ordini','fornitura','prodotti']
    putcofp=st.selectbox("Scegli la put che vuoi fare:\n",putcofp1,key="put1")
    #identificativo tra le put
    identificativo=st.text_input("Inserisci 1)clienti:clientiId,2)ordini:codiceordine,3)fornitura:id,4)prodotti:id:")

    if putcofp == 'clienti':
        nome=st.text_input("Nome:\n",key="cliente_nome")
        data={"nome":nome}
        st.success(f"Cliente aggiornato con successo: {nome}")
    elif putcofp == 'ordini':
        cliente =st.text_input("cliente:\n",key="putcliente")
        data =st.date_input("data:\n",key="putdata")
        try:
            cliente=int(cliente)
            data={"cliente":cliente,"data":data}
            st.success(f"ordine aggiornato con successo :{cliente} e {data}")
        except ValueError:
            st.error("dati ordine validi")
        
    elif putcofp == 'fornitura':
        codordine=st.text_input("codordine:\n",key="putordine")
        codiceprod=st.text_input("codiceprod:\n",key="putcodiceprod")
        qt=st.text_input("qt:\n",key="putqt")
        try:
            codordine=int(codordine)
            codiceprod=int(codiceprod)
            qt=int(qt)
            data={"codordine":codordine,"codiceprod":codiceprod,"qt":qt}
            st.success(f"fornitura aggiornato con successo :{codordine}, {codiceprod}, {qt}")
        except ValueError:
            st.error("dati delle forniture validi")
    elif putcofp == 'prodotti':
        nomeprod=st.text_input("nomeprod:\n",key="putnomeprod")
        prezzoprod=st.text_input("prezzoprod:\n",key="putprezzo")
        giacenza=st.text_input("giacenza:\n",key="putgiacenza")
        try:
            prezzoprod=int(prezzoprod)
            giacenza=int(giacenza)
            data={"nomeprod":nomeprod,"prezzoprod":prezzoprod,"giacenza":giacenza}
            st.success(f"prodotto aggiornato con successo :{nomeprod} , {prezzoprod}, {giacenza}")
        except ValueError:
            st.error("dati prodotti validi")
    if st.button("Invia put"):
        if identificativo:
            response=put_c_o_f_p(putcofp,identificativo,data)
        if response.status_code == 200:
            st.success(f"Dati inviati con successo: {response.json()}")
        else:
            st.error(f"Errore nell'invio dei dati: {response.status_code}")
    else:
        st.info("Compila i campi e clicca su 'Invia post' per inviare i dati")

    st.title("Delete clienti ,ordini,fornitura,prodotti")
    qsele=['clienti','ordini','fornitura','prodotti']
    deletecofp=st.selectbox("Scegli la delete 1)clienti,2)ordine,3)fornitura,4)prodotti",qsele)

    iden=st.text_input("Inserisci l'identificativo:")

    if st.button("Esegui delete"):
        if iden:
            response=delete_c_o_f_p(deletecofp,iden)
            if response:
                st.success(f"Eliminato: {response}")
            else:
                st.info("nessun dato")
                
        else:
            st.warning("Error nell'esecuzione")

if __name__ == "__main__":
    main()
