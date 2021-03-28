
import base64
import json
import re
from datetime import datetime
from urllib.parse import urlparse, urljoin

import feedparser
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
  host="167.86.120.98",
  port="3307",
  database="test_portales",
  user="eze_ellena",
  password="c3hdyX8Jvnua5ZBr"
)
mugre = ["rdquo;","&amp;","&gt",".ar",".com",";>>",";>","<br","&quot;","xmlns=http://www.w3.org/1999/>","<\n", "\n>","<<p>","<p>","</p","xmlns=http://www.w3.org/1999/>","xmlns=http://www.w3.org/1999/>","<br />","CDATA", "</div>>", "<div>", "</div>","%>", "<iframe>", "</iframe>", "100%", "<div", "http://w3.org/","xmlms","xhtml", ";>","]",'"',"'"]

def limpiar(texto, mugre):
    for m in mugre:
        texto = texto.replace(m,"")
    return texto
def obtenerTituloRss(item):

    try:
        Titulo = item["title"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
def obtenerDescripcionRss(item):

    try:
        Descripcion = limpiar(re.sub("<.*?>", "", item["summary"]), mugre)
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripcion ", e)
    try:
        Descripcion = limpiar(re.sub("<.*?>", "", item["content"][0].value), mugre)
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripcion ", e)
def obtenerImagenRss(link):
    response = requests.get(link, headers=headers).text
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"name":"twitter:image"})["content"]
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"property":"og:image"})["content"]
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
def obtenerFechaPublicacionRss(item):
    try:
        FechaPublicacion = item["published"]
        return FechaPublicacion
    except Exception as e:
        print("No se pudo obtener la FechaPublicacion ", e)
    try:
        FechaPublicacion = item["updated"]
        return FechaPublicacion
    except Exception as e:
        print("No se pudo obtener la FechaPublicacion ", e)
    try:
        FechaPublicacion = item["pubDate"]
        return FechaPublicacion
    except Exception as e:
        print("No se pudo obtener la FechaPublicacion ", e)
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
def obtenerTextoCompleto(response):

    try:
        TextoCompleto = BeautifulSoup(response, "html.parser").find("div", {"class": "fullpost__cuerpo"})
        TextoCompleto = str(TextoCompleto.contents)
        TextoCompleto = re.sub('</p>.*?<p>', ' ', TextoCompleto)

        TextoCompleto = TextoCompleto.replace("]", "").replace("[", "").replace(", '\n',", ' ')
        #TextoCompleto = "<br />".join(TextoCompleto.split("\n"))
        return TextoCompleto
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)

def obtenerFechaPublicacion(response):

    try:
        FechaPublicacion = BeautifulSoup(response, "html.parser").find("meta", {"property": "og:updated_time"})["content"]
        return FechaPublicacion
    except Exception as e:
        print("No se pudo obtener la FechaPublicacion ", e)
    try:
        FechaPublicacion = BeautifulSoup(response, "html.parser").find("meta", {"property": "article:published_time"})["content"]
        return FechaPublicacion
    except Exception as e:
        print("No se pudo obtener la FechaPublicacion ", e)
    try:
        FechaPublicacion = BeautifulSoup(response, "html.parser").find("p", {"data-v-da468678 style": "margin-top: 16px;"}).text
        return FechaPublicacion
    except Exception as e:
        print("No se pudo obtener la FechaPublicacion ", e)
def obtenerCategoria(response):
    try:
        Categoria = BeautifulSoup(response, "html.parser").find("span", {"data-v-da468678 class": "seccion"}).text
        return Categoria
    except Exception as e:
        print("No se pudo obtener la Categoria ", e)
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



