import tkinter as tk

def calculate():
    expression = entry.get()
    result = eval(expression)
    label.config(text=result)

def add_to_expression(value):
    current_expression = entry.get()
    new_expression = current_expression + str(value)
    entry.delete(0, tk.END)
    entry.insert(tk.END, new_expression)

root = tk.Tk()
root.title('Calculator')

entry = tk.Entry(root)
entry.pack()

# Create digit buttons
for i in range(1, 10):
    button = tk.Button(root, text=str(i), command=lambda i=i: add_to_expression(i))
    button.pack(side=tk.LEFT)

# Create operator buttons
operators = ['+', '-', '*', '/']
for operator in operators:
    button = tk.Button(root, text=operator, command=lambda operator=operator: add_to_expression(operator))
    button.pack(side=tk.LEFT)

button = tk.Button(root, text='=', command=calculate)
button.pack(side=tk.LEFT)

label = tk.Label(root, text='Result:')
label.pack()

root.mainloop()
