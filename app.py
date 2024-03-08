from flask import Flask
from flask import render_template
import json
import requests
import threading
from credentials import *

app = Flask(__name__)
global old_data

svgs = {
	"torrent": """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Calque_1" x="0px" y="0px" viewBox="0 0 344.1 431" style="enable-background:new 0 0 344.1 431;fill: #fff" xml:space="preserve" class="coalition-flag--icon">
					<style type="text/css">
						.st0{fill-rule:evenodd;clip-rule:evenodd;}
					</style>
					<g>
						<path class="st0" d="M13,335.9L13,335.9l226.4,0c52.1,0,94.3-42.2,94.3-94.3v0H107.3C55.2,241.6,13,283.8,13,335.9z"></path>
						<path class="st0" d="M185.5,357.8H88.2v0c0,40.4,32.8,73.2,73.2,73.2h97.3v0C258.6,390.6,225.9,357.8,185.5,357.8z"></path>
						<path class="st0" d="M257.5,132.8c-42.6,0-78,30.7-85.4,71.1c-7.4-40.5-42.8-71.1-85.4-71.1H0v0c0,48,38.9,86.8,86.8,86.8h83.8h2.8   h83.8c48,0,86.8-38.9,86.8-86.8v0H257.5z"></path>
						<path class="st0" d="M173.5,145.2l40.5-40.5c17.7-17.7,17.7-46.4,0-64.2L173.5,0L133,40.5c-17.7,17.7-17.7,46.4,0,64.2L173.5,145.2   z"></path>
					</g>
				</svg>""",
	"armada": """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Calque_1" x="0px" y="0px" viewBox="0 0 503.3 436.6" style="enable-background:new 0 0 503.3 436.6;fill: #fff" xml:space="preserve" class="coalition-flag--icon">
					<g>
						<path d="M248.1,22.4L248.1,22.4L230.1,0l-61.6,77.4c-18.6,23.3-18.6,56.4,0,79.7l12.3,15.5l49.3-62l169.5,213l9.8,12.4   c22,27.7,62.3,32.2,89.9,10.2l3.9-3.1L248.1,22.4z"></path>
						<path d="M25.5,431.6v5h345.9c35.3,0,64-28.7,64-64v-5H89.5C54.2,367.6,25.5,396.3,25.5,431.6z"></path>
						<path d="M26.4,366.6l49.1-61.8l0.2,0.2l37.9-47.7l3.1-3.9l49.3,62c0.5,0.6,1.1,1.3,1.6,1.9c22.3,25.9,61.3,29.8,88.3,8.3l3.9-3.1   l-2.5-3.1l-10-12.6l-12.8-16.1L160.7,198l-43.9-55.2l-6,7.5l-35.1,44.1l0,0l-0.2-0.2l-61.6,77.4c-1.2,1.5-2.3,3.1-3.4,4.7   c-14.1,21.4-14,49.1,0.1,70.5c1,1.6,2.2,3.1,3.3,4.6l12.3,15.5L26.4,366.6z"></path>
					</g>
				</svg>""",
	"la_légion": """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Calque_1" x="0px" y="0px" viewBox="0 0 417.6 421.6" style="enable-background:new 0 0 417.6 421.6;fill: #fff" xml:space="preserve" class="coalition-flag--icon mx-auto">
					<path d="M259.8,271.5c0-43-35-77.9-77.9-77.9h-3.7V340h-70.4v81.6h3.7c18.3,0,36-6.6,49.8-18.6c10-8.6,17.5-19.7,21.8-31.9  c11.2,30,39.9,50.5,73,50.5h77.8V340h-74L259.8,271.5L259.8,271.5z"></path>
					<g>
						<path d="M166.3,186.7c-10.7-10.7-26.9-14.4-45.5-10.4c-17.4,3.8-35.1,14-49.9,28.7c-14.8,14.8-25,32.5-28.7,49.9   c-4,18.6-0.3,34.7,10.4,45.5l5.3,5.3L171.6,192L166.3,186.7z"></path>
						<path d="M335.4,205.1c-14.8-14.8-32.5-25-49.9-28.7c-18.6-4-34.7-0.3-45.5,10.4l-5.3,5.3l113.7,113.6l5.3-5.3   c10.7-10.7,14.4-26.9,10.4-45.5C360.4,237.6,350.2,219.8,335.4,205.1z"></path>
					</g>
					<g>
						<path d="M227.1,131L340.7,17.3l-5.3-5.3C324.7,1.3,308.5-2.4,289.9,1.6c-17.4,3.8-35.1,14-49.9,28.7c-14.8,14.8-25,32.5-28.7,49.9   c-4,18.6-0.3,34.7,10.4,45.5L227.1,131z"></path>
						<path d="M184.7,125.7c10.7-10.7,14.4-26.9,10.4-45.5c-3.8-17.4-14-35.1-28.7-49.9c-14.8-14.8-32.5-25-49.9-28.7   C97.9-2.4,81.7,1.3,71,12l-5.3,5.3L179.4,131L184.7,125.7z"></path>
					</g>
					<g>
						<path d="M392.9,115c-15-9.6-34.7-15-55.6-15s-40.6,5.3-55.6,15c-16,10.3-24.8,24.3-24.8,39.5v7.5h160.7v-7.5   C417.6,139.4,408.8,125.3,392.9,115z"></path>
						<path d="M160.7,154.5c0-15.2-8.8-29.2-24.8-39.5c-15-9.6-34.7-15-55.6-15s-40.6,5.3-55.6,15C8.8,125.2,0,139.3,0,154.5v7.5h160.7   V154.5z"></path>
					</g>
				</svg>""",
}


