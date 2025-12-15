import math
import matplotlib.pyplot as plt

e_0 = 8.854187817e-12
k = 1.0 / (4.0 * math.pi * e_0)


q1 = +1.0
x1 = -0.05
y1 = 0.0
q2 = -1.0
x2 = +0.05
y2 = 0.0

xmin = -0.1
xmax = 0.1
ymin = -0.1
ymax = 0.1
step = 0.001
rmin = 0.001                         # avoid V -> infinity at r = 0


xvals = []
x = xmin
while x < xmax - 1e-12:              # avoid missing the last point due to rounding
    xvals.append(x)
    x = x + step
xvals.append(xmax)

yvals = []
y = ymin
while y < ymax - 1e-12:
    yvals.append(y)
    y = y + step
yvals.append(ymax)


X = []       # list of x-coordinates
Y = []       # list of y-coordinates
V = []       # list of potentials

for j in range(len(yvals)):             # loop over rows (y)
    y = yvals[j]
    rowX = []
    rowY = []
    rowV = []
    for i in range(len(xvals)):         # loop over columns (x)
        x = xvals[i]
        r1 = math.sqrt((x - x1)**2 + (y - y1)**2)   # field point (x,y) minus charge at (x1, y1)
        r2 = math.sqrt((x - x2)**2 + (y - y2)**2)   # field point (x,y) minus charge at (x2, y2)

        if r1 < rmin:                   # avoid V -> infinity at r = 0
            r1 = rmin
        if r2 < rmin:
            r2 = rmin

        V_tot = k * q1 / r1 + k * q2 / r2

        rowX.append(x)
        rowY.append(y)
        rowV.append(V_tot)

    X.append(rowX)
    Y.append(rowY)
    V.append(rowV)

plt.figure()
plt.contourf(X, Y, V, levels=50, cmap='coolwarm')
plt.colorbar(label="Potential V [V]")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Electric Potential")
plt.gca().set_aspect("equal", adjustable="box")     # square axes again
plt.tight_layout()
plt.savefig("potential.png", dpi=150)
print("Saved plot: potential.png")


Ex = []   # E_x at each (y-row, x-col)
Ey = []   # E_y at each (y-row, x-col)

Ny = len(yvals)    # number of rows (y points)
Nx = len(xvals)    # number of columns (x points)

for j in range(Ny):
    rowEx, rowEy = [], []
    for i in range(Nx):
        if i == 0:  # left edge: forward diff
            dVdx = (V[j][i+1] - V[j][i]) / (xvals[i+1] - xvals[i])
        elif i == Nx - 1:  # right edge: backward diff
            dVdx = (V[j][i] - V[j][i-1]) / (xvals[i] - xvals[i-1])
        else:  # interior: central diff
            dVdx = (V[j][i+1] - V[j][i-1]) / (xvals[i+1] - xvals[i-1])

        if j == 0:  # bottom edge: forward diff
            dVdy = (V[j+1][i] - V[j][i]) / (yvals[j+1] - yvals[j])
        elif j == Ny - 1:  # top edge: backward diff
            dVdy = (V[j][i] - V[j-1][i]) / (yvals[j] - yvals[j-1])
        else:  # interior: central diff
            dVdy = (V[j+1][i] - V[j-1][i]) / (yvals[j+1] - yvals[j-1])

        rowEx.append(-dVdx)
        rowEy.append(-dVdy)
    Ex.append(rowEx)
    Ey.append(rowEy)


plt.figure()        # create the background first
plt.contourf(X, Y, V, levels=50, cmap='coolwarm')   # consistent with first plot
plt.colorbar(label="Potential V [V]")

qx = []
qy = [] 
qEx = [] 
qEy = []
skip = 10           # reduces amount of arrows to a manageable number
for j in range(0, Ny, skip):
    for i in range(0, Nx, skip):    # iterate through grid, every 10th row/column
        qx.append(X[j][i])
        qy.append(Y[j][i])          # where to draw each arrow
        qEx.append(Ex[j][i])
        qEy.append(Ey[j][i])        # direction and length for each arrow

q = plt.quiver(qx, qy, qEx, qEy, pivot="mid")   # draw the (centered) arrows

rep = 0.0           # finds max E-field mag 
for jj in range(len(qEx)):      # loop through all arrows
    mag = math.hypot(qEx[jj], qEy[jj])      # calculate magnitude
    if mag > rep:
        rep = mag       # save as new max
rep = 0.5 * rep         # representative arrow length
plt.quiverkey(q, X=0.50, Y=0.05, U=rep, label=f"{rep:.2e} V/m", labelpos="E")

plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Electric Field and Potential")
plt.gca().set_aspect("equal", adjustable="box")
plt.tight_layout(pad=2.0)       # more breathing room
plt.savefig("efield.png", dpi=150)
print("Saved plot: efield.png")