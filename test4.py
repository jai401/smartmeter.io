import numpy as np
import matplotlib.pyplot as plt

a = np.array([1,2,17,20,16,3,5,4])

# use a masked array to suppress the values that are too low
a_masked = np.ma.masked_less_equal(a, 15)

# plot the full line
plt.plot(a, 'k')

# plot only the large values
plt.plot(a_masked, 'r', linewidth=2)

# add the threshold value (optional)
#plt.axhline(15, color='k', linestyle='--')
plt.show()
