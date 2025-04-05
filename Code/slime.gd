#SLIME
extends CharacterBody2D

#Variables
var player_position
var target
var direction = 1
var is_dead = false

@onready var player = get_parent().get_node('Player')
@onready var animation = $Animation
@onready var raycast = $RayCast2D
@onready var body_area = $BodyArea  

func _ready() -> void:
	player_position = player.position

func _InRangeToTakeDamage():
	if position.distance_to(player_position) <= G.P_ATK_RANGE and player.attacking:
		print('IN RANGE TAKING DAMAGE')
		_TakeDamage(10)

#damage logic
func _TakeDamage(damage: int) -> void:
	G.S_HP -= damage
	print("---------------------------------")
	print("Slime health:", G.S_HP)
	print("---------------------------------")

	if G.S_HP <= 0 and not is_dead:
		is_dead = true
		velocity = Vector2.ZERO
		animation.play("Death") 
		queue_free()

func _physics_process(delta: float) -> void:
	# Player position tracking
	player_position = player.position
	target = (player_position - position).normalized()

	if not is_on_floor():
		velocity += get_gravity() * delta  

	if position.distance_to(player_position) > 3:
		velocity.x = target.x * G.S_SPEED  
		animation.play("Run")

	else:
		velocity.x = 0  
		animation.play("Idle")

	move_and_slide()
	_InRangeToTakeDamage()