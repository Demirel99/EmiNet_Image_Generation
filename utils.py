import numpy as np
def generate_amplitude():
  # Set the mean and standard deviation
  mean = (255 + 0) / 2  # Center of the range 40 to 90
  std_dev = (255 - 0)/6  # A smaller standard deviation, adjust as needed

  # Generate a random number from a normal distribution
  random_number = np.random.normal(mean, std_dev)

  # Ensure the numbers are within the range 40 to 90
  random_number = np.clip(random_number, 40, 250)

  return random_number

def gauss2d(A,mat, sigma, center):
    gsize = np.array(mat).shape
    R,C =np.mgrid[0:gsize[0], 0:gsize[1]]
    mat = gaussC(A,R,C, sigma, center)
    return np.float32(mat)

def gaussC(A,x, y, sigma, center):
    xc = center[0]
    yc = center[1]
    exponent = ((x-xc)**2 + (y-yc)**2)/(2*sigma)
    val       = A*(np.exp(-exponent))
    return val

def create_circular_mask(h, w, center=None, radius=None):

    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask

def generate_amplitude():
  # Set the mean and standard deviation
  mean = (255 + 0) / 2  # Center of the range 40 to 90
  std_dev = (255 - 0)/6  # A smaller standard deviation, adjust as needed

  # Generate a random number from a normal distribution
  random_number = np.random.normal(mean, std_dev)

  # Ensure the numbers are within the range 40 to 90
  random_number = np.clip(random_number, 40, 250)

  return random_number

def generate_random_bac_number():
  # mean = 8
  # std_deviation = 2  # Adjust this value to control the spread of the distribution

  # # Generate random real numbers from the normal distribution
  # real_values = np.random.normal(mean, std_deviation)

  # Round the real numbers to the nearest integer
  integer_values = np.random.randint(0,50)#np.abs(np.round(real_values).astype(int))

  return integer_values