from builtins import print
import numpy


var1 = [0, 1, 2]
var2 = [10]
var3 = [20]


def asd():
    print("v1:", id(var1))


v1 = [0 for i in range(15)]
v2 = [i for i in range(20)]


v3 = v1[0:int(len(v1)/2)] + v2[int((len(v2)/2)):]

print(v3)

a1 = dict()
a1['k1'] = [0, 0]
a1['k2'] = [1, 1]

print(list(a1.keys()))
a2 = numpy.random.choice(list(a1.keys()), size=10)

print(type(a2))

