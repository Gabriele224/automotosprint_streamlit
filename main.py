from fastapi import FastAPI,HTTPException, Depends,Response
#from fastapi_views import methodview
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session,mapped_column,Mapped
from pydantic import BaseModel
from typing import List
from sqlalchemy import Text,Date,func,desc
from datetime import date

app = FastAPI()

SQLALCHEMY_DATABASE_URL='mysql+pymysql://gabriele:Gabry678@db:3306/automotosprint'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definizione delle tabelle
class clienti(Base): ## nome classi lettera grande
    __tablename__="clienti"
    clientiId= Column(Integer, primary_key=True,index=True)
    nome=Column(String(45), nullable=False)
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



class ordine(Base):
    __tablename__="ordine"
    codordine=Column(Integer, primary_key=True)
    cliente=Column(Integer, ForeignKey('clienti.clientiId'), nullable=False)
    data=Column(Date,default=date)

class forniture(Base):
    __tablename__="forniture"
    idforniture=Column(Integer,primary_key=True)
    codordine=Column(Integer ,ForeignKey('ordine.codordine'),nullable=False)
    codiceprod=Column(Integer,ForeignKey('prodotto.codiceprod'),nullable=False)
    qt=Column(Integer)

class prodotto(Base):
    __tablename__="prodotto"
    codiceprod=Column(Integer,primary_key=True)
    nomeprod=Column(String(45),nullable=False)
    prezzoprod=Column(Integer)
    giacenza=Column(Integer)

session=sessionmaker(bind=engine)
session=Session()

#pyndatic
class clienteCreate(BaseModel):
    nome:str

class ordineCreate(BaseModel):
    cliente:int
    data:date

class fornituraCreate(BaseModel):
    codordine:int
    codiceprod:int
    qt:int

class prodottoCreate(BaseModel):
    nomeprod:str
    prezzoprod:int
    giacenza:int

class ClienteUpdate(BaseModel):
    nome:str

class ordineUpdate(BaseModel):
    cliente:int
    data:date

class fornituraUpdate(BaseModel):
    codordine:int
    codiceprod:int
    qt:int

class prodottoUpdate(BaseModel):
    nomeprod:str
    prezzoprod:int
    giacenza:int

    class Config:
        orm_mode = True

#sessione database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
#1)Ottieni tutti gli utenti
@app.get("/clienti")
def cliente(db: Session = Depends(get_db)):
   client = db.query(clienti).all()
   return client

#2)Elenco dei clienti che comprano uno specifico prodotto
@app.get("/clienti_with_prodotto/{product}")
def clienti_with_prodotto(product:str,db:Session=Depends(get_db)):
    product=db.query(clienti).join(ordine).join(forniture).join(prodotto).filter(prodotto.nomeprod==product).all()
    return product

#3)Elenca i clienti indicando quanti ordini hanno effettuato
@app.get("/ordine_clienti")
def ordine_clienti(db:Session=Depends(get_db)):
    ord_effettuati=db.query(clienti.nome,func.count().label('tot_ordini')).select_from(ordine).join(clienti).group_by(clienti.clientiId)
    response_serializable=[
        {
            "nome":nome,
            "tot_ordini":tot_ordini

        } for nome,tot_ordini in ord_effettuati
        ]
    return response_serializable

#4)Elenca i clienti indicando il quantitativo di pezzi acquistato
@app.get("/clienti_acquisto")
def clienti_acquisto(db:Session=Depends(get_db)):
    client_acquist=db.query(clienti.nome, func.sum(forniture.qt).label('Quantità')).select_from(ordine).join(clienti).join(forniture).group_by(clienti.nome)
    response_serializable=[
        {
            "nome":nome,
            "Quantità":Quantità
        } for nome,Quantità in client_acquist
        ]
    return response_serializable
#5)Ottenimento cliente singolo
@app.get("/cliente_singolo/{client}")
def cliente_singolo(client:int,db:Session=Depends(get_db)):
    client_single=db.query(clienti.clientiId,clienti.nome).select_from(clienti).filter(clienti.clientiId==client).all()
    response_serializable=[
        {
            "clientiId":clientiId,
            "nome":nome
        } for clientiId,nome in client_single
        ]
    return response_serializable
