"""
테트리스 AI 학습 예제
Simple AI Training Example for Tetris

이 파일은 테트리스 환경을 사용하여 간단한 AI를 학습시키는 예제입니다.
여러 가지 AI 전략을 보여줍니다.
"""

import numpy as np
import random
from tetris_env import TetrisEnv


class RandomAI:
    """
    랜덤 AI: 무작위로 행동을 선택하는 가장 단순한 AI
    
    이 AI는 학습하지 않고 단순히 랜덤한 행동만 수행합니다.
    베이스라인(기준선)으로 사용할 수 있습니다.
    """
    
    def get_action(self, env):
        """
        랜덤한 행동을 선택
        
        Args:
            env: 현재 테트리스 환경 (사용하지 않음)
            
        Returns:
            0~6 사이의 랜덤 행동
        """
        return random.randint(0, 6)


class GreedyAI:
    """
    탐욕 AI: 즉각적인 보상이 가장 큰 행동을 선택하는 AI
    
    각 가능한 행동을 시뮬레이션하고 가장 좋은 결과를 내는 행동을 선택합니다.
    간단하지만 효과적인 전략입니다.
    """
    
    def __init__(self):
        """탐욕 AI 초기화"""
        pass
    
    def evaluate_state(self, env: TetrisEnv) -> float:
        """
        현재 상태를 평가하는 함수
        
        보드의 여러 특징을 분석하여 점수를 계산합니다.
        낮은 점수일수록 좋은 상태입니다.
        
        Args:
            env: 평가할 테트리스 환경
            
        Returns:
            상태 평가 점수 (낮을수록 좋음)
        """
        info = env.get_board_info()
        
        # 평가 가중치 (수동으로 조정된 값들)
        # 이 값들을 변경하여 AI의 전략을 바꿀 수 있습니다
        weight_holes = -10.0      # 구멍은 나쁨 (음수 가중치)
        weight_bumpiness = -1.0   # 울퉁불퉁함은 나쁨
        weight_height = -2.0      # 높이가 높으면 나쁨
        weight_lines = 5.0        # 라인 클리어는 좋음 (양수 가중치)
        
        # 최종 평가 점수 계산
        score = (
            weight_holes * info['holes'] +
            weight_bumpiness * info['bumpiness'] +
            weight_height * info['max_height'] +
            weight_lines * env.lines_cleared
        )
        
        return score
    
    def get_action(self, env: TetrisEnv) -> int:
        """
        현재 상태에서 가장 좋은 행동을 선택
        
        모든 가능한 행동을 시뮬레이션하고 가장 좋은 결과를 내는 행동을 반환합니다.
        
        Args:
            env: 현재 테트리스 환경
            
        Returns:
            선택된 행동 (0~6)
        """
        best_action = 0
        best_score = float('-inf')  # 매우 작은 값으로 초기화
        
        # 모든 가능한 행동을 시도
        for action in range(7):
            # 환경 복사 (시뮬레이션용)
            test_env = env.clone()
            
            # 행동 수행
            _, reward, done, _ = test_env.step(action)
            
            # 게임이 끝나지 않았으면 상태 평가
            if not done:
                score = self.evaluate_state(test_env) + reward
            else:
                # 게임 오버는 매우 나쁨
                score = -1000
            
            # 더 좋은 행동이면 업데이트
            if score > best_score:
                best_score = score
                best_action = action
        
        return best_action


class HeuristicAI:
    """
    휴리스틱 AI: 전문가의 규칙을 따르는 AI
    
    테트리스 전문가들이 사용하는 전략을 코드로 구현한 AI입니다.
    예: 구멍 만들지 않기, 평평하게 쌓기, 가장자리 먼저 채우기 등
    
    이 구현은 간단한 버전으로, GreedyAI와 유사하게 동작하지만
    전문가들이 선호하는 가중치를 사용합니다.
    """
    
    def __init__(self):
        """휴리스틱 AI 초기화"""
        # 전문가 규칙 기반 가중치 (조정 가능)
        self.weights = {
            'lines_cleared': 0.76,      # 라인 클리어는 매우 중요
            'holes': -0.36,             # 구멍은 피해야 함
            'bumpiness': -0.18,         # 평평하게 유지
            'height': -0.51,            # 높이는 낮게 유지
        }
    
    def evaluate_state(self, env: TetrisEnv) -> float:
        """
        전문가 규칙을 사용하여 상태를 평가
        
        Args:
            env: 평가할 테트리스 환경
            
        Returns:
            상태 평가 점수 (높을수록 좋음)
        """
        info = env.get_board_info()
        
        score = (
            self.weights['lines_cleared'] * env.lines_cleared +
            self.weights['holes'] * info['holes'] +
            self.weights['bumpiness'] * info['bumpiness'] +
            self.weights['height'] * info['aggregate_height']
        )
        
        return score
    
    def get_action(self, env: TetrisEnv) -> int:
        """
        최적의 행동을 선택
        
        모든 가능한 행동을 시뮬레이션하고 전문가 규칙으로 평가하여
        가장 좋은 행동을 반환합니다.
        
        Args:
            env: 현재 테트리스 환경
            
        Returns:
            선택된 행동 (0~6)
        """
        best_action = 0
        best_score = float('-inf')
        
        # 모든 가능한 행동을 시도
        for action in range(7):
            # 환경 복사 (시뮬레이션용)
            test_env = env.clone()
            
            # 행동 수행
            _, reward, done, _ = test_env.step(action)
            
            # 게임이 끝나지 않았으면 상태 평가
            if not done:
                score = self.evaluate_state(test_env) + reward
            else:
                # 게임 오버는 매우 나쁨
                score = -1000
            
            # 더 좋은 행동이면 업데이트
            if score > best_score:
                best_score = score
                best_action = action
        
        return best_action


