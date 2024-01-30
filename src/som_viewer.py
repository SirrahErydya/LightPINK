import os

import numpy as np

from qtpy.QtWidgets import QWidget, QVBoxLayout, QCheckBox

from glue_qt.config import qt_client
from glue.core.data_combo_helper import ComponentIDComboHelper

from echo import CallbackProperty, SelectionCallbackProperty
from echo.qt import (connect_checkable_button,
                                   autoconnect_callbacks_to_qt)

from glue.viewers.matplotlib.layer_artist import MatplotlibLayerArtist
from glue.viewers.matplotlib.state import MatplotlibDataViewerState, MatplotlibLayerState
from glue_qt.viewers.matplotlib.data_viewer import MatplotlibDataViewer

from glue_qt.utils import load_ui

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.image import AxesImage


class SOMViewerState(MatplotlibDataViewerState):

    x_att = SelectionCallbackProperty(docstring='The attribute to use on the x-axis')
    y_att = SelectionCallbackProperty(docstring='The attribute to use on the y-axis')

    def __init__(self, *args, **kwargs):
        super(SOMViewerState, self).__init__(*args, **kwargs)
        self._x_att_helper = ComponentIDComboHelper(self, 'x_att')
        self._y_att_helper = ComponentIDComboHelper(self, 'y_att')
        self.add_callback('layers', self._on_layers_change)
        self.add_callback('x_att', self._on_attribute_change)
        self.add_callback('y_att', self._on_attribute_change)

    def _on_layers_change(self, value):
        self._x_att_helper.set_multiple_data(self.layers_data)
        self._y_att_helper.set_multiple_data(self.layers_data)

    def _on_attribute_change(self, value):
        if self.x_att is not None:
            self.x_axislabel = self.x_att.label
        if self.y_att is not None:
            self.y_axislabel = self.y_att.label


class SOMLayerState(MatplotlibLayerState):
    fill = CallbackProperty(False, docstring='Whether to show the markers as filled or not')


class SOMLayerArtist(MatplotlibLayerArtist):

    _layer_state_cls = SOMLayerState

    def __init__(self, axes, *args, **kwargs):

        super(SOMLayerArtist, self).__init__(axes, *args, **kwargs)

        #self.artist = self.axes.plot([], [], 'o', mec='none')[0]
        self.artist = AxesImage(self.axes)
        self.axes.imshow(self.artist)
        self.mpl_artists.append(self.artist)

        self.state.add_callback('visible', self._on_visual_change)
        self.state.add_callback('zorder', self._on_visual_change)
        self.state.add_callback('alpha', self._on_visual_change)

        self._viewer_state.add_callback('x_att', self._on_attribute_change)
        self._viewer_state.add_callback('y_att', self._on_attribute_change)

    def _on_visual_change(self, value=None):

        self.artist.set_visible(self.state.visible)
        self.artist.set_zorder(self.state.zorder)
        self.artist.set_alpha(self.state.alpha)

        self.redraw()

    def _on_attribute_change(self, value=None):

        if self._viewer_state.x_att is None or self._viewer_state.y_att is None:
            return

        x = self.state.layer[self._viewer_state.x_att]
        y = self.state.layer[self._viewer_state.y_att]

        self.artist.set_data(x)

        self.axes.set_xlim(np.nanmin(x), np.nanmax(x))
        self.axes.set_ylim(np.nanmin(y), np.nanmax(y))

        self.redraw()

    def update(self):
        self._on_attribute_change()
        self._on_visual_change()


class SOMViewerStateWidget(QWidget):

    def __init__(self, viewer_state=None, session=None):

        super(SOMViewerStateWidget, self).__init__()

        self.ui = load_ui('viewer_state.ui', self,
                          directory=os.path.dirname(__file__))

        self.viewer_state = viewer_state
        self._connections = autoconnect_callbacks_to_qt(self.viewer_state, self.ui)


class SOMLayerStateWidget(QWidget):

    def __init__(self, layer_artist):

        super(SOMLayerStateWidget, self).__init__()

        self.checkbox = QCheckBox('Fill markers')
        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        self.setLayout(layout)

        self.layer_state = layer_artist.state
        self._connection = connect_checkable_button(self.layer_state, 'fill', self.checkbox)


class SOMDataViewer(MatplotlibDataViewer):

    LABEL = 'SOM viewer'
    _state_cls = SOMViewerState
    _options_cls = SOMViewerStateWidget
    _layer_style_widget_cls = SOMLayerStateWidget
    _data_artist_cls = SOMLayerArtist
    _subset_artist_cls = SOMLayerArtist

    def __init__(self, *args, **kwargs):
        super(SOMDataViewer, self).__init__(*args, **kwargs)



qt_client.add(SOMDataViewer)