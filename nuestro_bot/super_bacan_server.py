# Author: Octavio Vera #

import flask
import requests
import json
from apiclient.discovery import build
global chat_id 
global google_label


app = flask.Flask(__name__)
chat_id = {}
google_label = {}

@app.route("/", methods=["POST"])
def new_issue():
	user = "materia2017bot"
	personal_acces_token = "51b63894f42f10172f314671a45fb9ae0b3d33e2"
	credentials = (user, personal_acces_token)	
	if flask.request.headers['content-Type'] == 'application/json':
		if "issue" in flask.request.json:
			if flask.request.json["action"] == "closed":
				issue_num = flask.request.json["issue"]["number"]
				if str(issue_num) in google_label:
					if flask.request.json["issue"]["comments"] == 1:
						data = ["Googleable"]
						url = ("https://api.github.com/repos/ofvera/Tarea7/issues/" 
						+ str(issue_num) + "/labels")
						req = requests.post(url, 
							auth=credentials, data=json.dumps(data))
			elif flask.request.json["action"] == "opened":
				# Datos para crear mensaje #
				author = flask.request.json["issue"]["user"]["login"]
				num = flask.request.json["issue"]["number"]
				title = flask.request.json["issue"]["title"]
				body = flask.request.json["issue"]["body"]
				link = flask.request.json["issue"]["html_url"]
				# Mensaje Telegram #
				template = ("[{}]\n\n[#{} - {}]".format(author, num, title)
					+"\n\n{}\n\n[Link: {}]".format(body, link))
				url = ("https://api.telegram.org/bot341332977:" 
					+ "AAGvoIaOfq4HKKqwUi1ZNn-get4LnBQxELA/sendMessage")
				header = {'content-Type': 'application/json'}
				for _id in chat_id:
					message = {"chat_id": chat_id[_id], "text" : template}
					req = requests.post(url, 
						data=json.dumps(message), headers=header)
				# Obtenemos posible busqueda #
				body = flask.request.json["issue"]["body"]
				sender = flask.request.json["sender"]["login"]
				issue_num = flask.request.json["issue"]["number"]
				pos_md = body.replace("```","`")
				text_markdowns = pos_md.split("`")
				counter = 0
				found = False
				search_line = ""
				for pos in reversed(text_markdowns):
					counter += 1
					if "Error" in pos and counter%2 == 0:
						lines = pos.split("\n")
						for line in lines:
							if "Error" in line:
								found = True
								search_line = line
								break
						if found:
							break
				# realize search (search_line)#
				final = None
				if search_line != "":
					## Here start alternative
					search_engine_id = "015022355891199662167:czpyeaacdhi"
					api_key = "AIzaSyBbJwjbYegr-hBEG8H55ffDpOmJ7y7Y2-c"
					service = build('customsearch', 'v1', developerKey=api_key)
					collection = service.cse()
					num_requests = 6
					for i in range(0, num_requests):
						start_val = 1 + (i * 10)
						request = collection.list(
							q="python " + search_line,
				        	num=10, #this is the maximum & default anyway
				        	start=start_val,
				        	cx=search_engine_id
				        	)
						response = request.execute()
						found = False
						for item in response["items"]:
							if "answer" in item["pagemap"]:
								search_url = item["link"]
								answers = item["pagemap"]["answer"]
								for answer in answers:
									respuesta = answer["text"]
									upvote = answer["upvotecount"]
									# requerimiento de buena respuesta #
									if int(upvote) > 20:
										final = respuesta
										found = True
										break		
							if found:
								break
						if found:
							break
				if final != None:
					# subimos a git el comentario #
					google_label[str(issue_num)] = False
					comentario = ("**Encontramos la siguiente respuesta:** \n" +
						"{}\n\n[Link: {}]".format(final, search_url))
					data = {"body": comentario}
					url = ("https://api.github.com/repos/ofvera/Tarea7/issues/" 
						+ str(issue_num) + "/comments")
					req = requests.post(url, 
						auth=credentials, data=json.dumps(data))
			return "OK"
	return "NOT APPLIED"


