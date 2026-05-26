extends Control

@onready var questions_list = $VBoxContainer/ScrollContainer/QuestionsList
@onready var status_label = $VBoxContainer/StatusLabel
@onready var form_panel = $FormPopup
@onready var enunciado_input = $FormPopup/VBoxContainer/EnunciadoInput
@onready var a_input = $FormPopup/VBoxContainer/AInput
@onready var b_input = $FormPopup/VBoxContainer/BInput
@onready var c_input = $FormPopup/VBoxContainer/CInput
@onready var d_input = $FormPopup/VBoxContainer/DInput
@onready var resposta_select = $FormPopup/VBoxContainer/RespostaSelect

const ITEM_SCENE = preload("res://scenes/PerguntaItem.tscn")

var cadeira_id: int = -1
var editing_id: int = -1

func _ready():
	form_panel.visible = false
	buscar_cadeira_professor()

func buscar_cadeira_professor():
	status_label.text = "Carregando dados da cadeira..."

	HTTPManager.send_request("/cadeiras", HTTPClient.METHOD_GET)
	var response = await HTTPManager.request_completed
	var response_code = response[1]
	var body = response[3]

	if response_code == 200:
		for c in body:
			if c.professor_id == AuthManager.user_profile.id:
				cadeira_id = c.id
				carregar_perguntas()
				return
		status_label.text = "Erro: Você não está associado a nenhuma cadeira."
	else:
		status_label.text = "Erro ao buscar cadeiras."

func carregar_perguntas():
	status_label.text = "Carregando perguntas..."
	for child in questions_list.get_children():
		child.queue_free()

	HTTPManager.send_request("/cadeiras/" + str(cadeira_id) + "/perguntas", HTTPClient.METHOD_GET)
	var response = await HTTPManager.request_completed
	var response_code = response[1]
	var body = response[3]

	if response_code == 200:
		status_label.text = "Perguntas carregadas."
		for p in body:
			var item = ITEM_SCENE.instantiate()
			questions_list.add_child(item)
			item.setup(p)
			item.edit_requested.connect(_on_edit_pergunta)
			item.delete_requested.connect(_on_delete_pergunta)
	else:
		status_label.text = "Erro ao carregar perguntas."

func _on_nova_pergunta_pressed():
	editing_id = -1
	enunciado_input.text = ""
	a_input.text = ""
	b_input.text = ""
	c_input.text = ""
	d_input.text = ""
	resposta_select.selected = 0
	form_panel.visible = true

func _on_edit_pergunta(data):
	editing_id = data.id
	enunciado_input.text = data.enunciado
	a_input.text = data.opcao_a
	b_input.text = data.opcao_b
	c_input.text = data.opcao_c
	d_input.text = data.opcao_d
	var mapping = {"a": 0, "b": 1, "c": 2, "d": 3}
	resposta_select.selected = mapping.get(data.resposta_correta, 0)
	form_panel.visible = true

func _on_save_button_pressed():
	var body = {
		"enunciado": enunciado_input.text,
		"opcao_a": a_input.text,
		"opcao_b": b_input.text,
		"opcao_c": c_input.text,
		"opcao_d": d_input.text,
		"resposta_correta": ["a", "b", "c", "d"][resposta_select.selected]
	}

	if editing_id == -1:
		HTTPManager.send_request("/cadeiras/" + str(cadeira_id) + "/perguntas", HTTPClient.METHOD_POST, body, AuthManager.auth_token)
	else:
		HTTPManager.send_request("/cadeiras/perguntas/" + str(editing_id), HTTPClient.METHOD_PUT, body, AuthManager.auth_token)

	var response = await HTTPManager.request_completed
	var response_code = response[1]
	var response_body = response[3]

	if response_code in [200, 201]:
		form_panel.visible = false
		carregar_perguntas()
	else:
		status_label.text = "Erro ao salvar: " + str(response_body.get("detail", ""))

func _on_delete_pergunta(id):
	HTTPManager.send_request("/cadeiras/perguntas/" + str(id), HTTPClient.METHOD_DELETE, {}, AuthManager.auth_token)
	await HTTPManager.request_completed
	carregar_perguntas()

func _on_voltar_button_pressed():
	SceneManager.change_scene("res://scenes/MenuPrincipal.tscn")

func _on_cancel_button_pressed():
	form_panel.visible = false