#6)Elenco dei prodotti acquistati da un cliente specifico e la quantità acquistata
@app.get("/cliente_prodotto/{nome_cliente}")
def cliente_prodotto(nome_cliente:str,db:Session=Depends(get_db)):
    client_product=db.query(clienti.nome,prodotto.nomeprod,forniture.qt).select_from(clienti
                                          ).join(ordine,clienti.clientiId==ordine.cliente).join(forniture,
                                                                                                ordine.codordine==forniture.codordine
                                                              ).join(prodotto,forniture.codiceprod==prodotto.codiceprod
                                                                     ).filter(clienti.nome==nome_cliente).all()
    response_serializable=[
           {
            
               
               "nomeprod":nomeprod,
               "nome": nome,
               "qt":qt
           }
           for nomeprod,nome,qt in client_product
       ]
    return response_serializable
    
#7)Elenco dei clienti che hanno speso di più in totale
@app.get("/cliente_spesa")
def cliente_spesa(db:Session=Depends(get_db)):
    client_shop=db.query(clienti.nome.label('cliente'),func.sum(prodotto.prezzoprod.label('Spesa_cliente'))).select_from(clienti).join(ordine,clienti.clientiId==ordine.cliente).join(forniture,ordine.codordine==forniture.codordine).join(prodotto,forniture.codiceprod==prodotto.codiceprod).group_by(clienti.nome)
    response_serializable=[
           {
            
               "cliente": nome,
               "Spesa_cliente":prezzoprod
              
           }
           for nome,prezzoprod in client_shop
       ]
    return response_serializable


#Aggiunta di un nuovo cliente
@app.post("/clienti",response_model=clienteCreate)
def aggiungi_cliente(cliente:clienteCreate,db:Session=Depends(get_db)):
     db_cliente=clienti(nome=cliente.nome)
     db.add(db_cliente)
     db.commit()
     db.refresh(db_cliente)
     return db_cliente

#Modifica un seguente cliente
@app.route("/clienti/{clientiId}")
class Crudclienti():
    @app.put("/clienti/{clientiId}")
    def aggiornamento(clientiId:int,cliente_update:ClienteUpdate, db:Session=Depends(get_db)):
        db_cliente=db.query(clienti).filter(clienti.clientiId==clientiId).first()
        db_cliente.nome=cliente_update.nome
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
#Rimozione cliente
    @app.delete("/clienti/{clientiId}")
    def delete_cliente(clientiId:int,db:Session=Depends(get_db)):
        db_cliente=db.query(clienti).filter(clienti.clientiId==clientiId).first()
        db.delete(db_cliente)
        db.commit()
        return {"message":f"il cliente è stato eliminato {clientiId}"},200

####################################################

#Ottenimento tutti gli ordini
@app.get("/ordine")
def ordini(db:Session=Depends(get_db)):
    ord= db.query(ordine).all()
    return ord
#1)Elenco degli ordini effettuati da uno specifico cliente:
@app.get("/ordini/{name}")
def ordini(name:str,db: Session = Depends(get_db)):
        ord = db.query(ordine.codordine).select_from(ordine).join(clienti,ordine.cliente==clienti.clientiId).filter(clienti.nome== name).first()
        ordine_cliente=[{'codordine':codordine} for codordine in ord]
        return ordine_cliente

#3)Elenco degli ordini dei rispettivi clienti 
#con importo complessivo organizzato per importo
@app.get("/ordine_clienti")
def ordine_clienti(db:Session=Depends(get_db)):
    result=db.query(clienti.nome,ordine.codordine
                    ,func.sum(forniture.qt * prodotto.prezzoprod
                                                           ).label('TOT')).select_from(ordine
                                                                                       ).join(clienti,ordine.cliente==clienti.clientiId
                                                                                              ).join(forniture,ordine.codordine==forniture.codordine
                                                                                                     ).join(prodotto,forniture.codiceprod==prodotto.codiceprod
                                                                                                            ).group_by(clienti.nome,ordine.codordine)
    totale=[{'nome':nome,'codordine':codordine,'TOT':TOT} for nome,codordine,TOT in result]
    return totale

#4)indica il numero e la data di tutti gli ordini dove è 
# stato venduto uno specifico e il numero di 
# pezzi di quel prodotto venduti

