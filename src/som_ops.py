import pink
import math
import numpy as np
from tqdm import tqdm


def train_som(data, som_width, som_height, layout, no_rotations, epochs):
    neuron_dim = int(data.shape[1] / math.sqrt(2.0) * 2.0)
    euclid_dim = int(data.shape[1] * math.sqrt(2.0) / 2.0)
    width = som_width
    height = som_height
    if layout == 'cartesian-2d':
        np_som = np.zeros((width, height, neuron_dim, neuron_dim)).astype(np.float32)
    elif layout == 'hexagonal-2d':
        radius = (width - 1) / 2
        number_of_neurons = int(width * height - radius * (radius + 1))
        np_som = np.random.rand(number_of_neurons, neuron_dim, neuron_dim).astype(np.float32)
    else:
        raise AttributeError("Invalid layout: {0}".format(layout))
    som = pink.SOM(np_som, som_layout=layout)

    trainer = pink.Trainer(som, number_of_rotations=no_rotations, euclidean_distance_dim=euclid_dim,
                           distribution_function=pink.GaussianFunctor(1.1, 0.2))
    print("Start training...")
    for e in range(int(epochs)):
        print("Epoch {0}/{1}".format(e + 1, epochs))
        for point in tqdm(data):
            point = point.astype(np.float32)
            if point.max() > 1:
                point = point / 255
            trainer(pink.Data(point))
    trainer.update_som()
    np_som = np.array(som)
    np.save("test_data/som.npy", np_som)
    return np_som
