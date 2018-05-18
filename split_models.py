from data_helpers import split_model_file
import sys

def main(argv):
    """
    Split the models in smaller files for avoiding LFS issues.
    It should be run before every commit.
    """
    for mod in  ["models/event-types/model.ckpt", "models/event-related/model.ckpt", "models/info-types/model.ckpt"]:
        split_model_file(mod, remove=True)
      

if __name__ == "__main__":
    main(sys.argv)
