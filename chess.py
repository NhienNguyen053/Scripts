from copy import deepcopy
import random

# ============================================================
# CONSTANTS
# ============================================================

WHITE = "white"
BLACK = "black"

PIECES = {
    WHITE: {
        "king": "♔",
        "queen": "♕",
        "rook": "♖",
        "bishop": "♗",
        "knight": "♘",
        "pawn": "♙",
    },
    BLACK: {
        "king": "♚",
        "queen": "♛",
        "rook": "♜",
        "bishop": "♝",
        "knight": "♞",
        "pawn": "♟",
    },
}

BACK_RANK = [
    "rook",
    "knight",
    "bishop",
    "queen",
    "king",
    "bishop",
    "knight",
    "rook",
]

PIECE_VALUES = {
    "pawn": 100,
    "knight": 320,
    "bishop": 330,
    "rook": 500,
    "queen": 900,
    "king": 20_000,
}


# ============================================================
# POSITIONAL TABLES
# ============================================================

PAWN_TABLE = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    10,
    10,
    20,
    30,
    30,
    20,
    10,
    10,
    5,
    5,
    10,
    25,
    25,
    10,
    5,
    5,
    0,
    0,
    0,
    20,
    20,
    0,
    0,
    0,
    5,
    -5,
    -10,
    0,
    0,
    -10,
    -5,
    5,
    5,
    10,
    10,
    -20,
    -20,
    10,
    10,
    5,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

KNIGHT_TABLE = [
    -50,
    -40,
    -30,
    -30,
    -30,
    -30,
    -40,
    -50,
    -40,
    -20,
    0,
    0,
    0,
    0,
    -20,
    -40,
    -30,
    0,
    10,
    15,
    15,
    10,
    0,
    -30,
    -30,
    5,
    15,
    20,
    20,
    15,
    5,
    -30,
    -30,
    0,
    15,
    20,
    20,
    15,
    0,
    -30,
    -30,
    5,
    10,
    15,
    15,
    10,
    5,
    -30,
    -40,
    -20,
    0,
    5,
    5,
    0,
    -20,
    -40,
    -50,
    -40,
    -30,
    -30,
    -30,
    -30,
    -40,
    -50,
]

BISHOP_TABLE = [
    -20,
    -10,
    -10,
    -10,
    -10,
    -10,
    -10,
    -20,
    -10,
    0,
    0,
    0,
    0,
    0,
    0,
    -10,
    -10,
    0,
    5,
    10,
    10,
    5,
    0,
    -10,
    -10,
    5,
    5,
    10,
    10,
    5,
    5,
    -10,
    -10,
    0,
    10,
    10,
    10,
    10,
    0,
    -10,
    -10,
    10,
    10,
    10,
    10,
    10,
    10,
    -10,
    -10,
    5,
    0,
    0,
    0,
    0,
    5,
    -10,
    -20,
    -10,
    -10,
    -10,
    -10,
    -10,
    -10,
    -20,
]

