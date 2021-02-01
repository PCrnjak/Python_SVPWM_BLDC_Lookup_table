import math
import numpy
import matplotlib.pyplot as plt
from scipy import interpolate
import csv

numpy.set_printoptions(suppress=True)

# Change these values depending on you motor and encoder 
encoder_res = 1024
motor_poles = 21 # for 24N22P use 11 for 36N42P use 21 for 11N14P use 7

# Variable to adjust peak value of saddle to number we want 
# Usually peak must be 2 * A
var = 1039
# Peak value of saddle = A * 2
# Value is determined by pwm resolution on you MCU
# Here 2*A would be 100% duty cycle in our MCU
A = 900

sample = 1000
step = (2 * math.pi) / (sample)

a1 = list(numpy.arange(0,2*math.pi,step))
a1.append(math.pi)

sin1 = [var * math.sin(n) for n in a1]    
sin2 = [var * math.sin(n-((2*math.pi)/3)) for n in a1] 
sin3 = [var * math.sin(n+((2*math.pi)/3)) for n in a1] 

phase = []

for n in range(sample+1):
    temp = (min(sin1[n],sin2[n],sin3[n]) + max(sin1[n],sin2[n],sin3[n])) /2;
    phase.append(sin1[n] - temp + A )

n = int(motor_poles)
print(f"We need {n} periods for whole rotation")

y = phase * n

#plt.plot(y)
#plt.show()

x = range(1,n*len(phase)+1,1)
print(f"We have {len(x)} elements in old wave")
new_x = numpy.linspace(min(x),max(x),encoder_res)
print(f"We have {len(new_x)} elements in new wave")

set_interp = interpolate.interp1d(x, y, kind = 'linear')
new_y = set_interp(new_x)
new_y = new_y.astype(int)

# get last element of array and save it to new_y_last
new_y_last = new_y[len(new_y)-1]

# Plot resized wave
plt.plot(new_y)
plt.show()

# delete last element of array from our array
new_y = numpy.delete(new_y, -1)

# Edit YOUR_PATH to path you want to save your file:
# Example: C:\Users\Name\Desktop\my_file_2.csv

# Save array witout last element to csv file
numpy.savetxt(r'YOUR_PATH', new_y, newline = ',',fmt= '%-1.1d')
# Save last element to csv file (this remove last comma)
file = open(r'YOUR_PATH','a')
file.write(str(new_y_last))
file.close()
