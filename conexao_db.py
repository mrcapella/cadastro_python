import mysql.connector
class Conexao:

    #Inicializador da classe
    def __init__(self, tipo, sql, dados):
        self.tipo = tipo
        self.sql = sql
        self.dados = dados
        self.host = "localhost"
        self.user = "capella"
        self.passwd = "84011970"
        self.db = "workflow"
    
    #Função para conectar com o db e executar as querys
    def connect_db (self):
        
        db_connection = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.db)
        cursor = db_connection.cursor()

        #Testa o tipo de query à ser executada
        if (self.tipo == "C"):
            cursor.execute(self.sql)
            resultado = cursor.fetchall()
            return resultado    
        elif (self.tipo == "I"):
            cursor.execute(self.sql, self.dados)
            db_connection.commit()    
        else:
            cursor.execute(self.sql)
            db_connection.commit()

        #Fecha a conexão com o db
        db_connection.close()


