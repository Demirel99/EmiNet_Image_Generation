import numpy as np
from skimage.util import view_as_windows
from motion_pattern_1 import option_1
from motion_pattern_2 import option_2
from motion_pattern_3 import option_3
from utils import generate_random_bac_number
import matplotlib.pyplot as plt


num_frames = 33
no_bac_image_seq=np.load("C:\\Users\\Mehmet_Postdoc\\Desktop\\python_set_up_code\\EmiNet_image_generation_material\\data0413.npy")

tiles=view_as_windows(no_bac_image_seq, (33,128,128))

shape_0_rand=np.random.randint(0, tiles.shape[0])
shape_1_rand=np.random.randint(0, tiles.shape[1])
shape_2_rand=np.random.randint(0, tiles.shape[2])
selected_tile=tiles[shape_0_rand][shape_1_rand][shape_2_rand]

all_frames = np.float32(selected_tile)

background_save=np.float32(selected_tile)

combined_mask = np.zeros((33,3,128,128), dtype=bool)#np.zeros_like(all_frames, dtype=bool)  # Initialize masks

num_bac_real=generate_random_bac_number()
print(num_bac_real)

for i in range(num_bac_real):

  chance_same_location = 0.2

  start_frame=np.random.randint(0, num_frames+1)

  end_frame=np.random.randint(start_frame, num_frames+1)

  random_fo_same_loc=np.random.randint(0, num_frames+1)

  if (end_frame-start_frame>1):
    if (np.random.random() < chance_same_location):
      all_frames,combined_mask,_=option_2(all_frames, random_fo_same_loc,combined_mask)
    else:
      all_frames,combined_mask,_= option_1(start_frame, end_frame, all_frames, combined_mask)

number_of_error=np.random.randint(1, 20)
for z in range(number_of_error):
  all_frames,combined_mask,_=option_3(all_frames,combined_mask)


comb_arr=np.transpose(combined_mask, (0,2, 3, 1))

for i in range(32):
  print(i)
  plt.imshow(all_frames[i])
  plt.show()
  plt.imshow(np.float32(comb_arr[i]))
  plt.show()
