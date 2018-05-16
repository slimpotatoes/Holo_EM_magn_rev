# Test of phase Module (Manual)

import numpy as np
import math as math
import data as data
import phase as phase
import matplotlib.pyplot as plt
import statistics

##########################################################
# Test Difference of identical phase # 1
##########################################################

# Generate data to be passed through phase
data_em_test_1 = data.EMdata()

x1 = np.linspace(0, 255, 256)
y1 = np.linspace(0, 255, 256)
mx1, my1 = np.meshgrid(x1, y1)
data_em_test_1.holo_1 = np.sin(mx1 * 2 * np.pi / 16)
data_em_test_1.holo_2_aligned = data_em_test_1.holo_1
data_em_test_1.holo_ref = data_em_test_1.holo_1

# Circle of radius 1 centered around coordinate (192, 128)
r1 = 1
center1 = (144, 128)

# Pass through phase
phase.phase(center1, r1, data_em_test_1)

# Display results
fig_test_1_2d = plt.figure()
fig_test_1_2d_ax1 = fig_test_1_2d.add_subplot(2, 2, 1)
fig_test_1_2d_ax2 = fig_test_1_2d.add_subplot(2, 2, 2)
fig_test_1_2d_ax3 = fig_test_1_2d.add_subplot(2, 2, 3)
fig_test_1_2d_ax4 = fig_test_1_2d.add_subplot(2, 2, 4)
fig_test_1_2d_ax1.imshow(data_em_test_1.phase_1)
fig_test_1_2d_ax2.imshow(data_em_test_1.phase_2)
fig_test_1_2d_ax3.imshow(data_em_test_1.phase_ref)
fig_test_1_2d_ax4.imshow(data_em_test_1.diff_2_1_not_cor)
fig_test_1_2d_ax1.set_title('Unwrap-1')
fig_test_1_2d_ax2.set_title('Unwrap-2')
fig_test_1_2d_ax3.set_title('Unwrap-Ref')
fig_test_1_2d_ax4.set_title('2-1-uncor')
fig_test_1_1d = plt.figure()
fig_test_1_1d_ax1 = fig_test_1_1d.add_subplot(2, 2, 1)
fig_test_1_1d_ax2 = fig_test_1_1d.add_subplot(2, 2, 2)
fig_test_1_1d_ax3 = fig_test_1_1d.add_subplot(2, 2, 3)
fig_test_1_1d_ax4 = fig_test_1_1d.add_subplot(2, 2, 4)
fig_test_1_1d_ax1.plot(data_em_test_1.diff_1_ref[128, :])
# fig_test_1_1d_ax1.set_ylim(-np.pi, np.pi)
fig_test_1_1d_ax2.plot(data_em_test_1.diff_2_ref[128, :])
# fig_test_1_1d_ax2.set_ylim(-np.pi, np.pi)
fig_test_1_1d_ax3.plot(data_em_test_1.diff_2_1_cor[128, :])
# fig_test_1_1d_ax3.set_ylim(-np.pi, np.pi)
fig_test_1_1d_ax4.plot(data_em_test_1.diff_2_1_not_cor[128, :])
# fig_test_1_1d_ax4.set_ylim(-np.pi, np.pi)
fig_test_1_1d_ax1.set_title('1-Ref')
fig_test_1_1d_ax2.set_title('2-Ref')
fig_test_1_1d_ax3.set_title('2-1-cor')
fig_test_1_1d_ax4.set_title('2-1-uncor')

plt.show()

##########################################################
# Test Difference of known phase images # 2
##########################################################

# Generate data to be passed through phase
data_em_test_2 = data.EMdata()

x2 = np.linspace(0, 255, 256)
y2 = np.linspace(0, 255, 256)
mx2, my2 = np.meshgrid(x2, y2)
a2 = 4
b2 = 4.5
data_em_test_2.holo_1 = np.sin(mx2 * 2 * np.pi / a2)
data_em_test_2.holo_2_aligned = np.sin(mx2 * 2 * np.pi / b2)
data_em_test_2.holo_ref = data_em_test_2.holo_1

# Circle of radius 1 centered around coordinate (192, 128)
r2 = 20
center2 = (192, 128)

# Pass through phase
phase.phase(center2, r2, data_em_test_2)

# Display results
fig_test_2_2d = plt.figure()
fig_test_2_2d_ax1 = fig_test_2_2d.add_subplot(2, 2, 1)
fig_test_2_2d_ax2 = fig_test_2_2d.add_subplot(2, 2, 2)
fig_test_2_2d_ax3 = fig_test_2_2d.add_subplot(2, 2, 3)
fig_test_2_2d_ax4 = fig_test_2_2d.add_subplot(2, 2, 4)
fig_test_2_2d_ax1.imshow(data_em_test_2.phase_1)
fig_test_2_2d_ax2.imshow(data_em_test_2.phase_2)
fig_test_2_2d_ax3.imshow(data_em_test_2.phase_ref)
fig_test_2_2d_ax4.imshow(data_em_test_2.diff_2_1_not_cor)
fig_test_2_2d_ax1.set_title('Unwrap-1')
fig_test_2_2d_ax2.set_title('Unwrap-2')
fig_test_2_2d_ax3.set_title('Unwrap-Ref')
fig_test_2_2d_ax4.set_title('2-1-uncor')
fig_test_2_1d = plt.figure()
fig_test_2_1d_ax1 = fig_test_2_1d.add_subplot(2, 2, 1)
fig_test_2_1d_ax2 = fig_test_2_1d.add_subplot(2, 2, 2)
fig_test_2_1d_ax3 = fig_test_2_1d.add_subplot(2, 2, 3)
fig_test_2_1d_ax4 = fig_test_2_1d.add_subplot(2, 2, 4)
fig_test_2_1d_ax1.plot(data_em_test_2.diff_1_ref[128, :])
# fig_test_1_1d_ax1.set_ylim(-np.pi, np.pi)
fig_test_2_1d_ax2.plot(data_em_test_2.diff_2_ref[128, :])
# fig_test_1_1d_ax2.set_ylim(-np.pi, np.pi)
fig_test_2_1d_ax3.plot(data_em_test_2.diff_2_1_cor[128, :])
# fig_test_1_1d_ax3.set_ylim(-np.pi, np.pi)
fig_test_2_1d_ax4.plot(data_em_test_2.diff_2_1_not_cor[128, :])
# fig_test_1_1d_ax4.set_ylim(-np.pi, np.pi)
fig_test_2_1d_ax1.set_title('1-Ref')
fig_test_2_1d_ax2.set_title('2-Ref')
fig_test_2_1d_ax3.set_title('2-1-cor')
fig_test_2_1d_ax4.set_title('2-1-uncor')

slope_th = (2 * np.pi / b2) - (2 * np.pi / a2)
slope_exp = (data_em_test_2.diff_2_1_not_cor[128, 253] - data_em_test_2.diff_2_1_not_cor[128, 2]) / 251
error_slope = abs(slope_th - slope_exp)
print('Theoretical slope ', slope_th)
print('Experimental slope ', slope_exp)
print('Slope error ', error_slope)

plt.show()