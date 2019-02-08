import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from numpy import pi as PI

NROWS=5
NCOLS=5
NPLOTS=NROWS*NCOLS
PHASE_MAX = PI/2
PHASE_MIN = 0
A_MIN = 1
A_MAX = NROWS*2-1
B_MIN = 1
B_MAX = NROWS*2-2
FILE_NAME="Rhodonea_animation.mp4"

def P_FAMILY_X(t,a,k):
    return a*np.sin(k*t)*np.cos(t)
    
def P_FAMILY_Y(t,a,k):
    return a*np.sin(k*t)*np.sin(t)


fig, ax = plt.subplots(nrows=NROWS, ncols=NCOLS)

en_ax = list(enumerate(ax.flatten()))

def safe_div(y):
    if y == 0:
        return 0
    return "pi/"+str(round(PI/y,2))

#we will keep the ratios and phase diffs so as to be in a grid shape , phases will vary through columns 
#and ratios through rows

phases = np.linspace(PHASE_MIN,PHASE_MAX,NCOLS)
a = np.array(list(map(int,np.linspace(A_MIN,A_MAX,NROWS))))
b = np.array(list(map(int,np.linspace(B_MIN,B_MAX,NROWS))))

line=[None]*NPLOTS
pt=[None]*NPLOTS

temp_t = np.linspace(-PI,PI,600)
for axis_num,axis in en_ax:
     print(axis_num)
     x=P_FAMILY_X(temp_t,a[int(axis_num/NROWS)],b[int(axis_num%NROWS)])
     y=P_FAMILY_Y(temp_t,a[int(axis_num/NROWS)],b[int(axis_num%NROWS)])
     line[axis_num], = axis.plot(x,y,lw=2)
     pt[axis_num],= axis.plot(0,0,color='red', marker='o',markersize=1)
     axis.set_xlabel('b='+str(b[int(axis_num%NROWS)]))
     if(axis_num%NCOLS==0):
         axis.set_ylabel('a='+str(a[int(axis_num/NROWS)]))
     axis.set_yticklabels([])
     axis.set_xticklabels([])
    
    
def init():
    for axis_num,axis in en_ax:
        line[axis_num].set_data([], [])
        pt[axis_num].set_data([], [])
    return line,

x=[[] for l in range(NPLOTS)]
y=[[] for l in range(NPLOTS)]
# animation function.  This is called sequentially
def animate(i):
    t=-np.pi+i*np.pi/150
    for axis_num,axis in en_ax:
            x[axis_num].append(P_FAMILY_X(t,a[int(axis_num/NROWS)],b[int(axis_num%NROWS)]))
            y[axis_num].append(P_FAMILY_Y(t,a[int(axis_num/NROWS)],b[int(axis_num%NROWS)]))
            line[axis_num].set_data(x[axis_num], y[axis_num])
            pt[axis_num].set_data(x[axis_num][(len(x[axis_num])-1)],y[axis_num][(len(y[axis_num])-1)])
    return line,

ani = animation.FuncAnimation(fig, animate, init_func=init, interval=2, blit=False, save_count=500)

from matplotlib.animation import FFMpegWriter
writer = FFMpegWriter(fps=60, metadata=dict(artist='Me'), bitrate=500)
ani.save(FILE_NAME, writer=writer)

plt.show()
