from Atividade import conectarBanco
from Atividade import printBanco
from Atividade import printSelected
from Atividade import updateBanco
from Atividade import insertTabela
from Atividade import deleteRow
from sqlite3 import Connection

import os

def test_deleteRow():
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO pessoas VALUES (99,'Teste--','30/02/1999',1970);")
    conexao.commit()
    deleteRow(conexao,99)
    cursor.execute("SELECT * FROM pessoas WHERE codigo = 99")
    resultado = cursor.fetchone()
    assert resultado is None, "O registro não foi deletado com sucesso."
    conexao.close()

def test_criarTabela():
    conexao = conectarBanco()
    cursor = conexao.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pessoas';")
    resultado = cursor.fetchone()
    assert resultado is not None, "A tabela não existe."
    conexao.close()
    
def test_conecta_banco():
    conexao = conectarBanco()
    assert isinstance(conexao, Connection)
    conexao.close()

def test_database_file():
    assert os.path.isfile('unoesc_bd.db')
    
def test_print_banco():
    conexao = conectarBanco()
    isNotNull = printBanco(conexao)
    assert isNotNull != []
    conexao.close()

def test_print_selected():
    conexao = conectarBanco()
    isNotNull = printSelected(conexao, 1)
    assert isNotNull != []
    conexao.close()

def test_table_update():
    count_changes = 0
    conexao = conectarBanco()
    cursor = conexao.cursor()
    campo = ["nome","data_nascimento","salario"]
    for i in range(0, len(campo)):
        updateBanco(cursor, campo[i], "Teste++", 1)
        conexao.commit()
        if cursor.rowcount > 0:
            count_changes+=1
    assert count_changes == 3
    conexao.close()

def test_table_insert():
    conexao = conectarBanco()
    cursor = conexao.cursor()
    valores = ["Teste--","30/02/1999",1970]
    insertTabela(conexao, valores[0], valores[1], valores[2])
    cursor.execute(f'SELECT * FROM pessoas WHERE nome = "{valores[0]}" AND data_nascimento = "{valores[1]}" AND salario="{valores[2]}"')
    retorno = cursor.fetchall()
    assert retorno != []
    conexao.close()
    

