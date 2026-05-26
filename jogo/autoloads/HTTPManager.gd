extends Node

# URL base da API (ajustar para localhost no desenvolvimento)
const BASE_URL = "http://localhost:8000"

signal request_completed(result, response_code, headers, body)

func send_request(endpoint: String, method: HTTPClient.Method = HTTPClient.METHOD_GET, body: Dictionary = {}, token: String = ""):
	var http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_request_completed.bind(http_request))
	
	var headers = ["Content-Type: application/json"]
	if token != "":
		headers.append("Authorization: Bearer " + token)
	
	var query = JSON.stringify(body) if method != HTTPClient.METHOD_GET else ""
	var url = BASE_URL + endpoint
	
	var err = http_request.request(url, headers, method, query)
	if err != OK:
		push_error("Erro ao iniciar requisição HTTP: " + str(err))
		return err
	
	return OK

func _on_request_completed(result, response_code, headers, body, http_request):
	var response_body = {}
	if body.size() > 0:
		var json = JSON.new()
		var parse_err = json.parse(body.get_string_from_utf8())
		if parse_err == OK:
			response_body = json.get_data()
	
	request_completed.emit(result, response_code, headers, response_body)
	http_request.queue_free()
