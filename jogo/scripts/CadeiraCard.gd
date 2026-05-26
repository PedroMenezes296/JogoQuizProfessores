extends PanelContainer

signal selected(cadeira_data)

@onready var nome_label = $VBoxContainer/NomeLabel
@onready var descricao_label = $VBoxContainer/DescricaoLabel
@onready var cor_rect = $VBoxContainer/CorRect

var data: Dictionary

func setup(cadeira_data: Dictionary):
	data = cadeira_data
	nome_label.text = data.get("nome", "Sem nome")
	descricao_label.text = data.get("descricao", "")
	
	var cor_hex = data.get("cor_quadro", "#004d00")
	cor_rect.color = Color.from_string(cor_hex, Color.DARK_GREEN)

func _on_button_pressed():
	selected.emit(data)
