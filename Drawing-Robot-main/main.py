import ply.lex as lex
import ply.yacc as yacc
import turtle
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

window = Tk()
window.geometry("1000x700")
window.title("GUI")
window.config(bg="grey", highlightbackground='red')

#dosyadan alma
def file_open():
    tf = askopenfilename(initialdir='C:/', title='Select a File', filetype=(("Text File", ".txt"), ("All Files", "*.*")))
    tf = open(tf, 'r')
    data1 = tf.read()
    text.insert(END, data1)
    lexer_func()


canvas = Canvas(window, width=1000, height=400)
canvas.grid(row=0, columnspan=6, pady=20)

text = Text(window, width=50, height=10)
text.grid(row=1, column=1)

button = ttk.Button(window, text='Dosya Ac', command=file_open)
button.grid(row=2, column=1)

# mesaj
# frame2 = Frame(window, width=500, height=130, highlightbackground='black', highlightthickness=2)
# frame2.grid(row=1, column=2, padx=20, pady=20, ipadx=20, ipady=20)
text2 = Text(window, width=50, height=10)
text2.grid(row=1, column=2)

tim = turtle.RawTurtle(canvas)

def f(val):
    tim.forward(val)


def r(val):
    tim.right(val)


def color(val):
    if val == "K":
        tim.color("red")
    elif val == "Y":
        tim.color("green")
    elif val == "M":
        tim.color("blue")
    elif val == "S":
        tim.color("yellow")


def pensize(val):
    if val == 1:
        tim.width(1)
    elif val == 2:
        tim.width(5)
    elif val == 3:
        tim.width(10)

#------------------------------------------LEX--------------------------------------------------------------------------
def lexer_func():

    tokens = ('LOOP', 'FORWARD', 'RIGHT', 'CCOLOR', 'COLOR', 'PEN', 'NUMBER', 'LPAREN', 'RPAREN')


    t_LOOP = r'L'
    t_FORWARD = r'F'
    t_RIGHT = r'R'
    t_CCOLOR = r'COLOR'
    t_COLOR = r'[KYMS]'
    t_PEN = r'PEN'
    t_LPAREN = r'\['
    t_RPAREN = r'\]'

    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_ignore = ' \t'

    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    lexer = lex.lex()
    data = text.get('1.0', "end-1c")
    lexer.input(data)
    token_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        token_list.append(tok.value)
        print(tok)

    func(token_list)
    return token_list

#------------------------------------------YACC-------------------------------------------------------------------------
def yaccer():
    def p_statement(p):
        ''' statement : expression '''
        p[0] = p[1]

    def p_expression_fr(p):
        '''
        expression : FORWARD NUMBER
                   | RIGHT NUMBER
                   | PEN NUMBER
                   | CCOLOR COLOR
        '''
        p[0] = p[1], p[2]

    def p_expression_fr2(p):
        '''
         expression : FORWARD NUMBER statement
                   | RIGHT NUMBER statement
                   | PEN NUMBER statement
                   | CCOLOR COLOR statement
        '''
        p[0] = p[1], p[2], p[3]

    def p_expression_l(p):
        '''
        expression : LOOP NUMBER LPAREN statement RPAREN
        '''
        p[0] = p[1], p[2], p[3], p[4], p[5]

    def p_expression_l2(p):
        '''
        expression : LOOP NUMBER LPAREN statement RPAREN statement
        '''
        p[0] = p[1], p[2], p[3], p[4], p[5], p[6]

    def p_empty(p):
        'empty :'
        pass

    def p_error(p):
        print("Syntax error in input!")

    parser = yacc.yacc()
    s = "L 36[ L 4 [F 100 R 90] R 10]"

    result = parser.parse(s)
    print(result)


#-----------EKRANA ÇİZDİRME KOMUTU--------------------------------------------------------------------------------------
def func(tokens, index=0):
    tim.speed(0)
    a_parantez = 0
    k_parantez = 0
    for i in range(len(tokens)):
        if tokens[i] == '[':
            a_parantez = a_parantez+1
        elif tokens[i] == ']':
            k_parantez = k_parantez+1

    while index < len(tokens):

        secim = tokens[index]
        index += 1
        if a_parantez > k_parantez:
            hata = "Açtığınız parantezi kapatmadınız!"
            text2.insert(END, hata)
            quit(func())
        if secim == 'L':
            if type(tokens[index]) != int and tokens[index] != '[':
                hata  ="L komutundan sonra sayı değeri girmediniz ve parantez açmadınız!"
                text2.insert(END, hata)
                quit(func())
            elif type(tokens[index]) != int:
                hata = "L komutundan sonra sayı değeri girmediniz!"
                text2.insert(END, hata)
                quit(func())
            elif tokens[index+1] != '[':
                hata = "L komutundan sonra parantez açmadınız!"
                text2.insert(END, hata)
                quit(func())
            elif type(tokens[index]) == int and tokens[index+1] == '[':
                dongu = tokens[index]
                index += 2

                for _ in range(dongu):
                    new_index = func(tokens, index)

                index = new_index
        elif secim == 'F':
            if type(tokens[index]) == int:
                mesafe = tokens[index]
                index += 1
                f(mesafe)
            elif type(tokens[index]) != int:
                hata = "F komutundan sonra sayı koymadınız!"
                text2.insert(END, hata)
                quit(func())
        elif secim == 'R':
            if type(tokens[index]) == int:
                val = tokens[index]
                index += 1
                r(val)
            elif type(tokens[index]) != int:
                hata = "R komutundan sonra sayı koymadınız!"
                text2.insert(END, hata)
                quit(func())
        elif secim == 'COLOR':
            if tokens[index] == 'K' or tokens[index] == 'Y' or tokens[index] == 'M' or tokens[index] == 'S':
                value = tokens[index]
                index += 1
                color(value)
            else:
                hata = "COLOR komutundan sonra doğru renk değeri girmediniz!"
                text2.insert(END, hata)
                quit(func())
        elif secim == 'PEN':
            if tokens[index] == 1 or tokens[index] == 2 or tokens[index] == 3:
                value2 = tokens[index]
                index += 1
                pensize(value2)
            else:
                hata = "PEN komutundan sonra doğru boyut değeri girmediniz!"
                text2.insert(END, hata)
                quit(func())
        elif secim == ']':
            break
        elif type(secim) == int:
            hata = "Komutsuz sayı değeri girdiniz!"
            text2.insert(END, hata)
            quit(func())
        else:
            hata = "Tanımlanmamış bilgi girdiniz!"
            text2.insert(END, hata)
            quit(func())

    return index



window.mainloop()



