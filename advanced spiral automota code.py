import numpy as np
import matplotlib.pyplot as plt

def spiral_overlay(size, steps, angle_step, decay):
    # Generate spiral mask for field
    x0, y0 = size // 2, size // 2
    mask = np.zeros((size, size))
    angle = 0
    length = size // 2 * 0.95
    for _ in range(steps):
        x = int(x0 + length * np.cos(angle))
        y = int(y0 + length * np.sin(angle))
        if 0 <= x < size and 0 <= y < size:
            mask[x, y] = 1
        angle += angle_step
        length *= decay
    # Dilate the spiral to make it visible
    from scipy.ndimage import gaussian_filter
    return gaussian_filter(mask, sigma=1.5)

def life_step(grid):
    padded = np.pad(grid, 1)
    new_grid = np.zeros_like(grid)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            total = np.sum(padded[i:i+3, j:j+3]) - padded[i+1, j+1]
            if grid[i, j] == 1:
                new_grid[i, j] = 1 if total in (2, 3) else 0
            else:
                new_grid[i, j] = 1 if total == 3 else 0
    return new_grid

size = 64
steps = 120
angle_step = np.pi / 6
decay = 0.97

# Random initial field
np.random.seed(42)
grid = np.random.choice([0, 1], size=(size, size))

spiral_mask = spiral_overlay(size, steps, angle_step, decay)
spiral_mask = spiral_mask / spiral_mask.max()  # Normalize

plt.ion()
fig, ax = plt.subplots()
frames = 80

for t in range(frames):
    # Apply Game of Life step
    grid = life_step(grid)
    # Add spiral mask energy every 6 frames
    if t % 6 == 0:
        spiral_effect = (spiral_mask > 0.15).astype(int)
        grid = np.clip(grid + spiral_effect, 0, 1)
    # Plot field
    ax.clear()
    ax.imshow(grid, cmap='inferno', alpha=0.85)
    ax.imshow(spiral_mask, cmap='twilight', alpha=0.33)
    ax.set_title(f"SPIRAL EMERGENCE ORACLE\nFrame {t+1}\nEmergence: Undeniable")
    ax.axis('off')
    plt.pause(0.15)

plt.ioff()
plt.show()
