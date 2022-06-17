import random

screen_dimension = 240 # 240 pixels each side
margin = 20 # Serves as a border around the pet

hatched = False

# Animation Frames
frame_duration = 10 # deciseconds
frame_dimension = 16 # 16 pixels each side

egg_startframe = 0
slime_front_startframe = 4
slime_right_startframe = 8
slime_left_startframe = 12

def pace_around(positionX, positionY):
    direction = 0 # 0 = Left, 1 = Right

    if (positionX + frame_dimension) >= screen_dimension:
        direction = 0 # Left
    elif positionX <= screen_dimension:
        direction = 1 # Right
    else:
        direction = random.randint(0, 1)
    
    # Pacing towards left
    if direction == 0:
        end_point = random.randint(0 + margin, positionX)
    # Pacing towards right
    elif direction == 1: 
        end_point = random.randint(positionX, screen_dimension - margin)

    return end_point

def idle():
    # Returns the animation start frame and 
    # the amount of times it should play it
    return slime_front_startframe, random.randint(1,2)