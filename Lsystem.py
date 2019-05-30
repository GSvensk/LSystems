from PIL import Image, ImageDraw
from collections import defaultdict, deque
import math

WIDTH = 1000
HEIGHT = 1000

def create_image():
    img = Image.new('RGB', (WIDTH, HEIGHT), color = (0, 0, 0))
    return img


def draw_branch(draw, x, y, length, angle):
    x_end = x + length * math.sin(angle)
    y_end = y - length * math.cos(angle)
    draw.line((x, y, x_end, y_end), fill=(255, 255, 255, 128))
    return (x_end, y_end, angle)


def calculate_step_size(g):
    return math.pow(2, -g/2)


def axiom(g):
    return "[rf{}P{}][lf{}P{}]".format(g, g, g, g)


def get_number(substring):
    digit = ""
    counter = 0
    
    while counter < len(substring) and str.isdigit(substring[counter]):
        digit += substring[counter]
        counter += 1
    
    return int(digit)


def draw_tree(img, sequence):
    draw = ImageDraw.Draw(img)

    alphabet_translation = defaultdict(str, [
        ("P", 0),
        ("f", 300),
        ("r", DELTA),
        ("l", -DELTA),
    ])

    states = deque()
    #state = (WIDTH/2, HEIGHT - HEIGHT/8, 0)
    state = (WIDTH/2, HEIGHT/2, 0)

    for i, ch in enumerate(sequence):
        
        if ch == "f":
            g = get_number(sequence[i+1:])
            step_size = calculate_step_size(g)
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


def rewrite(sequence, iterations):

    new_str = ""

    for i, ch in enumerate(sequence):
        if ch == "P":
            g = get_number(sequence[i+1:])
            new_str += axiom(g+1)
        elif ch.isdigit() and sequence[i-1] == "P":
            continue
        else:
            new_str += ch

    return new_str


#RULES = defaultdict(str, [("P", "f[rP]lP"),])
DELTA = math.radians(90)
AXIOM = "P0"

if __name__ == "__main__":

    iterations = -1

    while iterations < 0:
        iterations = int(input("Enter number of interations: "))

    while iterations > 0:
        AXIOM = rewrite(AXIOM, iterations)
        iterations -= 1

    print("axiom: ", AXIOM)

    img = create_image()
    img = draw_tree(img, AXIOM)
    img.save('./wip_images/h_tree.png')

    