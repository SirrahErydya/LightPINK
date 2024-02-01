import numpy as np
from glue_qt.app.application import GlueApplication
from glue_qt.viewers.image import ImageViewer
from glue.core import Data, DataCollection
from src.som_viewer import SOMDataViewer
# create a GUI session


def show_som(som, layout):
    som_dim = som.shape[0]
    neuron_dim = som.shape[2]
    print(som_dim, neuron_dim)
    if layout == 'cartesian-2d':
        #img = Data(som=som.swapaxes(1, 2).reshape(som_dim*neuron_dim, som_dim*neuron_dim))
        img = Data(label="SOM prototypes", som=som)
        data_collection = DataCollection([img])
        app = GlueApplication(data_collection=data_collection)
        viewer = SOMDataViewer(som_dim, som_dim, app.session)
        viewer.register_to_hub(app.session.hub)
        app.add_widget(viewer)
        viewer.add_data(img)
        app.start()