@app.get("/ordine_venduti/{product}")
def ordine_venduti(product:str,db:Session=Depends(get_db)):
    result=db.query(ordine.codordine,forniture.qt).select_from(forniture
                                                               ).join(ordine,forniture.codordine==ordine.codordine
                                                                      ).join(prodotto,forniture.codiceprod==prodotto.codiceprod
                                                                             ).filter(prodotto.nomeprod==product).all()
    ord_venduti=[{'codordine':codordine,'qt':qt} for codordine,qt in result]
    return ord_venduti

#7)quali sono gli ordini che hanno più di un prodotto
@app.get("/ordine_with_prodotto")
def ordine_with_prodotto(db:Session=Depends(get_db)):
    result=db.query(ordine.codordine,func.count().label('PiuProdotti')
                    ).select_from(ordine
                                  ).join(forniture,ordine.codordine==forniture.codordine
                                         ).group_by(ordine.codordine)
    ord_with_product=[{'codordine':codordine,'PiuProdotti':PiuProdotti} for codordine,PiuProdotti in result]
    return ord_with_product

#Ottenimento di un singolo ordine
@app.get("/ordine_singolo/{codice_ordine}")
def cliente_singolo(codice_ordine:int,db:Session=Depends(get_db)):
    cod_ord=db.query(ordine.codordine,ordine.cliente,ordine.data).select_from(ordine).filter(ordine.codordine==codice_ordine).all()
    response_serializable=[
        {
            "codordine":codordine,
            "cliente":cliente,
            "data":data
        } for codordine,cliente,data in cod_ord
        ]
    return response_serializable

#Aggiunta di un ordine

@app.post("/ordini",response_model=ordineCreate)
def ordini(ordini:ordineCreate,db:Session=Depends(get_db)):
    db_ordini=ordine(cliente=ordini.cliente,data=ordini.data)
    db.add(db_ordini)
    db.commit()
    db.refresh(db_ordini)
    return {"message":f"L'ordine {db_ordini} è stato aggiunto"},200

#Aggiornamento dell'ordine
@app.route("/ordini/{codordine}")
class Crudordini():
    @app.put("/ordini/{codordine}")
    def ordini_aggiornamento(codordine:int,ordine_update:ordineUpdate,db:Session=Depends(get_db)):
        db_ordini=db.query(ordine).filter(ordine.codordine==codordine).first()
        db_ordini.cliente=ordine_update.cliente
        db_ordini.data=ordine_update.data
        db.commit()
        db.refresh(db_ordini)
        return db_ordini
#Rimozione intero ordine
    @app.delete("/ordini/{codordine}")
    def delete(codordine:int,db:Session=Depends(get_db)):
        db_ord=db.query(ordine).filter(ordine.codordine==codordine).first()
        db.delete()
        db.commit()
        return {"message":f"L'ordine {db_ord} eliminato con successo"},200

######################################################à

#1)Ottenimento di tutte le forniture
@app.get("/fornitura")
def fornitura(db:Session=Depends(get_db)):
    f=db.query(forniture).all()
    return f

#2)Ottenimento di una singola fornitura
@app.get("/fornitura/{id}")
def fornitura(id:int,db:Session=Depends(get_db)):
    forni=db.query(forniture.idforniture,forniture.codordine,forniture.codiceprod,forniture.qt
                   ).select_from(forniture
                                 ).filter(forniture.idforniture==id).all()
    response_serializable=[
        {
            "idforniture":idforniture,
            "codordine":codordine,
            "codiceprod":codiceprod,
            "qt":qt
        } for idforniture, codordine,codiceprod,qt in forni
        ]
    return response_serializable

#Aggiunta fornitura
@app.post("/fornitura",response_model=fornituraCreate)
def fornitura(forni:fornituraCreate,db:Session=Depends(get_db)):
    db_fornitura=forniture(codordine=forni.codordine,codiceprod=forni.codiceprod,qt=forni.qt)
    db.add(db_fornitura)
    db.commit()
    db.refresh(db_fornitura)
    return db_fornitura

