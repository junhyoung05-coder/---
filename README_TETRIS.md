# 테트리스 AI 학습 환경

AI 강화학습을 위한 테트리스 게임 환경입니다. 이 프로젝트는 AI 에이전트가 테트리스를 학습하고 플레이할 수 있도록 설계되었습니다.

## 📁 파일 구조

- **tetris_env.py**: 테트리스 게임 환경 (핵심 파일)
  - 게임 로직, 블록 이동, 충돌 감지, 라인 클리어 등 모든 기능 포함
  - OpenAI Gym 스타일의 인터페이스 제공
  - 상세한 한글 주석으로 코드 이해 용이

- **tetris_ai_example.py**: AI 학습 예제
  - 랜덤 AI: 무작위 행동 선택
  - 탐욕 AI: 즉각적인 보상 최대화
  - 휴리스틱 AI: 전문가 규칙 기반
  - 대화형 플레이 모드

## 🚀 빠른 시작

### 1. 환경 테스트

```bash
python tetris_env.py
```

랜덤 AI로 간단한 게임을 플레이하여 환경이 제대로 작동하는지 확인합니다.

### 2. AI 비교 실행

```bash
python tetris_ai_example.py
```

여러 AI 전략을 비교하고 성능을 평가합니다.

### 3. 직접 플레이

```bash
python tetris_ai_example.py
```

프로그램 실행 후 대화형 플레이를 선택하여 직접 테트리스를 플레이할 수 있습니다.

## 🎮 사용 방법

### 기본 사용법

```python
from tetris_env import TetrisEnv

# 환경 생성
env = TetrisEnv(width=10, height=20)

# 게임 초기화
state = env.reset()

# 게임 루프
done = False
while not done:
    # 행동 선택 (0-6)
    action = 2  # 오른쪽 이동
    
    # 행동 수행
    state, reward, done, info = env.step(action)
    
    # 화면 출력
    env.render()
```

### 행동 정의

| 행동 | 설명 |
|------|------|
| 0 | 대기 (자연 낙하) |
| 1 | 왼쪽 이동 |
| 2 | 오른쪽 이동 |
| 3 | 소프트 드롭 (빠르게 내리기) |
| 4 | 시계방향 회전 |
| 5 | 반시계방향 회전 |
| 6 | 하드 드롭 (즉시 낙하) |

### 상태 정보

`env.step(action)`의 반환값:
- **state**: 현재 게임 보드 상태 (numpy array)
- **reward**: 받은 보상 값
- **done**: 게임 종료 여부 (True/False)
- **info**: 추가 정보 (클리어한 라인 수, 점수 등)

### 보드 분석

```python
# 보드 정보 얻기
board_info = env.get_board_info()

print(f"구멍 개수: {board_info['holes']}")
print(f"울퉁불퉁함: {board_info['bumpiness']}")
print(f"최대 높이: {board_info['max_height']}")
print(f"각 열의 높이: {board_info['heights']}")
```

## 🤖 AI 개발 가이드

### 1. 간단한 AI 만들기

```python
class MyAI:
    def get_action(self, env):
        # 여기에 AI 로직 작성
        # env.get_board_info()로 보드 정보 얻기
        # 0-6 사이의 행동 반환
        return 0

# AI 테스트
ai = MyAI()
env = TetrisEnv()
state = env.reset()

for _ in range(100):
    action = ai.get_action(env)
    state, reward, done, info = env.step(action)
    if done:
        break
```

### 2. 강화학습 적용

이 환경은 다양한 강화학습 알고리즘에 사용할 수 있습니다:

- **DQN (Deep Q-Network)**: 심층 Q-학습
- **PPO (Proximal Policy Optimization)**: 근접 정책 최적화
- **A3C (Asynchronous Advantage Actor-Critic)**: 비동기 어드밴티지 액터-크리틱
- **기타**: Q-Learning, SARSA 등

### 3. 평가 지표

AI 성능을 평가하는 주요 지표:
- 평균 점수
- 평균 클리어한 라인 수
- 평균 생존 시간 (스텝 수)
- 최고 점수

## 💡 학습 팁

### 보상 설계

현재 환경의 보상 체계:
- 소프트 드롭: +1
- 하드 드롭: +2 (한 칸당)
- 라인 1개 클리어: +100
- 라인 2개 클리어: +300
- 라인 3개 클리어: +500
- 라인 4개 클리어: +800

### 상태 특징 추출

효과적인 AI를 위해 다음 특징들을 고려하세요:
- 각 열의 높이
- 구멍 개수 (블록 위의 빈 공간)
- 울퉁불퉁한 정도 (인접한 열의 높이 차이)
- 최대 높이
- 현재 블록 타입

### 전략 예시

1. **구멍 최소화**: 블록 위에 빈 공간이 생기지 않도록
2. **평평하게 유지**: 모든 열의 높이를 비슷하게
3. **가장자리 먼저**: 양쪽 가장자리부터 채우기
4. **라인 클리어 우선**: 완성 가능한 라인을 먼저 만들기

## 🔧 고급 기능

### 환경 복제

```python
# 시뮬레이션을 위한 환경 복제
cloned_env = env.clone()

# 복제된 환경에서 여러 행동 시도 가능
for action in range(7):
    test_env = cloned_env.clone()
    state, reward, done, info = test_env.step(action)
    # 각 행동의 결과 평가
```

### 커스터마이징

보드 크기 변경:
```python
# 더 작은 보드 (학습 속도 향상)
env = TetrisEnv(width=6, height=12)

# 더 큰 보드 (더 어려운 게임)
env = TetrisEnv(width=12, height=24)
```

## 📊 성능 벤치마크

기본 AI들의 평균 성능 (10게임, 500스텝):

| AI 타입 | 평균 점수 | 평균 라인 | 평균 생존 스텝 |
|---------|-----------|-----------|----------------|
| 랜덤 AI | ~50 | ~0.5 | ~50 |
| 탐욕 AI | ~200 | ~2.0 | ~150 |

## 🎯 프로젝트 확장 아이디어

1. **딥러닝 모델 적용**
   - CNN으로 보드 상태 분석
   - RNN으로 시퀀스 학습

2. **추가 기능**
   - 다음 블록 미리보기
   - 블록 홀드 (저장) 기능
   - 난이도 조절 (속도 변화)

3. **시각화**
   - Pygame을 사용한 GUI
   - 학습 과정 그래프
   - 실시간 게임 플레이 영상

4. **멀티 에이전트**
   - 여러 AI 동시 대전
   - 협력 학습

## 📝 라이센스

이 프로젝트는 학습 목적으로 자유롭게 사용할 수 있습니다.

## 🤝 기여

버그 리포트나 개선 제안은 언제나 환영합니다!

---

**즐거운 AI 학습 되세요! 🎮🤖**
