#!/usr/bin/python3

import sys

import requests
from bs4 import BeautifulSoup

user_data_url = 'https://si3.ufc.br/public/restauranteConsultarSaldo.do'
menu_url = 'http://www.ufc.br/restaurante/cardapio/1-restaurante-universitario-de-fortaleza'
data = {
  'codigoCartao': sys.argv[1],
  'matriculaAtreladaCartao': sys.argv[2]
}

def convert_to_dict(list_):
  """
    Converts a list into a dict, eg:
      ['a', 1, 'b', 2] -> {'a': 1, 'b': 2}

    Args:
      list_: a list to be converted
  """
  it = iter( list_ )
  
  return dict( zip(it,it) )

def print_user_credits(r):
  """
    Extracts the username and the amount of credits in the card

    Args:
      r: a requests.models.Response
  """
  
  raw_data = BeautifulSoup( r.text, 'html.parser' )
  raw_data.find( 'tbody' ).text

  user_info = raw_data.find( 'tbody' ).text.split('\n')
  
  # Removing empty strings from the list
  user_info = [ no_empty_str for no_empty_str in user_info if no_empty_str ]

  info_dict = convert_to_dict( user_info )

  print( "Usuário: {}\nCréditos: {}\n".format(
    info_dict.get( 'Nome:','Indisponível' ), info_dict.get( 'Créditos:','Indisponível' ) ))

def print_menu(r):
  """
    Get the menu of the day

    Args:
      r: a requests.models.Response
  """

  raw_data = BeautifulSoup( r.text, 'html.parser' )
  almoco = raw_data.find( class_='refeicao almoco' ).find_all( class_='desc' )
  jantar = raw_data.find( class_='refeicao jantar' ).find_all( class_='desc' )

  print( 'Cardápio:' )
  print( '  Almoço: ')
  for item in almoco:
    print( '   ', item.text )
      
  print( '  Jantar' )
  for item in jantar:
    print( '   ', item.text )

try:
  r = requests.post( user_data_url, data=data )
  print_user_credits( r )

except requests.exceptions.ConnectionError as e:
  print( e )
  print( 'Erro ao tentar obter a quantidade de créditos do usuário.' )

try:
  r = requests.get( menu_url )
  print_menu( r )

except requests.exceptions.ConnectionError:
  print( 'Erro ao tentar obter o cardápio do dia.' ) 
