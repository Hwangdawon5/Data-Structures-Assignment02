import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import glob
import os

# 1. 팀원들 CSV 데이터 취합 [cite: 8, 9]
all_files = glob.glob("*.csv")
combined_words = []
for f in all_files:
    try:
        # 다양한 인코딩 대응
        df = pd.read_csv(f, encoding='utf-8-sig') if 'utf-8' in f else pd.read_csv(f, encoding='cp949')
        # 데이터프레임에서 문자열만 추출
        words = df.select_dtypes(include=[object]).values.flatten().tolist()
        combined_words.extend([str(w).strip() for w in words if pd.notna(w) and len(str(w).strip()) > 0])
    except:
        continue

# 2. 스택 연산 기록 (과제 제약 조건 반영) [cite: 13, 14, 15, 16, 17]
stack = [] # stack 선언부터 시작 [cite: 16]
steps = []

def record(op):
    steps.append({"op": op, "state": list(stack)})

record("Stack Initialized")

# Push 연산: 모든 단어 사용 [cite: 14]
for word in combined_words:
    if len(stack) >= 10: # 크기 10 이하 유지 [cite: 17]
        popped = stack.pop()
        record(f"POP (Full): {popped}")
    stack.append(word)
    record(f"PUSH: {word}")

# Top 및 Pop 연산 최소 1회 이상 포함 [cite: 15]
if stack:
    record(f"TOP: {stack[-1]}")
    popped = stack.pop()
    record(f"POP: {popped}")

# 3. 애니메이션 시각화 [cite: 10, 18]
plt.rcParams['font.family'] = 'AppleGothic' # 맥북 한글 깨짐 방지
fig, ax = plt.subplots(figsize=(6, 8))

def update(i):
    ax.clear()
    step = steps[i]
    ax.set_title(step['op'], fontsize=15, pad=20)
    
    # 스택 바구니 그리기
    ax.plot([1, 1, 4, 4], [11, 0, 0, 11], color='black', lw=3)
    
    # 스택 내부 요소 (아래부터 쌓임) [cite: 12]
    for idx, val in enumerate(step['state']):
        color = 'pink' if 'PUSH' in step['op'] and idx == len(step['state'])-1 else 'lightblue'
        ax.add_patch(plt.Rectangle((1.1, idx + 0.1), 2.8, 0.8, color=color, ec='blue', alpha=0.5))
        ax.text(2.5, idx + 0.5, val, ha='center', va='center', fontsize=12)

    ax.set_xlim(0, 5)
    ax.set_ylim(-1, 12)
    ax.axis('off')

ani = animation.FuncAnimation(fig, update, frames=len(steps), interval=1000)
ani.save('2025XXXX.mp4', writer='ffmpeg') # 학번.mp4로 저장 
print("애니메이션 저장 완료!")
