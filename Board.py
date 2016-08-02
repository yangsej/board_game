import pyVulkan as Vk
from tkinter import *
from Unit import *

from win32api import GetSystemMetrics



class Board:
    def __init__(self, rows, cols):
        #맵의 크기
        self.rows = rows
        self.cols = cols

        #기본 설정
        self.row_pos = 8
        self.col_pos = 8

        self.rect_size = 50
        

        #보드와 유저들 프레임
        b_u_frame = Frame(root, )
        b_u_frame.pack(expand=True, fill=BOTH)

        #보드 프레임
        board_frame = Frame(b_u_frame)
        board_frame.grid_rowconfigure(0, weight=1)
        board_frame.grid_columnconfigure(0, weight=1)
        
        board_frame.pack(side=LEFT, expand=True, fill=BOTH)


        #보드 캔버스
        self.board_canvas = Canvas(board_frame, height=850,width=850, bg='black', confine=False,
                                   xscrollincrement=self.rect_size, yscrollincrement=self.rect_size)
        self.board_canvas.grid(row=0, column=0)#, sticky='nsew')


        #타일 생성
        self.canvas = []
        for r in range(rows):
            self.canvas.append([])
            for c in range(cols):
##                self.canvas[h].append(Button(board_canvas, height=3, width=6, bg='white', bd=1, relief=GROOVE, state=DISABLED))
##                board_canvas.create_window(w*50, h*50, anchor=NW, window=self.canvas[h][w])
                self.canvas[r].append(self.board_canvas.create_rectangle
                                      ((c*self.rect_size, r*self.rect_size), ((c+1)*self.rect_size, (r+1)*self.rect_size), fill='white', ))
        self.pos_rect = self.board_canvas.create_rectangle(
            (self.col_pos*self.rect_size, self.row_pos*self.rect_size),
            ((self.col_pos+1)*self.rect_size, (self.row_pos+1)*self.rect_size),
            outline='blue', width=5)#, fill='#8AC6ff')

        self.sel_rect = self.board_canvas.create_rectangle(
            (0, 0), (self.rect_size, self.rect_size),
            outline='yellow', width=3, state=HIDDEN,)#, fill='#8AC6ff')

        #보드와 스크롤 묶기
        root.bind('<Left>', self._scroll)
        root.bind('<Right>', self._scroll)
        root.bind('<Up>', self._scroll)
        root.bind('<Down>', self._scroll)

        #캔버스의 스크롤 구역 제한
        board_bbox = list(self.board_canvas.bbox(ALL))
        board_bbox[0] -= 49
        board_bbox[1] -= 49
        board_bbox[2] -= 1
        board_bbox[3] += 49
        self.board_canvas.config(scrollregion=board_bbox)
        


        #선택과 유저 프레임
        s_u_frame = Frame(b_u_frame,)
        s_u_frame.pack(side=RIGHT, fill=Y)


        #선택 리스트
        sel_Lab = Label(s_u_frame, text='선택지')
        sel_Lab.pack()
        
        self.sel_Lb = Listbox(s_u_frame, height=20, width=30, state=DISABLED)
        self.sel_Lb.pack()


        root.bind('z', self._select)
##        root.bind('Z', self._select)
        root.bind('x', self._select)
##        root.bind('X', self._select)
        
        
        #유저 리스트
        users_Lab = Label(s_u_frame, text='사용자')
        users_Lab.pack()
        
        users_Lb = Listbox(s_u_frame, width=30, activestyle=NONE, highlightcolor='white',
                           selectforeground='black', selectbackground='white')
        users_Lb.pack(fill=Y, expand=True)


        users_Lb.insert(END,'KSK')
        users_Lb.insert(END,'KSC')
        users_Lb.insert(END,'Computer1')
        users_Lb.insert(END,'Computer2')


        #정보 프레임
        i_frame = LabelFrame(root, text='info')
        i_frame.pack(fill=X, side=BOTTOM)

        #정보 라벨
        info_label = Label(i_frame,text='이름')
        info_label.pack(fill=X)
