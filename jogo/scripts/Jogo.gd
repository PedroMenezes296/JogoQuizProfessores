extends Control

@onready var enunciado_label = $UI/QuestionCard/VBoxContainer/Enunciado
@onready var opcoes_container = $UI/QuestionCard/VBoxContainer/Opcoes
@onready var placar_label = $UI/PlacarLabel
@onready var professor_sprite = $Professor
@onready var balao_fala = $Professor/BalaoFala
@onready var frase_label = $Professor/BalaoFala/Label

var current_question: Dictionary
var can_answer: bool = false
var question_start_time: float = 0.0

var professor_textures: Dictionary = {}

var frases_feliz = ["Muito bem!", "Exato!", "Você estudou!", "Parabéns!", "Boa resposta!"]
var frases_bravo = ["Preste atenção!", "Quase lá...", "Estude mais!", "Incorreto!", "Reveja a matéria!"]

func _ready():
	balao_fala.visible = false
	_carregar_texturas_professor()
	load_question()

func _carregar_texturas_professor():
	var id = GameManager.selected_cadeira.get("id", 1)
	for estado in ["normal", "feliz", "bravo"]:
		var path_jpg = "res://assets/professores/professor_%d_%s.jpg" % [id, estado]
		var path_png = "res://assets/professores/professor_%d_%s.png" % [id, estado]
		if ResourceLoader.exists(path_jpg):
			professor_textures[estado] = load(path_jpg)
		elif ResourceLoader.exists(path_png):
			professor_textures[estado] = load(path_png)

func load_question():
	current_question = GameManager.get_current_question()
	if current_question.is_empty():
		finish_game()
		return

	enunciado_label.text = current_question.enunciado

	var botoes = opcoes_container.get_children()
	botoes[0].text = "A)  " + current_question.opcao_a
	botoes[1].text = "B)  " + current_question.opcao_b
	botoes[2].text = "C)  " + current_question.opcao_c
	botoes[3].text = "D)  " + current_question.opcao_d

	for i in range(4):
		botoes[i].disabled = false

	var total = GameManager.current_questions.size()
	var atual = GameManager.current_question_index + 1
	placar_label.text = "Pergunta %d / %d  |  Acertos: %d" % [atual, total, GameManager.acertos]

	can_answer = true
	question_start_time = Time.get_ticks_msec() / 1000.0
	if professor_textures.has("normal"):
		professor_sprite.texture = professor_textures["normal"]
	balao_fala.visible = false

func _on_opcao_pressed(opcao_index: int):
	if not can_answer:
		return

	can_answer = false

	var resposta_escolhida = ["a", "b", "c", "d"][opcao_index]
	var acertou = (resposta_escolhida == current_question.resposta_correta)

	var tempo_gasto = (Time.get_ticks_msec() / 1000.0) - question_start_time
	GameManager.tempo_total += int(tempo_gasto)

	if acertou:
		GameManager.acertos += 1
		if professor_textures.has("feliz"):
			professor_sprite.texture = professor_textures["feliz"]
		frase_label.text = frases_feliz.pick_random()
	else:
		if professor_textures.has("bravo"):
			professor_sprite.texture = professor_textures["bravo"]
		frase_label.text = frases_bravo.pick_random()

	balao_fala.visible = true

	await get_tree().create_timer(2.0).timeout

	if GameManager.next_question():
		load_question()
	else:
		finish_game()

func finish_game():
	SceneManager.change_scene("res://scenes/Resultado.tscn")
