"""
테트리스 환경 데모
Simple Demo of Tetris Environment

이 스크립트는 테트리스 환경의 기본 사용법을 보여주는 간단한 데모입니다.
"""

from tetris_env import TetrisEnv
import random


def demo_basic_usage():
    """기본 사용법 데모"""
    print("=" * 60)
    print("데모 1: 기본 사용법")
    print("=" * 60)
    
    # 환경 생성
    env = TetrisEnv(width=10, height=20)
    
    print("\n1. 환경 초기화")
    state = env.reset()
    print(f"   - 보드 크기: {state.shape}")
    print(f"   - 초기 점수: {env.score}")
    
    print("\n2. 초기 상태 렌더링")
    env.render()
    
    print("\n3. 몇 가지 행동 수행")
    actions = [2, 2, 4, 6]  # 오른쪽, 오른쪽, 회전, 하드드롭
    action_names = ['오른쪽', '오른쪽', '회전', '하드드롭']
    
    for action, name in zip(actions, action_names):
        print(f"\n   행동: {name}")
        state, reward, done, info = env.step(action)
        print(f"   보상: {reward}")
        if done:
            print("   게임 종료!")
            break
    
    print("\n4. 최종 상태")
    env.render()


def demo_board_analysis():
    """보드 분석 기능 데모"""
    print("\n" + "=" * 60)
    print("데모 2: 보드 분석")
    print("=" * 60)
    
    env = TetrisEnv(width=10, height=20)
    env.reset()
    
    # 몇 개의 블록을 놓기
    for _ in range(5):
        for _ in range(random.randint(1, 3)):
            env.step(random.randint(1, 2))  # 좌우 이동
        env.step(6)  # 하드 드롭
    
    print("\n현재 게임 상태:")
    env.render()
    
    print("\n보드 분석 결과:")
    info = env.get_board_info()
    print(f"  각 열의 높이: {info['heights']}")
    print(f"  구멍 개수: {info['holes']}")
    print(f"  울퉁불퉁함: {info['bumpiness']}")
    print(f"  최대 높이: {info['max_height']}")
    print(f"  총 높이 합: {info['aggregate_height']}")


def demo_all_blocks():
    """모든 블록 타입 시연"""
    print("\n" + "=" * 60)
    print("데모 3: 7가지 테트리스 블록")
    print("=" * 60)
    
    from tetris_env import SHAPES
    
    for name, shape in SHAPES.items():
        print(f"\n블록 {name}:")
        for row in shape:
            print("  ", end="")
            for cell in row:
                if cell:
                    print("■ ", end="")
                else:
                    print("  ", end="")
            print()


def demo_rotation():
    """회전 기능 데모"""
    print("\n" + "=" * 60)
    print("데모 4: 블록 회전")
    print("=" * 60)
    
    env = TetrisEnv(width=10, height=20)
    env.reset()
    
    print("\n초기 상태:")
    env.render()
    
    print("\n시계방향 회전 4번:")
    for i in range(4):
        env.step(4)  # 시계방향 회전
        print(f"\n회전 {i+1}:")
        env.render()


def demo_scoring():
    """점수 시스템 데모"""
    print("\n" + "=" * 60)
    print("데모 5: 점수 시스템")
    print("=" * 60)
    
    env = TetrisEnv(width=10, height=20)
    env.reset()
    
    print("\n점수 규칙:")
    print("  - 소프트 드롭 (빠르게 내리기): +1")
    print("  - 하드 드롭 (즉시 낙하): 한 칸당 +2")
    print("  - 라인 1개 클리어: +100")
    print("  - 라인 2개 클리어: +300")
    print("  - 라인 3개 클리어: +500")
    print("  - 라인 4개 클리어: +800")
    
    total_reward = 0
    print("\n게임 플레이 중...")
    
    for step in range(30):
        action = random.randint(0, 6)
        state, reward, done, info = env.step(action)
        
        if reward > 0:
            total_reward += reward
            print(f"  스텝 {step}: 보상 +{reward} (총 보상: {total_reward})")
        
        if info.get('lines_cleared', 0) > 0:
            print(f"  🎉 {info['lines_cleared']}개 라인 클리어!")
        
        if done:
            print(f"\n게임 종료! (스텝 {step})")
            break
    
    print(f"\n최종 결과:")
    print(f"  총 보상: {total_reward}")
    print(f"  게임 점수: {env.score}")
    print(f"  클리어한 라인: {env.lines_cleared}")


def demo_clone():
    """환경 복제 기능 데모 (시뮬레이션용)"""
    print("\n" + "=" * 60)
    print("데모 6: 환경 복제 (미래 예측)")
    print("=" * 60)
    
    env = TetrisEnv(width=10, height=20)
    env.reset()
    
    print("\n원본 환경:")
    env.render()
    
    print("\n여러 행동을 시뮬레이션:")
    
    for action in range(3):
        cloned = env.clone()
        
        # 클론된 환경에서 행동 수행
        for _ in range(5):
            cloned.step(action)
        
        action_name = ['대기', '왼쪽', '오른쪽'][action]
        print(f"\n행동 '{action_name}'를 5번 반복한 결과:")
        cloned.render()
        
        info = cloned.get_board_info()
        print(f"  최대 높이: {info['max_height']}, 구멍: {info['holes']}")
    
    print("\n원본 환경은 변경되지 않음:")
    env.render()


def main():
    """모든 데모 실행"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "테트리스 환경 데모" + " " * 21 + "║")
    print("╚" + "═" * 58 + "╝")
    
    demos = [
        demo_basic_usage,
        demo_board_analysis,
        demo_all_blocks,
        demo_rotation,
        demo_scoring,
        demo_clone
    ]
    
    for i, demo in enumerate(demos, 1):
        try:
            demo()
            
            if i < len(demos):
                input("\nEnter 키를 눌러 다음 데모로... ")
        except KeyboardInterrupt:
            print("\n\n데모를 종료합니다.")
            break
    
    print("\n" + "=" * 60)
    print("데모 완료!")
    print("=" * 60)
    print("\n더 자세한 정보는 README_TETRIS.md 파일을 참고하세요.")
    print("AI 학습 예제는 tetris_ai_example.py를 실행하세요.")


if __name__ == "__main__":
    main()
