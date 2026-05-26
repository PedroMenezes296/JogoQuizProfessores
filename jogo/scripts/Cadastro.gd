extends Control

@onready var nome_input = $VBoxContainer/NomeInput
@onready var email_input = $VBoxContainer/EmailInput
@onready var matricula_input = $VBoxContainer/MatriculaInput
@onready var senha_input = $VBoxContainer/SenhaInput
@onready var error_label = $VBoxContainer/ErrorLabel
@onready var register_button = $VBoxContainer/RegisterButton

func _ready():
	error_label.text = ""
	HTTPManager.request_completed.connect(_on_register_request_completed)

func _on_register_button_pressed():
	if nome_input.text == "" or email_input.text == "" or senha_input.text == "":
		error_label.text = "Nome, E-mail e Senha são obrigatórios"
		return
	
	if senha_input.text.length() < 6:
		error_label.text = "A senha deve ter pelo menos 6 caracteres"
		return

	error_label.text = "Criando conta..."
	register_button.disabled = true
	
	var body = {
		"nome_completo": nome_input.text,
		"email_institucional": email_input.text,
		"senha": senha_input.text,
		"matricula": matricula_input.text if matricula_input.text != "" else null
	}
	
	HTTPManager.send_request("/auth/cadastro", HTTPClient.METHOD_POST, body)

func _on_register_request_completed(result, response_code, headers, body):
	register_button.disabled = false
	
	if response_code == 201:
		error_label.text = "Conta criada! Redirecionando..."
		await get_tree().create_timer(1.5).timeout
		SceneManager.change_scene("res://scenes/Login.tscn")
	else:
		error_label.text = "Erro: " + str(body.get("detail", "Erro desconhecido"))

func _on_voltar_button_pressed():
	SceneManager.change_scene("res://scenes/Login.tscn")
