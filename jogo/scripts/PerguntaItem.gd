extends HBoxContainer

signal edit_requested(pergunta_data)
signal delete_requested(pergunta_id)

@onready var enunciado_label = $Enunciado
@onready var status_label = $Status

var data: Dictionary

func setup(pergunta_data: Dictionary):
	data = pergunta_data
	enunciado_label.text = data.enunciado
	status_label.text = "[Ativa]" if data.ativa else "[Inativa]"
	status_label.modulate = Color.GREEN if data.ativa else Color.RED

func _on_edit_button_pressed():
	edit_requested.emit(data)

func _on_delete_button_pressed():
	delete_requested.emit(data.id)
