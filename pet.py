import random

screen_dimension = 240 # 240 pixels each side
margin = 10 # Serves as a border around the pet

hatched = False
speed = 1

# Animation Frames
frame_duration = 4 # deciseconds
frame_dimension = 16 # 16 pixels each side

egg_startframe = 0
slime_front_startframe = 4
slime_right_startframe = 8
slime_left_startframe = 12

# Status
hunger = 50
happiness = 50
hygiene = 50
sleep = 50

def pace_around(positionX):
    # Initializing variables
    direction = 0 # 0 = Left, 1 = Right
    distance = 0

    if (positionX + frame_dimension) >= screen_dimension + margin:
        direction = 0 # Left
    elif positionX <= 0 + margin:
        direction = 1 # Right
    else:
        direction = random.randint(0, 1)

    # Pacing towards left
    if direction == 0:
        try:
            distance = positionX - margin
            end_point = random.randint(0 + margin, distance)
        except:
            end_point = positionX
        current_animation = slime_left_startframe
    # Pacing towards right
    elif direction == 1: 
        try:
            distance = screen_dimension - margin - positionX
            end_point = random.randint(positionX, distance)
        except:
            end_point = positionX
        current_animation = slime_right_startframe

    return current_animation, end_point

def idle():
    # Returns the animation start frame and 
    return slime_front_startframe

def decrease_stats(time_count, hunger, happiness, hygiene, sleep):
    if time_count == 300:
        hunger -= random.randint(0, 2)
        happiness -= random.randint(0, 2)
        hygiene -= random.randint(0, 3)
        sleep -= random.randint(0, 1)
        time_count = 0
    return hunger, happiness, hygiene, sleep, time_count

def feed(hunger):
    hunger += 10
    if hunger > 100:
        hunger = 100
    return hunger

def pet(happiness):
    happiness += 10
    if happiness > 100:
        happiness = 100
    return happiness

def clean(hygiene):
    hygiene += 10
    if hygiene > 100:
        hygiene = 100
    return hygiene

def rest(sleep):
    sleep += 10
    if sleep > 100:
        sleep = 100
    return sleep