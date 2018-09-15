import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as lines
import kinetics 


def onclick(event):
   global cid_m
   cid_m = fig.canvas.mpl_connect('motion_notify_event',pull)

def check_nan():
    # to control, is the point in workspace of robot
    return not np.isnan(t[0]) and not np.isnan(t[3]) and not np.isnan(a[0]) and not np.isnan(a[1])

def pull(event):
    global t,a
    t = robot.inverse(event.xdata-origin[0],event.ydata-origin[1])
    a = robot.get_a2_a3(t[0],t[3],event.xdata-origin[0],event.ydata-origin[1])
    if check_nan():
        x_end.append(event.xdata)
        y_end.append(event.ydata)
    else:
        pass

def disconnect(event):
    fig.canvas.mpl_disconnect(cid_m)

def update(s):
    if check_nan():
        ## line 1 
        x = [origin[0],origin[0]+60*np.cos(t[0])]
        y = [origin[1],origin[1]+60*np.sin(t[0])]
        line1.set_data(x,y)

        ## line 2
        x = [x[1],x[1]+100*np.cos(a[0])]
        y = [y[1],y[1]+100*np.sin(a[0])]
        line2.set_data(x,y)

        
        ## line 4
        x = [origin[0]+80,origin[0]+80+60*np.cos(t[3])]
        y = [origin[1],origin[1]+60*np.sin(t[3])]
        line4.set_data(x,y)
        
        ## line 3
        x = [x[1],x[1]+100*np.cos(a[1])]
        y = [y[1],y[1]+100*np.sin(a[1])]
        line3.set_data(x,y)

        ## line 5
        x = [origin[0],origin[0]+80]
        y = [origin[1],30]
        line5.set_data(x,y)

        line6.set_data(x_end,y_end)
    else:
        pass
    
    return line6,line1,line2,line3,line4,line5


# pyhsical constrait of five bar mechanism, to get further information check kinetics.py
# Please change r[1:5] values, if you want to try another configuration

r1 = 60 
r2 = 100
r3 = 100
r4 = 60
r5 = 80

robot = kinetics.five_bar(r1,r2,r3,r4,r5)

x_in = 40 # initial end efector y position
y_in = 150 # initial end efector y position

# initial declarations of graph

pad = 30 # do not make me zero, unless you do not want everything will mess up   
xmax = r1+r2+r5/2+pad
ymax = r1+r2+pad*2
fig, ax = plt.subplots()
ax.axis([0,xmax,0,ymax])
origin = [xmax/2-r5/2,pad]
line1, = ax.plot([], [],lw=2,animated=True,c='b')
line2, = ax.plot([], [],lw=2,animated=True,c='b')
line3, = ax.plot([], [],lw=2,animated=True,c='b')
line4, = ax.plot([], [],lw=2,animated=True,c='b')
line5, = ax.plot([], [],lw=2,animated=True,c='b')
line6, = ax.plot([], [],lw=1,animated=True,c='g')
t = robot.inverse(x_in,y_in)
a = robot.get_a2_a3(t[0],t[3],x_in,y_in)
x_end = []
y_end = []   

# graph control functions

fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_release_event',disconnect)
ani = animation.FuncAnimation(fig, update,frames=None,blit=True)
plt.show()


