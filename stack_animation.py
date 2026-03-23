import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import matplotlib
matplotlib.rcParams['font.family'] = ['Noto Sans CJK JP']

# CSV 데이터
members = [
    {"name": "최윤지", "id": "20251259", "words": ["꽃축제", "라떼", "디저트"]},
    {"name": "최하은", "id": "20251261", "words": ["커피", "디저트", "커플"]},
    {"name": "황다원", "id": "20251267", "words": ["벚꽃", "테라스", "아인슈페너"]},
    {"name": "박다인", "id": "20252167", "words": ["스타벅스", "아메리카노", "꽃"]},
    {"name": "안예원", "id": "20252185", "words": ["나무", "바람", "개강"]},
    {"name": "정서하", "id": "20252213", "words": ["핑크", "캬라멜 라떼", "슈크림 라떼"]},
    {"name": "김우현", "id": "20251187", "words": ["아메리카노", "라떼", "연애"]},
]

# 애니메이션 시퀀스: (operation, argument, description)
# operations: 'declare', 'push', 'pop', 'top'
sequence = [
    ("declare", None,      "Stack<String> stack = new Stack<>();"),
    ("push",    "벚꽃",    'stack.push("벚꽃")  // 황다원'),
    ("push",    "라떼",    'stack.push("라떼")  // 최윤지'),
    ("push",    "커피",    'stack.push("커피")  // 최하은'),
    ("top",     None,      'stack.top()  → "커피"'),
    ("push",    "스타벅스",'stack.push("스타벅스")  // 박다인'),
    ("push",    "나무",    'stack.push("나무")  // 안예원'),
    ("push",    "핑크",    'stack.push("핑크")  // 정서하'),
    ("pop",     None,      'stack.pop()  ← "핑크"'),
    ("push",    "아메리카노", 'stack.push("아메리카노")  // 김우현'),
    ("push",    "꽃",      'stack.push("꽃")  // 박다인'),
    ("pop",     None,      'stack.pop()  ← "꽃"'),
    ("top",     None,      'stack.top()  → "아메리카노"'),
    ("pop",     None,      'stack.pop()  ← "아메리카노"'),
    ("push",    "커플",    'stack.push("커플")  // 최하은'),
    ("push",    "개강",    'stack.push("개강")  // 안예원'),
    ("top",     None,      'stack.top()  → "개강"'),
    ("pop",     None,      'stack.pop()  ← "개강"'),
    ("pop",     None,      'stack.pop()  ← "커플"'),
]

# Colors
STACK_BG   = "#F0F4FF"
CELL_COLOR = "#4A90D9"
CELL_EDGE  = "#1A5FA8"
TOP_COLOR  = "#E63946"
TOP_EDGE   = "#9B1D24"
OP_COLORS  = {"declare": "#6C757D", "push": "#2E7D32", "pop": "#C62828", "top": "#1565C0"}
BG_COLOR   = "#FAFAFA"
MAX_SIZE   = 10

fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor(BG_COLOR)

