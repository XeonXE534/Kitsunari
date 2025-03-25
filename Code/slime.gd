extends CharacterBody2D

# Variables
var player_position
var target
var direction = 1

#@onready var player = get_node("/root/Testlvl/Player")
@onready var player = get_node("/root/Testlvl/Player")
@onready var animation = $Animation
@onready var raycast = $RayCast2D
@onready var body_area = $BodyArea  # Ensure this is an Area2D node

@export var speed = 200
@export var health = 20

func _ready() -> void:
	# Check if player node exists
	  # Adjust this path to match your scene structure

	if player:
		print("Player node found")
		player.atk_start.connect(_on_player_atk)  # Connect the signal only if player is found
	else:
		print("Player node NOT found!")

func _on_player_atk() -> void:
	# Check if the attack hitbox overlaps
	var attack_hitbox = player.get_node("AtkArea")  # Adjust this path to match your player's attack hitbox node
	if body_area.overlaps_area(attack_hitbox):
		take_damage(10)

	#var connected = player.atk_start.is_connected(_on_player_atk)
	#print('is connected :', connected)
	#player.atk_start.connect(_on_player_atk)
	#animation.animation_finished.connect(_on_animation_animation_finished)
#
#func _physics_process(delta: float) -> void:
	## Player tracking
	#player_position = player.position
	#target = (player_position - position).normalized()
#
	#if not is_on_floor():
		#velocity += get_gravity() * delta  
#
	#if position.distance_to(player_position) > 3:
		#velocity.x = target.x * speed  
		#animation.play("Run")
#
	#else:
		#velocity.x = 0  
		#animation.play("Idle")
#
	#move_and_slide()
#
## Corrected take_damage
func take_damage(damage: int) -> void:
	health -= damage
	print("Slime health:", health)

	if health <= 0:
		velocity = Vector2.ZERO
		animation.play("Death")  # Play Death animation


#func _on_animation_animation_finished(anim_name: String) -> void:
	#if anim_name == "Death":
		#queue_free()
