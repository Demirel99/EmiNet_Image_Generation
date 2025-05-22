import numpy as np
from utils import generate_amplitude, gauss2d, create_circular_mask


def option_2(all_frames, random_fo_same_loc,mask):
    arr_shape = all_frames.shape[1]#
    out_unchanged = all_frames.copy()
    masks_unchanged=mask.copy()

    out = all_frames.copy()
    masks=mask.copy()
    psfs = np.zeros(out.shape, dtype=out.dtype)

    seq_length = all_frames.shape[0]

    all_frame_maxes = []
    all_added_maxes = []
    unique_frames = np.unique(np.random.randint(0, seq_length, random_fo_same_loc))

    condition_met_for_all = False
    loop_counter = 0
    while not condition_met_for_all:
        if loop_counter > 500:  # Check if the loop has iterated over 100 times
          return out_unchanged, masks_unchanged, psfs  # Exit function if true

        # Select rand_x and rand_y for the attempt
        rand_x = np.random.randint(1, 128)
        rand_y = np.random.randint(1, 128)

        temp_all_added_maxes = []
        temp_all_frame_maxes = []
        condition_met_for_all = True  # Assume condition is met, verify next

        for i in unique_frames:
            sigma = np.random.randint(4, 10)
            A = generate_amplitude()#np.random.randint(40,90)

            # Generate the Gaussian point spread function (PSF)
            psf = gauss2d(A, np.zeros([arr_shape, arr_shape]), sigma, [rand_x, rand_y])

            # Temporary output with the new PSF added
            temp_out = all_frames[i] + psf

            # Create a mask to identify the area affected by the PSF
            mat_mask = create_circular_mask(arr_shape, arr_shape, center=[rand_y, rand_x], radius=sigma)

            # Calculate the 0.25 quartile of frame's intensity for pixels > 1
            filtered_frame = all_frames[i][all_frames[i] > 1]
            if len(filtered_frame) > 0:
                quartile_value = np.quantile(filtered_frame, 0.25)
            else:
                quartile_value = np.quantile(all_frames[i], 0.25)  # Fallback to the whole frame if no elements are > 1

            # Check if the mean intensity in the mask area is greater than the quartile value
            if np.mean(all_frames[i][mat_mask]) <= quartile_value:
                condition_met_for_all = False  # Condition not met due to quartile check, break and retry
                break

            # Check if the condition is met for this frame
            added_max = np.max(temp_out[mat_mask])
            frame_max = np.max(all_frames[i])
            temp_all_added_maxes.append(added_max)
            temp_all_frame_maxes.append(frame_max)

            if added_max > frame_max:
                condition_met_for_all = False  # Additional condition not met, break and retry
                break

        if condition_met_for_all:
            # If condition is met for all frames, update the final arrays and output frames
            all_added_maxes = temp_all_added_maxes
            all_frame_maxes = temp_all_frame_maxes
            for idx, frame_i in enumerate(unique_frames):
                out[frame_i] += psf  # Update with the last psf calculated, assuming it's valid for all
                # if np.all(masks[frame_i] == 0):
                #   masks[frame_i] = mat_mask
                # else:
                #   masks[frame_i] = np.logical_or(masks[frame_i], mat_mask).astype(int)

                if np.all(masks[frame_i, 1] == 0):  # Check if the second channel is all zeros
                    masks[frame_i, 1] = mat_mask  # If so, directly assign the mask
                else:
                    masks[frame_i, 1] = np.logical_or(masks[frame_i, 1], mat_mask).astype(int)  # Otherwise, combine masks
        loop_counter += 1
    # all_frame_maxes = np.array(all_frame_maxes)
    # all_added_maxes = np.array(all_added_maxes)

    return out,masks,psfs