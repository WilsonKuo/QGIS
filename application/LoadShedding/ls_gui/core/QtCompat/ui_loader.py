import os

if os.environ['QT_API'].startswith('pyside'):
    # Originally from
    # https://github.com/ros-visualization/python_qt_binding/blob/kinetic-devel/src/python_qt_binding/binding_helper.py
    def _load_ui(ui_file, base_instance=None, custom_widgets=None):
        import sys
        # TODO: fix for PySide2
        from PySide.QtUiTools import QUiLoader
        from PySide.QtCore import QMetaObject

        class CustomUiLoader(QUiLoader):
            class_aliases = {
                'Line': 'QFrame',
            }

            def __init__(self, base_instance=None, custom_widgets=None):
                super(CustomUiLoader, self).__init__(base_instance)
                self._base_instance = base_instance
                self._custom_widgets = custom_widgets or {}

            def createWidget(self, class_name, parent=None, name=''):
                # don't create the top-level widget, if a base instance is set
                if self._base_instance and not parent:
                    return self._base_instance

                if class_name in self._custom_widgets:
                    widget = self._custom_widgets[class_name](parent)
                else:
                    widget = QUiLoader.createWidget(self, class_name, parent, name)

                if str(type(widget)).find(self.class_aliases.get(class_name, class_name)) < 0:
                    sys.modules['QtCore'].qDebug(str(
                        'PySide.loadUi(): could not find widget class "%s", defaulting to "%s"' % (
                            class_name, type(widget))))

                if self._base_instance:
                    setattr(self._base_instance, name, widget)

                return widget

        loader = CustomUiLoader(base_instance, custom_widgets)
        ui = loader.load(ui_file)
        QMetaObject.connectSlotsByName(ui)
        return ui

elif os.environ['QT_API'] == 'pyqt5':
    def _load_ui(ui_file, base_instance=None, custom_widgets=None):
        from PyQt5 import uic
        return uic.loadUi(ui_file, base_instance)
else:
    def _load_ui(ui_file, base_instance=None, custom_widgets=None):
        from PyQt4 import uic
        return uic.loadUi(ui_file, base_instance)


def qt_load_ui(ui_file, base_instance=None, custom_widgets=None):
    """
    Load a "ui" file created by Qt Designer at runtime. This is an alternative
    to compiling to a Python module (which normally would import either PySide
    or PyQt directly instead of using this compatibility library).

    PyQt4's uic says it takes "the file name or file-like object containing the .ui file".
    It works with pkg_resources.resource_stream (but not directly with pkgutil.get_data).
    Currently our PySide version only takes filenames; to take something else, we'd need
    to get it into some subclass of QIODevice.

    :type uifile: str
    :param uifile: Absolute path of .ui file
    :type baseinstance: QWidget
    :param baseinstance: the optional instance of the Qt base class.
                         If specified then the user interface is created in
                         it. Otherwise a new instance of the base class is
                         automatically created.
    :type custom_widgets: dict of {str:QWidget}
    :param custom_widgets: Class name and type of the custom classes used
                           in uifile if any. This can be None if no custom
                           class is in use. (Note: this is only necessary
                           for PySide, see
                           http://answers.ros.org/question/56382/what-does-python_qt_bindingloaduis-3rd-arg-do-in-pyqt-binding/
                           for more information)
    """
    return _load_ui(ui_file, base_instance, custom_widgets)