#Aggiornamento della fornitura
@app.route("/fornitura/{id}")
class Crudfornitura():
    @app.put("/fornitura/{id}")
    def fornitura_aggiornamento(id:int,fornitura_update:fornituraUpdate,db:Session=Depends(get_db)):
        db_fornitura=db.query(forniture).filter(forniture.idforniture==id).first()
        db_fornitura.codordine=fornitura_update.codordine
        db_fornitura.codiceprod=fornitura_update.codiceprod
        db_fornitura.qt=fornitura_update.qt
        db.commit()
        db.refresh(db_fornitura)
        return db_fornitura

#Rimozione della fornitura
    @app.delete("/fornitura/{id}")
    def delete(id:int,db:Session=Depends(get_db)):
        db_forni=db.query(forniture).filter(forniture.idforniture==id).first()
        db.delete()
        db.commit()
        return {"message":f"L'ordine {db_forni} eliminato con successo"},200

######################################################

#Ottenimento di tutti i prodotti
@app.get("/prodotti")
def prodotti(db:Session=Depends(get_db)):
    p=db.query(prodotto).all()
    return p

#Ottenimento di un singolo prodotto
@app.get("/prodotto_single/{codice}")
def prodotto_single(codice:int,db:Session=Depends(get_db)):
    prod=db.query(prodotto.codiceprod,prodotto.nomeprod,prodotto.prezzoprod,
                  prodotto.giacenza).select_from(prodotto).filter(prodotto.codiceprod==codice).all()
    p=[{'codiceprod':codiceprod,'nomeprod':nomeprod,
        'prezzoprod':prezzoprod,'giacenza':giacenza}
         for codiceprod,nomeprod,prezzoprod,giacenza in prod]
    return p

#1)Elenco dei prodotti più venduti in base alla quantità totale venduta
@app.get("/prodotti_qt")
def prodotti_qt(db:Session=Depends(get_db)):
    prod=db.query(prodotto.nomeprod,
                  func.sum(forniture.qt).label('totale_quantità')
                  ).select_from(prodotto).outerjoin(forniture,prodotto.codiceprod==forniture.codiceprod
                                                    ).group_by(prodotto.nomeprod
                                                               ).filter(prodotto.nomeprod.isnot(None)
                                                                        ).order_by(desc('totale_quantità')).all()
    p=[{'nomeprod':nomeprod,'totale_quantità':totale_quantità} 
       for nomeprod,totale_quantità in prod]
    return p

#2)prodotti non ancora ordinati da nessun cliente
@app.get("/prodotti_no_ordinati")
def prodotti_no_ordinati(db:Session=Depends(get_db)):
    subquery=db.query(forniture.codiceprod).distinct().subquery()

    p_no_o=db.query(prodotto.codiceprod,prodotto.nomeprod
                    ).outerjoin(subquery,prodotto.codiceprod==subquery.c.codiceprod
                                ).filter(subquery.c.codiceprod==None).all()
    p=[{'codiceprod':codiceprod,'nomeprod':nomeprod} for codiceprod,nomeprod in p_no_o]
    return p

#Aggiunta prodotto
@app.post("/prodotti",response_model=prodottoCreate)
def prodotti(prodotti:prodottoCreate,db:Session=Depends(get_db)):
    db_prodotti=prodotto(nomeprod=prodotti.nomeprod,prezzoprod=prodotti.prezzoprod,giacenza=prodotti.giacenza)
    db.add(db_prodotti)
    db.commit()
    db.refresh(db_prodotti)
    return db_prodotti

#Aggiornamento dell'ordine
@app.route("/prodotti/{cod_prod}")
class Crudprodotto():

    @app.put("/prodotti/{cod_prod}")
    def prodotti_aggiornamento(cod_prod:int,prodotto_update:prodottoUpdate,db:Session=Depends(get_db)):
        db_prodotto=db.query(prodotto).filter(prodotto.codiceprod==cod_prod).first()
        db_prodotto.nomeprod=prodotto_update.nomeprod
        db_prodotto.prezzoprod=prodotto_update.prezzoprod
        db_prodotto.giacenza=prodotto_update.giacenza
        db.commit()
        db.refresh(db_prodotto)
        return db_prodotto

#Rimozione intero ordine
    @app.delete("/prodotti/{cod_prod}")
    def delete(cod_prod:int,db:Session=Depends(get_db)):
        db_prod=db.query(prodotto).filter(prodotto.codiceprod==cod_prod).first()
        db.delete()
        db.commit()
        return {"message":f"L'ordine {db_prod} eliminato con successo"},200