ROOK_TABLE = [
    0,
    0,
    0,
    5,
    5,
    0,
    0,
    0,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    5,
    10,
    10,
    10,
    10,
    10,
    10,
    5,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

QUEEN_TABLE = [
    -20,
    -10,
    -10,
    -5,
    -5,
    -10,
    -10,
    -20,
    -10,
    0,
    0,
    0,
    0,
    0,
    0,
    -10,
    -10,
    0,
    5,
    5,
    5,
    5,
    0,
    -10,
    -5,
    0,
    5,
    5,
    5,
    5,
    0,
    -5,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    -5,
    -10,
    5,
    5,
    5,
    5,
    5,
    0,
    -10,
    -10,
    0,
    5,
    0,
    0,
    0,
    0,
    -10,
    -20,
    -10,
    -10,
    -5,
    -5,
    -10,
    -10,
    -20,
]

KING_TABLE = [
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -20,
    -30,
    -30,
    -40,
    -40,
    -30,
    -30,
    -20,
    -10,
    -20,
    -20,
    -20,
    -20,
    -20,
    -20,
    -10,
    20,
    20,
    0,
    0,
    0,
    0,
    20,
    20,
    20,
    30,
    10,
    0,
    0,
    10,
    30,
    20,
]

POSITION_TABLES = {
    "pawn": PAWN_TABLE,
    "knight": KNIGHT_TABLE,
    "bishop": BISHOP_TABLE,
    "rook": ROOK_TABLE,
    "queen": QUEEN_TABLE,
    "king": KING_TABLE,
}


# ============================================================
# HELPERS
# ============================================================


def opposite(color):
    return BLACK if color == WHITE else WHITE


def in_bounds(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def same_position(a, b):
    return a[0] == b[0] and a[1] == b[1]


def position_to_notation(row, col):
    return f"{chr(ord('a') + col)}{8 - row}"


def notation_to_position(value):
    if len(value) != 2:
        return None

    file = value[0]
    rank = value[1]

    if file < "a" or file > "h":
        return None

    if rank < "1" or rank > "8":
        return None

    return (8 - int(rank), ord(file) - ord("a"))


# ============================================================
# CHESS GAME
# ============================================================


class ChessGame:

    def __init__(self):
        self.board = self.create_board()
        self.turn = WHITE
        self.en_passant_target = None
        self.history = []

    # --------------------------------------------------------
    # BOARD
    # --------------------------------------------------------

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        for col in range(8):
            board[0][col] = {
                "type": BACK_RANK[col],
                "color": BLACK,
            }

            board[1][col] = {
                "type": "pawn",
                "color": BLACK,
            }

            board[6][col] = {
                "type": "pawn",
                "color": WHITE,
            }

            board[7][col] = {
                "type": BACK_RANK[col],
                "color": WHITE,
            }

        return board

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    def print_board(self):
        print()
        print("    a b c d e f g h")
        print("  +-----------------+")

        for row in range(8):
            line = f"{8 - row} |"

            for col in range(8):
                piece = self.board[row][col]

                if piece is None:
                    line += " ·"
                else:
                    line += " " + PIECES[piece["color"]][piece["type"]]

            line += f" | {8 - row}"

            print(line)

        print("  +-----------------+")
        print("    a b c d e f g h")
        print()

    # --------------------------------------------------------
    # KING
    # --------------------------------------------------------

    def find_king(self, color, board=None):
        if board is None:
            board = self.board

        for row in range(8):
            for col in range(8):
                piece = board[row][col]

                if piece and piece["color"] == color and piece["type"] == "king":
                    return row, col

        return None

    # --------------------------------------------------------
    # ATTACK DETECTION
    # --------------------------------------------------------

    def is_square_attacked(self, row, col, by_color, board=None):
        if board is None:
            board = self.board

        # Pawns
        direction = -1 if by_color == WHITE else 1

        for dc in (-1, 1):
            r = row - direction
            c = col - dc

            if not in_bounds(r, c):
                continue

            piece = board[r][c]

            if piece and piece["color"] == by_color and piece["type"] == "pawn":
                return True

        # Knights
        knight_moves = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]

        for dr, dc in knight_moves:
            r = row + dr
            c = col + dc

            if not in_bounds(r, c):
                continue

            piece = board[r][c]

            if piece and piece["color"] == by_color and piece["type"] == "knight":
                return True

        # King
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):

                if dr == 0 and dc == 0:
                    continue

                r = row + dr
                c = col + dc

                if not in_bounds(r, c):
                    continue

                piece = board[r][c]

                if piece and piece["color"] == by_color and piece["type"] == "king":
                    return True

        # Rooks / queens
        straight = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

        for dr, dc in straight:
            r = row + dr
            c = col + dc

            while in_bounds(r, c):
                piece = board[r][c]

                if piece:
                    if piece["color"] == by_color and piece["type"] in (
                        "rook",
                        "queen",
                    ):
                        return True

                    break

                r += dr
                c += dc

        # Bishops / queens
        diagonal = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        for dr, dc in diagonal:
            r = row + dr
            c = col + dc

            while in_bounds(r, c):
                piece = board[r][c]

                if piece:
                    if piece["color"] == by_color and piece["type"] in (
                        "bishop",
                        "queen",
                    ):
                        return True

                    break

                r += dr
                c += dc

        return False

    # --------------------------------------------------------
    # CHECK
    # --------------------------------------------------------

    def is_in_check(self, color, board=None):
        king = self.find_king(color, board)

        if king is None:
            return True

        return self.is_square_attacked(
            king[0],
            king[1],
            opposite(color),
            board,
        )

    # --------------------------------------------------------
    # PSEUDO LEGAL MOVES
    # --------------------------------------------------------

    def generate_pseudo_moves(
        self,
        row,
        col,
        color,
    ):
        piece = self.board[row][col]

        if not piece or piece["color"] != color:
            return []

        moves = []

        def add_move(
            to_row,
            to_col,
            promotion=None,
            castle=None,
            en_passant=False,
        ):
            if not in_bounds(to_row, to_col):
                return

            target = self.board[to_row][to_col]

            if target and target["color"] == color:
                return

            moves.append(
                {
                    "from": (row, col),
                    "to": (to_row, to_col),
                    "promotion": promotion,
                    "castle": castle,
                    "en_passant": en_passant,
                }
            )

        piece_type = piece["type"]

        # ====================================================
        # PAWN
        # ====================================================

        if piece_type == "pawn":

            direction = -1 if color == WHITE else 1
            start_row = 6 if color == WHITE else 1
            promotion_row = 0 if color == WHITE else 7

            forward = row + direction

            if in_bounds(forward, col) and self.board[forward][col] is None:
                if forward == promotion_row:

                    for promotion in (
                        "queen",
                        "rook",
                        "bishop",
                        "knight",
                    ):
                        add_move(
                            forward,
                            col,
                            promotion=promotion,
                        )
                else:
                    add_move(forward, col)

                # Double move
                two = row + direction * 2

                if row == start_row and self.board[two][col] is None:
                    add_move(two, col)

            # Captures
            for dc in (-1, 1):

                r = row + direction
                c = col + dc

                if not in_bounds(r, c):
                    continue

                target = self.board[r][c]

                if target and target["color"] != color:

                    if r == promotion_row:

                        for promotion in (
                            "queen",
                            "rook",
                            "bishop",
                            "knight",
                        ):
                            add_move(
                                r,
                                c,
                                promotion=promotion,
                            )
                    else:
                        add_move(r, c)

                # En passant
                if self.en_passant_target and same_position(
                    (r, c),
                    self.en_passant_target,
                ):
                    add_move(
                        r,
                        c,
                        en_passant=True,
                    )

        # ====================================================
        # KNIGHT
        # ====================================================

        elif piece_type == "knight":

            offsets = [
                (-2, -1),
                (-2, 1),
                (-1, -2),
                (-1, 2),
                (1, -2),
                (1, 2),
                (2, -1),
                (2, 1),
            ]

            for dr, dc in offsets:
                add_move(
                    row + dr,
                    col + dc,
                )

        # ====================================================
        # BISHOP / ROOK / QUEEN
        # ====================================================

        elif piece_type in (
            "bishop",
            "rook",
            "queen",
        ):

            directions = []

            if piece_type in (
                "bishop",
                "queen",
            ):
                directions.extend(
                    [
                        (-1, -1),
                        (-1, 1),
                        (1, -1),
                        (1, 1),
                    ]
                )

            if piece_type in (
                "rook",
                "queen",
            ):
                directions.extend(
                    [
                        (-1, 0),
                        (1, 0),
                        (0, -1),
                        (0, 1),
                    ]
                )

            for dr, dc in directions:

                r = row + dr
                c = col + dc

                while in_bounds(r, c):

                    target = self.board[r][c]

                    if target is None:
                        add_move(r, c)
                    else:

                        if target["color"] != color:
                            add_move(r, c)

                        break

                    r += dr
                    c += dc

        # ====================================================
        # KING
        # ====================================================

        elif piece_type == "king":

            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):

                    if dr == 0 and dc == 0:
                        continue

                    add_move(
                        row + dr,
                        col + dc,
                    )

            # Castling
            home_row = 7 if color == WHITE else 0

            if row == home_row and col == 4 and not self.is_in_check(color):

                # Kingside
                rook = self.board[home_row][7]

                if (
                    rook
                    and rook["type"] == "rook"
                    and rook["color"] == color
                    and self.board[home_row][5] is None
                    and self.board[home_row][6] is None
                    and not self.is_square_attacked(
                        home_row,
                        5,
                        opposite(color),
                    )
                    and not self.is_square_attacked(
                        home_row,
                        6,
                        opposite(color),
                    )
                ):
                    add_move(
                        home_row,
                        6,
                        castle="kingside",
                    )

                # Queenside
                rook = self.board[home_row][0]

                if (
                    rook
                    and rook["type"] == "rook"
                    and rook["color"] == color
                    and self.board[home_row][1] is None
                    and self.board[home_row][2] is None
                    and self.board[home_row][3] is None
                    and not self.is_square_attacked(
                        home_row,
                        3,
                        opposite(color),
                    )
                    and not self.is_square_attacked(
                        home_row,
                        2,
                        opposite(color),
                    )
                ):
                    add_move(
                        home_row,
                        2,
                        castle="queenside",
                    )

        return moves

    # --------------------------------------------------------
    # APPLY MOVE
    # --------------------------------------------------------

    def apply_move(self, move):

        from_row, from_col = move["from"]
        to_row, to_col = move["to"]

        piece = self.board[from_row][from_col]

        if piece is None:
            return

        self.board[from_row][from_col] = None

        # En passant capture
        if move.get("en_passant"):
            self.board[from_row][to_col] = None

        # Promotion
        self.board[to_row][to_col] = {
            "type": move.get("promotion") or piece["type"],
            "color": piece["color"],
        }

        # Castling
        if move.get("castle") == "kingside":

            rook = self.board[from_row][7]

            self.board[from_row][7] = None
            self.board[from_row][5] = rook

        elif move.get("castle") == "queenside":

            rook = self.board[from_row][0]

            self.board[from_row][0] = None
            self.board[from_row][3] = rook

    # --------------------------------------------------------
    # LEGAL MOVES
    # --------------------------------------------------------

    def legal_moves_from(
        self,
        row,
        col,
        color=None,
    ):
        if color is None:
            color = self.turn

        pseudo = self.generate_pseudo_moves(
            row,
            col,
            color,
        )

        legal = []

        for move in pseudo:

            original_board = self.board
            original_ep = self.en_passant_target

            self.board = deepcopy(original_board)

            self.apply_move(move)

            if not self.is_in_check(color):
                legal.append(move)

            self.board = original_board
            self.en_passant_target = original_ep

        return legal

    def all_legal_moves(self, color):

        result = []

        for row in range(8):
            for col in range(8):

                piece = self.board[row][col]

                if piece and piece["color"] == color:
                    result.extend(
                        self.legal_moves_from(
                            row,
                            col,
                            color,
                        )
                    )

        return result

    # --------------------------------------------------------
    # MAKE MOVE
    # --------------------------------------------------------

    def make_move(self, move):

        legal = self.legal_moves_from(
            move["from"][0],
            move["from"][1],
            self.turn,
        )

        selected = None

        for candidate in legal:

            if not same_position(
                candidate["to"],
                move["to"],
            ):
                continue

            if candidate.get("promotion") != move.get("promotion"):
                continue

            if candidate.get("castle") != move.get("castle"):
                continue

            if candidate.get("en_passant") != move.get("en_passant"):
                continue

            selected = candidate
            break

        if selected is None:
            return False

        self.history.append(
            {
                "board": deepcopy(self.board),
                "turn": self.turn,
                "en_passant_target": (
                    None
                    if self.en_passant_target is None
                    else tuple(self.en_passant_target)
                ),
            }
        )

        piece = self.board[selected["from"][0]][selected["from"][1]]

        self.apply_move(selected)

        self.en_passant_target = None

        if (
            piece
            and piece["type"] == "pawn"
            and abs(selected["to"][0] - selected["from"][0]) == 2
        ):
            self.en_passant_target = (
                (selected["from"][0] + selected["to"][0]) // 2,
                selected["from"][1],
            )

        self.turn = opposite(self.turn)

        return True

    # --------------------------------------------------------
    # UNDO
    # --------------------------------------------------------

    def undo(self):

        if not self.history:
            return False

        state = self.history.pop()

        self.board = state["board"]
        self.turn = state["turn"]
        self.en_passant_target = state["en_passant_target"]

        return True

    # --------------------------------------------------------
    # PARSE MOVE
    # --------------------------------------------------------

    def parse_move(self, text):

        parts = text.strip().lower().replace(",", " ").replace("-", " ").split()

        if len(parts) < 2:
            return None

        from_pos = notation_to_position(parts[0])
        to_pos = notation_to_position(parts[1])

        if from_pos is None or to_pos is None:
            return None

        promotion = None

        if len(parts) >= 3:

            promotions = {
                "q": "queen",
                "queen": "queen",
                "r": "rook",
                "rook": "rook",
                "b": "bishop",
                "bishop": "bishop",
                "n": "knight",
                "knight": "knight",
            }

            promotion = promotions.get(parts[2])

            if promotion is None:
                return None

        moves = self.legal_moves_from(
            from_pos[0],
            from_pos[1],
        )

        for move in moves:

            if not same_position(
                move["to"],
                to_pos,
            ):
                continue

            if move.get("promotion") != promotion:
                continue

            return move

        return None

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    def status(self):

        moves = self.all_legal_moves(self.turn)

        check = self.is_in_check(self.turn)

        if not moves:

            if check:
                return "checkmate"

            return "stalemate"

        if check:
            return "check"

        return "playing"


