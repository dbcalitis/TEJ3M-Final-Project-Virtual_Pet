# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
# SPDX-License-Identifier: MIT
# Creator : Daria Bernice Calitis
# Start Date : June 17, 2022
# Latest Update : June 17, 2022

""" Virtual Pet Game for the Clue Adafruit Board """

import time
import board
import displayio
import adafruit_imageload
from adafruit_clue import clue
from adafruit_display_text import label
import pet
import display
import terminalio

screen = board.DISPLAY

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("/slime.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

# Makes the background colour disappear
palette.make_transparent(0)

# Create a sprite (tilegrid)
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16)

# Sprite Group Display
sprite_group = displayio.Group(scale=5)
sprite_group.append(sprite)
sprite_group.x = 80
sprite_group.y = 80

# Loop through each sprite in the sprite sheet
source_index = 0

# Prevents spamming while holding the buttons
holding_buttons = False

# Sets the current animation of the slime sprite
current_animation = pet.slime_front_startframe
endpoint_reached = False
endpoint_x = 0

time_count = 0
time_count_stats = 0

display.group.append(sprite_group)

screen.show(display.group)

while True:
    if pet.hatched:
        # Once the time_count variable reaches the frame duration,
        # it repeats the current animation
        if time_count == pet.frame_duration:
            time_count = 0
            source_index += 1

        if endpoint_reached: 
            if current_animation == pet.slime_front_startframe:
                current_animation, endpoint_x = pet.pace_around(sprite_group.x)
            else:
                current_animation = pet.idle()
            endpoint_reached = False
        
        # If it did not reached its endpoint, it will move towards it.
        if not endpoint_reached:
            # checks if the pet has reached the endpoint
            if endpoint_x == sprite_group.x:
                endpoint_reached = True

            # Pet going to the left
            if current_animation == pet.slime_left_startframe:
                sprite_group.x -= pet.speed

            # Pet going to the right
            elif current_animation == pet.slime_right_startframe:
                sprite_group.x += pet.speed
        

        # Sets the animation frame
        sprite[0] = current_animation + source_index % 4
        
        if source_index == 4:
            endpoint_reached = True
        
        # Resets the frame to zero once it reaches the 4th frame
        source_index = source_index % 4

        # To keep track of time for the animation and stats
        time_count += 1
        time_count_stats += 1
        pet.hunger, pet.happiness, pet.hygiene, pet.sleep, time_count_stats = pet.decrease_stats(
            time_count_stats, pet.hunger, pet.happiness, pet.hygiene, pet.sleep
            )
        display.hunger_area.text = str(pet.hunger) + "%"
        display.happiness_area.text = str(pet.happiness) + "%"
        display.hygiene_area.text = str(pet.hygiene) + "%"
        display.sleep_area.text = str(pet.sleep) + "%"
    else:
        # Hatching Process (start of the game)
        if clue.button_a == True or clue.button_b == True:
            if not holding_buttons:
                source_index += 1
                holding_buttons = True
        else:
            holding_buttons = False 

        if source_index == 4:
            # Hatches the pet and displays its stats
            pet.hatched = True
            display.group.append(display.hunger_area)
            display.group.append(display.happiness_area)
            display.group.append(display.hygiene_area)
            display.group.append(display.sleep_area)
            display.group.append(display.image_stats_group)
            screen.show(display.group)
        
        sprite[0] = source_index % 4
    
    time.sleep(0.1)
