import numpy as np
import matplotlib.pyplot as plt

windows = ["rectangular", "hamming"]

def compute_spectrogram(data: list[float], overlap: float=0, window_size: int=0, 
                        window_type: str="hamming") -> list[list[float]]:
    spectrogram = []
    overlap_size = int(window_size*overlap)
    if overlap_size < 0 or overlap_size >= window_size:
        raise ValueError("Invalid overlap")
    data_length      = len(data)
    window_start_pos = 0
    window_shift = window_size - overlap_size
    while window_start_pos < data_length:
        if data_length - window_start_pos < window_size:
            pad_size = window_size - (data_length - window_start_pos)
            padded_data = np.pad(data[window_start_pos:window_start_pos + window_size], (0, pad_size), 'constant')
            windowed_data = window_func(padded_data, type=window_type)
            spectrogram.append(np.fft.fft(windowed_data).tolist()[:window_size//2])
            # spectrogram.append(np.fft.fft(padded_data).tolist()[:window_size//2])
        else:
            windowed_data = window_func(data[window_start_pos:window_start_pos + window_size], type=window_type)
            spectrogram.append(np.fft.fft(windowed_data).tolist()[:window_size//2])
            # spectrogram.append(np.fft.fft(data[window_start_pos:window_start_pos + window_size]).tolist()[:window_size//2])
        window_start_pos += window_shift
    return np.flip(np.array(spectrogram).T, axis=0).tolist()


def window_func(data, type: str="rectangular"):
    if type == "rectangular":
        return data
    if type == "hamming":
        length = len(data)
        indices = np.linspace(0, length, length, endpoint=False)
        a0 = 0.54
        w = a0 - (1 - a0) * np.cos(2 * np.pi * indices / (length - 1))
        return w * data
    if type == "hann":
        length = len(data)
        indices = np.linspace(0, length, length, endpoint=False)
        a0 = 0.5
        w = a0 - (1 - a0) * np.cos(2 * np.pi * indices / (length - 1))
        return w * data



if __name__ == "__main__":
    s = []
    t = []
    dt = 0.0005
    for i in range(10000):
    
        if i < 2000:
            s.append(np.sin(2 * np.pi * 200 * i * dt))
        elif i < 4000:
            s.append(np.sin(2 * np.pi * 250 * i * dt))
        elif i < 6000:
            s.append(np.sin(2 * np.pi * 350 * i * dt))
        elif i < 8000:
            s.append(np.sin(2 * np.pi * 800 * i * dt))
        elif i < 10000:
            s.append(np.sin(2 * np.pi * 950 * i * dt))
        t.append(i)

    fig, ax = plt.subplots()
    #ax.plot(t, s)
    sg = compute_spectrogram(s, '', 0, 128)
    print(sg)
    print(len(sg))
    print(len(sg[0]))

    ax.imshow(np.abs(sg), cmap='grey', extent=[0, len(sg), 0, 1/(2*dt)], aspect='auto')
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')
    #ax.grid()

    plt.show()