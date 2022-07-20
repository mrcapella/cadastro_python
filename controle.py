from tkinter import messagebox
from PyQt5 import uic,QtWidgets
from reportlab.pdfgen import canvas
from conexao_db import Conexao

#função para fechar o form Lista
def voltar_home():
    lista.close()

#função para gerar um arquivo pdf da lista de produtos
def gerar_pdf():   
    try:
        sql = "SELECT cadastro_codigo,cadastro_descricao,cadastro_preco,cadastro_categoria FROM workflow.wf_cadastro"
        consulta = Conexao("C",sql,"")
        resultado = consulta.connect_db()        
        y = 0
        pdf = canvas.Canvas("Cadastro_produtos.pdf")
        pdf.setFont("Times-Bold", 15)
        pdf.drawString(200,800, "Produtos cadastrados:")
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(10, 750, "CÓDIGO")
        pdf.drawString(110, 750, "DESCRIÇÃO")
        pdf.drawString(310, 750, "PREÇO")
        pdf.drawString(410, 750, "CATEGORIA")
        for i in range(0, len(resultado)):
            y += 20 #Variável para controlar o espaço entre as linhas
            pdf.drawString(10, (750-y), str(resultado[i][0]))
            pdf.drawString(110, (750-y), str(resultado[i][1]))
            pdf.drawString(310, (750-y), str(resultado[i][2]))
            pdf.drawString(410, (750-y), str(resultado[i][3]))        
        pdf.save()
    except:
        print("Erro na geração do arquivo PDF!")

#Função para receber os valores dos elementos do app
def funcao_principal():
    linha1 = cadastro.lineEdit.text()
    linha2 = cadastro.lineEdit_2.text()
    linha3 = cadastro.lineEdit_3.text()
    linha4 = cadastro.cbCategoria.currentText()

    if((linha1 == "") or (linha2 == "") or (linha3 == "") or (linha4 == "Selecione")):    
        messagebox.showwarning(title="Campos em branco", message="Todos os campos devem ser preenchidos.")
    else:
        #Query para inserir registro no db
        dados = (str(linha1),str(linha2),str(linha3),str(linha4))
        sql = "INSERT INTO wf_cadastro (cadastro_codigo,cadastro_descricao,cadastro_preco,cadastro_categoria) VALUES (%s,%s,%s,%s)"
        consulta = Conexao("I",sql, dados)
        consulta.connect_db()    
        cadastro.lineEdit.setText("")
        cadastro.lineEdit_2.setText("")
        cadastro.lineEdit_3.setText("")
        cadastro.cbCategoria.setCurrentText("Selecione")

#Função para exibir o produto que será atualizado o db
def editar_dados():
    edicao.show()
    linha = lista.tableWidget.currentRow()
    sql = "SELECT cadastro_codigo FROM wf_cadastro"
    consulta = Conexao("C",sql,"")
    cod = consulta.connect_db()
    sql = "SELECT * FROM wf_cadastro WHERE cadastro_codigo = "+ cod[linha][0]
    resultado = Conexao("C",sql,"")
    cod = resultado.connect_db()
    edicao.edCodigo.setText(cod[0][1])
    edicao.edDescricao.setText(cod[0][2])
    edicao.edPreco.setText(cod[0][3])
    edicao.cbCategoria.setCurrentText(cod[0][5])

#Função para alterar os dados dos produtos
def salvar_dados():
    codigo = edicao.edCodigo.text()
    descricao = edicao.edDescricao.text()
    preco = edicao.edPreco.text()
    categoria = edicao.cbCategoria.currentText()
    sql = "UPDATE wf_cadastro SET cadastro_codigo = '{}',cadastro_descricao = '{}',cadastro_preco = '{}',cadastro_categoria = '{}' WHERE cadastro_codigo = '{}'".format(codigo,descricao,preco,categoria,codigo)
    consulta = Conexao("U",sql,"")
    consulta.connect_db()    
    edicao.close()
    lista.close()
    abre_lista()

#Função para exibir a lista de produtos
def abre_lista():
    try:
        lista.show()
        sql = "SELECT cadastro_codigo,cadastro_descricao,cadastro_preco,cadastro_categoria FROM workflow.wf_cadastro"
        consulta = Conexao("C",sql,"")
        resultado = consulta.connect_db()
        print (resultado)
    except:
        print("Erro na inclusão do registro!")

    lista.tableWidget.setRowCount(len(resultado))
    lista.tableWidget.setColumnCount(4)

    #Loop para montar o grid com os dados retornados do db
    for i in range(0, len(resultado)):
        for j in range(0, 4):
             lista.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(resultado[i][j])))

    #Ajusta a largura das colunas no grid
    lista.tableWidget.setColumnWidth(0,70)
    lista.tableWidget.setColumnWidth(1,265)
    lista.tableWidget.setColumnWidth(2,70)
    lista.tableWidget.setColumnWidth(3,150)

#Função para excluir registro do db
def exclui_registro():
    try:
        lex = lista.tableWidget.currentRow()
        id_linha = lista.tableWidget.item(lex,0).text()
        sql = f"DELETE FROM wf_cadastro WHERE cadastro_codigo = '{id_linha}'"
        consulta = Conexao("E",sql,"")
        consulta.connect_db()
        lista.tableWidget.removeRow(lex)
    except:
        print("Erro na exclusão do registro!")

#Carrega os métodos do QT5
app = QtWidgets.QApplication([])
cadastro = uic.loadUi("cadastro.ui")
lista = uic.loadUi("lista_dados.ui")
edicao = uic.loadUi("editar.ui")
cadastro.pushButton.clicked.connect(funcao_principal)
cadastro.pushButton_2.clicked.connect(abre_lista)
lista.btExcluir.clicked.connect(exclui_registro)
lista.btVoltar.clicked.connect(voltar_home)
lista.btPdf.clicked.connect(gerar_pdf)
lista.btEditar.clicked.connect(editar_dados)
edicao.btSalvar.clicked.connect(salvar_dados)

#exibe o app
cadastro.show()
#executa o app
app.exec()