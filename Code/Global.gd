#GLOBALS
#pretty obivous what this file does lol
extends Node

func _ready() -> void:
        print("GLOBALS LOADED")
        print("--- Debugging process started ---")

#player vars and consts
@export var P_SPEED = 300.0
@export var P_JUMP_VELOCITY = -500.0
@export var P_GRAVITY = 20
@export var P_HP = 20
@export var P_ATK_DMG = 10  
@export var P_ATK_RANGE = 70

#slime vars and consts
@export var S_SPEED = 100.0 
@export var S_HP = 20