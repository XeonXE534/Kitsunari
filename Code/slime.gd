#SLIME
extends CharacterBody2D

#vars,consts and exports
const speed = 200
var player_position
var target
var health = 1

@onready var player = get_parent().get_node("Player")
@onready var animation = $Animation
@onready var raycast = $RayCast2D

func _physics_process(delta: float) -> void:

	#Player tracking
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
	
func take_damage(damage):
	health -= damage
	print("Slime health:", health)
	#velocity = Vector2.ZERO
	animation.play('Death')

	if health <= 0:
		animation.animation_finished.connect(queue_free, CONNECT_ONE_SHOT)

func _on_player_atk_start():
	player.get_node("AtkArea").connect("area_entered", _on_attack_area_entered)

func _on_player_attack_ended():
	if is_instance_valid(player.get_node("AtkArea")):
		if player.get_node("AtkArea").is_connected("area_entered", _on_attack_area_entered):
			player.get_node("AtkArea").disconnect("area_entered", _on_attack_area_entered)

func _on_attack_area_entered(area):
	if area.name == "AtkArea" and area.get_parent() == player:
		take_damage(player.atk_dmg)
