#PLAYER
extends CharacterBody2D

#variables
var direction_g = 0
var attacking = false

@onready var animation = $Animations

func _physics_process(_delta: float) -> void:
#Atk
	#Direction check for attack animation
	if direction_g > 0:  
		animation.flip_h = false 

	elif direction_g < 0:  
		animation.flip_h = true  

	# Attack Input
	if Input.is_action_just_pressed("SPACE") and attacking == false:
		attacking = true
		animation.play("Atk")  
		$AtkTimer.start()

	elif Input.is_action_just_released('SPACE') and attacking == true:
		attacking = false
		animation.play("Idle")
		$AtkTimer.stop()

#Gravity
	if not is_on_floor():
		velocity.y += G.P_GRAVITY

	if is_on_ceiling():
		velocity.y += G.P_GRAVITY * 2

	if is_on_floor():
		velocity.y = 0

# Handle jump
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