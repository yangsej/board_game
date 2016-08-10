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
        self.row_pos = 4
        self.col_pos = 4

        self.rect_size = 100
        

        #보드와 유저들 프레임
        b_u_frame = Frame(root, )
        b_u_frame.pack(expand=True, fill=BOTH)

        #보드 프레임
        board_frame = Frame(b_u_frame)
        board_frame.grid_rowconfigure(0, weight=1)
        board_frame.grid_columnconfigure(0, weight=1)
        
        board_frame.pack(side=LEFT, expand=True, fill=BOTH)


        #보드 캔버스
        self.board_canvas = Canvas(board_frame, height=900,width=900, bg='black', confine=False,
                                   xscrollincrement=self.rect_size, yscrollincrement=self.rect_size)
        self.board_canvas.grid(row=0, column=0)#, sticky='nsew')


        #타일 생성
        self.canvas = []
        for r in range(rows):
            self.canvas.append([])
            for c in range(cols):
                self.canvas[r].append(
                    {
                        'ID' : self.board_canvas.create_rectangle((c*self.rect_size, r*self.rect_size),
                                                                  ((c+1)*self.rect_size, (r+1)*self.rect_size),
                                                                  fill='white', ),
                    })
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
        root.bind('x', self._cancel)
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
        if self.sel_Lb.config('state')[-1] == DISABLED: # 판의 활성화 상태
            if self.board_canvas.itemcget(self.sel_rect, 'state') == NORMAL: # 유닛 선택 상태
                sel_coords = self.board_canvas.coords(self.sel_rect)
                sel_x = int(sel_coords[0])//self.rect_size
                sel_y = int(sel_coords[1])//self.rect_size
                unit = self.canvas[sel_y][sel_x].get('unit')
                
                self._move(unit)
                
            elif self.canvas[self.row_pos][self.col_pos].get('unit'): # 유닛의 존재 상태
                # 판 비활성화
                self.board_canvas.itemconfig(self.sel_rect, state=NORMAL)
                self.board_canvas.coords(self.sel_rect, self.board_canvas.coords(self.pos_rect))
                self.board_canvas.lift(self.sel_rect)
                self.board_canvas.config(state=DISABLED)

                # 선택지 활성화
                self.sel_Lb.config(state=NORMAL)
                self.sel_Lb.insert(END,'이동', '공격', '기술')
                self.sel_Lb.focus()
                self.sel_Lb.select_set(0)
                self.sel_Lb.activate(0)
                
        else:
            sel = self.sel_Lb.selection_get()
            if sel == '이동': self._move_range(self.canvas[self.row_pos][self.col_pos].get('unit'))
            elif sel == '공격': self._attack_range(self.canvas[self.row_pos][self.col_pos].get('unit'))
            elif sel == '기술': self._skill()
                

    def _cancel(self, event):
        pass

    def _move_range(self, unit):
        self.move_rects = []
        for m in range(-unit.stat['speed'], unit.stat['speed']+1):
            for n in range(-(unit.stat['speed']-abs(m)), unit.stat['speed']-abs(m)+1):
                if unit.x+m < 0 or unit.x+m > self.rows-1  or unit.y+n < 0 or unit.y+n > self.cols-1: pass
                elif self.canvas[unit.y+n][unit.x+m].get('unit', None): pass
                else:
                    self.move_rects.append(self.board_canvas.create_rectangle(
                    ((unit.x+m)*self.rect_size, (unit.y+n)*self.rect_size),
                    ((unit.x+m+1)*self.rect_size, (unit.y+n+1)*self.rect_size),
                    fill='skyblue'))

        # 판 활성화
        self.board_canvas.config(state=NORMAL)
        self.board_canvas.lift(self.sel_rect)
        self.board_canvas.lift(self.pos_rect)

        # 선택지 비활성화
        self.sel_Lb.delete(0, END)
        self.sel_Lb.config(state=DISABLED)


    def _move(self, unit):
        sel_coords = self.board_canvas.coords(self.sel_rect)
        sel_x = int(sel_coords[0])//self.rect_size
        sel_y = int(sel_coords[1])//self.rect_size
        dist = abs(self.row_pos - sel_y) + abs(self.col_pos - sel_x)
        if 0 < dist <= unit.stat['speed'] and not self.canvas[self.row_pos][self.col_pos].get('unit', False):
            self.canvas[self.row_pos][self.col_pos]['unit'] = self.canvas[unit.y][unit.x].pop('unit')

            self.board_canvas.coords(unit.image_ID,
                                     self.board_canvas.coords(self.pos_rect)[0] + self.rect_size//2,
                                     self.board_canvas.coords(self.pos_rect)[1] + self.rect_size//2)
            for R in self.move_rects:
                self.board_canvas.delete(R)
            del(self.move_rects)
            self.board_canvas.itemconfig(self.sel_rect, state=HIDDEN)

            unit.x = self.col_pos
            unit.y = self.row_pos

    def _attack_range(self, unit):
        self.attack_rects = []
        self.target_rects = []
        for m in range(-unit.stat['range'], unit.stat['range']+1):
            for n in range(-(unit.stat['range']-abs(m)), unit.stat['range']-abs(m)+1):
                if unit.x+m < 0 or unit.x+m > self.rows-1  or unit.y+n < 0 or unit.y+n > self.cols-1: pass
                elif not m and not n: pass
                else:
                    self.attack_rects.append(self.board_canvas.create_rectangle(
                    ((unit.x+m)*self.rect_size, (unit.y+n)*self.rect_size),
                    ((unit.x+m+1)*self.rect_size, (unit.y+n+1)*self.rect_size),
                    fill='orange'))

                    other_unit = self.canvas[unit.y+n][unit.x+m].get('unit', None)
                    if other_unit:
                        self.board_canvas.lift(other_unit.image_ID)
                        self.target_rects.append(self.board_canvas.create_rectangle(
                            (other_unit.x*self.rect_size, other_unit.y*self.rect_size),
                            ((other_unit.x+1)*self.rect_size, (other_unit.y+1)*self.rect_size),
                            outline='red', width=3))

        # 판 활성화
        self.board_canvas.config(state=NORMAL)
        for T in self.target_rects:
            self.board_canvas.lift(T)
        self.board_canvas.lift(self.sel_rect)
        self.board_canvas.lift(self.pos_rect)

        # 선택지 비활성화
        self.sel_Lb.delete(0, END)
        self.sel_Lb.config(state=DISABLED)
        
    def _skill(self):
        pass
            
    def set_unit(self, unit, x, y):
        unit.x = x
        unit.y = y

        unit.image = PhotoImage(file = unit.image)
        
        unit.image_ID = self.board_canvas.create_image(x*self.rect_size+unit.image.width()//2,
                                       y*self.rect_size+unit.image.height()//2,
                                       image=unit.image)
        self.board_canvas.lift(self.pos_rect)

        self.canvas[y][x]['unit'] = unit

##a.set_unit(1,3,Unit(speed = 5))
##a.set_unit(40,30,Unit())
##print(a)
##
##a.move(1,3)

root = Tk()
root.geometry('1200x1000+0+0')
root.title('턴제 게임')

a = Board(20,20)
a.set_unit(핫산, 0, 1)
a.set_unit(예거, 10,7)
root.mainloop()
