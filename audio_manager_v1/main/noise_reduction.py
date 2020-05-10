# -*- coding: utf-8 -*-

# Copyright (C) 2019 Chris Blackbourn

"""Noise reduction."""

import numpy
import scipy

import main.common as common


class spectrogram_helper:
    def __init__(self, source_pad, spectrogram, stride, sample_rate):
        self.spectrogram = spectrogram
        (self.block_count, dct_width) = spectrogram.shape
        self.stride = stride
 
        window_c = common.get_window_const(dct_width, 'tukey')
 
        for index in range(self.block_count):
            block_index = index * stride
            block = source_pad[block_index:block_index + dct_width] * window_c
#             dct = scipy.fftpack.dct(block)
            dct = scipy.fft.dct(block)
            spectrogram[index] = dct
 
        self.buckets = []
        msw = 50 * sample_rate // stride
        max_spec_width = min(msw, self.block_count)
        division_count = max(int((self.block_count * 1.7) / max_spec_width), 1)
        for i in range(division_count):
            t0 = 0
            if i:
                t0 = (self.block_count - max_spec_width) * \
                    i // (division_count - 1)
            t1 = min(t0 + max_spec_width, self.block_count)
            self.buckets.append((t0, t1))
 
        self.currentBucket = -2
 
    def get_tolerance(self, index):
        qb = (index, index, index)
        q = min(self.buckets, key=lambda x: abs(x[0] + x[1] - 2 * index))
        if self.currentBucket != q:
            self.currentBucket = q
            (t0, t1) = q
            bin_medians = numpy.median(abs(self.spectrogram[t0:t1, ]), axis=0)
            self.tolerance = 4 * \
                numpy.convolve(bin_medians, numpy.ones(8) / 8)[4:-3]
 
        return self.tolerance


# def noise_reduce_dct(source, sample_rate, options):
def noise_reduce_dct(source, sample_rate):
    original_sample_count = source.shape[0]
    dct_width = 2048

    trim_width = int(dct_width / 8)
    stride = dct_width - trim_width * 3

    block_count = (original_sample_count + stride - 1) // stride
    source_pad = numpy.pad(source, (stride, stride * 2), 'reflect')

    #print('Building spectrogram')
    spectrogram = numpy.empty((block_count, dct_width))

    sph = spectrogram_helper(source_pad, spectrogram, stride, sample_rate)

    # anything below bass_cut_off_freq requires specialised techniques
    bass_cut_off_freq = 100
    bass_cut_off_band = bass_cut_off_freq * 2 * dct_width // sample_rate

    spectrogram_trimmed = numpy.empty((block_count, dct_width))
    rms_tab = numpy.empty(block_count)

    for index in range(block_count):
        dct = spectrogram[index]

        mask = numpy.ones_like(dct)
        mask[:bass_cut_off_band] *= 0

        rms_tab[index] = common.rms(dct * mask)

        tolerance = sph.get_tolerance(index)
        for band in range(dct_width):
            if abs(dct[band]) < tolerance[band]:
                mask[band] *= 0.0

        maskCon = 10 * numpy.convolve(mask, numpy.ones(8) / 8)[4:-3]

        maskBin = numpy.where(maskCon > 0.1, 0, 1)
        spectrogram_trimmed[index] = maskBin

    rms_cutoff = numpy.median(rms_tab)

    result_pad = numpy.zeros_like(source_pad)
    for index in range(1, block_count - 1):
        dct = spectrogram[index]

        trim3 = spectrogram_trimmed[index - 1] * \
            spectrogram_trimmed[index] * spectrogram_trimmed[index + 1]
        dct *= (1 - trim3)

        if common.rms(dct) < rms_cutoff:
            continue  # too soft

#         rt = scipy.fftpack.idct(dct) / (dct_width * 2)
        rt = scipy.fft.idct(dct) / (dct_width * 2)

        block_index = index * stride
        result_pad[block_index + trim_width * 1:block_index + trim_width *
                   2] += rt[trim_width * 1:trim_width * 2] * numpy.linspace(0, 1, trim_width)
        result_pad[block_index +
                   trim_width *
                   2:block_index +
                   trim_width *
                   6] = rt[trim_width *
                           2:trim_width *
                           6]  # *numpy.linspace(1,1,stride8*4)
        result_pad[block_index + trim_width * 6:block_index + trim_width *
                   7] = rt[trim_width * 6:trim_width * 7] * numpy.linspace(1, 0, trim_width)

    result = result_pad[stride:stride + original_sample_count]
    return result


# def noise_reduce(source, sample_rate, options={}):
#     return noise_reduce_dct(source, sample_rate, options)

def noise_reduce(source, sample_rate):
    return noise_reduce_dct(source, sample_rate)




