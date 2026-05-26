extends Control

@onready var resultado_label = $VBoxContainer/ResultadoLabel
@onready var sub_label = $VBoxContainer/SubLabel
@onready var status_label = $VBoxContainer/StatusLabel

func _ready():
	var acertos = GameManager.acertos
	var total = GameManager.current_questions.size()
	var tempo = GameManager.tempo_total

	resultado_label.text = "Você acertou %d de %d!" % [acertos, total]
	sub_label.text = "Tempo total: %d segundos" % tempo

	registrar_partida(acertos, total, tempo)

func registrar_partida(acertos, total, tempo):
	status_label.text = "Enviando resultado..."

	var body = {
		"cadeira_id": GameManager.selected_cadeira.id,
		"total_perguntas": total,
		"acertos": acertos,
		"tempo_segundos": tempo
	}

	HTTPManager.send_request("/partidas/", HTTPClient.METHOD_POST, body, AuthManager.auth_token)
	var response = await HTTPManager.request_completed
	var response_code = response[1]
	var response_body = response[3]

	if response_code == 201:
		status_label.text = "Partida registrada com sucesso!"
	else:
		status_label.text = "Erro ao registrar partida: " + str(response_body.get("detail", "Erro desconhecido"))

func _on_menu_button_pressed():
	SceneManager.change_scene("res://scenes/MenuPrincipal.tscn")

func _on_jogar_novamente_button_pressed():
	SceneManager.change_scene("res://scenes/SelecaoCadeira.tscn")