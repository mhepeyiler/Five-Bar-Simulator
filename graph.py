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
    return not np.isnan(a[0]) and not np.isnan(a[1]) and not np.isnan(a[2]) and not np.isnan(a[3])

def pull(event):
    global a
    x = event.xdata-origin[0]
    y = event.ydata-origin[1]
    #print(x,y)
    robot.inverse(x,y)
    a[0] = robot.get_a11()
    a[1] = robot.get_a2(a[0],x,y)
    a[3] = robot.get_a42()
    a[2] = robot.get_a3(a[3],x,y)
    #print(a)
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
        x = [origin[0],origin[0]+r1*np.cos(a[0])]
        y = [origin[1],origin[1]+r1*np.sin(a[0])]
        line1.set_data(x,y)

        ## line 2
        x = [x[1],x[1]+r2*np.cos(a[1])]
        y = [y[1],y[1]+r2*np.sin(a[1])]
        line2.set_data(x,y)

        
        ## line 4
        x = [origin[0]+r5,origin[0]+r5+r4*np.cos(a[3])]
        y = [origin[1],origin[1]+r4*np.sin(a[3])]
        line4.set_data(x,y)
        
        ## line 3
        x = [x[1],x[1]+r3*np.cos(a[2])]
        y = [y[1],y[1]+r3*np.sin(a[2])]
        line3.set_data(x,y)

        ## line 5
        x = [origin[0],origin[0]+r5]
        y = [origin[1],pad]
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

if r2>r3:
    big_l = r2
else:
    big_l = r3
    
a = [0,0,0,0]
xmax = r1+big_l+r5/2+pad
ymax = r1+big_l+pad*2
fig, ax = plt.subplots()
ax.axis([0,xmax,0,ymax])
origin = [xmax/2-r5/2,pad]
line1, = ax.plot([], [],lw=2,animated=True,c='b')
line2, = ax.plot([], [],lw=2,animated=True,c='b')
line3, = ax.plot([], [],lw=2,animated=True,c='b')
line4, = ax.plot([], [],lw=2,animated=True,c='b')
line5, = ax.plot([], [],lw=2,animated=True,c='b')
line6, = ax.plot([], [],lw=1,animated=True,c='g')
robot.inverse(x_in,y_in)
a[0] = robot.get_a11()
a[1] = robot.get_a2(a[0],x_in,y_in)
a[3] = robot.get_a42()
a[2] = robot.get_a3(a[3],x_in,y_in)
x_end = []
y_end = []   

# graph control functions

fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_release_event',disconnect)
ani = animation.FuncAnimation(fig, update,frames=None,blit=True,interval=25)
plt.show()
