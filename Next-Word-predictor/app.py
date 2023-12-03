import tkinter as tk
import tkinter.font as font
import random
from model import predictor

# Declaration

txtbox = prediction1 = prediction2 = prediction3 = None

# Prediction model
def suggest(text):
    suggestions = ['-'] * 3
    for idx, i in enumerate(predictor.generate_suggestion(text)):
        suggestions[idx] = i[0]
    # print('Entered Text: ', text)
    # print(suggestions)
    return suggestions

# Handler
def handle_input(e, force=False):
    # print(e)
    if force or e.keysym=='space' or e.keysym=='Return':
        entered_text = txtbox.get('1.0','end-1c')
        s = suggest(entered_text)
        prediction1.config(text=s[2] or '-')
        prediction2.config(text=s[0] or '-')
        prediction3.config(text=s[1] or '-')
        
def handle_click(e):
    choice = e.widget.cget('text')
    if choice != '-':
        txtbox.insert("end-1c", choice+' ')
        handle_input({}, force=True)

# Widgets Configuration
window = tk.Tk()
myFont = font.Font(family='times', size=15, weight='bold')

txtbox = tk.Text(window, borderwidth=5, relief='ridge')
txtbox.grid(row = 1, columnspan = 3)
txtbox.bind('<Key>', handle_input)

prediction1 = tk.Button(text='-', width = 20, height=3,activeforeground = 'cyan',activebackground = '#333333', relief='raised')
prediction1.grid(row = 0, column = 2)
prediction1['font'] = myFont
prediction1.bind('<Button-1>', handle_click)

prediction2 = tk.Button(text='-',width = 20, height=3,activeforeground = 'cyan',activebackground = '#333333', relief='raised')
prediction2.grid(row = 0, column = 1)
prediction2['font'] = myFont
prediction2.bind('<Button-1>', handle_click)

prediction3 = tk.Button(text='-',width = 20, height=3,activeforeground = 'cyan',activebackground = '#333333', relief='raised')
prediction3.grid(row = 0, column = 0)
prediction3['font'] = myFont
prediction3.bind('<Button-1>', handle_click)

window.title('Word Predictor')
window.mainloop()
