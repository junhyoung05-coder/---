"""
테트리스 AI 빠른 시작 가이드
Quick Start Guide for Tetris AI

5분 안에 테트리스 AI를 시작할 수 있습니다!
"""

# ============================================================
# 1단계: 환경 설치
# ============================================================

# 필요한 패키지 설치 (터미널에서 실행)
# pip install numpy

# 또는 requirements.txt 사용:
# pip install -r requirements.txt


# ============================================================
# 2단계: 첫 번째 AI 만들기
# ============================================================

from tetris_env import TetrisEnv
import random


# 가장 간단한 AI: 랜덤 선택
class MyFirstAI:
    """나의 첫 번째 테트리스 AI"""
    
    def get_action(self, env):
        """
        행동을 선택하는 함수
        
        Args:
            env: 테트리스 환경
            
        Returns:
            0-6 사이의 행동 번호
        """
        # 랜덤하게 행동 선택
        return random.randint(0, 6)


# AI 테스트하기
def test_my_ai():
    """AI를 테스트하는 함수"""
    
    # 환경 생성
    env = TetrisEnv(width=10, height=20)
    
    # AI 생성
    ai = MyFirstAI()
    
    # 게임 시작
    env.reset()
    
    print("게임 시작!")
    print("-" * 40)
    
    # 100 스텝 동안 게임 플레이
    for step in range(100):
        # AI가 행동 선택
        action = ai.get_action(env)
        
        # 행동 수행
        state, reward, done, info = env.step(action)
        
        # 10 스텝마다 화면 출력
        if step % 10 == 0:
            env.render()
            print(f"스텝: {step}, 점수: {env.score}")
        
        # 게임 종료 확인
        if done:
            print("\n게임 종료!")
            print(f"최종 점수: {env.score}")
            print(f"클리어한 라인: {env.lines_cleared}")
            print(f"생존 스텝: {step}")
            break


# ============================================================
# 3단계: 더 똑똑한 AI 만들기
# ============================================================

class SmartAI:
    """조금 더 똑똑한 AI"""
    
    def get_action(self, env):
        """
        보드 상태를 분석해서 행동을 선택
        """
        # 보드 정보 가져오기
        info = env.get_board_info()
        
        # 전략 1: 높이가 너무 높으면 빨리 내리기
        if info['max_height'] > 15:
            return 6  # 하드 드롭
        
        # 전략 2: 구멍이 많으면 회전 시도
        if info['holes'] > 5:
            return 4  # 시계방향 회전
        
        # 전략 3: 가운데가 비었으면 가운데로
        heights = info['heights']
        middle = len(heights) // 2
        
        if heights[middle] < heights[0] and heights[middle] < heights[-1]:
            return random.choice([1, 2])  # 좌우 이동
        
        # 그 외에는 랜덤
        return random.randint(0, 6)


# ============================================================
# 4단계: AI 성능 비교
# ============================================================

def compare_ais():
    """여러 AI의 성능을 비교"""
    
    ai_classes = [
        ("랜덤 AI", MyFirstAI),
        ("스마트 AI", SmartAI)
    ]
    
    print("\nAI 성능 비교")
    print("=" * 60)
    
    for ai_name, ai_class in ai_classes:
        scores = []
        lines = []
        
        # 각 AI로 5게임 플레이
        for game in range(5):
            env = TetrisEnv()
            ai = ai_class()
            env.reset()
            
            for step in range(500):
                action = ai.get_action(env)
                _, _, done, _ = env.step(action)
                
                if done:
                    break
            
            scores.append(env.score)
            lines.append(env.lines_cleared)
        
        # 결과 출력
        avg_score = sum(scores) / len(scores)
        avg_lines = sum(lines) / len(lines)
        
        print(f"\n{ai_name}:")
        print(f"  평균 점수: {avg_score:.1f}")
        print(f"  평균 라인: {avg_lines:.1f}")
        print(f"  최고 점수: {max(scores)}")


# ============================================================
# 5단계: 직접 플레이해보기
# ============================================================

def play_myself():
    """
    직접 테트리스를 플레이
    
    조작법:
        0: 대기
        1: 왼쪽
        2: 오른쪽
        3: 빠르게 내리기
        4: 회전
        5: 반시계방향 회전
        6: 즉시 낙하
        q: 종료
    """
    env = TetrisEnv()
    env.reset()
    
    print("\n직접 플레이 모드")
    print("=" * 60)
    env.render()
    
    while True:
        try:
            action_input = input("\n행동 (0-6, q=종료): ").strip()
            
            if action_input == 'q':
                break
            
            action = int(action_input)
            if 0 <= action <= 6:
                state, reward, done, info = env.step(action)
                env.render()
                
                if reward > 0:
                    print(f"보상: +{reward}")
                
                if done:
                    print("\n게임 오버!")
                    print(f"최종 점수: {env.score}")
                    break
            else:
                print("0-6 사이의 숫자를 입력하세요.")
        
        except ValueError:
            print("올바른 숫자를 입력하세요.")
        except KeyboardInterrupt:
            print("\n게임 종료")
            break


# ============================================================
# 메인 메뉴
# ============================================================

def main():
    """메인 메뉴"""
    
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 18 + "테트리스 AI" + " " * 26 + "║")
    print("║" + " " * 18 + "빠른 시작" + " " * 28 + "║")
    print("╚" + "═" * 58 + "╝")
    
    print("\n선택하세요:")
    print("1. 내 첫 AI 테스트")
    print("2. AI 성능 비교")
    print("3. 직접 플레이")
    print("4. 전체 데모 보기")
    print("q. 종료")
    
    while True:
        choice = input("\n선택: ").strip()
        
        if choice == '1':
            test_my_ai()
        elif choice == '2':
            compare_ais()
        elif choice == '3':
            play_myself()
        elif choice == '4':
            import tetris_demo
            tetris_demo.main()
            break
        elif choice.lower() == 'q':
            print("프로그램을 종료합니다.")
            break
        else:
            print("1-4 또는 q를 입력하세요.")


# ============================================================
# 추가 학습 자료
# ============================================================

"""
다음 단계:

1. 강화학습 알고리즘 적용:
   - Q-Learning
   - Deep Q-Network (DQN)
   - Policy Gradient
   
2. 더 나은 특징 추출:
   - 보드의 높이 분포
   - 구멍의 위치와 깊이
   - 다음 블록 정보 활용
   
3. 학습 데이터 저장:
   - 게임 플레이 기록
   - 최고 점수 달성 전략
   - 실패 케이스 분석

4. 시각화:
   - 학습 과정 그래프
   - 실시간 게임 플레이
   - AI 의사결정 과정

참고 파일:
- tetris_env.py: 환경 상세 구현
- tetris_ai_example.py: 고급 AI 예제
- tetris_demo.py: 환경 기능 데모
- README_TETRIS.md: 완전한 문서
"""


if __name__ == "__main__":
    # 프로그램 실행
    main()
