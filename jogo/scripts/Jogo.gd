extends Control

@onready var quadro_rect = $Background/Quadro
@onready var enunciado_label = $UI/QuestionCard/VBoxContainer/Enunciado
@onready var opcoes_container = $UI/QuestionCard/VBoxContainer/Opcoes
@onready var timer_label = $UI/TimerLabel
@onready var placar_label = $UI/PlacarLabel
@onready var timer_node = $Timer
@onready var professor_sprite = $Professor
@onready var balao_fala = $Professor/BalaoFala
@onready var frase_label = $Professor/BalaoFala/Label

var current_question: Dictionary
var time_left: float = 15.0
var can_answer: bool = false
var question_start_time: float = 0.0

var frases_feliz = ["Muito bem!", "Exato!", "Você estudou!", "Parabéns!", "Boa resposta!"]
var frases_bravo = ["Preste atenção!", "Quase lá...", "Estude mais!", "Incorreto!", "Reveja a matéria!"]

func _ready():
	var cadeira = GameManager.selected_cadeira
	quadro_rect.color = Color.from_string(cadeira.get("cor_quadro", "#004d00"), Color.DARK_GREEN)
	balao_fala.visible = false
	load_question()

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

	time_left = 15.0
	can_answer = true
	question_start_time = Time.get_ticks_msec() / 1000.0
	professor_sprite.frame = 0
	balao_fala.visible = false
	timer_node.start()

func _process(delta):
	if can_answer:
		time_left -= delta
		timer_label.text = "⏱ %d" % ceil(time_left)
		if time_left <= 0:
			_on_timer_timeout()

func _on_opcao_pressed(opcao_index: int):
	if not can_answer:
		return

	can_answer = false
	timer_node.stop()

	var resposta_escolhida = ""
	if opcao_index >= 0:
		resposta_escolhida = ["a", "b", "c", "d"][opcao_index]
	var acertou = (resposta_escolhida == current_question.resposta_correta)

	var tempo_gasto = (Time.get_ticks_msec() / 1000.0) - question_start_time
	GameManager.tempo_total += int(tempo_gasto)

	if acertou:
		GameManager.acertos += 1
		professor_sprite.frame = 1
		frase_label.text = frases_feliz.pick_random()
	else:
		professor_sprite.frame = 2
		frase_label.text = frases_bravo.pick_random()

	balao_fala.visible = true

	await get_tree().create_timer(2.0).timeout

	if GameManager.next_question():
		load_question()
	else:
		finish_game()

func _on_timer_timeout():
	if not can_answer:
		return
	_on_opcao_pressed(-1)

func finish_game():
	SceneManager.change_scene("res://scenes/Resultado.tscn")
