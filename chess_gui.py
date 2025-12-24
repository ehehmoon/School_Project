import tkinter as tk
import chess
import chess.engine
from PIL import Image, ImageTk
import os
from plyer import notification

class ChessAI:
    def __init__(self, depth = 3, engine_path = 'stockfish/stockfish-windows-x86-64-avx2.exe'):
        self.depth = depth
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    def get_best_move(self, board):
        result = self.engine.play(board, chess.engine.Limit(depth=self.depth))
        return result.move

    def __del__(self):
        self.engine.quit()

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("체스 게임")
        self.root.geometry("480x520")  # 전체 창 크기 설정
        
        self.start_frame = tk.Frame(root, width=480, height=520)
        self.start_frame.pack(expand=True, fill=tk.BOTH)
        
        self.title_label = tk.Label(self.start_frame, text="체스 게임!", font=("맑은 고딕(본문)", 48, "bold"))
        self.title_label.pack(pady=100)
        
        self.start_button = tk.Button(self.start_frame, text="시작하기", command=self.start_game, font=("맑은 고딕(본문)", 24), padx=20, pady=10)
        self.start_button.pack(pady=50)
        
        self.game_frame = tk.Frame(root)
        
        self.board = chess.Board()
        self.ai = ChessAI(depth=3, engine_path='stockfish/stockfish-windows-x86-64-avx2.exe')

        self.canvas = tk.Canvas(self.game_frame, width=480, height=520)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.images = {}
        self.load_images()
        
        self.move_from = None

    def start_game(self):
        self.start_frame.pack_forget()
        self.game_frame.pack()
        self.update_board()
        
    def load_images(self):
        pieces = ['br', 'bn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wq', 'wk', 'wp']
        base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = f'{base_path}/images'
        for piece in pieces:
            try:
                image = Image.open(os.path.join(base_path, f"{piece}.png"))
                image = image.resize((60, 60), Image.LANCZOS)
                self.images[piece] = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                print(f"주의: {piece}를 위한 이미지 파일이 존재하지 않음.")

    def show_check_notification(self):
        """체크 상태일 때 알림 표시"""
        turn = "White" if self.board.turn else "Black"
        notification.notify(
            title='체크!',
            message=f'{turn}이(가) 체크 상태입니다!',
            app_name='Chess',
            app_icon='images/ban.ico',
            timeout=5,
        )

    def update_board(self):
        self.canvas.delete("all")
        for i in range(64):
            x = (i % 8) * 60
            y = (7 - (i // 8)) * 60
            color = "white" if (i + i // 8) % 2 == 0 else "gray"
            
            # 선택된 기물 하이라이트
            if self.move_from is not None and i == self.move_from:
                color = "lightblue"
            
            self.canvas.create_rectangle(x, y, x + 60, y + 60, fill=color)

            piece = self.board.piece_at(i)
            if piece:
                piece_symbol = piece.symbol().lower()
                color = 'w' if piece.color else 'b'
                piece_image = self.images.get(color + piece_symbol)
                if piece_image:
                    self.canvas.create_image(x + 30, y + 30, image=piece_image)
        
        # 이동 가능한 위치에 노란 원 표시
        if self.move_from is not None:
            for move in self.board.legal_moves:
                if move.from_square == self.move_from:
                    target_x = (move.to_square % 8) * 60
                    target_y = (7 - (move.to_square // 8)) * 60
                    self.canvas.create_oval(target_x + 20, target_y + 20, target_x + 40, target_y + 40, fill="#ffffaa", outline="")

        turn = "White" if self.board.turn else "Black"
        self.canvas.create_text(240, 490, text=f"차례: {turn}", fill="black")

        if self.board.is_checkmate():
            if turn == "White":
                self.root.title("체스 게임 - 패배하셨습니다")
            else:
                self.root.title("체스 게임 - 승리하셨습니다")
            
            self.canvas.create_text(240, 510, text=f"체크메이트! {turn} 패배!", fill="red", font=("맑은 고딕(본문)", 15, "bold"))

        elif self.board.is_stalemate():
            self.root.title("체스 게임 - 무승부입니다")
            self.canvas.create_text(240, 510, text=f"스타일메이트! 무승부!", fill="blue", font=("맑은 고딕(본문)", 15, "bold"))
        
        # 체크 상태 확인 및 알림
        elif self.board.is_check():
            self.show_check_notification()

    def on_click(self, event):
        if self.board.is_game_over():
            return

        square_size = 60
        x = event.x // square_size
        y = 7 - event.y // square_size
        square = chess.square(x, y)

        if self.move_from is not None:
            move = chess.Move(self.move_from, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_from = None
                self.update_board()
                if not self.board.is_game_over():
                    self.make_ai_move()
            else:
                notification.notify(
                    title = '경고',
                    message = '유효하지 않은 움직임입니다.',
                    app_name = 'Chess',
                    app_icon = 'images/ban.ico',
                    timeout = 5,
                )
                self.move_from = None
                self.update_board()
        else:
            piece = self.board.piece_at(square)
            if piece is not None and piece.color == self.board.turn:
                self.move_from = square
                self.update_board()

    def make_ai_move(self):
        ai_move = self.ai.get_best_move(self.board)
        if ai_move:
            self.board.push(ai_move)
            self.update_board()

root = tk.Tk()
app = ChessApp(root)
root.mainloop()
