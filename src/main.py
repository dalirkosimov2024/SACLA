import tifffile as tiff
import matplotlib.pyplot as plt 

# this is a new edit

path = "/home/dalir/Documents/cdt/japan/script/docs"
name = "1478724-02-shot"

def tif_runner(path, name):

    shot_id = name.split("-")[0]
    shot_number = name.split("-")[1]
    state = name.split("-")[2]

    if state == "ref":
        state = "BEFORE"
    elif state == "pref":
        state = "AFTER"
    elif state == "shot":
        state = "SHOT"

    print(shot_id)
    image = tiff.imread(f"{path}/{name}.tif")

    plt.imshow(image, cmap="plasma")
    plt.colorbar()
    plt.suptitle(f"|  {state}  |  SHOT NUMBER: {shot_number}  |  SHOT ID: {shot_id}  |")
    plt.show()
   

if __name__ == "__main__": 
    tif_runner(path, name)
