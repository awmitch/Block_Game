# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 11:58:45 2016

@author: alecwmitchell
"""

from Tkinter import *
from time import sleep,strftime
from random import random, randint
from PIL import Image, ImageTk
import datetime
import math
#from win32api import GetSystemMetrics

class App:
    def __init__(self,master):
        self.master = master
        self.master.title("Tile Adventures")
        self.menubar = Menu(self.master)
        self.difficulty = 10
        self.menubar.add_command(label='    Start %s'%(11-self.difficulty),command=self.start)

        self.master.config(menu=self.menubar)
        print "Width =", 1000
        print "Height =", 1000
        self.w = Canvas(self.master, width = 1000,height = 1000)
        self.w.pack()
        self.rate_mult = 10
        self.start_rate = 500
        self.rate =  self.start_rate
        self.x = 0
        self.y = 0
        self.flag = 0
        self.first_y_flag = 1
        self.power_flag = 0
        self.rpoints = 0
        self.bpoints = 0
        self.grid = {}
        self.trans_counter = {}
        self.images = {}
        self.blue_text = {}
        self.red_text = {}
#        for x in range(1,9):
#            self.images['%s'%x] = PhotoImage(file='%s.gif'%x)
#            self.images['0%s'%x] = PhotoImage(file='%s.gif'%x)
        self.power_spot = []
        self.power_cords = []
        self.inc = 1000/7.0
        for x in range(0,6):
            for y in range(0,6):
                if x == 0 or x == 5 or y == 0 or y == 5: 
                    color = 'grey'
                else:
                    color = 'black'
                self.grid['%s,%s'%(x,y)] = self.w.create_rectangle((self.inc*x, y*self.inc, self.inc*x+self.inc,y*self.inc+self.inc), fill="%s"%color)
        self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='green')
        self.rscore_text = self.w.create_text((self.inc*x+self.inc/2,y*self.inc+int(self.inc/3)),text='',fill='red',font=("Purisa", 48))
        self.bscore_text = self.w.create_text((self.inc*x+self.inc/2,y*self.inc+int(self.inc/1.5)),text='',fill='blue',font=("Purisa", 48))
#        self.rate_text = self.w.create_text((self.inc/2,self.inc/2),text='',fill='black',font=("Purisa", 48),width=150)
#        photo =  PhotoImage(file='01.gif')      
#        self.sonic = self.w.create_image(50,50,image=photo)
        self.prev = []
        self.block = []
        self.loop = [(5,5),(5,4),(5,3),(5,2),(5,1),(5,0),(4,0),(3,0),(2,0),(1,0),(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,5),(2,5),(3,5),(4,5)]
        self.loop_num = 0         
        self.spawn2()
        def key(event):
            if repr(event.char) == '\' \'':
                self.path = []
                if (self.x,self.y) == (0,0):
                    self.x_inc = 1
                    self.y_inc = 1
                elif (self.x,self.y) == (5,5):
                    self.x_inc = -1
                    self.y_inc = -1
                elif (self.x,self.y) == (0,5):
                    self.x_inc = 1
                    self.y_inc = -1
                elif (self.x,self.y) == (5,0):
                    self.x_inc = -1
                    self.y_inc = 1
                else:
                    if self.x == 0:
                        self.x_inc = 1
                        self.y_inc = 0
                    elif self.x == 5:
                        self.x_inc = -1
                        self.y_inc = 0
                    elif self.y == 0:
                        self.x_inc = 0
                        self.y_inc = 1
                    elif self.y == 5:
                        self.x_inc = 0
                        self.y_inc = -1
                self.path.append((self.x,self.y))
                if (self.x,self.y) in self.power_cords:
                    for num in range(0,len(self.power_cords)):
                        if (self.x,self.y) == self.power_cords[num]:
                            self.w.delete(self.power_spot[num])
                            self.power_cords.remove(self.power_cords[num])
                            self.power_spot.remove(self.power_spot[num])
                            self.power_flag = 1
                            break
                for it in range(0,5):
                    if (self.x+self.x_inc,self.y+self.y_inc) not in self.block or self.power_flag == 1:
                        if (self.x,self.y) in self.prev:
                            self.prev.remove((self.x,self.y))
                            self.w.delete(self.blue_text['(%s,%s)'%(self.x,self.y)][0])
                            if (self.x,self.y) not in self.block:
                                self.bpoints += 1
                                self.w.itemconfig(self.bscore_text,text=self.bpoints)
                                self.rate += self.rate/self.rate_mult/2
                                self.power_spot.append(self.w.create_text((self.inc*self.x+self.inc/2,self.inc*self.y+self.inc/2),text='%s'%(self.rate/self.rate_mult/2),fill='blue',font=("Purisa", 72)))
                                self.power_cords.append((self.x,self.y))
                                self.trans_counter['(%s,%s)'%self.power_cords[-1]] = 0
#                                self.w.itemconfig(self.rate_text,text='Rate %s'%self.rate)
                        if (self.x,self.y) in self.block and self.power_flag == 1:
                            self.block.remove((self.x,self.y))
                            self.w.delete(self.blue_text['(%s,%s)'%(self.x,self.y)][0])
                            self.rpoints += 1
                            self.w.itemconfig(self.rscore_text,text=self.rpoints)
                            self.rate += self.rate/self.rate_mult
                            self.power_spot.append(self.w.create_text((self.inc*self.x+self.inc/2,self.inc*self.y+self.inc/2),text='%s'%(self.rate/self.rate_mult),fill='red',font=("Purisa", 72)))
                            self.power_cords.append((self.x,self.y))
                            self.trans_counter['(%s,%s)'%self.power_cords[-1]] = 0
#                            self.w.itemconfig(self.rate_text,text='Rate %s'%self.rate)
                        if it == 0:
                            self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='grey')
                        else:
                            self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='black')
#                        self.w.delete(self.sonic)
                        self.x += self.x_inc
                        self.y += self.y_inc
                        self.path.append((self.x,self.y))
                        self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='green')
                        
                        if it == 4:
                            self.power_flag = 0
                            
                    else:
                        self.flag = 1
                        break
                        
                if self.flag == 1:
                    self.flag = 0
                    self.origin = self.path[0]
                    self.path.reverse()
                    for (self.x,self.y) in self.path:
                        if (self.x,self.y) in self.prev:
                            self.prev.remove((self.x,self.y))
                            self.w.delete(self.blue_text['(%s,%s)'%(self.x,self.y)][0])
                        if (self.x,self.y) == self.origin:
                            self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='green')
                        else:
                            self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='black')
                #sleep(.3)
                
            if repr(event.char) == '\'a\'' and self.x != 0 and (self.x-1,self.y) not in self.block:
                if self.y == 0 or self.y == 5:
                    self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='grey')
                    self.x -= 1
                    self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='green')
                    self.w.create_bitmap
                        
            elif repr(event.char) == '\'d\'' and self.x != 5 and (self.x+1,self.y) not in self.block:
                if self.y == 0 or self.y == 5:
                    self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='grey')
                    if (self.x,self.y) in self.prev:
                        self.prev.remove((self.x,self.y))
                    self.x += 1
                    self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='green')
                        
            elif repr(event.char) == '\'w\'' and self.y != 0 and (self.x,self.y-1) not in self.block:
                if self.x == 0 or self.x == 5:
                    self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='grey')
                    if (self.x,self.y) in self.prev:
                        self.prev.remove((self.x,self.y))
                    self.y -= 1
                    self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='green')
                    
            elif repr(event.char) == '\'s\'' and self.y != 5 and (self.x,self.y+1) not in self.block:
                if self.x == 0 or self.x == 5:
                    self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='grey')
                    if (self.x,self.y) in self.prev:
                        self.prev.remove((self.x,self.y))
                    self.y += 1
                    self.w.itemconfig(self.grid['%s,%s'%(self.x,self.y)],fill='green')
                    
            if self.active == (self.x,self.y):
                self.power_spot.append(self.w.create_text(self.x*self.inc+self.inc/2,self.y*self.inc+self.inc/2,fill='white',font=("Purisa", 72)))
                self.power_cords.append(self.active)
                self.trans_counter['(%s,%s)'%self.power_cords[-1]] = 0
                
                if (self.x,self.y) == (0,0) or (self.x,self.y) == (5,5):
                    self.w.insert(self.power_spot[-1],100,'\\')
                elif (self.x,self.y) == (0,5) or (self.x,self.y) == (5,0):
                    self.w.insert(self.power_spot[-1],100,'/')
                else:    
                    if self.y == 5:
                        self.w.insert(self.power_spot[-1],100,'^') 
                    if self.x == 5:
                        self.w.insert(self.power_spot[-1],100,'<')                
                    if self.y == 0:
                        self.w.insert(self.power_spot[-1],100,'v')                    
                    if self.x == 0:
                        self.w.insert(self.power_spot[-1],100,'>')


        self.master.bind("<Key>", key)
    
    def start(self):
        self.menubar.delete(1)
        self.menubar.add_command(label='Start %s'%(11-self.difficulty),command=self.start)
        self.rate += self.difficulty*self.start_rate/10
        self.difficulty -= 1
        self.seconds = 0
        self.minutes = 0
#        self.start_time = strftime("%M:%S")
#        col_flag = 0
#        self.start_flag = 1
#        self.start_seconds=''
#        self.start_minutes=''
#        for char in self.start_time:
#            if char == ':':
#                col_flag = 1
#            else:
#                if col_flag == 1:
#                    self.start_seconds += char
#                else:
#                    self.start_minutes += char
#        col_flag = 0
        self.time_text = self.w.create_text((self.inc/2,self.inc/2),text='%s:%s'%(self.minutes,self.seconds),fill='black',font=("Purisa", 48))
        self.master.after(1000,self.update_clock)
        self.spawn()
    def update_clock(self):
        if len(self.block) != 16:
#            self.time = strftime("%M:%S")
#            col_flag = 0
#            self.seconds=''
#            self.minutes=''
#            for char in self.time:
#                if char == ':':
#                    col_flag = 1
#                else:
#                    if col_flag == 1:
#                        self.seconds += char
#                    else:
#                        self.minutes += char
#            col_flag = 0
            self.seconds += 1
            if self.seconds == 60:
                self.minutes += 1
                self.seconds -= 60
            self.w.itemconfig(self.time_text,text='%s:%s'%(self.minutes,self.seconds))
            self.master.after(1000,self.update_clock)
        
    def spawn(self):
        if len(self.block) != 16:
            loc_x = int(random()*4)+1
            loc_y = int(random()*4)+1
            while (loc_x,loc_y) in self.block or (loc_x,loc_y)==(self.x,self.y):
                loc_x = int(random()*4)+1
                loc_y = int(random()*4)+1
            if (loc_x,loc_y) in self.prev:
                self.w.itemconfig(self.grid['%s,%s'%(loc_x,loc_y)],fill='red')
                self.block.append((loc_x,loc_y))
                self.w.itemconfig(self.blue_text['(%s,%s)'%(loc_x,loc_y)][0],text='%s'%(self.rate/self.rate_mult+self.blue_text['(%s,%s)'%(loc_x,loc_y)][1]))
                self.rate -= self.rate/self.rate_mult
#                self.w.itemconfig(self.rate_text,text='Rate %s'%self.rate)
                if len(self.block) != 16:
                    self.master.after(self.rate, self.spawn)
                else:
                    self.points = 0
            else:
                self.prev.append((loc_x,loc_y))
                self.blue_text['(%s,%s)'%(loc_x,loc_y)] = (self.w.create_text((self.inc*loc_x+self.inc/2,self.inc*loc_y+self.inc/2),text='%s'%(self.rate/self.rate_mult/2),fill='black',font=("Purisa", 72)),self.rate/self.rate_mult/2)
                self.w.itemconfig(self.grid['%s,%s'%(loc_x,loc_y)],fill='blue')
                self.master.after(self.rate, self.spawn)
                self.rate -= self.rate/self.rate_mult/2
#                self.w.itemconfig(self.rate_text,text='Rate %s'%self.rate)
                
    def spawn2(self):
        self.trail = round(500.0/self.rate)
        for num in range(0,len(self.power_spot)):
            self.trans_counter['(%s,%s)'%self.power_cords[num]] += 1     
        for num in range(0,len(self.power_spot)):
            if self.trans_counter['(%s,%s)'%self.power_cords[num]] > int(self.trail):
                self.w.delete(self.power_spot[num])
                self.power_cords.remove(self.power_cords[num])
                self.power_spot.remove(self.power_spot[num])
                break
        (loc_x,loc_y) = self.loop[self.loop_num]
        if self.loop_num == len(self.loop)-1:
            self.loop_num = 0
        else:
            self.loop_num += 1
  
        if self.first_y_flag == 1:
            self.prev_yx,self.prev_yy = loc_x,loc_y
            self.first_y_flag = 0
        else:
            if self.prev_yx == self.x and self.prev_yy == self.y:
                self.w.itemconfig(self.grid['%s,%s'%(self.prev_yx,self.prev_yy)],fill='green')
            else:
                self.w.itemconfig(self.grid['%s,%s'%(self.prev_yx,self.prev_yy)],fill='grey')

            self.prev_yx,self.prev_yy = loc_x,loc_y
            self.w.itemconfig(self.grid['%s,%s'%(loc_x,loc_y)],fill='orange')
            self.active = (loc_x,loc_y)
            if self.active == (self.x,self.y):
                self.power_spot.append(self.w.create_text(self.x*self.inc+self.inc/2,self.y*self.inc+self.inc/2,fill='white',font=("Purisa", 72)))
                self.power_cords.append(self.active)
                self.trans_counter['(%s,%s)'%self.power_cords[-1]] = 0 
                if (self.x,self.y) == (0,0) or (self.x,self.y) == (5,5):
                    self.w.insert(self.power_spot[-1],100,'\\')
                elif (self.x,self.y) == (0,5) or (self.x,self.y) == (5,0):
                    self.w.insert(self.power_spot[-1],100,'/')
                else:    
                    if self.y == 5:
                        self.w.insert(self.power_spot[-1],100,'^') 
                    if self.x == 5:
                        self.w.insert(self.power_spot[-1],100,'<')                
                    if self.y == 0:
                        self.w.insert(self.power_spot[-1],100,'v')                    
                    if self.x == 0:
                        self.w.insert(self.power_spot[-1],100,'>')
                self.w.itemconfig(self.grid['%s,%s'%(loc_x,loc_y)],fill='orange')
        self.master.after(self.rate,self.spawn2)  
        
root = Tk()
root.geometry("%dx%d+%d+%d" % (int(1000*6.0/7.0), int(1000*6.0/7.0), 0, 0))
app=App(root)
root.mainloop()