# ============================================================
# AI
# ============================================================


class ChessAI:

    def __init__(self, depth=3):
        self.depth = depth
        self.nodes = 0

    # --------------------------------------------------------
    # EVALUATION
    # --------------------------------------------------------

    def evaluate(self, game):

        score = 0

        for row in range(8):
            for col in range(8):

                piece = game.board[row][col]

                if piece is None:
                    continue

                value = PIECE_VALUES[piece["type"]]

                table = POSITION_TABLES[piece["type"]]

                table_row = row

                # Flip table for black.
                if piece["color"] == BLACK:
                    table_row = 7 - row

                positional = table[table_row * 8 + col]

                value += positional

                if piece["color"] == BLACK:
                    score += value
                else:
                    score -= value

        return score

    # --------------------------------------------------------
    # MINIMAX
    # --------------------------------------------------------

    def minimax(
        self,
        game,
        depth,
        alpha,
        beta,
        maximizing,
    ):
        self.nodes += 1

        status = game.status()

        if status == "checkmate":

            if game.turn == BLACK:
                return 1_000_000 + depth

            return -1_000_000 - depth

        if status == "stalemate":
            return 0

        if depth == 0:
            return self.evaluate(game)

        moves = game.all_legal_moves(game.turn)

        # Move ordering improves alpha-beta pruning.
        moves.sort(
            key=lambda move: self.move_priority(game, move),
            reverse=True,
        )

        if maximizing:

            best = -float("inf")

            for move in moves:

                original_board = deepcopy(game.board)

                original_turn = game.turn
                original_ep = game.en_passant_target

                game.apply_move(move)

                piece = original_board[move["from"][0]][move["from"][1]]

                game.en_passant_target = None

                if (
                    piece
                    and piece["type"] == "pawn"
                    and abs(move["to"][0] - move["from"][0]) == 2
                ):
                    game.en_passant_target = (
                        (move["from"][0] + move["to"][0]) // 2,
                        move["from"][1],
                    )

                game.turn = opposite(game.turn)

                value = self.minimax(
                    game,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                )

                game.board = original_board
                game.turn = original_turn
                game.en_passant_target = original_ep

                best = max(best, value)

                alpha = max(alpha, value)

                if beta <= alpha:
                    break

            return best

        else:

            best = float("inf")

            for move in moves:

                original_board = deepcopy(game.board)

                original_turn = game.turn
                original_ep = game.en_passant_target

                game.apply_move(move)

                piece = original_board[move["from"][0]][move["from"][1]]

                game.en_passant_target = None

                if (
                    piece
                    and piece["type"] == "pawn"
                    and abs(move["to"][0] - move["from"][0]) == 2
                ):
                    game.en_passant_target = (
                        (move["from"][0] + move["to"][0]) // 2,
                        move["from"][1],
                    )

                game.turn = opposite(game.turn)

                value = self.minimax(
                    game,
                    depth - 1,
                    alpha,
                    beta,
                    True,
                )

                game.board = original_board
                game.turn = original_turn
                game.en_passant_target = original_ep

                best = min(best, value)

                beta = min(beta, value)

                if beta <= alpha:
                    break

            return best

    # --------------------------------------------------------
    # MOVE PRIORITY
    # --------------------------------------------------------

    def move_priority(self, game, move):

        score = 0

        target = game.board[move["to"][0]][move["to"][1]]

        if target:
            score += PIECE_VALUES[target["type"]] * 10

        if move.get("promotion"):
            score += PIECE_VALUES[move["promotion"]]

        if move.get("castle"):
            score += 50

        return score + random.random()

    # --------------------------------------------------------
    # CHOOSE MOVE
    # --------------------------------------------------------

    def choose_move(self, game):

        moves = game.all_legal_moves(BLACK)

        if not moves:
            return None

        best_score = -float("inf")
        best_moves = []

        self.nodes = 0

        for move in moves:

            original_board = deepcopy(game.board)

            original_turn = game.turn
            original_ep = game.en_passant_target

            game.apply_move(move)

            piece = original_board[move["from"][0]][move["from"][1]]

            game.en_passant_target = None

            if (
                piece
                and piece["type"] == "pawn"
                and abs(move["to"][0] - move["from"][0]) == 2
            ):
                game.en_passant_target = (
                    (move["from"][0] + move["to"][0]) // 2,
                    move["from"][1],
                )

            game.turn = WHITE

            score = self.minimax(
                game,
                self.depth - 1,
                -float("inf"),
                float("inf"),
                False,
            )

            game.board = original_board
            game.turn = original_turn
            game.en_passant_target = original_ep

            if score > best_score:
                best_score = score
                best_moves = [move]

            elif score == best_score:
                best_moves.append(move)

        chosen = random.choice(best_moves)

        print(f"AI searched {self.nodes:,} positions.")

        return chosen


