import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import numpy as np
import os
import imageio
from matplotlib.pyplot import cm

# TODO: 1. Change N_Fourier to 2, 4, 8, 16, 32, 64, 128, get visualization results with differnet number of Fourier Series
# N_Fourier = 64

# TODO: optional, implement visualization for semi-circle
signal_name = "square"

def calculate_a0(T, f):
    return (1/T) * np.trapz([f(t) for t in np.linspace(0, T, 1000)], dx=T/1000)

def calculate_a(n, T, f):
    return (2/T) * np.trapz([f(t) * np.cos((2 * np.pi * n * t) / T) for t in np.linspace(0, T, 1000)], dx=T/1000)

def calculate_b(n, T, f):
    return (2/T) * np.trapz([f(t) * np.sin((2 * np.pi * n * t) / T) for t in np.linspace(0, T, 1000)], dx=T/1000)


# TODO: 2. Please implement the function that calculates the Nth fourier coefficient
# Note that n starts from 0
# For n = 0, return a0; n = 1, return b1; n = 2, return a1; n = 3, return b2; n = 4, return a2 ...
# n = 2 * m - 1(m >= 1), return bm; n = 2 * m(m >= 1), return am. 
def fourier_coefficient(n):
    T = 2 * np.pi
    if n == 0:
        return calculate_a0(T, function)
    elif n % 2 == 1: # n = 2*m - 1
        return calculate_b((n+1)/2, T, function)
    else: # n = 2*m
        print(calculate_a(n/2, T, function))
        return calculate_a(n/2, T, function)

# TODO: 3. implement the signal function
def square_wave(t):
    return 0.5 * np.sign(np.sin(t)) + 0.5

# TODO: optional. implement the semi circle wave function
def semi_circle_wave(t):
    return np.where(t < 0, 0, np.sqrt(np.pi**2 - (t - np.pi)**2))

def function(t):
    if signal_name == "square":
        return square_wave(t)
    elif signal_name == "semicircle":
        return semi_circle_wave(t)
    else:
        raise Exception("Unknown Signal")


def visualize(N_Fourier):
    # if not os.path.exists(signal_name):
    #     os.makedirs(signal_name)

    frames = 100
    output_path = signal_name + "-" + str(N_Fourier)
    os.makedirs(output_path, exist_ok=True)
    # x and y are for drawing the original function
    x = np.linspace(0, 2 * math.pi, 1000)
    y = np.zeros(1000, dtype = float)
    for i in range(1000):
        y[i] = function(x[i])

    for i in range(frames):
        figure, axes = plt.subplots()
        color=iter(cm.rainbow(np.linspace(0, 1, 2 * N_Fourier + 1)))

        time = 2 * math.pi * i / 100
        point_pos_array = np.zeros((2 * N_Fourier + 2, 2), dtype = float)
        radius_array = np.zeros((2 * N_Fourier + 1), dtype = float)

        point_pos_array[0, :] = [0, 0]
        radius_array[0] = fourier_coefficient(0)
        point_pos_array[1, :] = [0, radius_array[0]]

        circle = patches.Circle(point_pos_array[0], radius_array[0], fill = False, color = next(color))
        axes.add_artist(circle)

        f_t = function(time)
        for j in range(N_Fourier):
            # calculate circle for a_{n}
            radius_array[2 * j + 1] = fourier_coefficient(2 * j + 1)
            point_pos_array[2 * j + 2] = [point_pos_array[2 * j + 1][0] + radius_array[2 * j + 1] * math.cos((j + 1) * time),   # x axis
                                        point_pos_array[2 * j + 1][1] + radius_array[2 * j + 1] * math.sin((j + 1) * time)]     # y axis
            circle = patches.Circle(point_pos_array[2 * j + 1], radius_array[2 * j + 1], fill = False, color = next(color))
            axes.add_artist(circle)
            
            # calculate circle for b_{n}
            radius_array[2 * j + 2] = fourier_coefficient(2 * j + 2)
            point_pos_array[2 * j + 3] = [point_pos_array[2 * j + 2][0] + radius_array[2 * j + 2] * math.sin((j + 1) * time),   # x axis
                                        point_pos_array[2 * j + 2][1] + radius_array[2 * j + 2] * math.cos((j + 1) * time)]     # y axis
            circle = patches.Circle(point_pos_array[2 * j + 2], radius_array[2 * j + 2], fill = False, color = next(color))
            axes.add_artist(circle)
            
        plt.plot(point_pos_array[:, 0], point_pos_array[:, 1], 'o-')
        plt.plot(x, y, '-')
        plt.plot([time, point_pos_array[-1][0]], [f_t, point_pos_array[-1][1]], '-', color = 'r')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.savefig(os.path.join(output_path, "{}.png".format(i)))
        # plt.show()
        plt.close()
        
    images = []
    for i in range(frames):
        images.append(imageio.imread(os.path.join(output_path, "{}.png".format(i))))
    imageio.mimsave('{}.mp4'.format(output_path), images)
    print("finish", N_Fourier)


if __name__ == "__main__":
    visualize(N_Fourier = 2)
    visualize(N_Fourier = 4)
    visualize(N_Fourier = 8)
    visualize(N_Fourier = 16)
    visualize(N_Fourier = 32)
    visualize(N_Fourier = 64)
    visualize(N_Fourier = 128)