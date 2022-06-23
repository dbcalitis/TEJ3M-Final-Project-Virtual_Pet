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
hatched_triggered = False

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
        
        if clue.button_a:
            x = display.selection_group.x - 64 # pixels
            if x < 0:
                x = 192 # pixels
            display.selection_group.x = x           

        if clue.button_b:
            x = display.selection_group.x + 64 # pixels
            if x > 192:
                x = 0 # pixels
            display.selection_group.x = x            
        
        # Increasing Stats
        if clue.touch_0:
            tile_number = 28
            if display.selection_group.x == 0:
                pet.hunger = pet.feed(pet.hunger)
                tile_number = 26
            if display.selection_group.x == 64:
                pet.hygiene = pet.clean(pet.hygiene)
                tile_number = 27
            if display.selection_group.x == 128:
                pet.happiness = pet.pet(pet.happiness)
                tile_number= 26
            if display.selection_group.x >= 192:
                pet.sleep = pet.rest(pet.sleep)
                print(pet.sleep)
            display.effects[0, 0] = tile_number
            try:
                display.group.append(display.effects_group)
            except:
                pass
            finally:
                display.effects_group.x = sprite_group.x
                display.effects_group.y = sprite_group.y
                screen.show(display.group)
                clue.play_tone(1000, 0.05)
        else:
            try:
                display.group.remove(display.effects_group)
            except:
                pass
            finally:
                screen.show(display.group) 

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
        
        # Plays a tone when it hatches 
        if not hatched_triggered:
            hatched_triggered = True
            for sound in range(500, 2001, 500):
                clue.play_tone(sound, 0.05)
        
        display.instructions.x -= 10

        if display.instructions.x == -400:
            display.instructions.x = 240
    else:
        # Hatching Process (start of the game)
        if clue.gyro[0] >= 4 or clue.gyro[2] >= 4:
            source_index += 1

        if source_index == 4:
            # Hatches the pet and displays its stats
            pet.hatched = True
            display.group.append(display.hunger_area)
            display.group.append(display.happiness_area)
            display.group.append(display.hygiene_area)
            display.group.append(display.sleep_area)
            display.group.append(display.image_stats_group)
            display.group.append(display.buttons_group)
            display.group.append(display.selection_group)
            display.instructions.text = "Hold buttons A or B to change options and press Touch 0 to care for pet."
            screen.show(display.group)
            holding_buttons = False
            
        
        sprite[0] = source_index % 4
    
    time.sleep(0.1)
