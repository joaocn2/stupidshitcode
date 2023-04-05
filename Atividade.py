import sqlite3 
import sys
import time

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Definido funções de CRUD com o banco
def conectarBanco():
    conexao = None
    try:
        conexao = sqlite3.connect(r".\unoesc_bd.db",timeout=10)        
        return conexao
    except sqlite3.Error as e:
        print(e)
        return e
    
    
def criarTabela(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pessoas';")
    result = cursor.fetchall()
    if (result != []):
        pass
    else:
        conn = conexao.execute("CREATE TABLE pessoas (codigo INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT,data_nascimento TEXT,salario REAL (10,2));")
        conexao.commit()
        if(conn):
            print("\nTabela Criada")

def insertTabela(conexao,nomes,datas,sal):

    try:
        conn = conexao.execute(f'INSERT INTO pessoas (nome,data_nascimento,salario) VALUES ("{nomes}","{datas}",{sal});')
        conexao.commit()
        if(conn):
            print("\nInserção Concluída")
    except sqlite3.Error as error:
        print("\nFailed to insert data in sqlite table", error)
        
def deleteRow(conexao,codigo):
    try:
        cursor = conexao.cursor()
        conn = cursor.execute(f'DELETE FROM pessoas WHERE codigo = {codigo};')
        conexao.commit()
        if(conn):
            print("Exclusão Concluída")
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)
        
    
def updateBanco(conexao,campo,valor,id):
    conexao.execute(f'UPDATE pessoas SET "{campo}"="{valor}" WHERE codigo={id};')
    
def printBanco(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM pessoas;")
    registros = cursor.fetchall()
    for registro in registros:
        print("------------------------")
        print("Id : " , registro[0])
        print("Nome : " , registro[1])
        print("Data Nascimento : " , registro[2])
        print("Salario : R$" , registro[3])
        print("------------------------")
    cursor.close()
    return registros

def printSelected(conexao, id):
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM pessoas WHERE codigo={id};")
    registros = cursor.fetchall()
    print(registros)
    for registro in registros:
        print("------------------------")
        print("Id : " , registro[0])
        print("Nome : " , registro[1])
        print("Data Nascimento : " , registro[2])
        print("Salario : R$" , registro[3])
        print("------------------------")
    cursor.close()
    return registros
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Solicitando valores e chamando a função de CRUD


conexao = conectarBanco()

def insertTabelaValor():
    nome = input("Digite o nome: ")
    data = input("Data de Nascimento: ")
    salario = input("Salario: ")
    conf = input( f"Nome : {nome} \n"
                  + f"Data Nascimento : {data} \n"
                  + f"Salário : {salario} \n"
                  +"\nDeseja Continuar? \n"
                  +"Resposta (S/N) : ")
    if(conf.upper() == "S"):
        insertTabela(conexao,nome,data,salario)


def excluirTabela():
    printBanco(conexao)
    id = int(input("Qual id deseja excluir? \n"
                   +"id : "))
    cursor = conexao.cursor()
    cursor.execute(f'SELECT * FROM pessoas WHERE codigo = {id};')
    registros = cursor.fetchall()
    for registro in registros:
        print("------------------------")
        print("Id : " , registro[0])
        print("Nome : " , registro[1])
        print("Data Nascimento : " , registro[2])
        print("Salario : R$" , registro[3])
        print("------------------------")
    cursor.close()
    conf = input("Deseja Continuar? \n"
                 +"Resposta (S/N) : ")
    
    if(conf.upper() == "S"):
        deleteRow(conexao, id)
    
def updateTabela():
    printar()
    id = input("Escolha o Id que deseja editar : ")
    campo = input("Escolha o campo que deseja alterar : \n"
                  +" 1 - Nome \n"
                  +" 2 - Data de Nascimento \n"
                  +" 3 - Salário \n"
                  +" 4 - Sair"
                  +"Opção : ")
    
    valor = input("Digite o novo valor : ")
    if(campo == "1"):
        campo = "nome"
    elif(campo == "2"):
        campo = "data_nascimento"
    elif(campo == "3"):
        campo = "salario"
    elif(campo == "4"):
        sys.exit()
    else:
        pass
    updateBanco(conexao, campo, valor, id)

def printar():
    printBanco(conexao)
    
def menu():
    while(1<2):
        guia = input("Escolha uma opção : \n"
                      +" 1 - Inserir Valores \n"
                      +" 2 - Excluir Valores \n"
                      +" 3 - Printar Valores \n"
                      +" 4 - Alterar Valores \n"
                      +" 5 - Sair \n"
                      +"Opção: ")
        guia = int(guia)
        if(guia >= 1 and guia <= 5):
            if (guia == 1):
                insertTabelaValor()
            elif(guia == 2):
                excluirTabela()
            elif(guia == 3):
                printBanco(conexao)
                time.sleep(3)
            elif(guia == 4):
                updateTabela()
            elif(guia==5):
                sys.exit()
            
        else:
            print()
            print("Valor Inválido")
            time.sleep(3)