def draw_frame(frame_idx):
    ax.clear()
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Build stack state up to this frame
    stack = []
    popped_item = None
    top_item = None
    current_op, current_arg, current_desc = sequence[frame_idx]

    for i in range(frame_idx):
        op, arg, _ = sequence[i]
        if op == "push":
            stack.append(arg)
        elif op == "pop" and stack:
            stack.pop()

    # Apply current operation (for display)
    highlight_top = False
    if current_op == "push":
        stack.append(current_arg)
        highlight_top = True
    elif current_op == "pop" and stack:
        popped_item = stack.pop()
    elif current_op == "top" and stack:
        top_item = stack[-1]
        highlight_top = True

    # ── Title ──
    ax.text(5, 9.5, "Stack Animation", fontsize=16, fontweight='bold',
            ha='center', va='center', color='#1A1A2E')

    # ── Operation display ──
    op_color = OP_COLORS.get(current_op, "#333")
    ax.text(5, 8.9, f"[{current_op.upper()}]  {current_desc}",
            fontsize=10.5, ha='center', va='center', color=op_color,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFFFF',
                      edgecolor=op_color, linewidth=1.8))

    # ── Stack box ──
    box_left = 3.5
    box_right = 6.5
    box_bottom = 1.0
    cell_height = 0.58

    # Outer border
    rect = mpatches.FancyBboxPatch((box_left - 0.05, box_bottom - 0.05),
                                   (box_right - box_left + 0.1),
                                   (MAX_SIZE * cell_height + 0.3),
                                   boxstyle="round,pad=0.05",
                                   linewidth=2, edgecolor='#B0B8C1',
                                   facecolor=STACK_BG)
    ax.add_patch(rect)

    # Empty slots
    for i in range(MAX_SIZE):
        y = box_bottom + i * cell_height
        slot = mpatches.FancyBboxPatch((box_left, y), box_right - box_left, cell_height - 0.04,
                                       boxstyle="round,pad=0.02",
                                       linewidth=0.5, edgecolor='#D0D7DE', facecolor='#FFFFFF')
        ax.add_patch(slot)
        ax.text(box_left - 0.3, y + cell_height / 2, str(i),
                fontsize=7.5, ha='right', va='center', color='#999')

    # Filled cells
    for i, word in enumerate(stack):
        y = box_bottom + i * cell_height
        is_top = (i == len(stack) - 1)
        fc = TOP_COLOR if (is_top and highlight_top) else CELL_COLOR
        ec = TOP_EDGE if (is_top and highlight_top) else CELL_EDGE
        cell = mpatches.FancyBboxPatch((box_left, y), box_right - box_left, cell_height - 0.04,
                                       boxstyle="round,pad=0.04",
                                       linewidth=1.5, edgecolor=ec, facecolor=fc)
        ax.add_patch(cell)
        ax.text((box_left + box_right) / 2, y + cell_height / 2, word,
                fontsize=10, ha='center', va='center', color='white', fontweight='bold')

    # TOP arrow
    if stack:
        top_y = box_bottom + (len(stack) - 1) * cell_height + cell_height / 2
        ax.annotate("", xy=(box_right, top_y),
                    xytext=(box_right + 0.8, top_y),
                    arrowprops=dict(arrowstyle="->", color=TOP_COLOR, lw=2))
        ax.text(box_right + 0.9, top_y, "top", fontsize=9, color=TOP_COLOR,
                va='center', fontweight='bold')

    # ── Popped / Top label ──
    if popped_item:
        ax.text(5, 0.55, f'pop → "{popped_item}"', fontsize=11, ha='center',
                color='#C62828', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFEBEE', edgecolor='#C62828'))
    if top_item and not popped_item:
        ax.text(5, 0.55, f'top → "{top_item}"', fontsize=11, ha='center',
                color='#1565C0', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#E3F2FD', edgecolor='#1565C0'))

    # ── Stack label ──
    ax.text(5, box_bottom + MAX_SIZE * cell_height + 0.35,
            f"Stack (size: {len(stack)}/{MAX_SIZE})", fontsize=9,
            ha='center', va='bottom', color='#555')

    # ── Step counter ──
    ax.text(9.7, 0.2, f"step {frame_idx+1}/{len(sequence)}",
            fontsize=8, ha='right', color='#999')

# Animate: each frame holds for ~80 frames worth via repeat
HOLD = 45  # frames to hold each step
total_frames = len(sequence) * HOLD

def animate(frame):
    step = min(frame // HOLD, len(sequence) - 1)
    draw_frame(step)

anim = animation.FuncAnimation(fig, animate, frames=total_frames, interval=40, repeat=False)

writer = animation.FFMpegWriter(fps=25, bitrate=1800)
out_path = '/home/claude/stack_animation.mp4'
anim.save(out_path, writer=writer, dpi=120)
plt.close()
print(f"Saved: {out_path}")
