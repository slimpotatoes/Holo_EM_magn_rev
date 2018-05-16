# Image Display module

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import SpanSelector
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import shift
import numpy as np
import alignholo as alignholo


class GUIDisplayOverlap(object):

    def __init__(self, data_em):
        # 2D array to display with calibration cal in nm/pixel
        self.data_em = data_em
        self.image_data_1 = self.data_em.holo_1
        self.image_data_2 = self.data_em.holo_2
        # Window for image display + matplotlib parameters
        self.fig_image = plt.figure(num='align images', figsize=(10, 7), dpi=100)
        # Layout figure
        self.gs_fig_image = gridspec.GridSpec(8, 8)

        # Contrast histogram display and span selector
        self.ax_contrast = plt.subplot(self.gs_fig_image[0, 1:6])
        self.contrastbins = 256
        self.cmin = np.min([np.min(self.image_data_1), np.min(self.image_data_2)])
        self.cmax = np.max([np.max(self.image_data_1), np.max(self.image_data_2)])
        self.imhist, self.imbins = np.histogram(self.image_data_1, bins=self.contrastbins)
        self.imhist, self.imbins = np.histogram(self.image_data_2, bins=self.contrastbins)
        self.ax_contrast_span = None
        self.plot_contrast_histogram()

        # Define image axis
        self.ax_image = plt.subplot(self.gs_fig_image[1:-1, 0:-1])
        self.ax_image.set_axis_off()
        cdict_red = {'red': [(0.0, 0.0, 0.0), (0.5, 0.0, 0.1), (0.85, 1.0, 1.0), (1.0, 1.0, 1.0)],
                     'green': [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)],
                     'blue': [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)]}

        cdict_blue = {'red': [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)],
                      'green': [(0.0, 0.0, 0.0), (0.5, 0.0, 0.1), (0.85, 1.0, 1.0), (1.0, 1.0, 1.0)],
                      'blue': [(0.0, 0.0, 0.0), (0.5, 0.0, 0.1), (0.85, 1.0, 1.0), (1.0, 1.0, 1.0)]}
        self.cmap_1 = LinearSegmentedColormap('dark_red', cdict_red)
        self.cmap_2 = LinearSegmentedColormap('dark_blue', cdict_blue)
        self.ratio = np.mean(self.image_data_2)/np.mean(self.image_data_1)
        self.image_1 = self.ax_image.imshow(self.ratio * self.image_data_1, cmap=self.cmap_1, alpha=1)
        self.image_2 = self.ax_image.imshow(self.image_data_2, cmap=self.cmap_2, alpha=0.5)

        self.cid = self.connect()
        self.shift = np.array([0, 0])



    def connect(self):
        self.cid = self.fig_image.canvas.mpl_connect('key_press_event', self.shift_gui)
        self.cid1 = self.fig_image.canvas.mpl_connect('close_event', self.handle_close)
        return self.cid

    def shift_gui(self, event):
        h_shift = np.array([0, 1])
        v_shift = np.array([-1, 0])
        if event.key == 'up':
            self.shift = np.add(self.shift, v_shift)
            print(self.shift)
            self.image_data_2 = np.roll(self.image_data_2, (-1, 0), axis=(0, 1))
            self.update_image()
        if event.key == 'alt+up':
            self.shift = np.add(self.shift, 10 * v_shift)
            print(self.shift)
            self.image_data_2 = np.roll(self.image_data_2, (-10, 0), axis=(0, 1))
            self.update_image()
        if event.key == 'down':
            self.shift = np.subtract(self.shift, v_shift)
            print(self.shift)
            self.image_data_2 = np.roll(self.image_data_2, (1, 0), axis=(0, 1))
            self.update_image()
        if event.key == 'alt+down':
            self.shift = np.subtract(self.shift, 10 * v_shift)
            print(self.shift)
            self.image_data_2 = np.roll(self.image_data_2, (10, 0), axis=(0, 1))
            self.update_image()
        if event.key == 'right':
            self.shift = np.add(self.shift, h_shift)
            print(self.shift)
            self.image_data_2 = np.roll(self.image_data_2, (0, 1), axis=(0, 1))
            self.update_image()
        if event.key == 'alt+right':
            self.shift = np.add(self.shift, 10 * h_shift)
            print(self.shift)
            self.image_data_2 = np.roll(self.image_data_2, (0, 10), axis=(0, 1))
            self.update_image()
        if event.key == 'left':
            self.shift = np.subtract(self.shift, h_shift)
            print(self.shift)
            self.image_data_2 = np.roll(self.image_data_2, (0, -1), axis=(0, 1))
            self.update_image()
        if event.key == 'alt+left':
            self.shift = np.subtract(self.shift, 10 * h_shift)
            print(self.shift)
            self.image_data_2 = np.roll(self.image_data_2, (0, -10), axis=(0, 1))
            self.update_image()
        if event.key == 'm':
            print('Shift locked')
            return self.shift
        if event.key == 'shift':
            print('A faire')

    def disconnect(self):
        self.fig_image.canvas.mpl_disconnect(self.cid)
        self.fig_image.canvas.mpl_disconnect(self.cid1)

    def handle_close(self, event):
        self.disconnect()
        plt.close(self.fig_image)
        print('plot closed')

    def update_image(self):
        self.ax_image.cla()
        self.image_1 = self.ax_image.imshow(self.ratio * self.image_data_1, cmap=self.cmap_1, alpha=1)
        self.image_2 = self.ax_image.imshow(self.image_data_2, cmap=self.cmap_2, alpha=0.5)
        self.image_1.set_clim(vmin=self.cmin, vmax=self.cmax)
        self.image_2.set_clim(vmin=self.cmin, vmax=self.cmax)
        plt.draw()

    def update_image_clim(self):
        self.image_1.set_clim(vmin=self.cmin, vmax=self.cmax)
        self.image_2.set_clim(vmin=self.cmin, vmax=self.cmax)

    def contrast_span(self, cmin, cmax):
        self.cmin = cmin
        self.cmax = cmax
        self.update_image_clim()

    def update_cmin(self, event):
        self.cmin = float(event)
        self.contrast_span(self.cmin, self.cmax)

    def update_cmax(self, event):
        self.cmax = float(event)
        self.contrast_span(self.cmin, self.cmax)

    def plot_contrast_histogram(self):
        self.ax_contrast.cla()
        self.ax_contrast.plot(self.imbins[:-1], self.imhist, color='k')
        self.ax_contrast.set_axis_off()
        self.ax_contrast_span = SpanSelector(self.ax_contrast, self.contrast_span, 'horizontal',
                                             span_stays=True, rectprops=dict(alpha=0.5, facecolor='green'))
