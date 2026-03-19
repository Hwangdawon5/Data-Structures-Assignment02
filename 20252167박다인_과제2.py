import tkinter as tk
import time

raw_keywords = [
    # Keyword_1
    "아메리카노", "커피", "벚꽃", "나무", "핑크", "꽃축제", "스타벅스",
    # Keyword_2
    "라떼", "디저트", "테라스", "바람", "카라멜 라떼", "라떼", "아메리카노",
    # Keyword_3
    "연애", "커플", "아인슈페너", "개강", "슈크림 라떼", "디저트", "꽃"
]

words = []
[words.append(x) for x in raw_keywords if x not in words]

stack = []

class StackAnim:
    def __init__(self, root):
        self.root = root
        self.root.title("팀 과제: 스택 연산 애니메이션")
        self.canvas = tk.Canvas(root, width=700, height=600, bg="white")
        self.canvas.pack()
        

        self.canvas.create_text(350, 30, text="Stack Operations (Team Keywords)", font=("Malgun Gothic", 18, "bold"))
        self.canvas.create_text(350, 60, text="Constraint: Stack size <= 10", font=("Consolas", 10), fill="gray")
        
       
        self.run_animation()

    def draw_stack(self, command):
        self.canvas.delete("content") 
        
        self.canvas.create_text(200, 250, text=command, font=("Consolas", 16, "bold"), fill="blue", tags="content")
    
        start_x, start_y = 450, 500
        box_width, box_height = 180, 40

        for i, item in enumerate(stack):
            x1, y1 = start_x, start_y - (i * box_height)
            x2, y2 = start_x + box_width, y1 - box_height
            
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill="#f0f0f0", tags="content")
        
            self.canvas.create_text((x1 + x2)/2, (y1 + y2)/2, text=item, font=("Malgun Gothic", 12), tags="content")

        self.root.update()

    def run_animation(self):
  
        self.draw_stack("stack = []")
        time.sleep(1.5)

        for word in words:
        
            stack.append(word)
            self.draw_stack(f"stack.push('{word}')")
            time.sleep(0.8)

           
            if len(stack) >= 8:
              
                self.draw_stack(f"stack.top() -> '{stack[-1]}'")
                time.sleep(0.8)
                
               
                for _ in range(3):
                    popped = stack.pop()
                    self.draw_stack(f"stack.pop() -> '{popped}'")
                    time.sleep(0.8)

        self.draw_stack("모든 팀원 단어 처리 완료!")

# 실행부
if __name__ == "__main__":
    root = tk.Tk()
    app = StackAnim(root)
    root.mainloop()