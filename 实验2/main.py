import argparse
import numpy as np
import librosa

DTMF_FREQUENCIES = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477)
}

FRAME_DURATION = 1 / 64
ENERGY_THRESHOLD = 0.01


def calculate_rms(audio):
    """计算音频的均方根能量"""
    return np.sqrt(np.mean(audio**2))


def find_closest_key(low_freq, high_freq):
    """根据频率找到对应的按键"""
    for key, (low, high) in DTMF_FREQUENCIES.items():
        if abs(low_freq - low) < 20 and abs(high_freq - high) < 20:
            return key
    return -1


def get_key_from_frame(frame, sr):
    """分析单帧音频，返回对应按键"""
    # 计算短时傅里叶变换
    spectrum = np.abs(np.fft.rfft(frame)) #频率对应的能量
    freqs = np.fft.rfftfreq(len(frame), d=1/sr) #每个频率的值

    # 找到前两个最大的频率分量
    peak_indices = np.argsort(spectrum)[-2:]
    peak_freqs = freqs[peak_indices]

    # 根据频率判断按键
    if len(peak_freqs) < 2:
        return -1
    low_freq, high_freq = sorted(peak_freqs)
    return find_closest_key(low_freq, high_freq)


def key_tone_recognition(audio, sr):
    """DTMF 按键音识别"""
    frame_size = int(FRAME_DURATION * sr)
    num_frames = len(audio) // frame_size

    result = []
    for i in range(num_frames):
        frame = audio[i * frame_size: (i + 1) * frame_size]
        rms = calculate_rms(frame)

        if rms < ENERGY_THRESHOLD:  # 静默帧
            result.append(-1)
        else:  # 非静默帧
            key = get_key_from_frame(frame, sr)
            result.append(key)

    output = ' '.join(map(str, result))
    with open('tmp.txt', 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(output)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_file', type=str, help='test file name', required=True)
    args = parser.parse_args()

    # 加载音频文件
    input_audio_array, sr = librosa.load(args.audio_file, sr=48000, dtype=np.float32)

    # 识别按键音
    key_tone_recognition(input_audio_array, sr)

