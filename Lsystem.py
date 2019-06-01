from draw_image import draw_figure
import json


def get_number(substring):
    digit = ""
    counter = 0
    
    while counter < len(substring) and str.isdigit(substring[counter]):
        digit += substring[counter]
        counter += 1
    
    if digit == "":
        return 0

    return int(digit)


def rewrite(sequence, iterations, rule):

    new_str = ""

    for i, ch in enumerate(sequence):
        if ch == "P":
            g = get_number(sequence[i+1:])
            new_str += rule["P"].replace("g", str(g+1))
        elif ch.isdigit() and sequence[i-1] == "P":
            continue
        else:
            new_str += ch

    return new_str



if __name__ == "__main__":

    with open("image_configs.json") as json_file:
        configs = json.load(json_file)
    
    motive = configs["h_tree"]
    axiom = motive["axiom"]
    rule = motive["rules"][0]

    iterations = -1

    while iterations < 0:
        iterations = int(input("Enter number of interations: "))

    while iterations > 0:
        axiom = rewrite(axiom, iterations, rule)
        iterations -= 1

    draw_figure.draw_from_config(motive, axiom, "h_tree_test")
