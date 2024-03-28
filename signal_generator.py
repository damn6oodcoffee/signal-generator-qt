import math

class FrequencyModulator:
    def __init__(self, modulation_depth=None, period=None):
        if modulation_depth is None or period is None:
            return
        self.modulation_depth = modulation_depth
        self.period = period
        self.slope = self.modulation_depth / (self.period // 2)
    
    def get_freq(self, index):
        index = index % self.period
        half_period = self.period // 2
        if index < half_period:
            return self.slope * index
        else:
            return self.modulation_depth - self.slope * (index - half_period)
    
    def set_params(self, depth, period):
        self.modulation_depth = depth
        self.period = period
        self.slope = self.modulation_depth / (self.period // 2)


class SignalGenerator:
    def __init__(self, phase=None, freq=None, sample_rate=None, depth=None, fm_depth=None, fm_period=None):
        #self.phase = float(phase)
        self.phase = 0.0
        #self.freq = float(freq)
        #self.set_sample_rate(sample_rate)
        #self.set_bit_depth(depth)
        self.fm = FrequencyModulator(fm_depth, fm_period)
        self.last_index = 0

    def set_params(self, phase, freq, sample_rate, depth, fm_depth, fm_period):
        if phase is not None:
            self.phase = float(phase)
        self.freq = float(freq)
        self.set_sample_rate(sample_rate)
        self.set_bit_depth(depth)
        self.fm.set_params(fm_depth, fm_period)

    def set_phase(self, phase):
        self.phase = phase

    def set_freq(self, freq):
        self.freq = freq

    def set_sample_rate(self, sample_rate):
        self.sample_rate = float(sample_rate)
        self.time_interval = 1.0 / self.sample_rate

    def set_bit_depth(self, depth):
        self.levels = 1 << depth

    def get_samples(self, size):
        samples = []
        saw_samples = []
        phase_samples = []
        freq_samples = []
        #_phase = 0
        indices = []
        amplitude = (self.levels - 2) // 2
        for i in range(0, size):
            sample = amplitude * math.sin(
                #self.phase + 2 * math.pi * (self.freq + self.fm.get_freq(self.last_index + i)) * self.time_interval * i
                #_phase + 2 * math.pi * (self.freq + self.fm.get_freq(self.last_index + i)) * self.time_interval
                self.phase + 2 * math.pi * (self.freq + self.fm.get_freq(self.last_index + i)) * self.time_interval
            )
            self.phase += 2 * math.pi * (self.freq + self.fm.get_freq(self.last_index + i)) * self.time_interval
            saw_samples.append(self.fm.get_freq(self.last_index + i))
            phase_samples.append(self.phase + 2 * math.pi * (self.freq + self.fm.get_freq(self.last_index + i)) * self.time_interval * i)
            freq_samples.append((self.freq + self.fm.get_freq(self.last_index + i)))
            samples.append(int(math.floor(sample + 0.5) if sample > 0 else math.ceil(sample - 0.5)))
            #samples.append(sample)
            indices.append(self.last_index + i)


        #self.phase += 2 * math.pi * (self.freq + self.fm.get_freq(self.last_index + size)) * self.time_interval * size
        self.last_index += size

        sign = 1 if self.phase >= 0 else -1
        while not (self.phase < 2 * math.pi and self.phase >= 0):
            self.phase -= sign * 2 * math.pi

        return indices, samples
                        
    def reset(self, phase=0):
        self.last_index = 0
        self.phase = phase