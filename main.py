from board import Board


class Game:


    # constants for row pieces
    ROYAL_ROW = ("R1", "N1", "B1", "Q", "K", "B2", "N2", "R2")
    PAWN_ROW = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8")

    points = [0, 0]
    game_moves = []

    @staticmethod
    def intro():
        # can you put the intro stuff in here
        print(
            '\nWelcome to chess. Both players will alternate making moves as prompted by the text. To make a move, enter the name of the piece to be moved (Ex: Knight 1 = N1) when prompted, and enter the position of the destination tile (Ex: a3) when prompted. Have fun!\n'
        )

    # manages user input
    @classmethod
    def input(self, board, turn):
        pos = 'back'

        while pos == 'back':
            if turn:
                print('White, enter piece to be moved: ')
            else:
                print('Black, enter piece to be moved: ')

            Piece = None

            while (Piece not in self.ROYAL_ROW) and (Piece
                                                     not in self.PAWN_ROW):

                Piece = str(input('> '))

                if not Piece:
                    pass
                elif Piece[0] == 'p' or 'r' or 'n' or 'b' or 'q' or 'k':
                    Piece = Piece.capitalize()

                if not ((Piece in self.ROYAL_ROW) or (Piece in self.PAWN_ROW)):
                    print("You have not entered a valid piece. Try again.")

            # creates valid move list for selected piece
            for row in board.board:
                for piece in row:
                    if Piece == piece.text and turn == piece.side:
                        move_list, attack_list = board.valid_move(piece)
                        piece_coord = (piece.x, piece.y)

            if move_list or attack_list:
                # re-renders board with move list
                board.render(turn, moves=move_list, attacks=attack_list)

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
                            8 - pos_num, pos_let) not in attack_list:
                        board.render(turn)
                        print(
                            'You have not entered a valid position. Try again.'
                        )
                        pos = 'back'
            else:
                board.render(board, turn)
                print("Piece has no valid movements.")

        pos_let = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].index(pos[0])
        pos_num = int(pos[1])
        return piece_coord, (pos_let, 8 - pos_num)

    @classmethod
    def engine(self):
        turn = 1
        chessboard = Board()
        chessboard.render(turn)
        self.intro()
        while True:
            ((x1, y1), (x2, y2)) = self.input(chessboard, turn)
            chessboard.piece_replace(x2, y2, x1, y1, self.points)
            chessboard.render(turn)
            print(self.points)
            turn = -turn + 1


if __name__ == "__main__":
    Game.engine()
