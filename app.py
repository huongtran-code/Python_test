import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
import re 

API_KEY = "AIzaSyB_5B31t8IHDUYeTFD3W4caJ4_oACtiUB8"
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

chat_session = model.start_chat(history=[])

def send_message():
    user_input = entry_message.get().strip()
    if not user_input:
        return

    # 1. Hiển thị tin nhắn của người dùng lên màn hình chat
    text_chat.config(state=tk.NORMAL)
    text_chat.insert(tk.END, f"\n🧑‍💻 Bạn:\n", "user_tag")
    text_chat.insert(tk.END, f"{user_input}\n", "user_msg")
    
    entry_message.delete(0, tk.END)
    text_chat.see(tk.END)
    
    btn_send.config(state=tk.DISABLED, text="⏳...", bg="#95a5a6")
    root.update()

    try:
        # 2. Gửi prompt cho Gemini (giao tiếp tự nhiên)
        prompt = f"{user_input}. Nếu kết quả có code Python, hãy bọc code đó trong dấu nháy ```python."
        response = chat_session.send_message(prompt)
        
        # 3. Hiển thị tin nhắn của AI
        text_chat.insert(tk.END, f"\n🤖 AI:\n", "ai_tag")
        
        process_ai_response(response.text)
        
    except Exception as e:
        text_chat.insert(tk.END, f"\n⚠️ Lỗi: {str(e)}\n", "error_msg")
    
    # Khôi phục trạng thái nút và cuộn xuống cuối
    text_chat.config(state=tk.DISABLED)
    text_chat.see(tk.END)
    btn_send.config(state=tk.NORMAL, text="GỬI", bg="#3498db")

def process_ai_response(text):
    
    code_pattern = r"```python(.*?)```"
    matches = re.split(code_pattern, text, flags=re.DOTALL)
    
    is_code_block = False 

    for part in matches:
        part = part.strip()
        if not part: continue

        if not is_code_block:
            text_chat.insert(tk.END, f"{part}\n\n", "ai_msg")
        else:
            text_chat.insert(tk.END, "\n", "ai_msg")
            create_code_block(part)
            text_chat.insert(tk.END, "\n", "ai_msg")
        
        is_code_block = not is_code_block

def create_code_block(code_text):
    
    frame_code = tk.Frame(text_chat, bg="#f8f9fa", padx=5, pady=5)
    
    btn_copy = tk.Button(frame_code, text="Copy", command=lambda: copy_code(code_text), 
                         bg="#ecf0f1", fg="#7f8c8d", font=("Arial", 8), bd=0, padx=5)
    btn_copy.pack(anchor="ne", pady=(0, 5))

    code_widget = tk.Text(frame_code, font=("Consolas", 10), bg="#2c3e50", fg="white", 
                         height=10, width=60, wrap=tk.NONE)
    code_widget.insert(tk.END, code_text)
    code_widget.config(state=tk.DISABLED)
    code_widget.pack(fill="x")
    
    scroll_x = tk.Scrollbar(frame_code, orient="horizontal", command=code_widget.xview)
    code_widget.config(xscrollcommand=scroll_x.set)
    scroll_x.pack(fill="x")

    text_chat.window_create(tk.END, window=frame_code)
    text_chat.insert(tk.END, "\n") # Xuống dòng sau khi chèn khung code

def copy_code(code):
    root.clipboard_clear()
    root.clipboard_append(code)
    root.update() # Giữ code trong clipboard sau khi đóng ứng dụng
    messagebox.showinfo("Thông báo", "Đã copy code vào clipboard!")

def clear_chat():
    """Xóa lịch sử chat cũ"""
    global chat_session
    chat_session = model.start_chat(history=[])
    text_chat.config(state=tk.NORMAL)
    text_chat.delete(1.0, tk.END)
    text_chat.config(state=tk.DISABLED)
    welcome_message()

def welcome_message():
    """Hiển thị lời chào đầu tiên"""
    text_chat.config(state=tk.NORMAL)
    text_chat.insert(tk.END, "🤖 Trợ lý AI (Gemini 2.5 Flash):\n", "ai_tag")
    text_chat.insert(tk.END, "Xin chào! Bạn muốn giao tiếp, hỏi lỗi, hay yêu cầu viết code Python?\n\n", "ai_msg")
    text_chat.config(state=tk.DISABLED)

# --- GIAO DIỆN CHAT HIỆN ĐẠI ---
root = tk.Tk()
root.title("Python AI Programming Assistant")
root.geometry("750x650")
root.configure(bg="#f0f3f5")

# Header
header = tk.Frame(root, bg="#2c3e50", height=60)
header.pack(fill="x")
tk.Label(header, text="GIAO TIẾP & LẬP TRÌNH CÙNG AI", fg="white", bg="#2c3e50", font=("Segoe UI", 13, "bold")).pack(pady=15)

# Cấu hình Style Chat (Tags)
text_chat = scrolledtext.ScrolledText(root, font=("Segoe UI", 11), bg="#ffffff", bd=0, 
                                        highlightthickness=1, highlightbackground="#dcdde1")
text_chat.pack(pady=(20, 10), padx=25, fill="both", expand=True)

# Định nghĩa các thẻ định dạng tin nhắn
text_chat.tag_config("user_tag", foreground="#34495e", font=("Segoe UI", 10, "bold"), spacing1=10)
text_chat.tag_config("user_msg", foreground="#2c3e50", spacing3=10, background="#ecf0f1", wrap=tk.WORD)

text_chat.tag_config("ai_tag", foreground="#3498db", font=("Segoe UI", 10, "bold"), spacing1=10)
text_chat.tag_config("ai_msg", foreground="#34495e", spacing3=10)
text_chat.tag_config("error_msg", foreground="#e74c3c", font=("Arial", 10, "italic"))

text_chat.config(state=tk.DISABLED)

# Lời chào đầu tiên
welcome_message()

frame_input = tk.Frame(root, bg="#f0f3f5")
frame_input.pack(pady=(0, 15), padx=25, fill="x")

entry_message = tk.Entry(frame_input, font=("Segoe UI", 12), bd=0, highlightthickness=1)
entry_request = entry_message # Giữ nguyên tên biến cũ cho tiện sửa code
entry_message.config(highlightbackground="#dcdde1", highlightcolor="#3498db")
entry_message.pack(side="left", fill="x", expand=True, ipady=8)
entry_message.bind("<Return>", lambda event: send_message()) # Nhấn Enter để gửi

btn_send = tk.Button(frame_input, text="GỬI", command=send_message, 
                        bg="#3498db", fg="white", font=("Helvetica", 11, "bold"), 
                        bd=0, cursor="hand2", padx=25, activebackground="#2980b9", activeforeground="white")
btn_send.pack(side="right", padx=(10, 0), ipady=8)

# Nút xóa lịch sử chat
btn_clear = tk.Button(root, text="XÓA LỊCH SỬ CHAT", command=clear_chat, 
                        bg="#e74c3c", fg="white", font=("Helvetica", 9, "bold"), bd=0)
btn_clear.pack(side="right", padx=25, pady=(0, 15))

# Footer
tk.Label(root, text="Powered by Gemini 2.5 Flash API with Chat History", bg="#f0f3f5", fg="#95a5a6", font=("Arial", 8, "italic")).pack(pady=(0, 10))

root.mainloop()