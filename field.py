import numpy as np

def field_magn(dataem):
    potential = dataem.diff_2_1_cor
    potential_not_cor = dataem.diff_2_1_not_cor
    e_charge = 1.6 * 10 ** (-19)
    h_Planck = 6.62 * 10 ** (-34)
    thickness = 100 * 10 ** (-9)
    dataem.constant = h_Planck / ( 2 * np.pi * e_charge * thickness * dataem.pixel)
    B_cor = np.gradient(dataem.constant * potential)
    B_not_cor = np.gradient(dataem.constant * potential_not_cor)
    A = np.shape(potential)
    X, Y = np.meshgrid(np.arange(0, A[1]), np.arange(0, A[0]))
    dataem.field = B_cor, X, Y
    dataem.field_not_cor = B_not_cor, X, Y
    print('Calculation done')