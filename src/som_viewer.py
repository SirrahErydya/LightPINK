import os

import numpy as np
from astropy.visualization.wcsaxes import WCSAxesSubplot
from glue.viewers.common.layer_artist import LayerArtist
from glue.viewers.image.viewer import MatplotlibImageMixin
from glue.viewers.matplotlib.viewer import MatplotlibViewerMixin

from qtpy.QtWidgets import QWidget, QVBoxLayout, QRadioButton

from glue_qt.config import qt_client
from glue.core.data_combo_helper import ComponentIDComboHelper

from echo import CallbackProperty, SelectionCallbackProperty
from echo.qt import (connect_checkable_button,
                                   autoconnect_callbacks_to_qt)

from glue.viewers.image.layer_artist import ImageLayerArtist
from glue.viewers.image.state import ImageViewerState, ImageLayerState
from glue_qt.viewers.image.data_viewer import ImageViewer
from glue_qt.viewers.matplotlib.widget import MplWidget
from glue.viewers.image.frb_artist import imshow
from glue.viewers.image.composite_array import CompositeArray

from glue_qt.utils import load_ui

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.image import AxesImage


class SOMViewerState(ImageViewerState):
    def __init__(self, **kwargs):
        super(SOMViewerState, self).__init__(**kwargs)


class SOMLayerState(ImageLayerState):
    def __init__(self):
        super(SOMLayerState, self).__init__()


class SOMLayerArtist(LayerArtist):

    _layer_state_cls = ImageLayerState

    def __init__(self, axs, *args, **kwargs):
        super(SOMLayerArtist, self).__init__(*args, **kwargs)
        self.axs = axs
        self.images = []
        for i in range(len(self.axs)):
            image = ImageLayerArtist(self.axs[i], *args, **kwargs)
            self.images.append(image)

class SOMViewerStateWidget(QWidget):

    def __init__(self, viewer_state=None, session=None):

        super(SOMViewerStateWidget, self).__init__()

        self.ui = load_ui('viewer_state.ui', self,
                          directory=os.path.dirname(__file__))

        self.viewer_state = viewer_state
        #self._connections = autoconnect_callbacks_to_qt(self.viewer_state, self.ui)


class SOMLayerStateWidget(QWidget):

    def __init__(self, layer_artist):

        super(SOMLayerStateWidget, self).__init__()

        self.view_map = QRadioButton("View Map")
        self.view_img = QRadioButton("View single image")
        layout = QVBoxLayout()
        layout.addWidget(self.view_map)
        layout.addWidget(self.view_img)
        self.setLayout(layout)

        self.layer_state = layer_artist.state
        #self._connection = connect_checkable_button(self.layer_state, 'fill', self.checkbox)


class SOMWidget(MplWidget):
    def __init__(self):
        super(SOMWidget, self).__init__()


class SOMDataViewer(ImageViewer):

    LABEL = 'SOM viewer'
    _state_cls = SOMViewerState
    #_options_cls = SOMViewerStateWidget
    _layer_style_widget_cls = SOMLayerStateWidget
    _data_artist_cls = SOMLayerArtist
    _subset_artist_cls = SOMLayerArtist

    def __init__(self, *args, **kwargs):
        super(SOMDataViewer, self).__init__(*args, **kwargs)
        self.mpl_widget = SOMWidget()
        self.setCentralWidget(self.mpl_widget)
        self.central_widget = self.mpl_widget

        self.figure = self.create_plot()
        self.axs = self.figure.axes
        self.setup_callbacks()
        self.central_widget.resize(1500, 1500)
        self.resize(self.central_widget.size())

    def setup_callbacks(self):
        self._wcs_set = False
        self._changing_slice_requires_wcs_update = None
        self.state.add_callback('x_att', self._set_wcs)
        self.state.add_callback('y_att', self._set_wcs)
        self.state.add_callback('slices', self._on_slice_change)
        self.state.add_callback('reference_data', self._set_wcs, echo_old=True)

        for i in range(len(self.axs)):
            ax = self.axs[i]
            ax.set_adjustable('datalim')
            ax._composite = CompositeArray()
            ax._composite_image = imshow(ax, ax._composite, aspect='auto',
                                            origin='lower', interpolation='nearest')
        self._set_wcs()

    def get_data_layer_artist(self, layer=None, layer_state=None):
        return self.get_layer_artist(self._data_artist_cls, layer=layer, layer_state=layer_state)

    def get_layer_artist(self, cls, layer=None, layer_state=None):
        return cls(self.axs, self.state, layer=layer, layer_state=layer_state)

    def create_plot(self):
        figure = self.central_widget.canvas.fig
        for i in range(25):
            axes = WCSAxesSubplot(figure, 5, 5, i+1)
            axes.axis('off')
            figure.add_axes(axes)
        plt.tight_layout()
        return figure

qt_client.add(SOMDataViewer)