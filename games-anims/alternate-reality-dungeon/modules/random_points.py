import random

def get_random_target():
    rectangle1 = [(100, 160), (210, 160)]
    rectangle2 = [(150, 50), (210, 120)]
    
    area1 = (rectangle1[1][0] - rectangle1[0][0]) * (rectangle1[1][1] - rectangle1[0][1])
    area2 = (rectangle2[1][0] - rectangle2[0][0]) * (rectangle2[1][1] - rectangle2[0][1])
    
    total_area = area1 + area2
    
    random_number = random.uniform(0, total_area)
    
    if random_number < area1:
        chosen_rectangle = rectangle1
        offset = random_number
    else:
        chosen_rectangle = rectangle2
        offset = random_number - area1
    
    random_point = (
        int(chosen_rectangle[0][0] + offset / (chosen_rectangle[1][1] - chosen_rectangle[0][1])),
        int(chosen_rectangle[0][1] + offset % (chosen_rectangle[1][1] - chosen_rectangle[0][1]))
    )
    
    return random_point
