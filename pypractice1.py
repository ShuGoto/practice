# -*- coding: utf-8 -*-

"""
Reverberation
"""

from scipy import array, ceil, float64, int16, log2, zeros
from scipy import ifft
from scipy.fftpack import fft
from scipy.io.wavfile import read, write
import soundfile as sf
from scipy import fromstring
#from scikits.audiolab import wavread, wavwright

### 指定値以上の最小の2のべき乗の指数
#この作業の理由：FFTは2のべき乗ではないと行けないため，残った部分を0で埋める必要がある．
def nextpow2(n):
    return ceil(log2(abs(n)))
    #ceil = 小数点以下切り上げ
    #abs = 絶対値

def sampling_reverb(signal_array, impulse_response):
    sigL = len(signal_array)
    irL = len(impulse_response)

    ### インパルス応答の長さ調整
    new_irL = int((2 ** nextpow2(irL))* 2) #2フレーム分
    frameL = new_irL / 2
    #zeros:0で初期化した配列を作成（shape, dtype）
    new_IR = zeros(new_irL, dtype = float64)
    #[:]はスライス．今回の場合は一番最初からirLまでの長さの部分にimpulse＿responseを代入
    new_IR[: irL] = impulse_response

    ###入力信号を適度な長さにする．
    frame_num = int(ceil((sigL + frameL) / float(frameL)))
    new_sigL = frameL * frame_num
    new_sig = zeros(new_sigL, dtype = float64)
    new_sig[frameL : frameL + sigL] = signal_array

    ###インパルス応答の畳み込み
    ret = zeros(new_sigL - frame_num, dtype = float64)
    ir_fft = fft(new_IR)#インパルス応答のFFT
    for ii in xrange(frame_num - 1):
        s_ind = frameL * ii
        e_ind = frameL * (ii + 2)

        sig_fft = fft(new_sig[s_ind:e_ind])#信号のFFT
        ###畳み込み
        ret[s_ind : s_ind + frameL] = ifft(sig_fft * ir_fft)[frameL :].real

    print (new_irL, sigL, new_sigL)
    print len(sig_fft)
    print len(ir_fft)
    return ret[: sigL]


def test():
    wav_file = "/Users/shugoto/Desktop/programming/MyPythonProject/clapping.wav" #wavファイル読み込み
    impulse_response_file = "/Users/shugoto/Desktop/programming/MyPythonProject/ir1.wav" #IRファイル読み込み


    #データ本体，サンプリング周波数，ファイルフォーマット
    data, fs_sig = sf.read(wav_file)
    st_impulse_response, fs_ir = sf.read(impulse_response_file)
    assert fs_sig == fs_ir, "hahahaha" #サンプリング周波数が同じかどうかのチェック
    impulse_response = st_impulse_response[:,0]
    

    ###残響付加
    reverbed_signal = sampling_reverb(data, impulse_response)

    ##クリッピング防止
    if max(reverbed_signal) > 1:
        reverbed_signal /= (max(reverbed_signal) * 1.2)

    ###wavファイルに書き出し
    sf.write('/Users/shugoto/Desktop/programming/MyPythonProject/reverbpractice1.wav', reverbed_signal, fs_sig)

if __name__ == "__main__":
    test()
    