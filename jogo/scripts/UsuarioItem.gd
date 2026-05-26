extends HBoxContainer

signal role_change_requested(user_data)
signal chair_assign_requested(user_data)

@onready var nome_label = $Nome
@onready var email_label = $Email
@onready var role_label = $Role
@onready var chair_button = $ChairButton

var data: Dictionary

func setup(user_data: Dictionary):
	data = user_data
	nome_label.text = data.nome_completo
	email_label.text = data.email_institucional
	role_label.text = "[" + data.role.to_upper() + "]"
	
	# Só permite associar cadeira se for professor
	chair_button.visible = (data.role == "professor")

func _on_role_button_pressed():
	role_change_requested.emit(data)

func _on_chair_button_pressed():
	chair_assign_requested.emit(data)
