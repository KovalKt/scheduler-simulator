
CIRCLE_SIZE = 36
CIRCLE_R = CIRCLE_SIZE/2

class Node():
    def __init__(self, id, center_x, center_y):
        self.id = id
        self.x = center_x - CIRCLE_R
        self.y = center_y - CIRCLE_R
        self.center_x = center_x
        self.center_y = center_y
        self.weight = 0

    def is_selected(self, x1, y1):
        return (x1 < (self.center_x + CIRCLE_R) and x1 > (self.center_x - CIRCLE_R) and 
            y1 < (self.center_y + CIRCLE_R) and y1 > (self.center_y - CIRCLE_R))

    def set_weight(self, weight):
        self.weight = weight

    def set_new_coordinate(self, new_x, new_y):
        self.center_x = new_x
        self.center_y = new_y
        self.x = new_x - CIRCLE_R
        self.y = new_y - CIRCLE_R
