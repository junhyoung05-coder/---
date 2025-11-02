"""
테트리스 환경 (Tetris Environment)
AI 학습을 위한 테트리스 게임 환경

이 파일은 강화학습 AI가 테트리스를 학습할 수 있도록 설계된 환경입니다.
OpenAI Gym 스타일의 인터페이스를 제공합니다.
"""

import numpy as np
import random
from typing import Tuple, List, Optional


# 테트리스 블록 모양 정의 (Tetromino Shapes)
# 각 블록은 4x4 그리드에서 정의되며, 1은 블록이 있는 위치를 나타냅니다
SHAPES = {
    'I': np.array([
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]),
    'O': np.array([
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]),
    'T': np.array([
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0]
    ]),
    'S': np.array([
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0]
    ]),
    'Z': np.array([
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]),
    'J': np.array([
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0]
    ]),
    'L': np.array([
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0]
    ])
}

# 블록 색상 정의 (선택적으로 사용)
COLORS = {
    'I': 1,  # 하늘색
    'O': 2,  # 노란색
    'T': 3,  # 보라색
    'S': 4,  # 초록색
    'Z': 5,  # 빨간색
    'J': 6,  # 파란색
    'L': 7   # 주황색
}


class TetrisEnv:
    """
    테트리스 게임 환경 클래스
    
    이 클래스는 AI 에이전트가 테트리스를 학습할 수 있도록
    게임 상태, 행동, 보상 등을 관리합니다.
    
    주요 속성:
        board: 게임 보드 (높이 x 너비의 2D 배열)
        current_piece: 현재 떨어지는 블록
        current_pos: 현재 블록의 위치 [x, y]
        score: 현재 점수
        lines_cleared: 클리어된 라인 수
        game_over: 게임 종료 여부
    """
    
    def __init__(self, width: int = 10, height: int = 20):
        """
        테트리스 환경 초기화
        
        Args:
            width: 보드의 너비 (기본값: 10)
            height: 보드의 높이 (기본값: 20)
        """
        self.width = width
        self.height = height
        self.board = None
        self.current_piece = None
        self.current_piece_type = None
        self.current_pos = None
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.piece_list = list(SHAPES.keys())
        
        # 게임 초기화
        self.reset()
    
    def reset(self) -> np.ndarray:
        """
        게임을 초기 상태로 리셋
        
        Returns:
            초기 게임 보드 상태 (numpy array)
        """
        # 빈 보드 생성 (모든 셀이 0으로 초기화)
        self.board = np.zeros((self.height, self.width), dtype=int)
        
        # 점수 및 상태 초기화
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        
        # 첫 번째 블록 생성
        self._spawn_piece()
        
        return self._get_state()
    
    def _spawn_piece(self):
        """
        새로운 블록을 생성하고 보드 상단에 배치
        
        랜덤하게 블록 타입을 선택하고 보드 중앙 상단에 위치시킵니다.
        만약 새 블록이 기존 블록과 겹치면 게임 오버입니다.
        """
        # 랜덤하게 블록 타입 선택
        self.current_piece_type = random.choice(self.piece_list)
        self.current_piece = SHAPES[self.current_piece_type].copy()
        
        # 블록을 보드 중앙 상단에 배치
        self.current_pos = [0, self.width // 2 - 2]
        
        # 새 블록이 기존 블록과 겹치는지 확인 (게임 오버 조건)
        if self._check_collision(self.current_piece, self.current_pos):
            self.game_over = True
    
    def _check_collision(self, piece: np.ndarray, pos: List[int]) -> bool:
        """
        블록이 보드나 다른 블록과 충돌하는지 확인
        
        Args:
            piece: 확인할 블록 (4x4 numpy array)
            pos: 블록의 위치 [row, col]
            
        Returns:
            충돌하면 True, 아니면 False
        """
        piece_h, piece_w = piece.shape
        
        for i in range(piece_h):
            for j in range(piece_w):
                if piece[i][j]:  # 블록이 있는 위치만 확인
                    # 블록의 실제 보드 상 위치 계산
                    board_row = pos[0] + i
                    board_col = pos[1] + j
                    
                    # 보드 경계를 벗어나는지 확인
                    if board_row >= self.height:
                        return True
                    if board_col < 0 or board_col >= self.width:
                        return True
                    
                    # 보드 내부에서 다른 블록과 겹치는지 확인
                    if board_row >= 0 and self.board[board_row][board_col]:
                        return True
        
        return False
    
    def _merge_piece(self):
        """
        현재 블록을 보드에 고정시킴
        
        블록이 더 이상 아래로 이동할 수 없을 때 호출되며,
        블록을 보드에 병합하고 완성된 라인을 확인합니다.
        """
        piece_h, piece_w = self.current_piece.shape
        
        for i in range(piece_h):
            for j in range(piece_w):
                if self.current_piece[i][j]:
                    board_row = self.current_pos[0] + i
                    board_col = self.current_pos[1] + j
                    
                    # 보드 범위 내에 있는 경우에만 병합
                    if 0 <= board_row < self.height:
                        # 블록 타입에 따른 색상 값 저장
                        self.board[board_row][board_col] = COLORS[self.current_piece_type]
        
        # 완성된 라인 제거
        self._clear_lines()
    
    def _clear_lines(self) -> int:
        """
        완성된 라인을 찾아서 제거하고 점수 부여
        
        Returns:
            제거된 라인의 개수
        """
        lines_to_clear = []
        
        # 완성된 라인 찾기 (모든 셀이 채워진 행)
        for i in range(self.height):
            if np.all(self.board[i] != 0):
                lines_to_clear.append(i)
        
        # 라인 제거 및 위의 블록들 아래로 이동
        if lines_to_clear:
            # 제거할 라인을 삭제
            self.board = np.delete(self.board, lines_to_clear, axis=0)
            
            # 제거된 라인 수만큼 빈 라인을 맨 위에 추가
            new_lines = np.zeros((len(lines_to_clear), self.width), dtype=int)
            self.board = np.vstack([new_lines, self.board])
            
            # 점수 계산 (라인 수에 따라 기하급수적으로 증가)
            lines_count = len(lines_to_clear)
            points = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += points.get(lines_count, lines_count * 100)
            self.lines_cleared += lines_count
        
        return len(lines_to_clear)
    
    def _rotate_piece(self, clockwise: bool = True) -> np.ndarray:
        """
        블록을 회전시킴
        
        Args:
            clockwise: True면 시계방향, False면 반시계방향
            
        Returns:
            회전된 블록 (numpy array)
        """
        if clockwise:
            # 시계 방향 90도 회전: 전치 후 좌우 반전
            return np.rot90(self.current_piece, k=-1)
        else:
            # 반시계 방향 90도 회전: 전치 후 상하 반전
            return np.rot90(self.current_piece, k=1)
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, dict]:
        """
        행동을 수행하고 결과를 반환 (강화학습 표준 인터페이스)
        
        행동 정의:
            0: 아무것도 하지 않음 (자연 낙하)
            1: 왼쪽으로 이동
            2: 오른쪽으로 이동
            3: 아래로 빠르게 이동 (소프트 드롭)
            4: 시계방향 회전
            5: 반시계방향 회전
            6: 즉시 낙하 (하드 드롭)
        
        Args:
            action: 수행할 행동 (0~6)
            
        Returns:
            state: 새로운 게임 상태
            reward: 보상 값
            done: 게임 종료 여부
            info: 추가 정보 딕셔너리
        """
        if self.game_over:
            return self._get_state(), 0, True, {'game_over': True}
        
        reward = 0
        lines_cleared_before = self.lines_cleared
        
        # 행동 수행
        if action == 1:  # 왼쪽 이동
            new_pos = [self.current_pos[0], self.current_pos[1] - 1]
            if not self._check_collision(self.current_piece, new_pos):
                self.current_pos = new_pos
                
        elif action == 2:  # 오른쪽 이동
            new_pos = [self.current_pos[0], self.current_pos[1] + 1]
            if not self._check_collision(self.current_piece, new_pos):
                self.current_pos = new_pos
                
        elif action == 3:  # 소프트 드롭 (아래로 빠르게)
            new_pos = [self.current_pos[0] + 1, self.current_pos[1]]
            if not self._check_collision(self.current_piece, new_pos):
                self.current_pos = new_pos
                reward += 1  # 소프트 드롭 보너스
                
        elif action == 4:  # 시계방향 회전
            rotated = self._rotate_piece(clockwise=True)
            if not self._check_collision(rotated, self.current_pos):
                self.current_piece = rotated
                
        elif action == 5:  # 반시계방향 회전
            rotated = self._rotate_piece(clockwise=False)
            if not self._check_collision(rotated, self.current_pos):
                self.current_piece = rotated
                
        elif action == 6:  # 하드 드롭 (즉시 낙하)
            while not self._check_collision(
                self.current_piece,
                [self.current_pos[0] + 1, self.current_pos[1]]
            ):
                self.current_pos[0] += 1
                reward += 2  # 하드 드롭 보너스
            
            # 블록 고정
            self._merge_piece()
            self._spawn_piece()
            
            # 라인 클리어 보상
            lines_cleared_now = self.lines_cleared - lines_cleared_before
            if lines_cleared_now > 0:
                reward += lines_cleared_now * 100
            
            return self._get_state(), reward, self.game_over, {
                'lines_cleared': lines_cleared_now,
                'score': self.score
            }
        
        # 자연 낙하 (모든 행동 후 블록이 한 칸씩 아래로)
        new_pos = [self.current_pos[0] + 1, self.current_pos[1]]
        if self._check_collision(self.current_piece, new_pos):
            # 더 이상 아래로 갈 수 없으면 블록 고정
            self._merge_piece()
            self._spawn_piece()
            
            # 라인 클리어 보상
            lines_cleared_now = self.lines_cleared - lines_cleared_before
            if lines_cleared_now > 0:
                reward += lines_cleared_now * 100
        else:
            # 아래로 이동
            self.current_pos = new_pos
        
        return self._get_state(), reward, self.game_over, {
            'lines_cleared': self.lines_cleared - lines_cleared_before,
            'score': self.score
        }
    
    def _get_state(self) -> np.ndarray:
        """
        현재 게임 상태를 반환
        
        Returns:
            현재 보드에 현재 블록이 겹쳐진 상태 (numpy array)
        """
        # 보드 복사
        state = self.board.copy()
        
        # 현재 블록을 상태에 추가 (임시로 표시)
        if not self.game_over and self.current_piece is not None:
            piece_h, piece_w = self.current_piece.shape
            for i in range(piece_h):
                for j in range(piece_w):
                    if self.current_piece[i][j]:
                        board_row = self.current_pos[0] + i
                        board_col = self.current_pos[1] + j
                        
                        # 보드 범위 내에 있으면 표시
                        if 0 <= board_row < self.height and 0 <= board_col < self.width:
                            state[board_row][board_col] = COLORS[self.current_piece_type]
        
        return state
    
    def render(self, mode: str = 'human'):
        """
        게임 상태를 화면에 출력
        
        Args:
            mode: 렌더링 모드 ('human': 콘솔 출력)
        """
        if mode == 'human':
            state = self._get_state()
            
            print("\n" + "=" * (self.width * 2 + 2))
            for row in state:
                print("|", end="")
                for cell in row:
                    if cell == 0:
                        print("  ", end="")
                    else:
                        print("■ ", end="")
                print("|")
            print("=" * (self.width * 2 + 2))
            print(f"점수: {self.score} | 라인: {self.lines_cleared}")
            if self.game_over:
                print("게임 오버!")
    
    def get_board_info(self) -> dict:
        """
        AI 학습에 유용한 보드 정보 추출
        
        Returns:
            보드의 다양한 특징들을 담은 딕셔너리
        """
        # 각 열의 높이 계산
        heights = []
        for col in range(self.width):
            height = 0
            for row in range(self.height):
                if self.board[row][col] != 0:
                    height = self.height - row
                    break
            heights.append(height)
        
        # 구멍(hole) 개수 계산 (블록 위에 빈 공간)
        holes = 0
        for col in range(self.width):
            block_found = False
            for row in range(self.height):
                if self.board[row][col] != 0:
                    block_found = True
                elif block_found and self.board[row][col] == 0:
                    holes += 1
        
        # 울퉁불퉁한 정도 (bumpiness) 계산
        bumpiness = sum(abs(heights[i] - heights[i+1]) for i in range(len(heights)-1))
        
        # 최대 높이
        max_height = max(heights) if heights else 0
        
        return {
            'heights': heights,
            'holes': holes,
            'bumpiness': bumpiness,
            'max_height': max_height,
            'aggregate_height': sum(heights)
        }
    
    def clone(self):
        """
        현재 환경의 복사본을 생성 (시뮬레이션용)
        
        Returns:
            복사된 TetrisEnv 객체
        """
        cloned = TetrisEnv(self.width, self.height)
        cloned.board = self.board.copy()
        cloned.current_piece = self.current_piece.copy() if self.current_piece is not None else None
        cloned.current_piece_type = self.current_piece_type
        cloned.current_pos = self.current_pos.copy() if self.current_pos is not None else None
        cloned.score = self.score
        cloned.lines_cleared = self.lines_cleared
        cloned.game_over = self.game_over
        return cloned