def obtenerDatosParaRss(portal):
    try:
        response = feedparser.parse(portal)
        if response:
            for item in response["items"]:
                link = item["link"]
                try:
                    mycursor = conn.cursor()
                    innoticia = "SELECT * FROM noticias_enviadas_wordpress where link = '" + link + "'"
                    mycursor.execute(innoticia)
                    innoticia = mycursor.fetchall()
                except Exception as e:
                    print("")
                cantidad = len(innoticia)
                if cantidad != 0:
                    print("ya se encuentra en la base")
                else:
                    try:
                        Titulo = obtenerTituloRss(item)
                    except Exception as e:
                        print("No se pudo obtener el Título ", e)
                    try:
                        Descripcion = obtenerDescripcionRss(item)
                    except Exception as e:
                        print("No se pudo obtener la Descripcion ", e)
                    try:
                        Imagen = obtenerImagenRss(link)
                    except Exception as e:
                        print("No se pudo obtener la Imagen ", e)
                        Imagen = ""
                    try:
                        TextoCompleto = obtenerTextoCompleto(link)
                    except Exception as e:
                        print("No se pudo obtener la Imagen ", e)
                    try:
                        FechaPublicacion = obtenerFechaPublicacion(response)
                    except Exception as e:
                        print("No se pudo obtener la FechaPublicacion ", e)
                        FechaPublicacion = datetime.today()
                    try:
                        Categoria = obtenerCategoria(response)
                    except Exception as e:
                        print("No se pudo obtener la Categoria ", e)
                        Categoria = "Actualidad"

                    if not Titulo or not Descripcion or not TextoCompleto:
                        continue
                    else:
                        try:
                            user = 'admin'
                            pythonapp = 'gg36 HrXA owXn XdzS rXZ2 shko'
                            url = 'http://aguacerodigital.com/wp-json/wp/v2'
                            data_string = user + ':' + pythonapp
                            token = base64.b64encode(data_string.encode())
                            headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
                            imgsrc = Imagen
                            post = {'date': str(datetime.today()),
                                    'title': Titulo,
                                    'slug': 'rest-api-1',
                                    'status': 'publish',
                                    'content': Descripcion + ' <img src=' + imgsrc + '> ' + TextoCompleto,
                                    'author': '1',
                                    'excerpt': 'Exceptional post!',
                                    'format': 'standard',
                                    'post_tag': ['Actualidad'],
                                    'category': Categoria
                                    }
                            r = requests.post(url + '/posts', headers=headers, json=post)

                            print('Your post is published on ' + json.loads(r.content.decode('utf-8'))['link'])
                            try:
                                mycursor = conn.cursor()
                                sql = "INSERT INTO noticias_enviadas_wordpress (link, titulo, descripcion,tema,campaña,nombreWordPress) VALUES (%s, %s, %s, %s, %s, %s)"
                                val = (link, Titulo, Descripcion, "", "", url)
                                mycursor.execute(sql, val)
                                Portales = mycursor.fetchall()
                            except Exception as e:
                                print("Error al Obtener portales ", e)
                        except Exception as e:
                            print("Error al Obtener portales ", e)

    except Exception as e:
        print("Error al ejecutar la consulta")

if __name__ == "__main__":
    try:
        while True:
#"http://www.sanjavierenreflejos.com.ar/?feed=rss2",
#"http://www.sanjustonoticias.com.ar/",
#"https://www.sanjustoylaweb.com.ar/",
            Portales = [


                "https://sanjustoadiario.com/"
            ]
            for link in Portales:
                if "feed" in link:
                    obtenerDatosParaRss(link)
                else:
                    try:

                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                                          'Firefox/55.0'}
                        links = get_all_website_links(link)
                        links = list(links)
                        for link in links:
                            try:
                                mycursor = conn.cursor()
                                innoticia = "SELECT * FROM noticias_enviadas_wordpress where link = '" + link + "'"
                                mycursor.execute(innoticia)
                                innoticia = mycursor.fetchall()
                            except Exception as e:
                                print("")
                            cantidad = len(innoticia)
                            if cantidad != 0:
                                print("ya se publico")
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
                                TextoCompleto = obtenerTextoCompleto(response)
                            except Exception as e:
                                print("No se pudo obtener el TextoCompleto ", e)
                            try:
                                FechaPublicacion = obtenerFechaPublicacion(response)
                            except Exception as e:
                                print("No se pudo obtener la FechaPublicacion ", e)
                            try:
                                Categoria = obtenerCategoria(response)
                                if Categoria is None:
                                    Categoria = "Actualidad"
                            except Exception as e:
                                print("No se pudo obtener la Categoria ", e)
                                Categoria = "Actualidad"

                            if not Titulo or not Descripcion or not Imagen or not TextoCompleto or not Categoria or not FechaPublicacion:
                                continue
                            else:
                                try:
                                    user = 'admin'
                                    pythonapp = 'gg36 HrXA owXn XdzS rXZ2 shko'
                                    url = 'http://aguacerodigital.com//wp-json/wp/v2'
                                    data_string = user + ':' + pythonapp
                                    token = base64.b64encode(data_string.encode())
                                    headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
                                    imgsrc = Imagen
                                    post = {'date': str(datetime.today()),
                                            'title': Titulo,
                                            'slug': 'rest-api-1',
                                            'status': 'publish',
                                            'content': Descripcion + ' <img src='+ imgsrc + '> ' + TextoCompleto,
                                            'author': '1',
                                            'excerpt': 'Exceptional post!',
                                            'format': 'standard',
                                            'post_tag': ['Actualidad'],
                                            'category': Categoria
                                            }
                                    r = requests.post(url + '/posts', headers=headers, json=post)

                                    print('Your post is published on ' + json.loads(r.content.decode('utf-8'))['link'])
                                    try:
                                        mycursor = conn.cursor()
                                        sql = "INSERT INTO noticias_enviadas_wordpress (link, titulo, descripcion,tema,campaña,nombreWordPress) VALUES (%s, %s, %s, %s, %s, %s)"
                                        val = (link, Titulo,Descripcion,"","",url)
                                        mycursor.execute(sql, val)
                                        Portales = mycursor.fetchall()
                                    except Exception as e:
                                        print("Error al Obtener portales ", e)
                                except Exception as e:
                                    print("Error al Obtener portales ", e)
                    except Exception as e:
                        print("Error al Obtener portales ", e)
    except Exception as e:
        print("Error al Obtener portales ", e)