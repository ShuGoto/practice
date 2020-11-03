# -*- coding: utf-8 -*-

import numpy as np
import scipy.fftpack as fft
import wave # wavファイルを扱うライブラリのインポート
import matplotlib.pyplot as plt 


def mkwhite(t, fs=48000):

    tap = int(t*fs) #tap数の確認，時間＊サンプリング周波数
    white = np.random.randn(tap) #tap数分のランダムな値を作成し，配列へ
    white /= np.max(np.abs(white)) #最大値を1として正規化
    return white


def mkpink(t, fs=48000):

    tap = int(t*fs)
    white = mkwhite(t, fs)
    WHITE = fft.fft(white) #ホワイトノイズにfftをかけたもの

    pink_filter = np.concatenate((np.array([1]), 1/np.sqrt(np.arange(start=fs/tap, stop=fs, step=fs/tap))))
    PINK = WHITE * pink_filter
    pink = np.real(fft.ifft(PINK))
    pink /= np.max(np.abs(pink))

    return pink


#n回のピンクバースト音を繰り返す
def pinkblock(n):
    #一連のノイズ：前後20msずつにテーバをかけ，定常の時間は200ms，空白時間は100ms，計340ms
    pinklong = mkpink(0.34, 48000)
    for i in range(0, 480 * 2):
        pinklong[i] = pinklong[i] * i * 1/960
    for i in range(10560, 10560 + 960):
        pinklong[i] = pinklong[i] - ((i - 10560) * 1/960) * pinklong[i]
    for i in range(11520, 11520 + 4800):
        pinklong[i] = 0

    pinklong = np.tile(pinklong, n)

    return pinklong

## wav ファイルに書き出す
# numpy ２次元配列を wave ファイルに書き込む関数
def writewav(filename, data, ws=3, fs=48000, e=-1):
    '''
    Parameters
    ----------
    filename: strings
        frequency of sine-wave
    data: numpy.ndarray
        number of samples of sine-wave
    ws: int
        byte width of samples.
        1: 8 bit, 2: 16 bit, 3: 24 bit, 4: 32 bit
    fs: int
        sampling rate
    '''
    nchannels = data.shape[1]
    sampwidth = ws
    data = (data * (2 ** (8 * sampwidth - 1) + e)).reshape(data.size, 1)
    
    if sampwidth == 1:
        data = data + 128
        frames = data.astype(np.uint8).tostring()
    elif sampwidth == 2:
        frames = data.astype(np.int16).tostring()
    elif sampwidth == 3:
        a32 = np.asarray(data, dtype = np.int32)
        a8 = (a32.reshape(a32.shape + (1,)) >> np.array([0, 8, 16])) & 255
        frames = a8.astype(np.uint8).tostring()
    elif sampwidth == 4:
        frames = data.astype(np.int32).tostring()
    
    w = wave.open(filename, 'wb')
    w.setparams((nchannels, sampwidth, fs, 0, 'NONE', 'not compressed'))
    w.writeframes(frames)
    w.close()
    return

import soundfile as sf

print("どちらのpinknoiseを作りますか？\n 持続pinknoiseを作成する場合は,1\n ピンクバーストノイズを作成する場合は,2\n") 
select = input("入力してください：")
select = int(select)

if select == 1:
    time = int(input("持続時間を入力してください"))
    x = mkpink(time, fs=48000)
    filename = input("ファイル名を入力しでください")
    sf.write(filename, x, 48000, subtype='PCM_24')
elif select == 2:
    num = int(input("回数を選択してください"))
    x = pinkblock(num)
    filename = input("ファイル名を入力しでください")
    sf.write(filename, x, 48000, subtype='PCM_24')
else:
    print("入力エラー")

