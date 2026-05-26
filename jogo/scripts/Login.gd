extends Control

@onready var email_input = $VBoxContainer/EmailInput
@onready var senha_input = $VBoxContainer/SenhaInput
@onready var error_label = $VBoxContainer/ErrorLabel
@onready var login_button = $VBoxContainer/LoginButton

func _ready():
	error_label.text = ""
	HTTPManager.request_completed.connect(_on_login_request_completed)

func _on_login_button_pressed():
	var email = email_input.text
	var senha = senha_input.text
	
	if email == "" or senha == "":
		error_label.text = "Preencha todos os campos"
		return
	
	error_label.text = "Autenticando..."
	login_button.disabled = true
	
	var body = {
		"email_institucional": email,
		"senha": senha
	}
	
	HTTPManager.send_request("/auth/login", HTTPClient.METHOD_POST, body)

func _on_login_request_completed(result, response_code, headers, body):
	login_button.disabled = false
	
	if response_code == 200:
		AuthManager.login(body.access_token, body.user)
		SceneManager.change_scene("res://scenes/MenuPrincipal.tscn")
	else:
		error_label.text = "Erro: " + str(body.get("detail", "Erro desconhecido"))

func _on_cadastro_button_pressed():
	SceneManager.change_scene("res://scenes/Cadastro.tscn")
