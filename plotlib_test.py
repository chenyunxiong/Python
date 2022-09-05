from cmath import sin
import numpy
from matplotlib import pyplot

# x = numpy.linspace(-numpy.pi, numpy.pi, 256)
# cosX = numpy.cos(x)
# sinX = numpy.sin(x)

# pyplot.plot(x, cosX, '--', linewidth = 2)
# pyplot.plot(x, sinX)
# pyplot.show()

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = pyplot.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

pyplot.show()