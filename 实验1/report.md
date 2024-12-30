> 刘雅迪
>
> 计26
>
> 学号：2021010521

# 实验一：傅里叶级数的可视化

傅里叶级数的写法：利用numpy库

```python
def calculate_a0(T, f):
    return (1/T) * np.trapz([f(t) for t in np.linspace(0, T, 1000)], dx=T/1000)

def calculate_a(n, T, f):
    return (2/T) * np.trapz([f(t) * np.cos((2 * np.pi * n * t) / T) for t in np.linspace(0, T, 1000)], dx=T/1000)

def calculate_b(n, T, f):
    return (2/T) * np.trapz([f(t) * np.sin((2 * np.pi * n * t) / T) for t in np.linspace(0, T, 1000)], dx=T/1000)
```



## 任务一：可视化方波信号

方波函数：

```python
def square_wave(t):
    return 0.5 * np.sign(np.sin(t)) + 0.5
```

可视化结果举例：

当n = 128时：

![](./square-128/1.png)



## 任务二：可视化半圆波信号

半圆波函数：

```python
def semi_circle_wave(t):
    return np.where(t < 0, 0, np.sqrt(np.pi**2 - (t - np.pi)**2))
```

可视化结果举例：

当n = 128时：

![](./semicircle-128/1.png)



当n比较小时，傅里叶级数展开g(t)并不近似等于原函数f(t)，所以可视化结果中的红线并不是近似与x轴平行，而是会上下波动。随着n的值的变大，红线逐渐与x轴平行。