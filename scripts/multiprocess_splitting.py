# Author : Eoin McLoughlin
import os
import time
import cv2 as cv

import multiprocessing



def process_video_multiprocessing(info):
    """ Takes a video as input and splits that video into a number of frames.
    Args:
        info (Tuple) :  A tuple containing all of the neccessary information needed to split the subset of frames to the correct folder 
                        Made up of: (i, video_path, frame_jump_unit, parent_frame_folder_path)
                        i (int) : The group number of this pool 
                        video_path (String) : The name of the video being split
                        frame_jump_unit (int) : The number of frames each process must split
                        parent_frame_folder_path (String) : The file path to the parent folder where each  process will store their frames

        
    """
    # Extract arguments from tuple
    (group_number, video_path, frame_jump_unit, parent_frame_folder_path) = info
    # Read video file
    vidcap = cv.VideoCapture(video_path)

    vidcap.set(cv.CAP_PROP_POS_FRAMES, frame_jump_unit * group_number)

    # get height, width and frame count of the video
    width, height = (int(vidcap.get(cv.CAP_PROP_FRAME_WIDTH)),
                    int(vidcap.get(cv.CAP_PROP_FRAME_HEIGHT))
                    )

    no_of_frames = int(vidcap.get(cv.CAP_PROP_FRAME_COUNT))
    fps = int(vidcap.get(cv.CAP_PROP_FPS))
    proc_frames = 0

    # Create folder 
    group_folder_name = parent_frame_folder_path + str(group_number) + "/"
    # Create folder to store video frames from this pool
    create_folder(group_folder_name)
    # Keep track of frames in each batch 
    frame_counter = 0
    try:
        while proc_frames < frame_jump_unit:
            ret, frame = vidcap.read()
            if not ret:
                break   

            # write the frame to the correct sub folder
            frame_path = group_folder_name + "{}.jpg".format(frame_counter)
            cv.imwrite(frame_path, frame)
            frame_counter+=1
            proc_frames += 1

    except:
        # Release resources
        vidcap.release()

    # Release resources
    vidcap.release()



def multi_process(num_processes, video_path, frame_jump_unit, parent_frame_folder_path, video_name):

    # Parallel execution of splitting across different cores
    p = multiprocessing.Pool(num_processes)
    p.map(process_video_multiprocessing, [(i, video_path, frame_jump_unit, parent_frame_folder_path) for i in range(num_processes)])


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def multiprocessor_splitting_main(video_path):
    """ The main function used for taking a video and splitting it into frames using multiprocessing
    Args:
        video_path (String) : A string representing the file path to the video Eg "videos/video_to_be_split.mp4"
        
    """
    file_name = video_path.split("/")[1]
    video_frames = "video_frames/"
    video_name = file_name.split(".")[0]
    parent_video_frame_path = video_frames + video_name + "/"
    
    # Create all the neccessary folders
    create_folder(video_frames)
    create_folder(parent_video_frame_path)

    # Get total frame count of the video and number of cores available to use
    cap = cv.VideoCapture(video_path)
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    num_processes = multiprocessing.cpu_count()
    
    # Deciding how many frame each process should deal with each
    frame_jump_unit =  frame_count// num_processes
    # Create a series of processes that will split a certain amount of frames depending on the total number of frames and number of cores available
    multi_process(num_processes, video_path, frame_jump_unit, parent_video_frame_path, video_name)

    return frame_count

if __name__ == "__main__":
    multiprocessor_splitting_main()