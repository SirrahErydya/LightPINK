import numpy as np
from glue_qt.app.application import GlueApplication
from glue_qt.viewers.image import ImageViewer
from glue.core import Data, DataCollection
from src.som_viewer import SOMDataViewer
# create a GUI session


def show_som(som, layout):
    som_dim = som.shape[0]
    neuron_dim = som.shape[2]
    if layout == 'cartesian-2d':
        img = Data(som=som)
        data_collection = DataCollection([img])
        app = GlueApplication(data_collection=data_collection)
        viewer = app.new_data_viewer(ImageViewer)
        viewer.add_data(img)
        app.start()




