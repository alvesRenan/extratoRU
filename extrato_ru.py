#!/usr/bin/python3

import sys
import requests

url = "https://si3.ufc.br/public/restauranteConsultarSaldo.do"
data = {
    "codigoCartao": sys.argv[1],
    "matriculaAtreladaCartao": sys.argv[2]
    }

r = requests.post(url, data=data)
html_response = r.text.split(">")

usuario, _ = html_response[97].split('<')
saldo, _ = html_response[103].split('<')

print("Usuário: {}\nCréditos: {}".format(usuario, saldo))