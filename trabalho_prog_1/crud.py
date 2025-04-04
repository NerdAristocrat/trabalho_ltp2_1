import sqlite3

# Função para criar o banco de dados e a tabela
def criar_banco():
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        );
    ''')
    conexao.commit()
    conexao.close()

# Função para criar um novo produto
def criar_produto(nome, quantidade, preco):
    try:
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, quantidade, preco) 
            VALUES (?, ?, ?)
        ''', (nome, quantidade, preco))
        conexao.commit()
        print("Produto criado com sucesso!")
    except sqlite3.IntegrityError:
        print(f"Erro: O produto '{nome}' já existe.")
    finally:
        conexao.close()

# Função para listar todos os produtos
def listar_produtos():
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    
    if produtos:
        print("\nProdutos no estoque:")
        for produto in produtos:
            print(f"ID: {produto[0]} | Nome: {produto[1]} | Quantidade: {produto[2]} | Preço: R${produto[3]:.2f}")
    else:
        print("Nenhum produto encontrado.")
    
    conexao.close()

# Função para atualizar a quantidade e o preço de um produto
def atualizar_produto(id_produto, quantidade, preco):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (id_produto,))
    produto = cursor.fetchone()
    
    if produto:
        cursor.execute('''
            UPDATE produtos SET quantidade = ?, preco = ? WHERE id = ?
        ''', (quantidade, preco, id_produto))
        conexao.commit()
        print(f"Produto ID {id_produto} atualizado com sucesso!")
    else:
        print("Erro: Produto não encontrado.")
    
    conexao.close()

# Função para deletar um produto pelo ID
def deletar_produto(id_produto):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (id_produto,))
    produto = cursor.fetchone()
    
    if produto:
        cursor.execute('DELETE FROM produtos WHERE id = ?', (id_produto,))
        conexao.commit()
        print(f"Produto ID {id_produto} deletado com sucesso!")
    else:
        print("Erro: Produto não encontrado.")
    
    conexao.close()

# Função para exibir o menu interativo
def menu():
    while True:
        print("\n----- Menu de Operações -----")
        print("1. Criar um novo produto")
        print("2. Listar todos os produtos")
        print("3. Atualizar um produto")
        print("4. Deletar um produto")
        print("5. Sair")
        
        escolha = input("Escolha uma opção (1-5): ")
        
        if escolha == '1':
            nome = input("Digite o nome do produto: ")
            quantidade = int(input("Digite a quantidade do produto: "))
            preco = float(input("Digite o preço do produto: R$ "))
            criar_produto(nome, quantidade, preco)
        
        elif escolha == '2':
            listar_produtos()
        
        elif escolha == '3':
            id_produto = int(input("Digite o ID do produto a ser atualizado: "))
            quantidade = int(input("Digite a nova quantidade do produto: "))
            preco = float(input("Digite o novo preço do produto: R$ "))
            atualizar_produto(id_produto, quantidade, preco)
        
        elif escolha == '4':
            id_produto = int(input("Digite o ID do produto a ser deletado: "))
            deletar_produto(id_produto)
        
        elif escolha == '5':
            print("Saindo do programa...")
            break
        
        else:
            print("Opção inválida, tente novamente.")

# Função principal para executar o programa
def main():
    criar_banco()
    menu()

if __name__ == '__main__':
    main()