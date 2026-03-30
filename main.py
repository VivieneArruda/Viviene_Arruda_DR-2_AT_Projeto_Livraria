import requests
from bs4 import BeautifulSoup
import csv
import sys


def obter_html(url):
    resposta = requests.get(url)
    if resposta.status_code != 200:
        print(f"Erro ao acessar o site. Status code: {resposta.status_code}")
        sys.exit()
    resposta.encoding = "utf-8"
    print("Conexão bem-sucedida!")
    return resposta.text


def extrair_dados(html):
    soup = BeautifulSoup(html, "html.parser")
    print(soup.title.string)

    livros_html = soup.find_all("article", class_="product_pod")
    print(len(livros_html))

    dados = []
    for livro in livros_html:
        titulo = livro.find("h3").find("a")["title"]
        preco = livro.find("p", class_="price_color").text
        dados.append({
            "titulo": titulo,
            "preco": preco
        })

    print(dados)
    return dados


def salvar_csv(dados):
    with open("relatorio_livros.csv", "w", newline="", encoding="utf-8-sig") as arquivo:
        campos = ["titulo", "preco"]
        writer = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
        writer.writeheader()
        writer.writerows(dados)

    print("Relatório CSV gerado com sucesso!")


def main():
    url = "http://books.toscrape.com/"
    html = obter_html(url)
    dados = extrair_dados(html)
    salvar_csv(dados)


if __name__ == "__main__":
    main()
