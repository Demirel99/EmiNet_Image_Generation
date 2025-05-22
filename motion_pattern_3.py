import numpy as np
from utils import generate_amplitude, gauss2d, create_circular_mask

def option_3(all_frames,mask):
    background_unchanged = all_frames.copy()
    masks_unchanged=mask.copy()

    background_t = all_frames.copy()
    psfs = np.zeros(background_t.shape, dtype=background_t.dtype)

    arr_size = background_t.shape[1]
    rand_x = np.random.randint(1, 128)
    rand_y = np.random.randint(1, 128)
    sigma = np.random.randint(4, 10)
    mat_mask = create_circular_mask(arr_size, arr_size, center=[rand_y, rand_x], radius=sigma)

    frame_with_psf = np.random.randint(0, 33)
    # print(frame_with_psf)

    filtered_frame = background_t[frame_with_psf][background_t[frame_with_psf] > 1]
    if len(filtered_frame) > 0:
        quartile_value = np.quantile(filtered_frame, 0.25)
    else:
        quartile_value = np.quantile(background_t[frame_with_psf], 0.25)
    loop_counter=0
    while True:
        if loop_counter > 100:  # Check if the loop has iterated over 100 times
            return background_unchanged, masks_unchanged, psfs  # Exit function if true
        if np.mean(background_t[frame_with_psf][mat_mask]) > quartile_value:
            A = generate_amplitude()#np.random.randint(40,90)
            psf = gauss2d(A, np.zeros([arr_size, arr_size]), sigma, [rand_x, rand_y])
            out = background_t[frame_with_psf] + psf
            while np.max(out[mat_mask]) > np.max(background_t[frame_with_psf]):
                if loop_counter > 100:  # Check if the loop has iterated over 100 times
                  return background_unchanged, masks_unchanged, psfs  # Exit function if true
                A = np.random.randint(40,90)#generate_amplitude()#
                psf = gauss2d(A, np.zeros([arr_size, arr_size]), sigma, [rand_x, rand_y])
                out = background_t[frame_with_psf] + psf
                loop_counter += 1
            break
        else:
            rand_x = np.random.randint(1, 128)
            rand_y = np.random.randint(1, 128)
            sigma = np.random.randint(4, 10)
            mat_mask = create_circular_mask(arr_size, arr_size, center=[rand_y, rand_x], radius=sigma)
        loop_counter += 1

    background_t[frame_with_psf] = out
    psfs[frame_with_psf] = psf
    return background_t, mask, psfs