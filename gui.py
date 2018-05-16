import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
from matplotlib.widgets import Button
from matplotlib.colors import LinearSegmentedColormap
from tkinter import filedialog
import numpy as np
import guidisplay as guidisplay
import guimask as guimask
import guirectangle as guirect
import imagedisplay


class HoloEMgui(object):

    def __init__(self, data_em):
        self.dataEM = data_em
        self.fig_flow = None
        self.event_input = None
        self.event_align = None
        self.event_ft = None
        self.event_phase = None
        self.event_refine = None
        self.event_field = None
        self.fig_align = None
        self.fig_mask = None
        self.fig_potential = None
        self.fig_field = None
        self.circle = None
        self.shift = [0, 0]

    def flow(self):
        self.fig_flow = plt.figure(num='SMG Flow', figsize=(2, 5))
        self.fig_flow.canvas.mpl_connect('key_press_event', self.custom_plot)
        gs_button = grid.GridSpec(6, 1)
        self.event_input = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[0, 0])), 'Input')
        self.event_align = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[1, 0])), 'Align')
        self.event_ft = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[2, 0])), 'FT')
        self.event_phase = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[3, 0])), 'Phase')
        self.event_refine = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[4, 0])), 'Refine')
        self.event_field = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[5, 0])), 'Field')


    @staticmethod
    def open_files():
        file_path_holo_1 = filedialog.askopenfilename(title="Load first hologram")
        file_path_holo_2 = filedialog.askopenfilename(title="Load second hologram")
        file_path_holo_ref = filedialog.askopenfilename(title="Load reference hologram")
        #file_path_holo_ref_2 = filedialog.askopenfilename(title="Load reference hologram 2")
        return file_path_holo_1, file_path_holo_2, file_path_holo_ref

    def align_holo(self):
        self.fig_align = guidisplay.GUIDisplayOverlap(self.dataEM)
        plt.show()

    def mask_holo(self):
        self.fig_mask = plt.figure(num='Define mask')
        self.ax_fig_mask = self.fig_mask.add_subplot(1, 1, 1)

        ft_holo_1 = self.fft_display(np.fft.fft2(self.dataEM.holo_1))
        ft_holo_2 = self.fft_display(np.fft.fft2(self.dataEM.holo_2))
        ft_holo_ref = self.fft_display(np.fft.fft2(self.dataEM.holo_ref))

        self.ax_fig_mask.imshow(np.log1p(ft_holo_1), cmap='gray')
        self.ax_fig_mask.imshow(np.log1p(ft_holo_2), cmap='gray', alpha=0.25)
        self.ax_fig_mask.imshow(np.log1p(ft_holo_ref), cmap='gray', alpha=0.25)

        guimaskcreate = guimask.MaskCreator(self.ax_fig_mask, self.dataEM.holo_1)
        guimaskcreate.make_circle('Mask')
        self.circle = guimask.MaskEditor(self.ax_fig_mask.artists[0])
        self.circle.connect()
        plt.show()

    @staticmethod
    def fft_display(fft):
        return np.fft.fftshift(np.abs(fft ** 2))

    def phase_holo(self):
        self.fig_phase = plt.figure()
        self.ax_fig_phase_1 = self.fig_phase.add_subplot(3, 2, 1)
        self.ax_fig_phase_2 = self.fig_phase.add_subplot(3, 2, 2)
        self.ax_fig_phase_diff = self.fig_phase.add_subplot(3, 2, 3)
        self.ax_fig_phase_diff_1 = self.fig_phase.add_subplot(3, 2, 4)
        self.ax_fig_ampltiude_1 = self.fig_phase.add_subplot(3, 2, 5)
        self.ax_fig_ampltiude_2 = self.fig_phase.add_subplot(3, 2, 6)
        self.ax_fig_phase_1.imshow(self.wrap(self.dataEM.diff_1_ref), cmap='gray')
        self.ax_fig_phase_2.imshow(self.wrap(self.dataEM.diff_2_ref), cmap='gray')
        self.ax_fig_phase_diff.imshow(self.dataEM.diff_2_1_cor, cmap='gray')
        self.ax_fig_phase_diff_1.imshow(self.dataEM.diff_2_1_not_cor, cmap='gray')
        self.ax_fig_ampltiude_1.imshow(self.dataEM.amplitude_1, cmap='gray')
        self.ax_fig_ampltiude_2.imshow(self.dataEM.amplitude_2, cmap='gray')

        guirectcreate = guirect.RectCreator(self.ax_fig_phase_diff, self.dataEM.diff_2_1_cor)
        guirectcreate.make_rectangle('Rect')
        self.rect = guirect.RectEditor(self.fig_phase, self.ax_fig_phase_diff, guirectcreate.rect)
        self.rect.connect()

        plt.show()

    @staticmethod
    def wrap(phase):
        return phase - np.round(phase / (2 * np.pi)) * 2 * np.pi

    def reference_extract(self, rectangle):
        x0, y0 = rectangle.get_xy()
        x1, y1 = x0 + rectangle.get_width(), y0 + rectangle.get_height()
        print(int(x0), int(y0), int(x1), int(y1))
        return int(x0), int(y0), int(x1), int(y1)

    def refine_gui(self):
        self.ax_fig_phase_diff.imshow(self.dataEM.diff_2_1_cor, cmap='gray')
        self.fig_phase.canvas.draw()

    def field_gui(self):
        self.fig_potential = plt.figure(num='Potential')
        self.ax_fig_potential = self.fig_potential.add_subplot(1, 1, 1)
        image_potential = self.ax_fig_potential.imshow(self.dataEM.diff_2_1_cor, cmap='gray')
        level = np.arange(int(np.min(self.dataEM.diff_2_1_cor[100:-100, 100: -100])),
                          int(np.max(self.dataEM.diff_2_1_cor[100:-100, 100: -100])), 0.1)
        contour = self.ax_fig_potential.contour(self.dataEM.diff_2_1_cor, level, linewidths=2)
        #self.ax_fig_potential.clabel(contour, inline=1, fontsize=10, hold=False)
        self.ax_fig_potential.set_axis_off()
        cbar = plt.colorbar(image_potential)
        cbar.add_lines(contour)

        print('Potential mapped')

        self.fig_potential_not_cor = plt.figure(num='Potential not cor')
        self.ax_fig_potential_not_cor = self.fig_potential_not_cor.add_subplot(1, 1, 1)
        self.ax_fig_potential_not_cor.imshow(self.dataEM.diff_2_1_not_cor, cmap='gray')
        level_1 = np.arange(int(np.min(self.dataEM.diff_2_1_not_cor[100:-100, 100: -100])),
                            int(np.max(self.dataEM.diff_2_1_not_cor[100:-100, 100: -100])), 1)
        contour_1 = self.ax_fig_potential_not_cor.contour(self.dataEM.diff_2_1_not_cor, level_1)
        self.ax_fig_potential_not_cor.clabel(contour_1, inline=1, fontsize=10, hold=False)
        self.ax_fig_potential_not_cor.set_axis_off()
        print('Potential uncorrected mapped')

        orient = np.arctan2(self.dataEM.field[0][0], self.dataEM.field[0][1])

        fig_temp_B = plt.figure()
        axis_temp_B = fig_temp_B.add_subplot(1, 1, 1)
        image_temp_B = axis_temp_B.imshow(orient, cmap='hsv', vmin=-np.pi, vmax=np.pi, alpha=0.6)
        fig_temp_B.colorbar(image_temp_B)
        axis_temp_B.quiver(self.dataEM.field[1][50:-50:20, 50:-50:20],
                           self.dataEM.field[2][50:-50:20, 50:-50:20],
                           self.dataEM.field[0][0][50:-50:20, 50:-50:20] / self.dataEM.constant,
                           self.dataEM.field[0][1][50:-50:20, 50:-50:20] / self.dataEM.constant,
                           scale=0.6, units='width', pivot='mid', color='k', alpha=0.7, headwidth=4, width = 0.002)
        axis_temp_B.set_axis_off()
        fig_temp_B.show()

        orient_not_cor = np.arctan2(self.dataEM.field_not_cor[0][0], self.dataEM.field_not_cor[0][1])

        fig_temp_B_not_cor = plt.figure()
        axis_temp_B_not_cor = fig_temp_B_not_cor.add_subplot(1, 1, 1)
        image_temp_B_not_cor = axis_temp_B_not_cor.imshow(orient_not_cor, cmap='hsv', vmin=-np.pi, vmax=np.pi, alpha=0.6)
        fig_temp_B_not_cor.colorbar(image_temp_B_not_cor)
        axis_temp_B_not_cor.quiver(self.dataEM.field_not_cor[1][50:-50:20, 50:-50:20],
                                   self.dataEM.field_not_cor[2][50:-50:20, 50:-50:20],
                                   self.dataEM.field_not_cor[0][0][50:-50:20, 50:-50:20] / self.dataEM.constant,
                                   self.dataEM.field_not_cor[0][1][50:-50:20, 50:-50:20] / self.dataEM.constant,
                                   scale=0.6, units='width', pivot='mid', color='k', alpha=0.5)
        axis_temp_B_not_cor.set_axis_off()
        fig_temp_B_not_cor.show()
        print('Field mapped')

        fig_temp_B_magn = plt.figure()
        axis_temp_B_magn = fig_temp_B_magn.add_subplot(1, 1, 1)
        image_temp_B_magn = axis_temp_B_magn.imshow(np.sqrt(np.square(self.dataEM.field[0][0][50:-50, 50:-50])+
                                                            np.square(self.dataEM.field[0][1][50:-50, 50:-50])),
                                                    vmin=0, vmax=2)
        fig_temp_B_magn.colorbar(image_temp_B_magn)
        axis_temp_B_magn.set_axis_off()
        fig_temp_B_magn.show()

        fig_temp_B_magnnotcor = plt.figure()
        axis_temp_B_magnnotcor = fig_temp_B_magnnotcor.add_subplot(1, 1, 1)
        image_temp_B_magnnotcor = axis_temp_B_magnnotcor.imshow(np.sqrt(np.square(self.dataEM.field_not_cor[0][0][50:-50, 50:-50]) +
                                                            np.square(self.dataEM.field_not_cor[0][1][50:-50, 50:-50])),
                                                    vmin=0, vmax =2)
        fig_temp_B_magnnotcor.colorbar(image_temp_B_magnnotcor)
        axis_temp_B_magnnotcor.set_axis_off()
        fig_temp_B_magnnotcor.show()

        plt.show()

    def custom_plot(self, event):
        if event.key == '1':
            data_to_display = self.dataEM.holo_1
            p = self.dataEM.pixel * 10 **(9)
            imagedisplay.ImageDisplay(data_to_display, cal=p)
        if event.key == '2':
            data_to_display = self.dataEM.holo_2
            p = self.dataEM.pixel * 10 **(9)
            imagedisplay.ImageDisplay(data_to_display, cal=p)
        if event.key == '3':
            data_to_display = self.dataEM.diff_2_1_cor
            p = self.dataEM.pixel * 10 **(9)
            imagedisplay.ImageDisplay(data_to_display, cal=p)
        if event.key == '4':
            data_to_display = np.sqrt(np.square(self.dataEM.field[0][0]) +
                                      np.square(self.dataEM.field[0][1]))
            p = self.dataEM.pixel * 10 **(9)
            imagedisplay.ImageDisplay(data_to_display, cal=p)