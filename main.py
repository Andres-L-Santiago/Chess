from os import system, name
from color import colors
from cells import Cell


def clear():

    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')


class game:

    # constants for row pieces
    ROYAL_ROW = ("R1", "N1", "B1", "Q", "K", "B2", "N2", "R2")
    PAWN_ROW = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8")

    # Creates chessboard to be modified later

    def board_initialize():
        # creates 8x8 matrix
        return [[Cell(x, y) for x in range(8)] for y in range(8)]

    def board_render(board, turn, **kwargs):
        moves = False
        if kwargs:
            moves = kwargs["moves"]
        # clears console
        clear()
        #prints title for chessboard
        print(colors.bg.black,
              "                                 Chess                                  ",
              sep="")
        print(colors.reset + colors.bg.black,
              "      a       b       c       d       e       f       g       h        ")
        # iterates through rows
        for row in range(8):
            # initializes row string with number and white space
            row_str = '    '
            row_str_text = f' {8 - row}  '
            # iterates through each piece in the row
            for piece in range(8):
                if board[row][piece].side == 0 and board[row][
                        piece].piece_type != None:
                    text_color = colors.fg.Dark_Ch
                elif board[row][piece].side == 1 and board[row][
                        piece].piece_type != None:
                    text_color = colors.fg.Light_Ch
                # calculates background color
                if moves and (row, piece) in moves:
                    back_color = colors.bg.On_IGreen
                elif moves and (row, piece, 1) in moves:
                    back_color = colors.bg.red
                elif row % 2 + piece % 2 == 1:
                    back_color = colors.bg.Dark_Ch
                else:
                    back_color = colors.bg.Light_Ch
                # prints queen or king pieces with extra space
                if board[row][piece].piece_type == "Q" or board[row][
                        piece].piece_type == "K":
                    row_str += f'{back_color}        {colors.reset + colors.bg.black}'
                    row_str_text += f'{back_color}   {text_color + board[row][piece].text}    {colors.reset + colors.bg.black}'
                # prints piece text
                else:
                    row_str += f'{back_color}        {colors.reset + colors.bg.black}'
                    row_str_text += f'{back_color}   {text_color + board[row][piece].text}   {colors.reset + colors.bg.black}'
            row_str += '    '
            row_str_text += f'  {8 - row} '
            print(row_str)
            print(row_str_text)
            print(row_str)
        # prints column labels at bottom of board
        print(colors.reset + colors.bg.black,
              "      a       b       c       d       e       f       g       h        ")

    def intro():
        # can you put the intro stuff in here
        print(
            '\nWelcome to chess. Both players will alternate making moves as prompted by the text. To make a move, enter the name of the piece to be moved (Ex: Knight 1 = N1) when prompted, and enter the position of the destination tile (Ex: a3) when prompted. Have fun!\n'
        )

    # checks if piece exists or what color it has
    def piece_check(board, text, color):
        exists = False
        for row in board:
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
    def piece_replace(piece_win, piece_lose):
        piece_lose.num, piece_win.num = piece_win.num, None
        piece_lose.side, piece_win.side = piece_win.side, None
        piece_lose.piece_type, piece_win.piece_type = piece_win.piece_type, None
        piece_lose.text, piece_win.text = piece_win.text, '  '
        if piece_win.piece_type == 'P':
            piece_lose.moved, piece_win.moved = True, None

    # checks whether position is a valid move
    # ex. same side piece results in invalid move position
    def valid_piece_check(board, y, x, color, moves):
        if board[y][x].side == color:
            return True
        elif board[y][x].piece_type == None:
            moves.append((y, x))
        elif board[y][x].side != color and board[y][x].piece_type != "K":
            moves.append((y, x, 1))
            return True

    # checks piece type and creates list of valid moves
    def valid_move(board, piece):
        x_coord, y_coord = piece.x, piece.y
        moves = []

        # creates list for pawn pieces
        if piece.piece_type == 'P':
            # finds direction of travel based on piece side
            dir = -2 * piece.side + 1
            # calls valid piece check function
            game.valid_piece_check(board, y_coord + dir, x_coord, piece.side,
                                   moves)
            # lets piece move two spaces if it hasn't moved before
            if not piece.moved:
                game.valid_piece_check(board, y_coord + 2 * dir, x_coord,
                                       piece.side, moves)
        # creates list for rook pieces
        elif piece.piece_type == "R":

            for space in range(y_coord - 1, -1, -1):
                if game.valid_piece_check(board, space, x_coord, piece.side,
                                          moves):
                    break

            for space in range(x_coord + 1, 8):
                if game.valid_piece_check(board, y_coord, space, piece.side,
                                          moves):
                    break

            for space in range(y_coord + 1, 8):
                if game.valid_piece_check(board, space, x_coord, piece.side,
                                          moves):
                    break

            for space in range(x_coord - 1, -1, -1):
                if game.valid_piece_check(board, y_coord, space, piece.side,
                                          moves):
                    break
        # creates list for knight pieces
        elif piece.piece_type == "N":

            if y_coord - 2 >= 0 and x_coord - 1 >= 0:
                game.valid_piece_check(board, y_coord - 2, x_coord - 1,
                                       piece.side, moves)

            if y_coord - 2 >= 0 and x_coord + 1 <= 7:
                game.valid_piece_check(board, y_coord - 2, x_coord + 1,
                                       piece.side, moves)

            if y_coord - 1 >= 0 and x_coord + 2 <= 7:
                game.valid_piece_check(board, y_coord - 1, x_coord + 2,
                                       piece.side, moves)

            if y_coord + 1 <= 7 and x_coord + 2 <= 7:
                game.valid_piece_check(board, y_coord + 1, x_coord + 2,
                                       piece.side, moves)

            if y_coord + 2 <= 7 and x_coord + 1 <= 7:
                game.valid_piece_check(board, y_coord + 2, x_coord + 1,
                                       piece.side, moves)

            if y_coord + 2 <= 7 and x_coord - 1 >= 0:
                game.valid_piece_check(board, y_coord + 2, x_coord - 1,
                                       piece.side, moves)

            if y_coord + 1 <= 7 and x_coord - 2 >= 0:
                game.valid_piece_check(board, y_coord + 1, x_coord - 2,
                                       piece.side, moves)

            if y_coord - 1 >= 0 and x_coord - 2 >= 0:
                game.valid_piece_check(board, y_coord - 1, x_coord - 2,
                                       piece.side, moves)
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
                if game.valid_piece_check(board, y_coord - 1 * space,
                                          x_coord - 1 * space, piece.side,
                                          moves):
                    break

            for space in range(top_right):
                space += 1
                if game.valid_piece_check(board, y_coord - 1 * space,
                                          x_coord + 1 * space, piece.side,
                                          moves):
                    break

            for space in range(bottom_right):
                space += 1
                if game.valid_piece_check(board, y_coord + 1 * space,
                                          x_coord + 1 * space, piece.side,
                                          moves):
                    break
            for space in range(bottom_left):
                space += 1
                if game.valid_piece_check(board, y_coord + 1 * space,
                                          x_coord - 1 * space, piece.side,
                                          moves):
                    break

        # creates list for queen pieces
        elif piece.piece_type == "Q":

            for space in range(y_coord - 1, -1, -1):
                if game.valid_piece_check(board, space, x_coord, piece.side,
                                          moves):
                    break

            for space in range(x_coord + 1, 8):
                if game.valid_piece_check(board, y_coord, space, piece.side,
                                          moves):
                    break

            for space in range(y_coord + 1, 8):
                if game.valid_piece_check(board, space, x_coord, piece.side,
                                          moves):
                    break

            for space in range(x_coord - 1, -1, -1):
                if game.valid_piece_check(board, y_coord, space, piece.side,
                                          moves):
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
                if game.valid_piece_check(board, y_coord - 1 * space,
                                          x_coord - 1 * space, piece.side,
                                          moves):
                    break

            for space in range(top_right):
                space += 1
                if game.valid_piece_check(board, y_coord - 1 * space,
                                          x_coord + 1 * space, piece.side,
                                          moves):
                    break

            for space in range(bottom_right):
                space += 1
                if game.valid_piece_check(board, y_coord + 1 * space,
                                          x_coord + 1 * space, piece.side,
                                          moves):
                    break

            for space in range(bottom_left):
                space += 1
                if game.valid_piece_check(board, y_coord + 1 * space,
                                          x_coord - 1 * space, piece.side,
                                          moves):
                    break

        # creates list for king pieces
        elif piece.piece_type == "K":
            if y_coord > 0 and x_coord > 0:
                game.valid_piece_check(board, y_coord - 1, x_coord - 1,
                                       piece.side, moves)

            if y_coord > 0:
                game.valid_piece_check(board, y_coord - 1, x_coord, piece.side,
                                       moves)

            if y_coord > 0 and x_coord < 7:
                game.valid_piece_check(board, y_coord - 1, x_coord + 1,
                                       piece.side, moves)

            if x_coord < 7:
                game.valid_piece_check(board, y_coord, x_coord + 1, piece.side,
                                       moves)

            if y_coord < 7 and x_coord < 7:
                game.valid_piece_check(board, y_coord + 1, x_coord + 1,
                                       piece.side, moves)

            if y_coord < 7:
                game.valid_piece_check(board, y_coord + 1, x_coord, piece.side,
                                       moves)

            if y_coord < 7 and x_coord > 0:
                game.valid_piece_check(board, y_coord + 1, x_coord - 1,
                                       piece.side, moves)

            if x_coord > 0:
                game.valid_piece_check(board, y_coord, x_coord - 1, piece.side,
                                       moves)

        return moves

    # manages user input
    def input(board, turn):
        pos = 'back'

        while pos == 'back':
            if turn:
                print('White, enter piece to be moved: ')
            else:
                print('Black, enter piece to be moved: ')

            Piece = None

            while (Piece not in game.ROYAL_ROW) and (Piece
                                                     not in game.PAWN_ROW):

                Piece = str(input('> '))

                if not Piece:
                    pass
                elif Piece[0] == 'p' or 'r' or 'n' or 'b' or 'q' or 'k':
                    Piece = Piece.capitalize()

                if not ((Piece in game.ROYAL_ROW) or (Piece in game.PAWN_ROW)):
                    print("You have not entered a valid piece. Try again.")

            # creates valid move list for selected piece
            for row in board:
                for piece in row:
                    if Piece == piece.text and turn == piece.side:
                        move_list = game.valid_move(board, piece)
                        piece_coord = (piece.x, piece.y)

            if move_list:
                # rerenders board with move list
                game.board_render(board, turn, moves=move_list)

                print('Enter where you want {} to move:'.format(Piece))
                print('(if you\'d like to change your piece, type "back")')

                while (len(pos) != 2) or (int(pos[1]) not in range(
                        1, 9)) or (pos[0] not in 'abcdefgh') and pos:

                    pos = input('> ')

                    if pos != 'back' and pos[0] in [
                            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'
                    ]:
                        pos_let = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                                   'h'].index(pos[0])
                        pos_num = int(pos[1])
                    if (len(pos) == 2) and ((int(pos[1]) in range(
                            1, 9))) and (pos[0] in 'abcdefgh'):
                        pass
                    elif pos != 'back':
                        print(
                            'You have not entered a valid position. Try again.'
                        )
                    elif pos == 'back':
                        break
                if pos != 'back':
                    pos_let = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                               'h'].index(pos[0])
                    pos_num = int(pos[1])
                    if (8 - pos_num, pos_let) not in move_list and (
                            8 - pos_num, pos_let, 1) not in move_list:
                        game.board_render(board, turn)
                        print(
                            'You have not entered a valid position. Try again.'
                        )
                        pos = 'back'
            else:
                game.board_render(board, turn)
                print("Piece has no valid movements.")

        pos_let = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].index(pos[0])
        pos_num = int(pos[1])
        return piece_coord, (pos_let, 8 - pos_num)

    def engine():
        turn = 1
        Chessboard = game.board_initialize()
        game.board_render(Chessboard, turn)
        game.intro()
        while True:
            ((x1, y1), (x2, y2)) = game.input(Chessboard, turn)
            game.piece_replace(Chessboard[y1][x1], Chessboard[y2][x2])
            game.board_render(Chessboard, turn)
            turn = -turn + 1


if __name__ == "__main__":
    game.engine()
