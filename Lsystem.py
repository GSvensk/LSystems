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


def draw_tree(img, string):
    draw = ImageDraw.Draw(img)

    alphabet_translation = defaultdict(str, [
        ("P", 50),
        ("f", 50),
        ("r", DELTA),
        ("l", -DELTA),
    ])

    states = deque()
    state = (WIDTH/2, HEIGHT - HEIGHT/8, 0)

    for ch in string:
        
        if ch in ("f", "P"):
            state = draw_branch(draw, state[0], state[1], alphabet_translation[ch], state[2])
        elif ch == "[":
            states.append(state)
        elif ch == "]":
            state = states.pop()
        else:
            state = (state[0], state[1], state[2] + alphabet_translation[ch])

    return img


def rewrite(string):

    new_str = ""

    for ch in string:
        if ch == "P":
            new_str += "f[rP]lP"
        else:
            new_str += ch

    return new_str


RULES = defaultdict(str, [("P", "f[rP]lP"),])
DELTA = math.radians(30)
AXIOM = "P"

if __name__ == "__main__":

    iterations = -1

    while iterations < 0:
        iterations = int(input("Enter number of interations: "))

    while iterations > 0:
        AXIOM = rewrite(AXIOM)
        iterations -= 1

    img = create_image()
    img = draw_tree(img, AXIOM)
    img.save('./wip_images/probabilistic_tree.png')

    