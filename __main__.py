import argparse
from src.som_ops import train_som
from src.visualization import show_som
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize and interact with a big data set via PINK SOMs ")
    parser.add_argument("dataset", metavar='d', type=str, help="Path to the dataset to visualize.")
    parser.add_argument("--som", type=str, help="Path to the SOM, if one is already trained")
    parser.add_argument("--width", metavar='w', type=int, default=5,
                        help="Width of the SOM to train. (Default: 5")
    parser.add_argument("--height", metavar='h', type=int, default=5,
                        help="Height of the SOM to train. (Default: 5")
    parser.add_argument("--layout", metavar='l', type=str, default="cartesian-2d",
                        help="The layout of the SOM to train. (Default: cartesian-2d)")
    parser.add_argument("--rot", metavar='r', type=int, default=1,
                        help="Number of rotations in the SOM to train. (Default: 1)")
    parser.add_argument("--epochs", metavar='e', type=int, default=1,
                        help="Number of training epochs. (Default: 1)")
    args = parser.parse_args()

    data = np.load(args.dataset)

    if args.som is None:
        som = train_som(data, args.width, args.height, args.layout, args.rot, args.epochs)
    else:
        som = np.load(args.som)
    show_som(som, args.layout)