##        info_label.place(bordermode=OUTSIDE, x=0, y=0, height=100, width=100)


    def _scroll(self, event):
        if self.sel_Lb.config('state')[-1] == DISABLED:
            if event.keysym == 'Left':
                if self.col_pos > 0:
                    self.board_canvas.xview_scroll(-1, UNITS)
                    self.col_pos -= 1
                    self.board_canvas.move(self.pos_rect, -self.rect_size, 0)
            elif event.keysym == 'Right':
                if self.col_pos < self.cols-1:
                    self.board_canvas.xview_scroll(1, UNITS)
                    self.col_pos += 1
                    self.board_canvas.move(self.pos_rect, self.rect_size, 0)
            elif event.keysym == 'Up':
                if self.row_pos > 0:
                    self.board_canvas.yview_scroll(-1, UNITS)
                    self.row_pos -= 1
                    self.board_canvas.move(self.pos_rect, 0, -self.rect_size)
            elif event.keysym == 'Down':
                if self.row_pos < self.rows-1:
                    self.board_canvas.yview_scroll(1, UNITS)
                    self.row_pos += 1
                    self.board_canvas.move(self.pos_rect, 0, self.rect_size)
        else:
            pass

    def _select(self, event):
        if event.keysym == 'z':
            if self.sel_Lb.config('state')[-1] == DISABLED:
                self.board_canvas.itemconfig(self.sel_rect, state=NORMAL)
                self.board_canvas.coords(self.sel_rect, self.board_canvas.coords(self.pos_rect))
                self.board_canvas.lift(self.sel_rect)
                self.board_canvas.config(state=DISABLED)

                
                self.sel_Lb.config(state=NORMAL)
                self.sel_Lb.insert(END,'이동')
                self.sel_Lb.insert(END,'공격')
                self.sel_Lb.insert(END,'기술')
                self.sel_Lb.insert(END,'취소')
                self.sel_Lb.focus()
                self.sel_Lb.select_set(0)
                self.sel_Lb.activate(0)
##                print(dir(self.sel_Lb))
            else:
                sel = self.sel_Lb.selection_get()
                
                
                
                
##                self.board_canvas.move(self.sel_rect,
##                                       self.board_canvas.itemcget(self.sel_rect, x)
##                                       - self.board_canvas.itemget(self.pos_rect, x),
##                                       self.board_canvas.itemcget(self.sel_rect, y)
##                                       - self.board_canvas.itemget(self.pos_rect, y),)
            pass
        elif event.keysym == 'x':
            pass

    def set_unit(self, x, y, unit):
        unit.x = x
        unit.y = y

        self.image = PhotoImage(file = unit.image)
##        h = self.image.height()
##        w = self.image.width()
##        self.image = self.image.zoom(self.rect_size)
##        self.image = self.image.subsample(w, h)
        self.board_canvas.create_image(x*self.rect_size+self.image.width()//2,
                                       y*self.rect_size+self.image.height()//2,
                                       image=self.image)
        self.board_canvas.lift(self.pos_rect)


    def move(self, x, y):
        temp = self.frame
        unit = temp[x][y]

        print(unit)
        if type(unit) == Unit:
            for m in range(-unit.stat['speed'], unit.stat['speed']+1):
                for n in range(-(unit.stat['speed']-abs(m)), unit.stat['speed']-abs(m)+1):
                    if (not n and not m) or (x+m < 0 or x+m > self.height or y+n < 0 or y+n > self.width): continue
                    temp[x+m][y+n] = '■'

            show = ''
            for h in temp:
                for w in h:
                    show += str(w)
                show += '\n'
            print(show)


            xto = int(input("x 이동량: "))
            yto = int(input("y 이동량: "))
            self.frame[x][y] = '□'
            self.frame[x+xto][y+yto] = unit

            for m in range(-unit.stat['speed'], unit.stat['speed']+1):
                for n in range(-(unit.stat['speed']-abs(m)), unit.stat['speed']-abs(m)+1):
                    if (not n and not m) or (x+m < 0 or x+m > self.height or y+n < 0 or y+n > self.width): continue
                    temp[x+m][y+n] = '□'

            show = ''
            for h in temp:
                for w in h:
                    show += str(w)
                show += '\n'
            print(show)

            unit.move(xto,yto)


##a.set_unit(1,3,Unit(speed = 5))
##a.set_unit(40,30,Unit())
##print(a)
##
##a.move(1,3)

root = Tk()
root.geometry('1200x1000+0+0')
root.title('턴제 게임')

a = Board(10,10)
a.set_unit(0,1,핫산)
root.mainloop()
