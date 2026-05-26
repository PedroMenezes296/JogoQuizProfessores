extends Node

var auth_token: String = ""
var user_profile: Dictionary = {}

func is_logged_in() -> bool:
	return auth_token != ""

func get_role() -> String:
	return user_profile.get("role", "aluno")

func login(token: String, profile: Dictionary):
	auth_token = token
	user_profile = profile
	# Aqui poderíamos salvar o token em um config file para persistência
	print("Usuário logado: ", user_profile.nome_completo, " [", get_role(), "]")

func logout():
	auth_token = ""
	user_profile = {}
	get_tree().change_scene_to_file("res://scenes/Login.tscn")
