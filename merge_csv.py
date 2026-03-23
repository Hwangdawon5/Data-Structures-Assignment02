import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 과제 요구사항: 스택 선언부터 시작 [cite: 16]
stack = []
steps = []

# 1. Push 연산: 팀원들의 모든 단어를 사용 [cite: 11, 14]
for word in combined_words:
    if len(stack) >= 10: # 제약 조건: 크기 10 이하 유지 
        popped = stack.pop()
        steps.append({"op": f"POP: {popped}", "state": list(stack)})
    
    stack.append(word)
    steps.append({"op": f"PUSH: {word}", "state": list(stack)})

# 2. Top 연산 포함 
if stack:
    steps.append({"op": f"TOP: {stack[-1]}", "state": list(stack)})

# 시각화 설정 (맥북 한글 깨짐 방지)
plt.rcParams['font.family'] = 'AppleGothic'

fig, ax = plt.subplots(figsize=(5, 8))

def update(i):
    ax.clear()
    curr = steps[i]
    ax.set_title(curr['op'], fontsize=14)
    
    # 스택 그리기
    for idx, val in enumerate(curr['state']):
        ax.add_patch(plt.Rectangle((0.1, idx), 0.8, 0.8, color='skyblue', alpha=0.6))
        ax.text(0.5, idx+0.4, val, ha='center', va='center')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 11)
    ax.axis('off')

ani = animation.FuncAnimation(fig, update, frames=len(steps), interval=1000)
# 파일명은 본인 학번으로 변경 
ani.save('2025XXXX.mp4', writer='ffmpeg') 
plt.show()
