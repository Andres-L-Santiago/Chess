class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moved = None

        if y == 0 or y == 7:
            if 0 <= x <= 4:
                self.num = 1
            else:
                self.num = 2
            if x == 0 or x == 7:
                self.piece_type = 'R'
            elif x == 1 or x == 6:
                self.piece_type = 'N'
            elif x == 2 or x == 5:
                self.piece_type = 'B'
            elif x == 3:
                self.piece_type = 'Q'
            elif x == 4:
                self.piece_type = 'K'
        elif y == 1 or y == 6:
            self.num = x + 1
            self.piece_type = 'P'
            self.moved = False
        else:
            self.side = None
            self.piece_type = None
            self.num = None

        if y == 0 or y == 1:
            self.side = 0
        elif y == 7 or y == 6:
            self.side = 1

        if self.piece_type == 'K' or self.piece_type == 'Q':
            self.text = self.piece_type
        elif self.piece_type:
            self.text = self.piece_type + str(self.num)
        else:
            self.text = '  '
# please undo