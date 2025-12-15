import math
import matplotlib.pyplot as plt

def f(x):
    return 2.0 + 0.75 * math.tanh(2.0 * x)

def f_analytic(x):
    c = math.cosh(2.0 * x)
    return 1.5 / c ** 2

a = -2.0
b = 2.0
steps = [1.0, 0.5, 0.1]
curves = []                 # label, x values and dfdx values for each i

for i in steps:
    xvals = []              # x coordinates
    x = a
    while x < b - 1e-12:    # add points from a up to b
        xvals.append(x)
        x = x + i           # step forward
    xvals.append(b)

    fvals = []
    for x in xvals:         # f(x) at each point
        fvals.append(f(x))

    dfdx = [0.0] * len(xvals)
    dfdx[0] = (fvals[1] - fvals[0]) / (xvals[1] - xvals[0])     # forward difference

    for n in range(1, len(xvals) - 1):
        dfdx[n] = (fvals[n + 1] - fvals[n - 1]) / (xvals[n + 1] - xvals[n - 1])     # central difference

    dfdx[-1] = (fvals[-1] - fvals[-2]) / (xvals[-1] - xvals[-2]) # backward difference

    curves.append((f"i = {i}", xvals, dfdx)) 


plt.figure()
for label, x, y in curves:
    plt.plot(x, y, label=label)
xd = []
fd = []
x = a
dx = 0.01
while x <= b + 1e-12:
    xd.append(x)
    fd.append(f_analytic(x))
    x = x + dx

plt.plot(xd, fd, linestyle="--", label="analytic f'(x)")
plt.xlabel("x")
plt.ylabel("df/dx")
plt.title("Central Difference and Analytic Derivative")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("central.png", dpi=150)
print("Saved plot as central.png.")