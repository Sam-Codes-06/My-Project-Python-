import cv2
import numpy as np
from numpy.fft import fftshift, ifftshift, fft2, ifft2
import matplotlib.pyplot as plt

def mean_filter(image, grid=(3, 3)):
    return cv2.blur(image, grid)

def median_filter(image, grid=3):
    return cv2.medianBlur(image.astype('float32'), grid)

def gaussian_filter(image, grid=(5, 5), stdv=50):
    return cv2.GaussianBlur(image, grid, stdv)

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

def plot(img1, img2):
    plt.figure(figsize=(10, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(img1, cmap='gray')
    plt.title('Original Image')

    plt.subplot(1, 2, 2)
    plt.imshow(img2, cmap='gray')
    plt.title('Magnified Image')

    plt.show()

img, p, N, ld, f1, f2, z, b = 'image13', 8e-6, 800, 500e-9, 12e-2, 48e-2, 10e-6, 0.
img1, img2 = four_f_magnification(img, p, N, ld, f1, f2)
# img1, img2 = fresnel_magnification(img, p, N, ld, b, z)
plot(img1, img2)