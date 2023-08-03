import tkinter as tk

def calculate():
    expression = entry.get()
    result = eval(expression)
    label.config(text=result)

root = tk.Tk()
root.title('Calculator')

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text='Calculate', command=calculate)
button.pack()

label = tk.Label(root, text='Result:')
label.pack()

root.mainloop()
