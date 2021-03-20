
import base64
import json
from datetime import datetime
from urllib.parse import urlparse, urljoin
import mysql.connector
import requests
import mysql.connector
from bs4 import BeautifulSoup

"""
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Server=localhost;'
                      'Database=ScraperNoticias;'
                      'Trusted_Connection=yes;')
"""
conn = mysql.connector.connect(
  host="10.3.0.125",
  port="3307",
  database="test_portales",
  user="eze_ellena",
  password="L9vMKWedYEzcBxdy"
)

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
def obtenerTitulo(response):
    Titulo = ""
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("meta", {"name": "twitter:title"})["content"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("meta", {"property": "og:title"})["content"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = \
        json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[0][
            "headline"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = \
        json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[
            "headline"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("p", {"data-v-da468678 class": 'titulo'})
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
def obtenerDescripcion(response):
    Descripcion = ""
    try:
        Descripcion = BeautifulSoup(response, "html.parser").find("meta", {"name": "twitter:description"})["content"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripción ", e)
    try:
        Descripcion = BeautifulSoup(response, "html.parser").find("meta", {"property": "og:description"})["content"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripción ", e)
    try:
        Descripcion = \
        json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[0][
            "description"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripción ", e)
    try:
        Descripcion = \
        json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[
            "description"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripción ", e)
    try:
        Descripcion = \
        BeautifulSoup(response, "html.parser").find("p", {"data-v-da468678 class": 'anticipo'})
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripción ", e)
def obtenerImagen(response):
    Imagen = ""
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"name": "twitter:image"})["content"]
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"property": "og:image"})["content"]
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("a", {"data-v-da468678 href": ""}).text
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
def obtenerTextoCompleto(response,link):
    try:
        TextoCompleto = BeautifulSoup(response, "html.parser").find("div", {"itemprop": "articleBody"})
        TextoCompleto = str(TextoCompleto.contents)
        TextoCompleto = TextoCompleto.replace("]"," ").replace(", ","").replace("[, ","")
        return TextoCompleto
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        TextoCompleto = BeautifulSoup(response, "html.parser").find("div", {"class": "entry-body"})
        TextoCompleto = str(TextoCompleto.contents)
        TextoCompleto = TextoCompleto.replace("'\\n'"," ").replace("]"," ").replace("[ , ","").replace(",  , "," ")
        return TextoCompleto
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        TextoCompleto = BeautifulSoup(response, "html.parser").find("div", {"id": "texto_tpl6"})
        TextoCompleto = str(TextoCompleto.contents)
        return TextoCompleto
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        TextoCompleto = BeautifulSoup(response, "html.parser").find("div", {"id": "cuerpo"})
        TextoCompleto = str(TextoCompleto.contents)
        return TextoCompleto
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        TextoCompleto = "Para seguir leyendo siga el siguiente Link "+ link +""
        return TextoCompleto
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)


def get_all_website_links(Portal):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()

    internal_urls = set()
    external_urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(Portal).netloc
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0', }
    soup = BeautifulSoup(requests.get(Portal, headers=headers).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(Portal, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            continue
        # print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return internal_urls

if __name__ == "__main__":
    try:
        while True:
            Portales = ["https://www.agritotal.com/","https://www.baenegocios.com/seccion/agroindustria/"]
            for link in Portales:
                try:

                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                                      'Firefox/55.0'}
                    links = get_all_website_links(link)
                    links = list(links)
                    for link in links:
                        response = requests.get(link, headers=headers).text
                        try:
                            Titulo = obtenerTitulo(response)
                        except Exception as e:
                            print("No se pudo obtener el Título ", e)
                        try:
                            Descripcion = obtenerDescripcion(response)
                        except Exception as e:
                            print("No se pudo obtener la Descripcion ", e)
                        try:
                            Imagen = obtenerImagen(response)
                        except Exception as e:
                            print("No se pudo obtener la Imagen ", e)
                        try:
                            TextoCompleto = obtenerTextoCompleto(response,link)
                        except Exception as e:
                            print("No se pudo obtener la Imagen ", e)

                        if not Titulo or not Descripcion or not Imagen or not TextoCompleto:
                            continue
                        else:
                            try:
                                user = 'alejandro.sartorio'
                                pythonapp = 'mkDo 3xVt PIEa eYPs Y7MB rHig'
                                url = 'https://somoscampoonline.com/wp-json/wp/v2'
                                data_string = user + ':' + pythonapp
                                token = base64.b64encode(data_string.encode())
                                headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
                                imgsrc = Imagen
                                post = {'date': str(datetime.today()),
                                        'title': Titulo,
                                        'slug': 'rest-api-1',
                                        'status': 'publish',
                                        'content': Descripcion + '\n\n<img src='+ imgsrc + '>\n' + TextoCompleto,
                                        'author': '1',
                                        'excerpt': 'Exceptional post!',
                                        'format': 'standard',
                                        'post_tag': 'Actualidad',
                                        'category': 'Actualidad'
                                        }
                                r = requests.post(url + '/posts', headers=headers, json=post)

                                print('Your post is published on ' + json.loads(r.content.decode('utf-8'))['link'])
                            except Exception as e:
                                print("Error al Obtener portales ", e)
                except Exception as e:
                    print("Error al Obtener portales ", e)
    except Exception as e:
        print("Error al Obtener portales ", e)