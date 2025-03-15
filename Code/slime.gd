#SLIME
extends CharacterBody2D

const speed = 200
var player_position
var target
@onready var player = get_parent().get_node("Player")

func _physics_process(delta: float) -> void:

	player_position = player.position
	target = (player_position - position).normalized()

	if not is_on_floor():
		velocity += get_gravity() * delta  

	if position.distance_to(player_position) > 3:
		velocity.x = target.x * speed  
		$AnimatedSprite2D.play("Run")
	else:
		velocity.x = 0  
		$AnimatedSprite2D.play("Idle")

	move_and_slide()