def train_and_evaluate(ai_class, num_games: int = 10, max_steps: int = 1000):
    """
    AI를 여러 게임으로 평가하는 함수
    
    Args:
        ai_class: 평가할 AI 클래스
        num_games: 플레이할 게임 수
        max_steps: 게임당 최대 스텝 수
        
    Returns:
        평균 점수, 평균 라인 수, 평균 생존 스텝 수
    """
    scores = []
    lines = []
    steps = []
    
    print(f"\n{ai_class.__name__} 평가 중...")
    print("-" * 50)
    
    for game in range(num_games):
        # AI와 환경 초기화
        ai = ai_class()
        env = TetrisEnv(width=10, height=20)
        state = env.reset()
        
        # 게임 플레이
        for step in range(max_steps):
            # AI가 행동 선택
            action = ai.get_action(env)
            
            # 행동 수행
            state, reward, done, info = env.step(action)
            
            # 게임 종료 확인
            if done:
                steps.append(step)
                break
        
        # 결과 기록
        scores.append(env.score)
        lines.append(env.lines_cleared)
        
        # 진행 상황 출력
        if (game + 1) % 5 == 0:
            print(f"게임 {game + 1}/{num_games} 완료")
    
    # 통계 계산
    avg_score = np.mean(scores)
    avg_lines = np.mean(lines)
    avg_steps = np.mean(steps) if steps else max_steps
    
    print(f"\n결과:")
    print(f"  평균 점수: {avg_score:.2f}")
    print(f"  평균 클리어 라인: {avg_lines:.2f}")
    print(f"  평균 생존 스텝: {avg_steps:.2f}")
    print(f"  최고 점수: {max(scores)}")
    print(f"  최고 라인: {max(lines)}")
    
    return avg_score, avg_lines, avg_steps


def interactive_play():
    """
    사람이 직접 플레이할 수 있는 모드
    
    키보드 입력으로 테트리스를 플레이합니다.
    """
    print("\n테트리스 게임 시작!")
    print("=" * 50)
    print("조작법:")
    print("  0: 대기 (자연 낙하)")
    print("  1: 왼쪽")
    print("  2: 오른쪽")
    print("  3: 소프트 드롭 (빠르게 내리기)")
    print("  4: 시계방향 회전")
    print("  5: 반시계방향 회전")
    print("  6: 하드 드롭 (즉시 낙하)")
    print("  q: 게임 종료")
    print("=" * 50)
    
    env = TetrisEnv(width=10, height=20)
    state = env.reset()
    env.render()
    
    while True:
        # 사용자 입력 받기
        try:
            user_input = input("\n행동을 선택하세요 (0-6, q=종료): ").strip()
            
            if user_input.lower() == 'q':
                print("게임을 종료합니다.")
                break
            
            action = int(user_input)
            
            if 0 <= action <= 6:
                # 행동 수행
                state, reward, done, info = env.step(action)
                
                # 화면 출력
                env.render()
                
                if reward > 0:
                    print(f"보상: +{reward}")
                
                if info.get('lines_cleared', 0) > 0:
                    print(f"🎉 {info['lines_cleared']}개 라인 클리어!")
                
                # 게임 종료 확인
                if done:
                    print("\n게임 오버!")
                    print(f"최종 점수: {env.score}")
                    print(f"클리어한 라인: {env.lines_cleared}")
                    break
            else:
                print("0-6 사이의 숫자를 입력하세요.")
                
        except ValueError:
            print("올바른 입력이 아닙니다.")
        except KeyboardInterrupt:
            print("\n게임을 종료합니다.")
            break


if __name__ == "__main__":
    """
    메인 실행 코드
    """
    print("=" * 50)
    print("테트리스 AI 학습 예제")
    print("=" * 50)
    
    # 여러 AI 비교
    print("\n다양한 AI 전략 비교")
    
    # 1. 랜덤 AI
    random_score, random_lines, random_steps = train_and_evaluate(
        RandomAI, 
        num_games=10, 
        max_steps=500
    )
    
    # 2. 탐욕 AI
    greedy_score, greedy_lines, greedy_steps = train_and_evaluate(
        GreedyAI, 
        num_games=10, 
        max_steps=500
    )
    
    # 결과 비교
    print("\n" + "=" * 50)
    print("최종 비교 결과")
    print("=" * 50)
    print(f"{'AI 타입':<15} {'평균 점수':<12} {'평균 라인':<12} {'평균 스텝':<12}")
    print("-" * 50)
    print(f"{'랜덤 AI':<15} {random_score:<12.2f} {random_lines:<12.2f} {random_steps:<12.2f}")
    print(f"{'탐욕 AI':<15} {greedy_score:<12.2f} {greedy_lines:<12.2f} {greedy_steps:<12.2f}")
    
    improvement = ((greedy_score - random_score) / random_score * 100) if random_score > 0 else 0
    print(f"\n탐욕 AI는 랜덤 AI보다 {improvement:.1f}% 더 좋은 성능을 보입니다.")
    
    # 대화형 플레이 제안
    print("\n" + "=" * 50)
    user_choice = input("직접 플레이해보시겠습니까? (y/n): ").strip().lower()
    if user_choice == 'y':
        interactive_play()
