import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def import_json(json_path):
    """Loads data from a JSON file into a readable JSON object.
    Args: 
        json_path (JSON): A JSON file containing key point information.
    
    Returns:
        jump_height (Int): The height the user has jumped in centimeters.
    """
    with open(json_path, "r") as f:
        json_data = json.load(f)

    return json_data


# share_info, historical_data = get_historical_data(sys.argv[1])

def display_graph(dists):

    # Colouring lines 
    plt.plot(dists, color = 'magenta')
    # plt.plot(dists2, color = 'green')

    # #plt.savefig(save_path + "/{}.png".format(ref_code))
    # green = mpatches.Patch(color='green', label='leg angles')
    # magenta = mpatches.Patch(color='magenta', label='Spine angles')
    # plt.legend(handles=[green, magenta], bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0)
    plt.show()
    plt.close()


def display_graph_two(dists, dists2):
    # Colouring lines 
    plt.plot(dists, color = 'magenta')
    plt.plot(dists2, color = 'green')

    # #plt.savefig(save_path + "/{}.png".format(ref_code))
    magenta = mpatches.Patch(color='magenta', label='Arg 1')
    green = mpatches.Patch(color='green', label='Arg 2')
    plt.legend(handles=[green, magenta], bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0)
    plt.show()
    plt.close()


def create_csv(df, path, name):
    print("Creating ", name)
    file_path = path + name
    if os.path.exists(file_path):
        os.remove(file_path)
    df.to_csv(file_path)
    return
