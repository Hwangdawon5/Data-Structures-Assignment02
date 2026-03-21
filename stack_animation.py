import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import platform

# 1. 한글 폰트 깨짐 방지 설정 (운영체제에 맞게 자동 설정)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False
 
# 2. 팀원들이 작성한 21개의 단어 데이터
words = [
    "아메리카노", "라떼", "연애", "커피", "디저트", "커플", "벚꽃", "테라스", 
    "아인슈페너", "나무", "바람", "개강", "핑크", "캬라멜 라떼", "슈크림 라떼", 
    "꽃축제", "라떼", "디저트", "스타벅스", "아메리카노", "꽃"
]

# 3. 애니메이션 시나리오 구성 (크기 10 이하를 유지하도록 push, pop, top 적절히 배치)
operations = [("init", "stack = Stack()")]

# [1~5번 단어 Push]
for w in words[0:5]: operations.append(("push", w))
operations.append(("top", None)) # top 연산 확인
operations.append(("pop", None)) # 1개 pop (현재 크기 4)

# [6~10번 단어 Push]
for w in words[5:10]: operations.append(("push", w)) # (현재 크기 9)
operations.append(("pop", None)) 
operations.append(("pop", None)) # 2개 pop (현재 크기 7)

# [11~13번 단어 Push]
for w in words[10:13]: operations.append(("push", w)) # (현재 크기 10 - 최대치 도달)
operations.append(("top", None))
for _ in range(4): operations.append(("pop", None)) # 4개 pop (현재 크기 6)

# [14~17번 단어 Push]
for w in words[13:17]: operations.append(("push", w)) # (현재 크기 10)
for _ in range(3): operations.append(("pop", None)) # 3개 pop (현재 크기 7)

# [18~20번 단어 Push]
for w in words[17:20]: operations.append(("push", w)) # (현재 크기 10)
for _ in range(3): operations.append(("pop", None)) # 3개 pop (현재 크기 7)

# [21번 마지막 단어 Push]
operations.append(("push", words[20])) # (최종 크기 8)
operations.append(("top", None))


# 4. 애니메이션 그리기 설정
fig, ax = plt.subplots(figsize=(10, 6))
stack = []

def update(frame):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off') # 테두리 숨기기

    op, val = operations[frame]
    code_str = ""

    # 스택 연산 로직
    if op == "init":
        stack.clear()
        code_str = "stack = []"
    elif op == "push":
        stack.append(val)
        code_str = f'stack.push("{val}")'
    elif op == "pop":
        if stack:
            popped = stack.pop()
            code_str = f'stack.pop() # 반환: {popped}'
    elif op == "top":
        if stack:
            top_val = stack[-1]
            code_str = f'stack.top() # 최상단: {top_val}'

    # 화면 좌측: 현재 실행 중인 코드 라인 출력
    ax.text(0.5, 6, code_str, fontsize=20, va='center', ha='left',
            bbox=dict(facecolor='#f0f8ff', edgecolor='#4682b4', boxstyle='round,pad=0.5', lw=2))

    # 화면 우측: 스택 구조 그리기 (위가 뚫린 상자 형태)
    ax.plot([6, 6], [11, 1], color='black', lw=3) # 왼쪽 벽
    ax.plot([6, 9], [1, 1], color='black', lw=3)  # 바닥
    ax.plot([9, 9], [1, 11], color='black', lw=3) # 오른쪽 벽

    # 스택 내부의 데이터 그리기
    for i, item in enumerate(stack):
        rect = patches.Rectangle((6.1, 1.1 + i), 2.8, 0.8, facecolor='#ffe4e1', edgecolor='black')
        ax.add_patch(rect)
        ax.text(7.5, 1.5 + i, item, fontsize=14, ha='center', va='center')

    # 상단에 현재 스택 크기 표시
    ax.text(7.5, 11.5, f"Stack Size: {len(stack)}/10", fontsize=12, ha='center', va='center', color='gray')

# 애니메이션 객체 생성 (1프레임당 1초(1000ms) 간격)
ani = animation.FuncAnimation(fig, update, frames=len(operations), interval=1000, repeat=False)

# 5. MP4 파일로 저장
print("애니메이션을 렌더링하고 있습니다. 잠시만 기다려주세요...")
ani.save('20251267.mp4', writer='ffmpeg', fps=1)
print("저장 완료! '20251267.mp4' 파일을 확인해 보세요.")