extends Control

@onready var user_list = $VBoxContainer/ScrollContainer/UserList
@onready var status_label = $VBoxContainer/StatusLabel

# Popups
@onready var role_popup = $RolePopup
@onready var role_option = $RolePopup/VBoxContainer/RoleOption
@onready var chair_popup = $ChairPopup
@onready var chair_option = $ChairPopup/VBoxContainer/ChairOption

const ITEM_SCENE = preload("res://scenes/UsuarioItem.tscn")

var current_selected_user: Dictionary
var cadeiras_cache: Array = []

func _ready():
	role_popup.visible = false
	chair_popup.visible = false
	carregar_usuarios()
	carregar_cadeiras()

func carregar_usuarios():
	status_label.text = "Carregando usuários..."
	for child in user_list.get_children():
		child.queue_free()

	HTTPManager.send_request("/admin/usuarios", HTTPClient.METHOD_GET, {}, AuthManager.auth_token)
	var response = await HTTPManager.request_completed
	var response_code = response[1]
	var body = response[3]

	if response_code == 200:
		status_label.text = "Usuários carregados."
		for u in body:
			var item = ITEM_SCENE.instantiate()
			user_list.add_child(item)
			item.setup(u)
			item.role_change_requested.connect(_on_role_change_requested)
			item.chair_assign_requested.connect(_on_chair_assign_requested)
	else:
		status_label.text = "Erro ao carregar usuários."

func carregar_cadeiras():
	HTTPManager.send_request("/cadeiras", HTTPClient.METHOD_GET)
	var response = await HTTPManager.request_completed
	var response_code = response[1]
	var body = response[3]

	if response_code == 200:
		cadeiras_cache = body
		chair_option.clear()
		for c in body:
			chair_option.add_item(c.nome, c.id)

func _on_role_change_requested(user_data):
	current_selected_user = user_data
	var mapping = {"aluno": 0, "professor": 1, "admin": 2}
	role_option.selected = mapping.get(user_data.role, 0)
	role_popup.visible = true

func _on_save_role_pressed():
	var new_role = ["aluno", "professor", "admin"][role_option.selected]
	var body = {"role": new_role}

	HTTPManager.send_request("/admin/usuarios/" + current_selected_user.id + "/role",
		HTTPClient.METHOD_PATCH, body, AuthManager.auth_token)
	var response = await HTTPManager.request_completed
	var response_code = response[1]

	if response_code == 200:
		role_popup.visible = false
		carregar_usuarios()
	else:
		status_label.text = "Erro ao alterar role."

func _on_chair_assign_requested(user_data):
	current_selected_user = user_data
	chair_popup.visible = true

func _on_save_chair_pressed():
	var chair_id = chair_option.get_selected_id()
	var body = {"cadeira_id": chair_id}

	HTTPManager.send_request("/admin/usuarios/" + current_selected_user.id + "/cadeira",
		HTTPClient.METHOD_PATCH, body, AuthManager.auth_token)
	var response = await HTTPManager.request_completed
	var response_code = response[1]

	if response_code == 200:
		chair_popup.visible = false
		carregar_usuarios()
	else:
		status_label.text = "Erro ao associar cadeira."

func _on_voltar_button_pressed():
	SceneManager.change_scene("res://scenes/MenuPrincipal.tscn")

func _on_cancel_popup_pressed():
	role_popup.visible = false
	chair_popup.visible = false