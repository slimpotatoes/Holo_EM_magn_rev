import numpy as np
import matplotlib.pyplot as plt
import data as data
import alignholo as alignholo

image_1= np.array([[1, 0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                   [1, 0, 0, 1, 0, 0, 1]])
image_2= np.array([[1, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 1, 0],
                   [1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 0],
                   [1, 0, 0, 0, 0, 1, 1]])

data_test = data.EMdata()
data_test.holo_1 = image_1
data_test.holo_2 = image_2

shift_gui=[1, -2]
axis=(0, 1)

alignholo.shift_holo(shift_gui, data_test)
image_1_crop, image_2_crop = alignholo.crop_phase(shift_gui, data_test.holo_1, data_test.holo_2)

fig_test = plt.figure()
fig_test_ax_1 = fig_test.add_subplot(1, 3, 1)
fig_test_ax_1.imshow(data_test.holo_1 + data_test.holo_2, cmap='gray')
fig_test_ax_2 = fig_test.add_subplot(1, 3, 2)
fig_test_ax_2.imshow(data_test.holo_1 + data_test.holo_2_aligned, cmap='gray')
fig_test_ax_3 = fig_test.add_subplot(1, 3 ,3)
fig_test_ax_3.imshow(image_1_crop + image_2_crop, cmap='gray')
plt.show()

image_1a= np.array([[1, 0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                   [1, 0, 0, 1, 0, 0, 1]])
image_2a= np.array([[1, 1, 0, 0, 0, 0, 1], [0, 1, 0, 0, 0, 0, 0],
                   [0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1], [0, 1, 0, 0, 0, 0, 0],
                   [1, 1, 0, 0, 0, 0, 1]])

data_testa = data.EMdata()
data_testa.holo_1 = image_1a
data_testa.holo_2 = image_2a

shift_guia=[-1, 2]
axisa=(0, 1)

alignholo.shift_holo(shift_guia, data_testa)
image_1_cropa, image_2_cropa = alignholo.crop_phase(shift_guia, data_testa.holo_1, data_testa.holo_2)

fig_testa = plt.figure()
fig_testa_ax_1 = fig_testa.add_subplot(1, 3, 1)
fig_testa_ax_1.imshow(data_testa.holo_1 + data_testa.holo_2, cmap='gray')
fig_testa_ax_2 = fig_testa.add_subplot(1, 3, 2)
fig_testa_ax_2.imshow(data_testa.holo_1 + data_testa.holo_2_aligned, cmap='gray')
fig_testa_ax_3 = fig_testa.add_subplot(1, 3 ,3)
fig_testa_ax_3.imshow(image_1_cropa + image_2_cropa, cmap='gray')
plt.show()

image_1_big = np.zeros((999, 999))
image_1_big[499, :] = 1
image_1_big[:, 499] = 1
image_2_big = np.zeros((999, 999))
image_2_big[699, :] = 1
image_2_big[:, 399] = 1

data_test_big = data.EMdata()
data_test_big.holo_1 = image_1_big
data_test_big.holo_2 = image_2_big

shift_gui_big=[-200, 100]
alignholo.shift_holo(shift_gui_big, data_test_big)
image_1_big_crop, image_2_big_crop = alignholo.crop_phase(shift_gui_big, data_test_big.holo_1, data_test_big.holo_2)

fig_test_big = plt.figure()
fig_test_big_ax_1 = fig_test_big.add_subplot(1, 3, 1)
fig_test_big_ax_1.imshow(data_test_big.holo_1 + data_test_big.holo_2, cmap='gray')
fig_test_big_ax_2 = fig_test_big.add_subplot(1, 3, 2)
fig_test_big_ax_2.imshow(data_test_big.holo_1 + data_test_big.holo_2_aligned, cmap='gray')
fig_test_big_ax_3 = fig_test_big.add_subplot(1, 3, 3)
fig_test_big_ax_3.imshow(image_1_big_crop + image_2_big_crop, cmap='gray')
plt.show()