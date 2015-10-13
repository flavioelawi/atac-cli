try:
  # Python 2 import
  from xmlrpclib import Server
except ImportError:
  # Python 3 import
  from xmlrpc.client import Server

from colorama import Fore,init
init()

class ataccli:

	def __init__(self):
		####### INSERT DEV KEY HERE ################
		DEV_KEY = ''
		####### INSERT DEV KEY HERE ################
		s1 = Server('http://muovi.roma.it/ws/xml/autenticazione/1')
		self.s2 = Server('http://muovi.roma.it/ws/xml/paline/7')
		self.token = s1.autenticazione.Accedi(DEV_KEY, '')

	def getInfoLinea(self,linea):

		res = self.s2.paline.Percorsi(self.token, linea, 'it')
		#print(type(res))
		percorso=[]
		i=0
		while i < len(res.get('risposta').get('percorsi')):
			perc = res.get('risposta').get('percorsi')[i].get('id_percorso')
			capolinea = res.get('risposta').get('percorsi')[i].get('capolinea')
			percorso.append((perc, capolinea))
			#print("Percorso %s: " + percorso + " Capolinea: %s") % (i, capolinea)
			i=i+1

		return percorso

	def getPercorso(self,linea):
		percorso=self.getInfoLinea(linea)

		for i in percorso:
			res = self.s2.paline.Percorso(self.token, i[0], '', '', '')
			print(Fore.YELLOW + "Linea Bus %s capolinea %s" + Fore.RESET) % (linea, i[1])
			p = 0
			while p < len(res.get('risposta').get('fermate')):
				palina = res.get('risposta').get('fermate')[p].get('id_palina')
				nome = res.get('risposta').get('fermate')[p].get('nome_ricapitalizzato')
				try:
					veicolo = res.get('risposta').get('fermate')[p].get('veicolo')

				except:
					pass
				if veicolo:
					print (Fore.RED + "%s: %s <-----" + Fore.RESET) % (palina,nome)
				else:

					print (Fore.CYAN + "%s: " + Fore.RESET + "%s") % (palina,nome)

				p=p+1

if __name__ == '__main__':
	# parse arguments
	import argparse
	parser = argparse.ArgumentParser(description = "CLI muovi.roma.it")

	subparsers = parser.add_subparsers()

	parser_find = subparsers.add_parser('linea', help="Informazioni sulla linea")
	parser_find.add_argument("linea",type=str, help="Numero della linea da cercare")
	parser_find.set_defaults(which='linea')

	args = parser.parse_args()

	if args.which is 'linea':
		atac = ataccli()
		atac.getPercorso(args.linea)
