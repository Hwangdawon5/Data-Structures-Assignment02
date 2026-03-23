import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os

# 1. 정리된 merge.csv 파일 읽기 [cite: 9]
current_path = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(current_path, "merge.csv")

combined_words = []

if os.path.exists(csv_file):
    try:
        # 한글 깨짐 방지를 위해 utf-8-sig 또는 cp949로 읽기
        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
        except:
            df = pd.read_csv(csv_file, encoding='cp949')
        
        # '단어'가 포함된 열을 찾거나, 전체 데이터에서 문자열만 추출
        target_col = [c for c in df.columns if '단어' in c]
        if target_col:
            # 지정된 열이 있으면 해당 열의 데이터만 추출
            combined_words = df[target_col[0]].dropna().astype(str).str.strip().tolist()
        else:
            # 열 이름을 모를 경우 데이터프레임 내 모든 문자열 추출
            for val in df.values.flatten():
                s_val = str(val).strip()
                if s_val and not s_val.isdigit() and s_val.lower() != 'nan':
                    combined_words.append(s_val)
                    
        print(f"✅ merge.csv에서 {len(combined_words)}개의 단어를 불러왔습니다.")
    except Exception as e:
        print(f"❌ 파일 읽기 실패: {e}")
else:
    print(f"❌ {csv_file} 파일을 찾을 수 없습니다.")
    combined_words = ["벚꽃", "말차라떼", "봄바람"] # 파일 없을 때 비상용

# 2. 스택 연산 기록 (과제 제약 조건 준수) [cite: 14, 15, 16, 17]
stack = [] # stack 선언부터 시작 [cite: 16]
steps = []

def record(op):
    steps.append({"op": op, "state": list(stack)})

record("Stack Initialized")

# Push 연산 [cite: 14]
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
plt.rcParams['font.family'] = 'AppleGothic' # 맥북용
fig, ax = plt.subplots(figsize=(6, 8))

def update(i):
    ax.clear()
    step = steps[i]
    ax.set_title(step['op'], fontsize=15, pad=20)
    
    # 스택 바구니 외곽선 [cite: 10]
    ax.plot([1, 1, 4, 4], [11, 0, 0, 11], color='black', lw=3)
    
    # 스택 내부 요소 시각화 [cite: 12]
    for idx, val in enumerate(step['state']):
        is_last = (idx == len(step['state']) - 1)
        color = 'pink' if is_last and 'PUSH' in step['op'] else 'lightblue'
        ax.add_patch(plt.Rectangle((1.1, idx + 0.1), 2.8, 0.8, color=color, ec='blue', alpha=0.6))
        ax.text(2.5, idx + 0.5, val, ha='center', va='center', fontsize=11, fontweight='bold')

    ax.set_xlim(0, 5)
    ax.set_ylim(-1, 12)
    ax.axis('off')

ani = animation.FuncAnimation(fig, update, frames=len(steps), interval=1000)
ani.save('20252213.mp4', writer='ffmpeg')
print("✅ 애니메이션 제작 완료: 20252213.mp4")