def get_token():
	auth_server_url = "https://api.intra.42.fr/oauth/token"
	token_req_payload = {
		"grant_type": "client_credentials",
		"client_secret" : secret,
		"client_id" : uid,
	}
	token_response = requests.post(auth_server_url,
	data=token_req_payload, verify=False, allow_redirects=False)
	return json.loads(token_response.text)


# "users" : [
# 					{
# 						"avatar" : "https://cdn.intra.42.fr/users/120fd9a78cad62db47d3c39c42ae8c20/vst-pier.jpg",
# 						"username" : "vst-pier",
# 						"name" : "Valerie St-Pierre",
# 						"score" : "105",
# 						"position" : "1",
# 					},
# 					{
# 						"avatar" : "https://cdn.intra.42.fr/users/120fd9a78cad62db47d3c39c42ae8c20/vst-pier.jpg",
# 						"username" : "vst-pier 2",
# 						"name" : "Valerie St-Pierre 2",
# 						"score" : "92",
# 						"position" : "2",
# 					},
# 					{
# 						"avatar" : "https://cdn.intra.42.fr/users/120fd9a78cad62db47d3c39c42ae8c20/vst-pier.jpg",
# 						"username" : "vst-pier 3",
# 						"name" : "Valerie St-Pierre 3",
# 						"score" : "35",
# 						"position" : "3",
# 					}
# 				],

#242 Torrent
#243 Legion
#249 L'Armada

def get_users(token):
	user_data = {
		"armada": {
			"id": 249,
			"users": []
		},

		"la_légion": {
			"id": 243,
			"users": []
		},

		"torrent": {
			"id": 242,
			"users": []
		},
	}

	for coalition in user_data:
		api_call_headers = {'Authorization': 'Bearer ' + token['access_token']}
		api_call_response = json.loads(requests.get("https://api.intra.42.fr/v2/coalitions/" + str(user_data[coalition]['id']) + "/coalitions_users?page[size]=3&sort[this_year_score]", headers=api_call_headers, verify=False).text)
		for user in api_call_response:
			api_call_response_login = json.loads(requests.get("https://api.intra.42.fr/v2/users/" + str(user['user_id']), headers=api_call_headers, verify=False).text)
			user_data[coalition]["users"].append(
				{
					'id': user['user_id'],
					'score': user['score'],
					'position': user['rank'],
					'name': api_call_response_login['usual_full_name'],
					'username': api_call_response_login['login'],
					'avatar': api_call_response_login['image']['link']
				}
			)
	return (user_data)

def get_coalition_data():
	token = get_token()
	user_data = get_users(token)
	api_call_headers = {'Authorization': 'Bearer ' + token['access_token']}
	api_call_response = requests.get("https://api.intra.42.fr/v2/blocs/70", headers=api_call_headers, verify=False)
	coalition_data: list = json.loads(api_call_response.text)['coalitions']
	coalition_data.sort(key=lambda k: k["score"])

	coalitions_data = []
	position = 3
	score_total = 0
	score_max = 0
	score_min = 10000000

	for coalition in coalition_data:
		score_total += coalition['score']
		if (score_max < coalition['score']):
			score_max = coalition['score']
		if (score_min > coalition['score']):
			score_min = coalition['score']

	for coalition in coalition_data:
		data = {
			"name": None,
			"display_name": None,
			"svg": None,
			"position": 1,
			"heigth": "60%",
			"score": None,
			"users": user_data[str.lower(coalition['slug'])]['users']
		}
		data['name'] = str.lower(coalition['slug'])
		data['svg'] = svgs[str.lower(coalition['slug'])]
		data['display_name'] = coalition['name']
		data['score'] = coalition['score']
		data['position'] = position
		position -= 1
		data['height'] = str(70 + ((coalition['score'] - score_min) / (score_max - score_min) * 10)) + "%"

		if (position == 2):
			coalitions_data.insert(2, data)
		elif (position == 1):
			coalitions_data.insert(0, data)
		elif (position == 0):
			coalitions_data.insert(1, data)

	global old_data
	old_data = coalitions_data
	return (coalitions_data)

get_coalition_data()

@app.route("/")
def	get():
	threading.Thread(target=get_coalition_data)
	return render_template('index.jinja', data={
		"coalitions": old_data,
	})

app.run(host="0.0.0.0", port=80)