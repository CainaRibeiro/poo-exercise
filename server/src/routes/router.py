from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler
import json
import pandas as pd

caminho_excel = r"E:\Faculdade\terceiro_periodo\POO\poo-exercise\server\db.xlsx"


class Fornecedores:
    def __init__(self):
        self.excel = pd.read_excel(caminho_excel)
        self.excel = self.excel.rename(columns={'Unnamed: 0': 'index'})


class Acoes(Fornecedores):
    def __init__(self):
        super().__init__()

    def adicionar_fornecedor(self, nome, preco_km, email, estado, telefone, avaliacao=None):
        try:
            if nome.lower() in self.excel['Nome'].values:
                raise ValueError(f'O fornecedor {nome} já está cadastrado.')

            new_row = pd.DataFrame(
                {'id': [len(self.excel)],
                 'Nome': [nome.lower()],
                 'Preco_km': [preco_km],
                 'Email': [email],
                 'Avaliacao': [0],
                 'Estado': [estado],
                 'Telefone': [telefone]})
            self.excel = pd.concat([self.excel, new_row], ignore_index=True)
            self.excel.to_excel(caminho_excel, index=False)
        except ValueError as err:
            print(f"Error: {err}")

    def remover_fornecedor(self, nome):
        if nome.lower() in self.excel['Nome'].values:
            self.excel = self.excel[self.excel['Nome'] != nome]
            print(f'O fornecedor {nome} foi removido com sucesso.')
        else:
            print(f'O fornecedor {nome} não está cadastrado.')
            raise ValueError('Fornecedor não cadastrado')

    def aplicar_avaliacao(self, nome, avaliacao):
        if nome.lower() in self.excel['Nome'].values:
            self.excel.loc[self.excel['Nome'] == nome, 'Avaliacao'] = avaliacao
            print(f'Avaliacao {avaliacao} aplicada ao fornecedor {nome}.')
        else:
            print(f'O fornecedor {nome} não está cadastrado.')
            raise ValueError('Fornecedor não cadastrado')

    def pesquisa_fornecedores(self):
        return self.excel

    def pesquisa_fornecedor(self, nome=None, estado=None):
        if nome or estado:
            conditions = []
            if nome:
                conditions.append(self.excel['Nome'] == nome)
            if estado:
                conditions.append(self.excel['Estado'] == estado)

            combined_condition = pd.Series(True, index=self.excel.index)
            for condition in conditions:
                combined_condition &= condition

            result = self.excel[combined_condition]

            if result.empty:
                print('Nenhum fornecedor encontrado com os critérios fornecidos.')
                raise ValueError('Fornecedor não encontrado')
            return result
        else:
            print('Pelo menos um parâmetro de pesquisa deve ser fornecido.')
            raise ValueError('Parâmetros de pesquisa ausentes')

    def calcula_frete(self, nome, distancia):
        preco_km = self.excel.loc[self.excel['Nome'] == nome.lower(), 'Preco_km'].iloc[0]
        return f'{distancia * preco_km}'


class RequestHandler(BaseHTTPRequestHandler):
    acao = Acoes()

    def do_POST(self):
        url = urlparse(self.path)
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')

        match url.path:
            case '/api/v1/add_fornecedor':
                try:
                    data = json.loads(body)
                    if data["nome"].lower() in self.acao.excel['Nome'].str.lower().values:
                        raise ValueError(f'O fornecedor {data["nome"]} já está cadastrado.')
                    if data["nome"] in self.acao.excel['Nome'].values:
                        raise ValueError(f'O fornecedor {data["nome"]} já está cadastrado.')
                    self.acao.adicionar_fornecedor(nome=data["nome"],
                                                   estado=data["estado"],
                                                   preco_km=data["preco_km"],
                                                   email=data["email"],
                                                   telefone=data["telefone"])

                    response = f'Dados recebidos: {data["nome"]}'
                    self.send_response(201)
                except ValueError as error:
                    response = f'Error: {error}'
                    self.send_response(404)

            case '/api/v1/add_avaliacao':
                try:
                    data = json.loads(body)
                    if not data["nome"] or not data["avaliacao"]:
                        raise ValueError("Faltando dado(s) obrigatório(s)")
                    self.acao.aplicar_avaliacao(nome=data["nome"], avaliacao=data["avaliacao"])
                    response = f'Avaliacao adicionada {data["nome"]}: {data["avaliacao"]}'
                except ValueError as error:
                    response = f'Error: {error}'
                    self.send_response(404)

            case '/api/v1/remover_fornecedor':
                try:
                    data = json.loads(body)
                    if not data["nome"]:
                        raise ValueError("Campo nome é obrigatório para remoção de fornecedor")
                    self.acao.remover_fornecedor(nome=data["nome"])
                    response = f'Fornecedor removido: {data["nome"]}'
                except ValueError as error:
                    response = f'Error: {error}'
                    self.send_response(404)

            case '/api/v1/fornecedor':
                try:
                    data = json.loads(body)
                    response = f'{self.acao.pesquisa_fornecedor(nome=data["nome"], estado=data["estado"])}'
                except ValueError as error:
                    response = f'Error: {error}'
                    self.send_response(404)

            case '/api/v1/calcula-frete':
                try:
                    data = json.loads(body)
                    if not data["nome"] or not data["distancia"]:
                        raise ValueError("Dados faltando")
                    response = f'{self.acao.calcula_frete(nome=data["nome"], distancia=data["distancia"])}'
                except ValueError as error:
                    response = f'Error: {error}'
                    self.send_response(404)
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
                    fornecedores_df = self.acao.pesquisa_fornecedores()
                    if fornecedores_df.empty:
                        raise ValueError('Excel vazio')
                    fornecedores_list = fornecedores_df.to_dict(orient='records')
                    response = json.dumps(fornecedores_list)
                except Exception as error:
                    print(error)
                    response = f'Error: {error}'
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