# ============================================================
# MOVE DISPLAY
# ============================================================


def describe_move(move):

    start = position_to_notation(
        move["from"][0],
        move["from"][1],
    )

    end = position_to_notation(
        move["to"][0],
        move["to"][1],
    )

    text = f"{start} {end}"

    if move.get("promotion"):
        text += " " + move["promotion"][0]

    return text


# ============================================================
# MAIN
# ============================================================


def main():

    print("=" * 40)
    print("          PYTHON CHESS AI")
    print("=" * 40)

    print()
    print("You are WHITE.")
    print("The computer is BLACK.")
    print()

    print("Difficulty:")
    print("  1 = Easy")
    print("  2 = Medium")
    print("  3 = Hard")
    print()

    difficulty = input("Choose difficulty [2]: ").strip()

    if difficulty == "1":
        depth = 2
    elif difficulty == "3":
        depth = 4
    else:
        depth = 3

    game = ChessGame()
    ai = ChessAI(depth)

    print()
    print("Move examples:")
    print("  e2 e4")
    print("  g1 f3")
    print("  e7 e8 q")
    print()
    print("Commands:")
    print("  undo")
    print("  board")
    print("  help")
    print("  quit")
    print()

    while True:

        game.print_board()

        status = game.status()

        # ----------------------------------------------------
        # GAME OVER
        # ----------------------------------------------------

        if status == "checkmate":

            winner = opposite(game.turn)

            print(f"CHECKMATE! " f"{winner.upper()} wins!")

            break

        if status == "stalemate":

            print("STALEMATE! Draw.")

            break

        if status == "check":

            print(f"{game.turn.upper()} is in CHECK!")

        # ----------------------------------------------------
        # PLAYER TURN
        # ----------------------------------------------------

        if game.turn == WHITE:

            text = input("Your move > ").strip()

            command = text.lower()

            if command in (
                "quit",
                "exit",
            ):
                print("Goodbye!")
                break

            if command == "board":
                continue

            if command == "help":

                print()
                print("Move:")
                print("  e2 e4")
                print()
                print("Promotion:")
                print("  e7 e8 q")
                print()
                print("Commands:")
                print("  undo")
                print("  board")
                print("  help")
                print("  quit")
                print()

                continue

            if command == "undo":

                # Undo both the AI move and
                # player's previous move.
                if len(game.history) >= 2:
                    game.undo()
                    game.undo()
                    print("Undid your last move.")
                else:
                    print("Nothing to undo.")

                continue

            move = game.parse_move(text)

            if move is None:
                print("Illegal move.")
                continue

            game.make_move(move)

        # ----------------------------------------------------
        # AI TURN
        # ----------------------------------------------------

        else:

            print("AI is thinking...")

            ai_move = ai.choose_move(game)

            if ai_move is None:
                continue

            print(
                "AI plays:",
                describe_move(ai_move),
            )

            game.make_move(ai_move)


if __name__ == "__main__":
    main()
