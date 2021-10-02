from cells import Cell
from color import Colors
from os import system, name


class Board:

    def clear(self):

        if name == 'nt':
            _ = system('cls')

        else:
            _ = system('clear')

    ROYAL_ROW = ("R1", "N1", "B1", "Q", "K", "B2", "N2", "R2")
    PAWN_ROW = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8")

    # Creates chessboard to be modified later
    def __init__(self):
        # creates 8x8 matrix
        self.board = [[Cell(x, y) for x in range(8)] for y in range(8)]

    def render(self, turn, **kwargs):
        moves = False
        attacks = False
        if kwargs:
            moves = kwargs["moves"]
            attacks = kwargs["attacks"]
        # clears console
        self.clear()
        #prints title for chessboard
        print(
            Colors.bg.black,
            "                                 Chess                                  ",
            sep="")
        print(
            Colors.reset + Colors.bg.black,
            "      a       b       c       d       e       f       g       h        "
        )
        # iterates through rows
        for row in range(8):
            # initializes row string with number and white space
            row_str = '    '
            row_str_text = f' {8 - row}  '
            # iterates through each piece in the row
            for piece in range(8):
                if self.board[row][piece].side == 0 and self.board[row][
                        piece].piece_type != None:
                    text_color = Colors.fg.Dark_Ch
                elif self.board[row][piece].side == 1 and self.board[row][
                        piece].piece_type != None:
                    text_color = Colors.fg.Light_Ch
                # calculates background color
                if moves and (row, piece) in moves:
                    back_color = Colors.bg.On_IGreen
                elif attacks and (row, piece) in attacks:
                    back_color = Colors.bg.red
                elif row % 2 + piece % 2 == 1:
                    back_color = Colors.bg.Dark_Ch
                else:
                    back_color = Colors.bg.Light_Ch
                # prints queen or king pieces with extra space
                if self.board[row][piece].piece_type == "Q" or self.board[row][
                        piece].piece_type == "K":
                    row_str += f'{back_color}        {Colors.reset + Colors.bg.black}'
                    row_str_text += f'{back_color}   {text_color + self.board[row][piece].text}    {Colors.reset + Colors.bg.black}'
                # prints piece text
                else:
                    row_str += f'{back_color}        {Colors.reset + Colors.bg.black}'
                    row_str_text += f'{back_color}   {text_color + self.board[row][piece].text}   {Colors.reset + Colors.bg.black}'
            row_str += '    '
            row_str_text += f'  {8 - row} '
            print(row_str)
            print(row_str_text)
            print(row_str)
        # prints column labels at bottom of board
        print(
            Colors.reset + Colors.bg.black,
            "      a       b       c       d       e       f       g       h        "
        )

    def piece_check(self, text, color):
        exists = False
        for row in self.board:
            for piece in row:
                if piece.piece_type == text and piece.side == color:
                    exists = True
        return exists

    # swaps two pieces in the matrix
    def piece_swap(piece1, piece2):
        piece1.text, piece2.text = piece2.text, piece1.text
        piece1.piece_type, piece2.piece_type = piece2.piece_type, piece1.piece_type
        piece1.side, piece2.side = piece2.side, piece1.side

    # replaces piece lose with piece win
    def piece_replace(self, x1, y1, x2, y2):
        print(x1, y1, x2, y2)
        self.board[y1][x1].num, self.board[y2][x2].num = self.board[y2][
            x2].num, None
        self.board[y1][x1].side, self.board[y2][x2].side = self.board[y2][
            x2].side, None
        self.board[y1][x1].piece_type, self.board[y2][
            x2].piece_type = self.board[y2][x2].piece_type, None
        self.board[y1][x1].text, self.board[y2][x2].text = self.board[y2][
            x2].text, '  '
        if self.board[y1][x1].piece_type == 'P':
            self.board[y1][x1].moved, self.board[y2][x2].moved = True, None

    # checks whether position is a valid move
    # ex. same side piece results in invalid move position
    def valid_piece_check(self, y, x, color, moves, attacks):
        if self.board[y][x].side == color:
            return True
        elif self.board[y][x].piece_type == None:
            moves.append((y, x))
        elif self.board[y][x].side != color and self.board[y][
                x].piece_type != "K":
            attacks.append((y, x))
            return True

    def valid_move(self, piece):
        x_coord, y_coord = piece.x, piece.y
        moves = []
        attacks = []

        # creates list for pawn pieces
        if piece.piece_type == 'P':
            # finds direction of travel based on piece side
            dir = -2 * piece.side + 1
            # calls valid piece check function
            self.valid_piece_check(y_coord + dir, x_coord, piece.side, moves,
                                   attacks)
            # lets piece move two spaces if it hasn't moved before
            if not piece.moved:
                self.valid_piece_check(y_coord + 2 * dir, x_coord, piece.side,
                                       moves, attacks)
            # checks for diagonal attacks
            if x_coord - 1 >= 0 and self.board[y_coord + dir][x_coord - 1].piece_type:
              attacks.append((y_coord + dir, x_coord - 1))
            if x_coord + 1 <= 7 and self.board[y_coord + dir][x_coord + 1].piece_type:
              attacks.append((y_coord + dir, x_coord - 1))
        # creates list for rook pieces
        elif piece.piece_type == "R":

            for space in range(y_coord - 1, -1, -1):
                if self.valid_piece_check(space, x_coord, piece.side, moves,
                                          attacks):
                    break

            for space in range(x_coord + 1, 8):
                if self.valid_piece_check(y_coord, space, piece.side, moves,
                                          attacks):
                    break

            for space in range(y_coord + 1, 8):
                if self.valid_piece_check(space, x_coord, piece.side, moves,
                                          attacks):
                    break

            for space in range(x_coord - 1, -1, -1):
                if self.valid_piece_check(y_coord, space, piece.side, moves,
                                          attacks):
                    break
        # creates list for knight pieces
        elif piece.piece_type == "N":

            if y_coord - 2 >= 0 and x_coord - 1 >= 0:
                self.valid_piece_check(y_coord - 2, x_coord - 1, piece.side,
                                       moves, attacks)

            if y_coord - 2 >= 0 and x_coord + 1 <= 7:
                self.valid_piece_check(y_coord - 2, x_coord + 1, piece.side,
                                       moves, attacks)

            if y_coord - 1 >= 0 and x_coord + 2 <= 7:
                self.valid_piece_check(y_coord - 1, x_coord + 2, piece.side,
                                       moves, attacks)

            if y_coord + 1 <= 7 and x_coord + 2 <= 7:
                self.valid_piece_check(y_coord + 1, x_coord + 2, piece.side,
                                       moves, attacks)

            if y_coord + 2 <= 7 and x_coord + 1 <= 7:
                self.valid_piece_check(y_coord + 2, x_coord + 1, piece.side,
                                       moves, attacks)

            if y_coord + 2 <= 7 and x_coord - 1 >= 0:
                self.valid_piece_check(y_coord + 2, x_coord - 1, piece.side,
                                       moves, attacks)

            if y_coord + 1 <= 7 and x_coord - 2 >= 0:
                self.valid_piece_check(y_coord + 1, x_coord - 2, piece.side,
                                       moves, attacks)

            if y_coord - 1 >= 0 and x_coord - 2 >= 0:
                self.valid_piece_check(y_coord - 1, x_coord - 2, piece.side,
                                       moves, attacks)
        # creates list for bishop pieces
        elif piece.piece_type == "B":

            if y_coord < x_coord:
                top_left = y_coord
                bottom_right = 7 - x_coord
            else:
                top_left = x_coord
                bottom_right = 7 - y_coord

            if y_coord < 7 - x_coord:
                top_right = y_coord
                bottom_left = x_coord
            else:
                top_right = 7 - x_coord
                bottom_left = 7 - y_coord

            for space in range(top_left):
                space += 1
                if self.valid_piece_check(y_coord - 1 * space,
                                          x_coord - 1 * space, piece.side,
                                          moves, attacks):
                    break

            for space in range(top_right):
                space += 1
                if self.valid_piece_check(y_coord - 1 * space,
                                          x_coord + 1 * space, piece.side,
                                          moves, attacks):
                    break

            for space in range(bottom_right):
                space += 1
                if self.valid_piece_check(y_coord + 1 * space,
                                          x_coord + 1 * space, piece.side,
                                          moves, attacks):
                    break
            for space in range(bottom_left):
                space += 1
                if self.valid_piece_check(y_coord + 1 * space,
                                          x_coord - 1 * space, piece.side,
                                          moves, attacks):
                    break

        # creates list for queen pieces
        elif piece.piece_type == "Q":

            for space in range(y_coord - 1, -1, -1):
                if self.valid_piece_check(space, x_coord, piece.side, moves,
                                          attacks):
                    break

            for space in range(x_coord + 1, 8):
                if self.valid_piece_check(y_coord, space, piece.side, moves,
                                          attacks):
                    break

            for space in range(y_coord + 1, 8):
                if self.valid_piece_check(space, x_coord, piece.side, moves,
                                          attacks):
                    break

            for space in range(x_coord - 1, -1, -1):
                if self.valid_piece_check(y_coord, space, piece.side, moves,
                                          attacks):
                    break

            if y_coord < x_coord:
                top_left = y_coord
                bottom_right = 7 - x_coord
            else:
                top_left = x_coord
                bottom_right = 7 - y_coord

            if y_coord < 7 - x_coord:
                top_right = y_coord
                bottom_left = x_coord
            else:
                top_right = 7 - x_coord
                bottom_left = 7 - y_coord

            for space in range(top_left):
                space += 1
                if self.valid_piece_check(y_coord - 1 * space,
                                          x_coord - 1 * space, piece.side,
                                          moves, attacks):
                    break

            for space in range(top_right):
                space += 1
                if self.valid_piece_check(y_coord - 1 * space,
                                          x_coord + 1 * space, piece.side,
                                          moves, attacks):
                    break

            for space in range(bottom_right):
                space += 1
                if self.valid_piece_check(y_coord + 1 * space,
                                          x_coord + 1 * space, piece.side,
                                          moves, attacks):
                    break

            for space in range(bottom_left):
                space += 1
                if self.valid_piece_check(y_coord + 1 * space,
                                          x_coord - 1 * space, piece.side,
                                          moves, attacks):
                    break

        # creates list for king pieces
        elif piece.piece_type == "K":
            if y_coord > 0 and x_coord > 0:
                self.valid_piece_check(y_coord - 1, x_coord - 1, piece.side,
                                       moves, attacks)

            if y_coord > 0:
                self.valid_piece_check(y_coord - 1, x_coord, piece.side, moves,
                                       attacks)

            if y_coord > 0 and x_coord < 7:
                self.valid_piece_check(y_coord - 1, x_coord + 1, piece.side,
                                       moves, attacks)

            if x_coord < 7:
                self.valid_piece_check(y_coord, x_coord + 1, piece.side, moves,
                                       attacks)

            if y_coord < 7 and x_coord < 7:
                self.valid_piece_check(y_coord + 1, x_coord + 1, piece.side,
                                       moves, attacks)

            if y_coord < 7:
                self.valid_piece_check(y_coord + 1, x_coord, piece.side, moves,
                                       attacks)

            if y_coord < 7 and x_coord > 0:
                self.valid_piece_check(y_coord + 1, x_coord - 1, piece.side,
                                       moves, attacks)

            if x_coord > 0:
                self.valid_piece_check(y_coord, x_coord - 1, piece.side, moves,
                                       attacks)

        return moves, attacks