@app.route("/telegram/", methods=["POST"])
def comando_telegram():
	user = "ofvera"
	personal_acces_token = "51b63894f42f10172f314671a45fb9ae0b3d33e2"
	credentials = (user, personal_acces_token)	
	if "message" not in flask.request.json:
		return "NOT APPLIED"
	if flask.request.headers['content-Type'] == 'application/json':
		text = flask.request.json['message']['text'].split(" ")
		this_chat_id = flask.request.json['message']['chat']['id']
		#print(flask.request.json)
		user_telegram = flask.request.json['message']['from']['id']
		action = text[0]
		if action == "/get":
			## /get event
			try:
				issue_num = text[1].replace("#","")
				issue_num = int(issue_num)
				url = ("https://api.github.com/repos/ofvera/Tarea7/issues/" 
						+ str(issue_num))
				req = requests.get(url, auth=credentials)
				# CONFIRMAMOS QUE SE LOGRO #
				author = req.json()["user"]["login"]
				num = req.json()["number"]
				title = req.json()["title"]
				body = req.json()["body"]
				link = req.json()["html_url"]
				template = ("[{}]\n\n[#{} - {}]".format(author, num, title)
					+"\n\n{}\n\n[Link: {}]".format(body, link))
			except ValueError:
				issue_num = text[1]
				template = ("Issue Number Error: {} ".format(issue_num)
					+ "no se acepta como issue")
			except IndexError:
				template = ("Format Error: El comando debe ser"
					+ "</get #issue_num>")
			except KeyError:
				template = ("Issue Number Error: {} ".format(issue_num)
					+ "no existe en el repositorio")
			finally:
				url = ("https://api.telegram.org/bot341332977:" 
				+ "AAGvoIaOfq4HKKqwUi1ZNn-get4LnBQxELA/sendMessage")
				message = {"chat_id": this_chat_id, "text" : template}
				header = {'content-Type': 'application/json'}
				req = requests.post(url, 
					data=json.dumps(message), headers=header)

		elif action == "/post":
			## /post event
			try:
				issue_num = text[1].replace("#","")
				issue_num = int(issue_num)
				texto = text[2:]
				comentario = ""
				for palabra in texto:
					comentario += palabra + " "
				data = {"body": comentario}
				url = ("https://api.github.com/repos/ofvera/Tarea7/issues/" 
					+ str(issue_num) + "/comments")
				req = requests.post(url, 
					auth=credentials, data=json.dumps(data))
				# CONFIRMAMOS QUE SE LOGRO #
				template = ("Se posteo tu comentario en "
					+"el issue {} exitosamente!".format(issue_num))
			except ValueError:
				issue_num = text[1]
				template = ("Issue Number Error:" 
				+ " {} no se acepta como issue".format(issue_num))
			except IndexError:
				template = ("Format Error: El comando debe ser"
					+ " </post #issue_num *respuesta>")
			except KeyError:
				template = ("Issue Number Error: {} ".format(issue_num)
					+ "no existe en el repositorio")
			finally:	
				url = ("https://api.telegram.org/bot341332977:" 
				+ "AAGvoIaOfq4HKKqwUi1ZNn-get4LnBQxELA/sendMessage")
				message = {"chat_id": this_chat_id, "text" : template}
				header = {'content-Type': 'application/json'}
				req = requests.post(url, 
					data=json.dumps(message), headers=header)

		elif action == "/label":
			## /label event
			try:
				issue_num = text[1].replace("#","")
				issue_num = int(issue_num)
				label = ""
				for palabra in text[2:]:
					label += palabra + " "
				data = [label[:-1]]
				url = ("https://api.github.com/repos/ofvera/Tarea7/issues/" 
				+ str(issue_num) + "/labels")
				req = requests.post(url, 
					auth=credentials, data=json.dumps(data))
				# CONFIRMAMOS QUE SE LOGRO #
				template = ("Se agrego el label <" 
					+ "{}> al issue {} exitosamente!".format(label,issue_num))
			except ValueError:
				issue_num = text[1]
				template = ("Issue Number Error: " 
					+ "{} no se acepta como issue".format(issue_num))
			except IndexError:
				template = ("Format Error: El comando debe ser"
					+ " </label #issue_num *label>")
			except KeyError:
				template = ("Issue Number Error: {} ".format(issue_num)
					+ "no existe en el repositorio")
			finally:
				url = ("https://api.telegram.org/bot341332977:" 
				+ "AAGvoIaOfq4HKKqwUi1ZNn-get4LnBQxELA/sendMessage")
				message = {"chat_id": this_chat_id, "text" : template}
				header = {'content-Type': 'application/json'}
				req = requests.post(url, 
					data=json.dumps(message), headers=header)

		elif action == "/close":
			## /close event
			try:
				issue_num = text[1].replace("#","")
				issue_num = int(issue_num)
				data = {"state":"closed"}
				url = ("https://api.github.com/repos/ofvera/Tarea7/issues/" 
					+ str(issue_num))
				req = requests.patch(url, 
					auth=credentials, data=json.dumps(data))
				# CONFIRMAMOS QUE SE LOGRO #
				template = "Issue {} fue cerrado exitosamente!".format(issue_num)
			except ValueError:
				issue_num = text[1]
				template = ("Issue Number Error: " 
					+ "{} no se acepta como issue".format(issue_num))
			except IndexError:
				template = ("Format Error: El comando debe ser"
					+ " </close #issue_num>")
			except KeyError:
				template = ("Issue Number Error: {} ".format(issue_num)
					+ "no existe en el repositorio")
			finally:
				url = ("https://api.telegram.org/bot341332977:" 
				+ "AAGvoIaOfq4HKKqwUi1ZNn-get4LnBQxELA/sendMessage")
				message = {"chat_id": this_chat_id, "text" : template}
				header = {'content-Type': 'application/json'}
				req = requests.post(url, 
					data=json.dumps(message), headers=header)

		elif action == "/start":
			# si no tenemos el id lo agregamos
			chat_id[user_telegram] = this_chat_id
			template = "Bienvenido a Gitbot!"
			url = ("https://api.telegram.org/bot341332977:" 
				+ "AAGvoIaOfq4HKKqwUi1ZNn-get4LnBQxELA/sendMessage")
			message = {"chat_id": this_chat_id, "text" : template}
			header = {'content-Type': 'application/json'}
			req = requests.post(url, 
				data=json.dumps(message), headers=header)

		elif action == "/exitbot":
			#Agrege remover tu chat#
			del chat_id[user_telegram]
			template = "x.x Adios"
			url = ("https://api.telegram.org/bot341332977:" 
				+ "AAGvoIaOfq4HKKqwUi1ZNn-get4LnBQxELA/sendMessage")
			message = {"chat_id": this_chat_id, "text" : template}
			header = {'content-Type': 'application/json'}
			req = requests.post(url, 
				data=json.dumps(message), headers=header)

		else:
			template = "Comando Invalido"
			url = ("https://api.telegram.org/bot341332977:" 
				+ "AAGvoIaOfq4HKKqwUi1ZNn-get4LnBQxELA/sendMessage")
			message = {"chat_id": this_chat_id, "text" : template}
			header = {'content-Type': 'application/json'}
			req = requests.post(url, 
				data=json.dumps(message), headers=header)
		return "OK"
	return"NOT APPLIED"
