# from winpty import PtyProcess

# proc = PtyProcess.spawn('python')
# proc.write('print("hello, world!")\r\n')
# a = proc.read()
# print(a)
# proc.write('exit()\r\n')
# while proc.isalive():
# 	print(proc.readline())
import customtkinter as ctk
from winpty import PtyProcess
from ansi2html import Ansi2HTMLConverter
proc = PtyProcess.spawn('bash.exe')
# while True:
#     command = input("Enter command: ")
#     if command.lower() == 'exit':
#         break
#     proc.write(command + '\r\n')
#     print(proc.read())
#     # output = proc.read()
# proc.write('exit()\r\n')
# # while proc.isalive():
# #     print(proc.readline())


root = ctk.CTk()
root.geometry("400x300")

textbox = ctk.CTkTextbox(root, width=300, height=200)
textbox.pack(pady=20)
textbox.insert("0.0", "Output will appear here...\n")

input_area = ctk.CTkEntry(root, placeholder_text="Enter command here")
input_area.pack(pady=10)

def run_command():
    command = input_area.get()
    proc.write(command + '\r\n')
    output = proc.read()
    clear_output = Ansi2HTMLConverter().convert(output)
    textbox.insert("end", clear_output + "\n")
button = ctk.CTkButton(root, text="Run Command", command=run_command)
button.pack(pady=10)
root.mainloop()