extends Control

@onready var chair_option = $VBoxContainer/HBox/ChairOption
@onready var ranking_list = $VBoxContainer/ScrollContainer/RankingList
@onready var status_label = $VBoxContainer/StatusLabel

func _ready():
	carregar_cadeiras()

func carregar_cadeiras():
	status_label.text = "Carregando cadeiras..."

	HTTPManager.send_request("/cadeiras", HTTPClient.METHOD_GET)
	var response = await HTTPManager.request_completed
	var response_code = response[1]
	var body = response[3]

	if response_code == 200:
		chair_option.clear()
		for c in body:
			chair_option.add_item(c.nome, c.id)
		if body.size() > 0:
			_on_chair_selected(0)
	else:
		status_label.text = "Erro ao carregar cadeiras."

func _on_chair_selected(index):
	var chair_id = chair_option.get_item_id(index)
	carregar_ranking(chair_id)

func carregar_ranking(chair_id):
	status_label.text = "Carregando ranking..."
	for child in ranking_list.get_children():
		child.queue_free()

	HTTPManager.send_request("/partidas/ranking/" + str(chair_id), HTTPClient.METHOD_GET)
	var response = await HTTPManager.request_completed
	var response_code = response[1]
	var body = response[3]

	if response_code == 200:
		status_label.text = ""
		if body.size() == 0:
			status_label.text = "Nenhuma partida registrada para esta cadeira."

		var pos = 1
		for entry in body:
			var h_box = HBoxContainer.new()
			h_box.custom_minimum_size.y = 40

			var pos_label = Label.new()
			pos_label.text = str(pos) + "º"
			pos_label.custom_minimum_size.x = 50

			var nome_label = Label.new()
			nome_label.text = entry.nome_completo
			nome_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL

			var acertos_label = Label.new()
			acertos_label.text = str(entry.acertos) + "/" + str(entry.total_perguntas)
			acertos_label.custom_minimum_size.x = 100
			acertos_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER

			var tempo_label = Label.new()
			tempo_label.text = str(entry.tempo_segundos) + "s"
			tempo_label.custom_minimum_size.x = 80
			tempo_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER

			var pontos_label = Label.new()
			pontos_label.text = str(entry.pontuacao_total) + " pts"
			pontos_label.custom_minimum_size.x = 120
			pontos_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT

			h_box.add_child(pos_label)
			h_box.add_child(nome_label)
			h_box.add_child(acertos_label)
			h_box.add_child(tempo_label)
			h_box.add_child(pontos_label)

			ranking_list.add_child(h_box)
			pos += 1
	else:
		status_label.text = "Erro ao carregar ranking."

func _on_voltar_button_pressed():
	SceneManager.change_scene("res://scenes/MenuPrincipal.tscn")