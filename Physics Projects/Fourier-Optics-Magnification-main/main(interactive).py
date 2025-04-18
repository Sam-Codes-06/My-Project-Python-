import cv2
import numpy as np
from numpy.fft import fftshift, ifftshift, fft2, ifft2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# Filters
def mean_filter(image, grid=(3, 3)):
    return cv2.blur(np.abs(image), grid)


def median_filter(image, grid=3):
    return cv2.medianBlur(np.abs(image).astype('float32'), grid)


def gaussian_filter(image, grid=(5, 5), stdv=50):
    return cv2.GaussianBlur(np.abs(image), grid, stdv)


def four_f_magnification(img, p, N, ld, f1, f2):
    # Loading image
    img = cv2.imread(img + '.jpg', 0)
    g1 = cv2.resize(img, (N, N))

    # pixel dimensions
    dx, dy = p, p

    # Spatial dimensions
    Lx, Ly = N * dx, N * dy

    # Image Grid
    m, n = np.meshgrid(np.arange(-N / 2, N / 2), np.arange(-N / 2, N / 2))
    x, y = m * dx, n * dy

    # Frequency Grid (Fixed)
    fx, fy = np.arange(-N / 2, N / 2) / Lx, np.arange(-N / 2, N / 2) / Ly
    fx, fy = np.meshgrid(fx, fy)

    # Wavelength and Propagation Constant
    k = 2 * np.pi / ld

    # ASM Propagation: g1 to g2 (distance f1)
    alpha = np.sqrt(k ** 2 - 4 * np.pi ** 2 * (fx ** 2 + fy ** 2) + 0j)
    G1 = fftshift(fft2(ifftshift(g1)))
    H = np.exp(1j * alpha * f1)
    G2 = G1 * H
    g2 = fftshift(ifft2(ifftshift(G2)))

    # Lens 1: Applying Transmittance
    lens_transmittance = np.exp(-1j * np.pi * (x ** 2 + y ** 2) / (ld * f1))
    g3 = g2 * lens_transmittance

    # ASM Propagation: g3 to g4 (distance f1)
    G3 = fftshift(fft2(ifftshift(g3)))
    H = np.exp(1j * alpha * f1)
    G4 = G3 * H
    g4 = fftshift(ifft2(ifftshift(G4)))  # Fourier Transform of g1

    # ASM Propagation: g4 to g5 (distance f2)
    G4 = fftshift(fft2(ifftshift(g4)))
    H = np.exp(1j * alpha * f2)
    G5 = G4 * H
    g5 = fftshift(ifft2(ifftshift(G5)))

    # Lens 2: Applying Transmittance
    lens_transmittance = np.exp(-1j * np.pi * (x ** 2 + y ** 2) / (ld * f2))
    g6 = g5 * lens_transmittance

    # ASM Propagation: g6 to g7 (distance f2)
    G6 = fftshift(fft2(ifftshift(g6)))
    H = np.exp(1j * alpha * f2)
    G7 = G6 * H
    g7 = fftshift(ifft2(ifftshift(G7)))  # Final output

    # Apply filters
    if filter == 'gaussian':
        g7 = gaussian_filter(g7)
    elif filter == 'mean':
        g7 = mean_filter(g7)
    elif filter == 'median':
        g7 = median_filter(g7)
    else:
        pass

    return np.abs(g1), np.fliplr(np.flipud(np.abs(g7)))

def fresnel_magnification(img, p, N, ld, b, z):
    # Loading image
    img = cv2.imread(img + '.jpg', 0)
    g1 = cv2.resize(img, (N, N))

    # Pixel dimensions
    dx, dy = p, p

    # Spatial dimensions
    Lx, Ly = N * dx, N * dy

    # Image Grid
    m, n = np.meshgrid(np.arange(-N / 2, N / 2), np.arange(-N / 2, N / 2))
    x, y = m * dx, n * dy

    # Frequency Grid (Fixed)
    fx, fy = np.arange(-N / 2, N / 2) / Lx, np.arange(-N / 2, N / 2) / Ly
    fx, fy = np.meshgrid(fx, fy)

    # Wavelength and Propagation Constant
    k = 2 * np.pi / ld

    # Beta factor adjustment
    b = b * 1e+10

    # Applying Illumination function
    u_inp = np.exp(1j * b * (x ** 2 + y ** 2))
    g1 = u_inp * g1

    # ASM Propagation: g1 to g2
    alpha = np.sqrt(k ** 2 - 4 * np.pi ** 2 * (fx ** 2 + fy ** 2) + 0j)
    G1 = fftshift(fft2(ifftshift(g1)))
    H = np.exp(1j * alpha * z)
    G2 = G1 * H
    g2 = fftshift(ifft2(ifftshift(G2)))

    # Apply filters
    if filter == 'gaussian':
        g2 = gaussian_filter(g2)
    elif filter == 'mean':
        g2 = mean_filter(g2)
    elif filter =='median':
        g2 = median_filter(g2)
    else:
        pass

    return np.abs(g1), np.abs(g2)


