extends Node

func change_scene(scene_path: String):
	# Poderíamos adicionar uma animação de fade aqui futuramente
	get_tree().change_scene_to_file(scene_path)
