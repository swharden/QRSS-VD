import numpy

a=numpy.zeros((512,200))
b=numpy.zeros((512,1))+1
c=numpy.hstack((a,b))
print c
