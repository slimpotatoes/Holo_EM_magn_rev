# GPA Module


import mask as mask
import numpy as np
from skimage.restoration import unwrap_phase
import alignholo as alignholo
# import dm3_lib


def phase(center, r, shift_gui, dataEM):

    # Load the elements
    ft_holo_1 = np.fft.fft2(dataEM.holo_1)
    ft_holo_2 = np.fft.fft2(dataEM.holo_2)
    ft_holo_ref = np.fft.fft2(dataEM.holo_ref)

    # Generate the mask in the image space
    m, g_uns = mask.mask_gaussian(center, r, ft_holo_1.shape)

    # Mask and calculate the phase component
    masked_ft_holo_1 = np.multiply(m, np.fft.fftshift(ft_holo_1))
    masked_ft_holo_2 = np.multiply(m, np.fft.fftshift(ft_holo_2))
    masked_ft_holo_ref = np.multiply(m, np.fft.fftshift(ft_holo_ref))
    # masked_ft_holo_ref_2 =  np.multiply(m, np.fft.fftshift(ft_holo_ref_2))

    # shift and crop before unwraping
    i_fft_1 = np.fft.ifft2(np.fft.ifftshift(masked_ft_holo_1))
    i_fft_2 = np.fft.ifft2(np.fft.ifftshift(masked_ft_holo_2))
    amplitude_1_distorded = np.abs(i_fft_1)
    amplitude_2_distorded = np.abs(i_fft_2)
    phase_1_distorded = np.angle(i_fft_1)
    phase_2_distorded = np.angle(i_fft_2)

    dataEM.phase_ref = unwrap_phase(np.angle(np.fft.ifft2(np.fft.ifftshift(masked_ft_holo_ref))), seed=None)
    phase_1_distorded_unwrap = unwrap_phase(phase_1_distorded, seed=None)
    phase_2_distorded_unwrap = unwrap_phase(phase_2_distorded, seed=None)

    phase_1_unwrap = phase_1_distorded_unwrap # - dataEM.phase_ref
    phase_2_unwrap = phase_2_distorded_unwrap # - dataEM.phase_ref

    phase_unwrap_crop = alignholo.crop_phase(shift_gui, phase_1_unwrap, phase_2_unwrap)
    phase_crop = alignholo.crop_phase(shift_gui, phase_1_distorded, phase_2_distorded)
    amplitude_crop = alignholo.crop_phase(shift_gui, amplitude_1_distorded, amplitude_2_distorded)

    dataEM.phase_1 = phase_unwrap_crop[0]
    dataEM.phase_2 = phase_unwrap_crop[1]
    dataEM.amplitude_1 = amplitude_crop[0]
    dataEM.amplitude_2 = amplitude_crop[1]

    # dataEM.phase_ref_2 = unwrap_phase(np.angle(np.fft.ifft2(np.fft.ifftshift(masked_ft_holo_ref_2))))

    dataEM.diff_1_ref_notsmoothed = dataEM.phase_1
    dataEM.diff_2_ref_notsmoothed = dataEM.phase_2
    dataEM.diff_2_1_not_cor_notsmoothed = unwrap_phase(phase_crop[1], seed=None) - unwrap_phase(phase_crop[0], seed=None)
    # dataEM.diff_2_1_cor_notsmoothed = unwrap_phase(phase_crop[1], seed=None) - unwrap_phase(phase_crop[0], seed=None)
    dataEM.diff_2_1_cor_notsmoothed = dataEM.diff_2_ref_notsmoothed - dataEM.diff_1_ref_notsmoothed

    '''dataEM.diff_1_ref = gaussian_filter(dataEM.diff_1_ref_notsmoothed, 6)
    dataEM.diff_2_ref = gaussian_filter(dataEM.diff_2_ref_notsmoothed, 6)
    dataEM.diff_2_1_not_cor = gaussian_filter(dataEM.diff_2_1_not_cor_notsmoothed, 6)
    dataEM.diff_2_1_cor = gaussian_filter(dataEM.diff_2_1_cor_notsmoothed, 6)'''

    dataEM.diff_1_ref = dataEM.diff_1_ref_notsmoothed
    dataEM.diff_2_ref = dataEM.diff_2_ref_notsmoothed
    dataEM.diff_2_1_not_cor = dataEM.diff_2_1_not_cor_notsmoothed
    dataEM.diff_2_1_cor = dataEM.diff_2_1_cor_notsmoothed

    print('Pente 1 ', (dataEM.diff_2_1_cor[501, 500] - dataEM.diff_2_1_cor[500, 500]) / 2)
    print('Pente 2 ', (dataEM.diff_2_1_cor[500, 501] - dataEM.diff_2_1_cor[500, 500]) / 2)

    e_charge = 1.6 * 10 ** (-19)
    h_Planck = 6.62 * 10 ** (-34)
    thickness = 100 * 10 ** (-9)
    constant = e_charge * thickness / h_Planck

    print('B 1 ', (dataEM.diff_2_1_cor[502, 500] - dataEM.diff_2_1_cor[500, 500]) / (2 * constant) )
    print('B 2 ', (dataEM.diff_2_1_cor[500, 502] - dataEM.diff_2_1_cor[500, 500]) / (2 * constant) )