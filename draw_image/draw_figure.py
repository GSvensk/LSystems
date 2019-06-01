from PIL import Image, ImageDraw
from collections import defaultdict, deque
import math
import ast


def draw_from_config(config, axiom, img_name, width = 1000, height = 1000):

    config, background_color, start_state, fill = parse_config(config, width, height)
    alphabet_translation = create_alphabet_translations(config["angle"], config["f"], config["P"])

    img = create_image(background_color)
    img = draw_tree(img, axiom, start_state, alphabet_translation, config["step_rate"], config["f"])
    img.save('./wip_images/{}.png'.format(img_name))
    

def parse_config(config, width = 1000, height = 1000):
    background_color = ast.literal_eval(config["settings"]["background"])
    start_state = (
                    width * float(config["start_state"]["width"]),
                    height * float(config["start_state"]["height"]),
                    math.radians(float(config["start_state"]["angle"]))
                  )
    fill = ast.literal_eval(config["settings"]["fill"])
    return config, background_color, start_state, fill


def create_alphabet_translations(angle, f, P = 0):
    delta = math.radians(angle)

    return defaultdict(str, [
        ("P", P),
        ("f", f),
        ("r", delta),
        ("l", -delta),
    ])


def create_image(background_color, width = 1000, height = 1000):
    img = Image.new('RGB', (width, height), color = background_color)
    return img


def draw_branch(draw, x, y, length, angle, fill = (255, 255, 255, 128)):
    x_end = x + length * math.sin(angle)
    y_end = y - length * math.cos(angle)
    draw.line((x, y, x_end, y_end), fill = fill)
    return (x_end, y_end, angle)


def get_number(substring):
    digit = ""
    counter = 0
    
    while counter < len(substring) and str.isdigit(substring[counter]):
        digit += substring[counter]
        counter += 1
    
    #if digit == "":
    #    return 0

    return int(digit)


def draw_tree(img, sequence, start_state, alphabet_translation, step_rate, f = 100):

    draw = ImageDraw.Draw(img)
    states = deque()
    state = start_state

    for i, ch in enumerate(sequence):
        
        if ch == "f":
            g = get_number(sequence[i+1:])
            #decrease step length by step_rate ^ g
            step_size = math.pow(step_rate, g)
            state = draw_branch(draw, state[0], state[1], step_size * alphabet_translation[ch], state[2])
        elif ch == "[":
            states.append(state)
        elif ch == "]":
            state = states.pop()
        elif ch == "P":
            continue
        elif ch in ("r", "l"):
            state = (state[0], state[1], state[2] + alphabet_translation[ch])
        elif str.isdigit(ch):
            continue

    return img