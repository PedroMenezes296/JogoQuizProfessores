extends Control

@onready var grid_container = $VBoxContainer/ScrollContainer/GridContainer
@onready var loading_label = $VBoxContainer/LoadingLabel

const CARD_SCENE = preload("res://scenes/CadeiraCard.tscn")

func _ready():
	loading_label.text = "Carregando cadeiras..."
	HTTPManager.send_request("/cadeiras/", HTTPClient.METHOD_GET)
	var response = await HTTPManager.request_completed
	var response_code = response[1]
	var body = response[3]

	loading_label.visible = false

	if response_code == 200:
		for cadeira in body:
			var card = CARD_SCENE.instantiate()
			grid_container.add_child(card)
			card.setup(cadeira)
			card.selected.connect(_on_cadeira_selected)
	else:
		loading_label.visible = true
		loading_label.text = "Erro ao carregar cadeiras."

func _on_cadeira_selected(cadeira_data):
	loading_label.visible = true
	loading_label.text = "Carregando perguntas..."

	HTTPManager.send_request("/cadeiras/" + str(cadeira_data.id) + "/perguntas", HTTPClient.METHOD_GET)
	var response = await HTTPManager.request_completed
	var response_code = response[1]
	var body = response[3]

	if response_code == 200:
		if body.size() > 0:
			GameManager.start_game(cadeira_data, body)
		else:
			loading_label.text = "Nenhuma pergunta cadastrada nesta cadeira ainda."
	else:
		loading_label.text = "Erro ao buscar perguntas."

func _on_voltar_button_pressed():
	SceneManager.change_scene("res://scenes/MenuPrincipal.tscn")
