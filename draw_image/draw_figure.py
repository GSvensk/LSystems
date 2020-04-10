from PIL import Image, ImageDraw
from collections import defaultdict, deque
import math
import ast
import random
from pathlib import Path


def draw_from_config(config, axiom, img_name, width = 1000, height = 1000):

    config, background_color, start_state, angle_deviation, fill, branch_width = parse_config(config, width, height)
    alphabet_translation = create_alphabet_translations(config["angle"], config["f"], config["P"])

    img = create_image(background_color)
    img = draw_tree(img, axiom, start_state, alphabet_translation, config["step_rate"],  angle_deviation, config["f"], fill = fill, branch_width = branch_width)
    Path("./wip_images").mkdir(parents=True, exist_ok=True)
    img.save('./wip_images/{}.png'.format(img_name))
    

def parse_config(config, width = 1000, height = 1000):
    background_color = ast.literal_eval(config["settings"]["background"])
    start_state = (
                    width * float(config["start_state"]["width"]),
                    height * float(config["start_state"]["height"]),
                    math.radians(float(config["start_state"]["angle"]))
                  )
    angle_deviation = config["angle_deviation_degrees"]
    fill = ast.literal_eval(config["settings"]["fill"])
    branch_width = ast.literal_eval(config["settings"]["line_width"])
    return config, background_color, start_state, angle_deviation, fill, branch_width


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


def draw_branch(draw, x, y, length, angle, fill = (255, 255, 255, 128), branch_width = 1):
    x_end = x + length * math.sin(angle)
    y_end = y - length * math.cos(angle)
    draw.line((x, y, x_end, y_end), fill = fill, width = branch_width)
    return (x_end, y_end, angle)


def get_number(substring):
    digit = ""
    counter = 0
    
    while counter < len(substring) and str.isdigit(substring[counter]):
        digit += substring[counter]
        counter += 1

    return int(digit)


def draw_tree(img, sequence, start_state, alphabet_translation, step_rate, angle_deviation = 0, f = 100, fill = (255, 255, 255, 128), branch_width = 1):

    draw = ImageDraw.Draw(img)
    states = deque()
    state = start_state

    for i, ch in enumerate(sequence):
        
        if ch == "f":
            g = get_number(sequence[i+1:])
            #decrease step length by step_rate ^ g
            rand_factor = random.uniform(0.8, 1.2)
            step_reduction = math.pow(step_rate, g)
            step_size = rand_factor * step_reduction * alphabet_translation[ch]
            line_width = int(branch_width * step_reduction) if branch_width * step_reduction > 1 else 1
            fill = fill[:3] + (int(fill[3] * 2 * step_reduction),)

            state = draw_branch(draw, state[0], state[1], step_size, state[2], fill = fill, branch_width = line_width)
        elif ch == "[":
            states.append(state)
        elif ch == "]":
            state = states.pop()
        elif ch == "P":

            if alphabet_translation[ch] == 0:
                continue

            g = get_number(sequence[i+1:])
            #decrease step length by step_rate ^ g
            rand_factor = random.uniform(0.8, 1.2)
            step_reduction = math.pow(step_rate, g)
            step_size = rand_factor * step_reduction * alphabet_translation[ch]
            line_width = int(branch_width * step_reduction) if branch_width * step_reduction > 1 else 1
            fill = fill[:3] + (int(fill[3] * 2 * step_reduction),)
            state = draw_branch(draw, state[0], state[1], step_size, state[2], fill = fill, branch_width = line_width)

        elif ch in ("r", "l"):

            angle_noise = math.radians(random.randint(-angle_deviation, angle_deviation))
            angle_rotation = state[2] + alphabet_translation[ch] + angle_noise
            state = (state[0], state[1], angle_rotation)
        elif str.isdigit(ch):
            continue

    return img