import numpy as np
from utils import generate_amplitude, gauss2d, create_circular_mask

def option_1(start_frame, end_frame, background, mask):
    # Initialize the PSFs array with the same shape as background_t, filled with zeros
    background_unchanged = background.copy()
    masks_unchanged=mask.copy()
    background_t = background.copy()
    masks=mask.copy()
    psfs = np.zeros(background_t.shape, dtype=background_t.dtype)

    arr_size = background_t.shape[1]
    rand_x = np.random.randint(1, 128)
    rand_y = np.random.randint(1, 128)
    sigma = np.random.randint(4, 10)
    mat_mask = create_circular_mask(arr_size, arr_size, center=[rand_y, rand_x], radius=sigma)

    for k in range(start_frame, end_frame):

        filtered_frame = background_t[k][background_t[k] > 1]
        if len(filtered_frame) > 0:  # Ensure there are elements greater than 1
            quartile_value = np.quantile(filtered_frame, 0.25)
        else:
            quartile_value = np.quantile(background_t[k], 0.25)  # Fallback to the whole frame if no elements are > 1

        if k == start_frame:
            loop_counter = 0
            while True:
                if loop_counter > 100:  # Check if the loop has iterated over 100 times
                    return background_unchanged, masks_unchanged, psfs  # Exit function if true
                if np.mean(background_t[k][mat_mask]) > quartile_value:
                    A = generate_amplitude()#np.random.randint(40, 90)
                    psf = gauss2d(A, np.zeros([arr_size, arr_size]), sigma, [rand_x, rand_y])
                    out = background_t[k] + psf
                    # masks[k] = mat_mask  # Update the mask for this frame
                    if np.all(masks[k,0] == 0):
                      masks[k,0] = mat_mask
                    else:
                      masks[k,0] = np.logical_or(masks[k,0], mat_mask).astype(int)
                    psfs[k] = psf  # Save the PSF for this frame
                    out_rand_x = rand_x
                    out_rand_y = rand_y

                    while np.max(out[mat_mask]) > np.max(background_t[k]):#### Make changes for this while loop #####
                        if loop_counter > 100:  # Check inside nested loop
                            return background_unchanged, masks_unchanged, psfs  # Exit function if loop iteration exceeds 100
                        A = generate_amplitude()#np.random.randint(40, 90)
                        psf = gauss2d(A, np.zeros([arr_size, arr_size]), sigma, [rand_x, rand_y])
                        out = background_t[k] + psf
                        loop_counter += 1

                    break
                else:
                    rand_x = np.random.randint(1, 128)
                    rand_y = np.random.randint(1, 128)
                    sigma = np.random.randint(4, 10)
                    mat_mask = create_circular_mask(arr_size, arr_size, center=[rand_y, rand_x], radius=sigma)
                loop_counter += 1
        else:
            angle = np.random.uniform(0, 2 * np.pi)
            displacement = np.random.uniform(0, 8)
            delta_x = int(displacement * np.cos(angle))
            delta_y = int(displacement * np.sin(angle))
            new_x = out_rand_x + delta_x
            new_y = out_rand_y + delta_y

            if 0 <= new_x < arr_size and 0 <= new_y < arr_size:
                rand_x = new_x
                rand_y = new_y

            mat_mask = create_circular_mask(arr_size, arr_size, center=[rand_y, rand_x], radius=sigma)
            loop_counter = 0
            while True:
                if loop_counter > 100:  # Check if the loop has iterated over 100 times
                    return background_unchanged, masks_unchanged, psfs  # Exit function if true
                if np.mean(background_t[k][mat_mask]) > quartile_value:
                    A = generate_amplitude()#np.random.randint(40, 90)
                    psf = gauss2d(A, np.zeros([arr_size, arr_size]), sigma, [rand_x, rand_y])
                    out = background_t[k] + psf

                    if np.all(masks[k,0] == 0):
                      masks[k,0] = mat_mask
                    else:
                      masks[k,0] = np.logical_or(masks[k,0], mat_mask).astype(int)
                    psfs[k] = psf  # Save the PSF for this frame
                    out_rand_x = rand_x
                    out_rand_y = rand_y
                    while np.max(out[mat_mask]) > np.max(background_t[k]):#### Make changes for this while loop #####
                        if loop_counter > 100:  # Check inside nested loop
                            return background_unchanged, masks_unchanged, psfs  # Exit function if loop iteration exceeds 100
                        A = generate_amplitude()#np.random.randint(40, 90)
                        psf = gauss2d(A, np.zeros([arr_size, arr_size]), sigma, [rand_x, rand_y])
                        out = background_t[k] + psf
                        loop_counter += 1
                    break
                else:
                    angle = np.random.uniform(0, 2 * np.pi)
                    displacement = np.random.uniform(0, 8)
                    delta_x = int(displacement * np.cos(angle))
                    delta_y = int(displacement * np.sin(angle))
                    new_x = out_rand_x + delta_x
                    new_y = out_rand_y + delta_y

                    if 0 <= new_x < arr_size and 0 <= new_y < arr_size:
                        rand_x = new_x
                        rand_y = new_y

                    sigma = np.random.randint(4, 10)
                    mat_mask = create_circular_mask(arr_size, arr_size, center=[rand_y, rand_x], radius=sigma)
                loop_counter += 1

        background_t[k] = out

    return background_t, masks, psfs