if __name__ == "__main__":
    """
    테스트 코드: 간단한 게임 플레이 데모
    """
    print("테트리스 환경 테스트")
    print("간단한 랜덤 AI로 게임을 플레이합니다.")
    
    # 환경 생성
    env = TetrisEnv(width=10, height=20)
    
    # 초기 상태
    state = env.reset()
    
    # 게임 플레이 (최대 100 스텝)
    total_reward = 0
    for step in range(100):
        # 랜덤 행동 선택
        action = random.randint(0, 6)
        
        # 행동 수행
        state, reward, done, info = env.step(action)
        total_reward += reward
        
        # 5 스텝마다 화면 출력
        if step % 5 == 0:
            env.render()
            print(f"스텝: {step}, 행동: {action}, 보상: {reward}")
        
        # 게임 종료 확인
        if done:
            env.render()
            print(f"\n게임 종료! 총 보상: {total_reward}")
            print(f"최종 점수: {env.score}, 클리어한 라인: {env.lines_cleared}")
            break
    
    # 보드 정보 출력
    board_info = env.get_board_info()
    print(f"\n보드 분석:")
    print(f"  - 구멍 개수: {board_info['holes']}")
    print(f"  - 울퉁불퉁함: {board_info['bumpiness']}")
    print(f"  - 최대 높이: {board_info['max_height']}")
