import matplotlib.pyplot as plt
import numpy as np


def mandelbrot(c, max_iter):
    z = np.zeros_like(c, dtype=np.complex128)
    div_time = np.full(c.shape, max_iter, dtype=int)
    m = np.full(c.shape, True, dtype=bool)

    for i in range(max_iter):
        z[m] = z[m] * z[m] + c[m]
        diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=m)
        div_time[diverged & m] = i
        m[diverged] = False
    return div_time


def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    c = x[:, np.newaxis] + 1j * y[np.newaxis, :]
    return mandelbrot(c, max_iter)


def julia(c, z, max_iter):
    div_time = np.full(z.shape, max_iter, dtype=int)
    m = np.full(z.shape, True, dtype=bool)

    for i in range(max_iter):
        z[m] = z[m] * z[m] + c
        diverged = np.greater(np.abs(z), 2, out=np.full(z.shape, False), where=m)
        div_time[diverged & m] = i
        m[diverged] = False
    return div_time


def julia_set(c, xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    z = x[:, np.newaxis] + 1j * y[np.newaxis, :]
    return julia(c, z, max_iter)


def on_move(event):
    global last_position
    if event.inaxes == ax1 and (
        last_position is None
        or abs(event.xdata - last_position[0]) > 0.01
        or abs(event.ydata - last_position[1]) > 0.01
    ):
        last_position = (event.xdata, event.ydata)
        x, y = event.xdata, event.ydata
        c = x + 1j * y

        z = c
        line_data = [(x, y)]
        for _ in range(max_iter):
            if abs(z) > 2:
                break
            z = z * z + c
            line_data.append((z.real, z.imag))
        line.set_data(zip(*line_data))

        n3 = julia_set(c, xmin, xmax, ymin, ymax, width, height, max_iter)
        ax2.imshow(
            n3.T,
            extent=[xmin, xmax, ymin, ymax],
            origin="lower",
            cmap="twilight_shifted",
        )

        fig.canvas.draw_idle()


xmin, xmax, ymin, ymax = -2.0, 2.0, -2.0, 2.0
width, height = 400, 400
max_iter = 256
last_position = None

n3 = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

ax1.imshow(
    n3.T, extent=[xmin, xmax, ymin, ymax], origin="lower", cmap="twilight_shifted"
)
ax1.set_title("Mandelbrot Set")
(line,) = ax1.plot([], [], color="white", lw=0.5)

ax2.set_xlim(xmin, xmax)
ax2.set_ylim(ymin, ymax)
ax2.set_title("Julia Set")

fig.canvas.mpl_connect("motion_notify_event", on_move)
plt.show()
