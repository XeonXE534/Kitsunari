#PLAYER
extends CharacterBody2D

# Signals
signal atk_start
signal atk_end

#vars,consts and exports
var direction_g = 0
var attacking = false
@export var atk_dmg = 10  
@export var atk_rng = 20   
@onready var atk_col = $AtkArea/AtkCol
@onready var animation = $Animations


func _ready() -> void:
	atk_col.disabled = true

func _physics_process(delta: float) -> void:
	#Atk
	if direction_g > 0:  
		animation.flip_h = false 
	elif direction_g < 0:  
		animation.flip_h = true  

	# Attack Input
	if Input.is_action_just_pressed("SPACE") and not attacking:
		attacking = true
		atk_start.emit() 
		animation.play("Atk")  
		atk_col.disabled = false 
		$AtkTimer.start()

	elif Input.is_action_just_released('SPACE') and attacking == true:
		attacking = false
		atk_col.disabled = true
		animation.play("Idle")
		atk_end.emit()
		
	#Gravity
	if not is_on_floor():
		velocity.y += G.P_GRAVITY

	if is_on_ceiling():
		velocity.y += G.P_GRAVITY * 2
		
	if is_on_floor():
		velocity.y = 0

	# Handle jump.
	if Input.is_action_just_pressed("W") and is_on_floor():
		velocity.y = G.P_JUMP_VELOCITY
		animation.play("Jump")

	# Movement
	var direction := Input.get_axis("A", "D")
	if is_zero_approx(velocity.x) and is_on_floor() and attacking == false:
		animation.play('Idle')
		direction_g = 0

	if velocity.x > 0 and attacking == false:  
		animation.play("Run")
		animation.flip_h = false 
		direction_g = 1

	elif velocity.x < 0 and attacking == false:  
		animation.play("Run")
		animation.flip_h = true   
		direction_g = -1

	if direction:
		velocity.x = direction * G.P_SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, G.P_SPEED)

	move_and_slide()

func _on_atk_timer_timeout():
	attacking = false
	atk_end.emit()
	atk_col.disabled = true 
	if not is_zero_approx(velocity.x) and is_on_floor():
		animation.play("Run")
	elif is_zero_approx(velocity.x) and is_on_floor():
		animation.play("Idle")
