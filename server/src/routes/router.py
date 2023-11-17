from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler
import json

import pandas as pd


class Fornecedores:
    def __init__(self):
        self.df = pd.read_excel(r"E:\Faculdade\terceiro_periodo\POO\poo-exercise\server\db.xlsx")

    def adicionar_fornecedor(self, nome, produto, servico, localidade, nota=None):
        try:
            if nome in self.df['Nome'].values:
                print(f'O fornecedor {nome} já está cadastrado.')
            else:
                new_row = [nome, produto, servico, nota, localidade]
                self.df.loc[len(self.df)] = new_row
                print(f'O fornecedor {nome} foi cadastrado com sucesso.')
                print(self.df)
        except ValueError as err:
            print(f"Error: {err}")

    def remover_fornecedor(self, nome):
        if nome in self.df['Nome'].values:
            self.df = self.df[self.df['Nome'] != nome]
            print(f'O fornecedor {nome} foi removido com sucesso.')
        else:
            print(f'O fornecedor {nome} não está cadastrado.')

    def aplicar_nota(self, nome, nota):
        if nome in self.df['Nome'].values:
            self.df.loc[self.df['Nome'] == nome, 'Nota'] = nota
            print(f'Nota {nota} aplicada ao fornecedor {nome}.')
        else:
            print(f'O fornecedor {nome} não está cadastrado.')

    def pesquisa_fornecedores(self, produto=None, servico=None, localidade=None):
        conditions = []
        if produto:
            conditions.append(self.df['Produto'] == produto)
        if servico:
            conditions.append(self.df['Servico'] == servico)
        if localidade:
            conditions.append(self.df['Localidade'] == localidade)

        if conditions:
            result = self.df[all(conditions)]
        else:
            result = self.df

        return result



class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        url = urlparse(self.path)
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')

        match url.path:
            case '/api/v1/add_fornecedor':
                data = json.loads(body)
                Fornecedores().adicionar_fornecedor(nome=data["nome"], localidade=data["localidade"], produto=data["produto"], servico=data["servico"])
                response = f'Dados recebidos: {data["nome"]}'
            case _:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('NOT FOUND'.encode('utf-8'))
                return

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def do_GET(self):
        url = urlparse(self.path)

        match url.path:
            case '/api/v1/fornecedores':
                try:
                    fornecedores_df = Fornecedores().pesquisa_fornecedores()
                    fornecedores_list = fornecedores_df.to_dict(orient='records')
                    response = json.dumps(fornecedores_list)
                    print(response)
                except Exception as Err:
                    print(Err)
                    response = Err
            case _:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('NOT FOUND'.encode('utf-8'))
                return

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
