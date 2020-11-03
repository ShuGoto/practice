#補完IR作成プログラム
#3度ごとのIRから0.5度ごとのIRを補完して作成

import numpy as np
import matplotlib.pyplot as plt 

def complement(azi):
    newazi1 = azi + 1
    newazi2 = azi + 2
    azi1 = azi
    if azi1 - 10 < 0:
        azi1 = "00" + str(azi1)
    elif azi1 - 100 < 0:
        azi1 = "0" + str(azi1)
    else:
        azi1 = str(azi1)
    ir1_filename = '/Users/shugoto/Desktop/IR/補完IR/ir_4096taps_elevetion090_azimuth%s.npy' % azi1
    ir1 =  np.load(ir1_filename)
    if azi == 357:
        ir2_filename = '/Users/shugoto/Desktop/IR/補完IR/ir_4096taps_elevetion090_azimuth000.npy' 
    else:
        azi2 = azi + 3
        if azi2 - 10 < 0:
            azi2 = "00" + str(azi2)
        elif azi2 - 100 < 0:
            azi2 = "0" + str(azi2)
        else:
            azi2 = str(azi2)
        ir2_filename = '/Users/shugoto/Desktop/IR/補完IR/ir_4096taps_elevetion090_azimuth%s.npy' %azi2
    ir2 =  np.load(ir2_filename)

    ir1_f = np.fft.fft(ir1)
    ir2_f = np.fft.fft(ir2)

    r = 1/3
    ir_f_1 = r*ir1_f + (1 - r)*ir2_f
    y1 = np.real(np.fft.ifft(ir_f_1))
    if newazi1 - 10 < 0:
        newazi1 = "00" + str(newazi1)
    elif newazi1 - 100 < 0:
        newazi1 = "0" + str(newazi1)
    else:
        newazi1 = str(newazi1)
    filename1 = '/Users/shugoto/Desktop/IR/補完IR/ir_4096taps_elevetion090_azimuth%s.npy' %newazi1
    np.save(filename1, y1)

    r = 2/3
    ir_f_2 = r*ir1_f + (1 - r)*ir2_f
    y2 = np.real(np.fft.ifft(ir_f_2))
    if newazi2 - 10 < 0:
        newazi2 = "00" + str(newazi2)
    elif newazi2 - 100 < 0:
        newazi2 = "0" + str(newazi2)
    else:
        newazi2 = str(newazi2)
    filename2 = '/Users/shugoto/Desktop/IR/補完IR/ir_4096taps_elevetion090_azimuth%s.npy' %newazi2
    np.save(filename2, y2)

    # fig1 = plt.figure()
    # plt.plot(y1[0,:])
    # fig2 = plt.figure()
    # plt.plot(y2[0,:])
    # fig3 = plt.figure()
    # plt.plot(ir1[0,:])
    # plt.show()


for i in range(0,360,3):
    complement(i)
print("補完IRを生成しました")





