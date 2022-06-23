from adafruit_display_text import label
import displayio
import pet
import terminalio
import adafruit_imageload

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("/slime.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

# Makes the background colour disappear
palette.make_transparent(0)

# Create the background TileGrid
background = displayio.TileGrid(
    sprite_sheet,
    pixel_shader=palette,
    width=10,
    height=8,
    tile_width=16,
    tile_height=16,
)

# Create the image statistics TileGrid
image_stats = displayio.TileGrid(
    sprite_sheet,
    pixel_shader=palette,
    width=10,
    height=8,
    tile_width=16,
    tile_height=16,
)

# Create the buttons TileGrid
buttons = displayio.TileGrid(
    sprite_sheet,
    pixel_shader=palette,
    width=10,
    height=8,
    tile_width=16,
    tile_height=16,
)

# Create the buttons TileGrid
selection = displayio.TileGrid(
    sprite_sheet,
    pixel_shader=palette,
    width=10,
    height=8,
    tile_width=16,
    tile_height=16,
)

# Create the buttons TileGrid
effects = displayio.TileGrid(
    sprite_sheet,
    pixel_shader=palette,
    width=10,
    height=8,
    tile_width=16,
    tile_height=16,
)

# Create a group to hold the background
background_group = displayio.Group(scale=5)
background_group.append(background)
for x in range(0, 10):
    for y in range(0, 8):
        background[x, y] = 16 # tile number

# Set text, font, and color for the Title
text = "Virtual Pet"
font = terminalio.FONT
color = 000000

text_area = label.Label(font, text=text, color=color, scale=2)
text_area.x = 55
text_area.y = 10

instructions = label.Label(font, text="Shake vigorously to hatch", color=color, scale=1)
instructions.x = 50
instructions.y = 70

group = displayio.Group()
group.append(background_group)
group.append(text_area)
group.append(instructions)

# Pet Statistics Display
image_stats_group = displayio.Group(scale=2)
image_stats_group.append(image_stats)
for x in range(0, 10):
    for y in range(0, 8):
        image_stats[x, y] = 31 # tile number
image_stats[0, 1] = 17 # tile number
image_stats[2, 1] = 18 # tile number
image_stats[4, 1] = 19 # tile number
image_stats[6, 1] = 20 # tile number

# Buttons Display
buttons_group = displayio.Group(scale=2)
buttons_group.append(buttons)
for x in range(0, 10):
    for y in range(0, 8):
        buttons[x, y] = 31 # tile number
buttons[0, 6] = 21 # tile number
buttons[2, 6] = 22 # tile number
buttons[4, 6] = 23 # tile number
buttons[6, 6] = 24 # tile number

# Buttons Display
selection_group = displayio.Group(scale=2)
selection_group.append(selection)
for x in range(0, 10):
    for y in range(0, 8):
        selection[x, y] = 31 # tile number
selection[0, 6] = 25 # tile number

hunger_area = label.Label(font, text=str(pet.hunger) + "%", color=color, scale=1)
hunger_area.x = 38
hunger_area.y = 48

happiness_area = label.Label(font, text=str(pet.happiness) + "%", color=color, scale=1)
happiness_area.x = 98
happiness_area.y = 48

hygiene_area = label.Label(font, text=str(pet.hygiene) + "%", color=color, scale=1)
hygiene_area.x = 158
hygiene_area.y = 48

sleep_area = label.Label(font, text=str(pet.sleep) + "%", color=color, scale=1)
sleep_area.x = 210
sleep_area.y = 48

# Effects display
effects_group = displayio.Group(scale=5)
effects_group.append(effects)
for x in range(0, 10):
    for y in range(0, 8):
        effects[x, y] = 31 # tile number
