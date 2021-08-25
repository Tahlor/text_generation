import numpy as np
from timeit import default_timer as timer
import multiprocessing
a = np.random.random((256, 256))
b = np.random.random((100, 256, 256))

start = timer()
for i in range(10):
    np.fft.fft2(a)
end = timer()
print("np.fft.fft2, 1 slice", (end - start)/10)

start = timer()
for i in range(10):
     bf=np.fft.fftn(b, axes=(1, 2,))
end = timer()
print("np.fft.fftn, 100 slices", (end - start)/10)
print("bf[3,42,42]",bf[3,42,42])


import pyfftw

aa = pyfftw.empty_aligned((256, 256), dtype='float64')
af= pyfftw.empty_aligned((256, 129), dtype='complex128')
bb = pyfftw.empty_aligned((100,256, 256), dtype='float64')
bf= pyfftw.empty_aligned((100,256, 129), dtype='complex128')
cpus = multiprocessing.cpu_count()
cpus = 1

print('number of threads:' , cpus)
fft_object_a = pyfftw.FFTW(aa, af,axes=(0,1), flags=('FFTW_MEASURE',), direction='FFTW_FORWARD',threads=cpus)

fft_object_b = pyfftw.FFTW(bb, bf,axes=(1,2),flags=('FFTW_MEASURE',), direction='FFTW_FORWARD',threads=cpus)


aa=a
bb=b
start = timer()
for i in range(10):
    fft_object_a(aa)
end = timer()
print("pyfftw, 1 slice",(end - start)/10)

start = timer()
for i in range(10):
    fft_object_b(bb)
end = timer()
print("pyfftw, 100 slices", (end - start)/10)
print("bf[3,42,42]",bf[3,42,42])