def plot_four_f_magnification(img):

    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    plt.subplots_adjust(bottom=0.4)

    # Compute initial images
    original, magnified = four_f_magnification(img, pixel_init, N_init, wavelength_init, focal_length1_init, focal_length2_init)

    # Display images
    img1_display = ax[0].imshow(original, cmap='gray')
    ax[0].set_title("Original Image")

    img2_display = ax[1].imshow(magnified, cmap='gray')
    ax[1].set_title("Magnified Image")

    # Create sliders
    slider_axes = [
        plt.axes([0.2, 0.3, 0.65, 0.03]),  # Focal Length 1
        plt.axes([0.2, 0.25, 0.65, 0.03]),  # Focal Length 2
        plt.axes([0.2, 0.2, 0.65, 0.03]),  # N
        plt.axes([0.2, 0.15, 0.65, 0.03]),  # Pixel size
        plt.axes([0.2, 0.1, 0.65, 0.03])   # Wavelength
    ]

    slider_f1 = Slider(slider_axes[0], 'Focal Length 1', min(f_range), max(f_range), valinit=focal_length1_init, valstep=f_range)
    slider_f2 = Slider(slider_axes[1], 'Focal Length 2', min(f_range), max(f_range), valinit=focal_length2_init, valstep=f_range)
    slider_N = Slider(slider_axes[2], 'N', min(N_range), max(N_range), valinit=N_init, valstep=N_range)
    slider_p = Slider(slider_axes[3], 'Pixel Size', min(pixel_range), max(pixel_range), valinit=pixel_init, valstep=pixel_range)
    slider_ld = Slider(slider_axes[4], 'Wavelength', min(wavelength_range), max(wavelength_range), valinit=wavelength_init, valstep=wavelength_range)

    # Update function
    def update(val):
        f1 = slider_f1.val
        f2 = slider_f2.val
        N = slider_N.val
        p = slider_p.val
        ld = slider_ld.val

        _, magnified = four_f_magnification(img, p, int(N), ld, f1, f2)
        img2_display.set_data(magnified)
        fig.canvas.draw_idle()

    # Connect sliders
    slider_f1.on_changed(update)
    slider_f2.on_changed(update)
    slider_N.on_changed(update)
    slider_p.on_changed(update)
    slider_ld.on_changed(update)

    plt.show()


def plot_fresnel_magnification(img):
    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    plt.subplots_adjust(bottom=0.4)

    original, magnified = fresnel_magnification(img, pixel_init, N_init, wavelength_init, beta_init, z_init)

    img1_display = ax[0].imshow(original, cmap='gray')
    ax[0].set_title("Original Image")

    img2_display = ax[1].imshow(magnified, cmap='gray')
    ax[1].set_title("Magnified Image")

    slider_axes = [
        plt.axes([0.2, 0.3, 0.65, 0.03]),  # Beta
        plt.axes([0.2, 0.25, 0.65, 0.03]),  # z
        plt.axes([0.2, 0.2, 0.65, 0.03]),  # N
        plt.axes([0.2, 0.15, 0.65, 0.03]),  # Pixel size
        plt.axes([0.2, 0.1, 0.65, 0.03])  # Wavelength
    ]

    slider_beta = Slider(slider_axes[0], 'Beta', min(beta_range), max(beta_range), valinit=beta_init)
    slider_z = Slider(slider_axes[1], 'z', 10e-6, 100e-5, valinit=z_init)
    slider_N = Slider(slider_axes[2], 'N', min(N_range), max(N_range), valinit=N_init, valstep=N_range)
    slider_p = Slider(slider_axes[3], 'Pixel Size', min(pixel_range), max(pixel_range), valinit=pixel_init,
                      valstep=pixel_range)
    slider_ld = Slider(slider_axes[4], 'Wavelength', min(wavelength_range), max(wavelength_range),
                       valinit=wavelength_init, valstep=wavelength_range)

    def update(val):
        b = slider_beta.val
        z = slider_z.val
        N = int(slider_N.val)
        p = slider_p.val
        ld = slider_ld.val

        _, magnified = fresnel_magnification(img, p, N, ld, b, z)
        img2_display.set_data(magnified)
        fig.canvas.draw_idle()

    slider_beta.on_changed(update)
    slider_z.on_changed(update)
    slider_N.on_changed(update)
    slider_p.on_changed(update)
    slider_ld.on_changed(update)

    plt.show()


pixel_init, N_init, wavelength_init, focal_length1_init, focal_length2_init = 8e-6, 800, 500e-9, 12e-2, 12e-2
z_init = 10e-6
beta_init = 0.

beta_range = np.linspace(0., 10., 100)
pixel_range = [i * 1e-6 for i in range(1, 11)]
N_range = [200 + i * 100 for i in range(0, 9)]
wavelength_range = [100 * i * 1e-9 for i in range(1, 9)]
f_range = [i * 1e-2 for i in range(1, 49)]
filter = 'median'
plot_fresnel_magnification('image15')
plot_four_f_magnification('image15')
