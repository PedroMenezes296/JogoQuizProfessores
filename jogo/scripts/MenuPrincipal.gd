extends Control

@onready var saudacao_label = $VBoxContainer/SaudacaoLabel
@onready var play_button = $VBoxContainer/PlayButton
@onready var professor_button = $VBoxContainer/ProfessorButton
@onready var admin_button = $VBoxContainer/AdminButton

func _ready():
	var profile = AuthManager.user_profile
	saudacao_label.text = "Olá, " + profile.get("nome_completo", "Estudante") + "!"
	
	# Controle de visibilidade baseado no role
	var role = AuthManager.get_role()
	professor_button.visible = (role == "professor" or role == "admin")
	admin_button.visible = (role == "admin")

func _on_play_button_pressed():
	SceneManager.change_scene("res://scenes/SelecaoCadeira.tscn")

func _on_regras_button_pressed():
	SceneManager.change_scene("res://scenes/Regras.tscn")

func _on_ranking_button_pressed():
	SceneManager.change_scene("res://scenes/Ranking.tscn")

func _on_professor_button_pressed():
	SceneManager.change_scene("res://scenes/PainelProfessor.tscn")

func _on_admin_button_pressed():
	SceneManager.change_scene("res://scenes/PainelAdmin.tscn")

func _on_logout_button_pressed():
	AuthManager.logout()
