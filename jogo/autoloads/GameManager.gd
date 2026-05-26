extends Node

var selected_cadeira: Dictionary = {}
var current_questions: Array = []
var current_question_index: int = 0
var acertos: int = 0
var tempo_total: int = 0

func start_game(cadeira_data: Dictionary, questions: Array):
	selected_cadeira = cadeira_data
	current_questions = questions
	current_questions.shuffle() # Embaralha as perguntas
	# Limita a 10 perguntas conforme regra de negócio
	if current_questions.size() > 10:
		current_questions = current_questions.slice(0, 10)
	
	current_question_index = 0
	acertos = 0
	tempo_total = 0
	
	SceneManager.change_scene("res://scenes/Jogo.tscn")

func get_current_question() -> Dictionary:
	if current_question_index < current_questions.size():
		return current_questions[current_question_index]
	return {}

func next_question() -> bool:
	current_question_index += 1
	return current_question_index < current_questions.size()
