extends CharacterBody2D

# Variables
var player_position
var target
var direction = 1

@onready var player = get_parent().get_node('Player')
@onready var animation = $Animation
@onready var raycast = $RayCast2D
@onready var body_area = $BodyArea  

@export var speed = 200
@export var health = 20

func _ready() -> void:
	var countexe = OS.get_processor_count()
	
	print("-------Debug Process Start---------")
	print(countexe)
	print(player)
	if player:
		if player.has_signal("atk_start"):
			player.atk_start.connect(_on_player_atk)
			print("Connected `atk_start` signal!")
			print("---------------------------------")
		else:
			print("Error: Player does not have `atk_start` signal!")
			print("---------------------------------")
	else:
		print("Player node NOT found!")
		print("---------------------------------")

func _on_player_atk() -> void:
	print("_on_player_atk() run conditions met!")
	print("---------------------------------")
	var attack_hitbox = player.get_node("AtkArea")  
	if body_area.overlaps_area(attack_hitbox):
		take_damage(10)


func _physics_process(delta: float) -> void:
	# Player tracking
	player_position = player.position
	target = (player_position - position).normalized()

	if not is_on_floor():
		velocity += get_gravity() * delta  

	if position.distance_to(player_position) > 3:
		velocity.x = target.x * speed  
		animation.play("Run")

	else:
		velocity.x = 0  
		animation.play("Idle")

	move_and_slide()

 #Corrected take_damage
func take_damage(damage: int) -> void:
	OS.crash("CRASH")
	health -= damage
	print("Slime health:", health)
	print("---------------------------------")

	if health <= 0:
		velocity = Vector2.ZERO
		animation.play("Death") 

	var connected = player.atk_start.is_connected(_on_player_atk)

	print('is connected :', connected)
	print("---------------------------------")
	player.atk_start.connect(_on_player_atk)
	animation.animation_finished.connect(_on_animation_animation_finished)


func _on_animation_animation_finished(anim_name: String) -> void:
	if anim_name == "Death":
		queue_free()
