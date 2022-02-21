#!/usr/bin/python3
# coding=utf-8
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Darren Liang, Stephen Hung'


import os
import sys
import datetime
import platform
import logging
import logging.handlers

from core.acsQt                   import labels
from core.QtCompat.QtWidgets      import QAction
from core.QtCompat                import QtWidgets, QtGui, QtCore, Slot, Qt
from core.QtCompat.QtCore         import (PYQT_VERSION_STR, QT_VERSION_STR, QSettings)

from core.MyWidgets.application       import create_q_application
from core.OracleInterface   import OracleInterface

from view.uf             import UFTableView
from view.xref           import XREFTableView
from view.groups         import GroupsTableView
from view.configuration  import ConfigurationTableView

from model.uf            import UFTableModel
from model.xref          import XREFTableModel
from model.groups        import GroupsTableModel
from model.configuration import ConfigurationTableModel

from dialog.mode0 import mode0_ExecDialog, mode0_StopDialog
from dialog.mode1 import mode1_ExecDialog, mode1_StopDialog
from dialog.mode2 import mode2_ExecDialog, mode2_StopDialog
from dialog.mode3 import mode3_ExecDialog

from collections               import OrderedDict
from delegate.combobox  import ComboBoxDelegate
from delegate.spinbox   import SpinBoxDelegate

from version     import __version__
from widgets     import DockWidget, GroupsWidget, FeederWidget, SubstationWidget, \
                        FromDateWidget, ToDateWidget, ExecButtonWidget, StopButtonWidget, \
                        LightWidget

from factory import ThreadPool, Worker
from export  import ExportTable


TITLE = "LS_APP" 
LOG_FILENAME = 'adms_report.log'
LOG_FORMAT   = '%(asctime)s [%(process)d] %(levelname)s %(name)s: %(message)s'

USER  = os.getenv('ORACLE_USER', 'acs_das')
PSWD  = os.getenv('ORACLE_PW'  , 'acs_das')
TNS   = os.getenv('ORACLE_DBSTRING', 'emsa')
PRISMdb = OracleInterface(USER, PSWD, TNS)

DEFAULT_REFRESH_INTERVAL_MILLIS = 2000
COPYRIGHT_YEAR = 2022
DEFAULT_WIDTH  = 1300
DEFAULT_HEIGHT = 800

logger = logging.getLogger(__name__)

# LOCKFLAG = ('Enable(0)', 'Disable(1)')
# STATE    = ('Open(0)', 'Close(1)')
# TOOGLE   = ('ON(0)', 'OFF(1)')

LOCKFLAG = ('Enable(0)', 'Disable(1)')
STATE    = ('Open(0)'  , 'Close(1)')
TOOGLE   = ('ON(0)'    , 'OFF(1)')

class LSApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(LSApp, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        #=====================================================================
        # Configuration Settings
        #=====================================================================
        self.settings   = QSettings("acstw", TITLE)
        self.threadpool = ThreadPool()

        #=====================================================================
        # models
        #=====================================================================
        self.uf_model     = UFTableModel(self)
        self.xref_model   = XREFTableModel(self)
        self.groups_model = GroupsTableModel(self)
        self.config_model = ConfigurationTableModel(self)
        self.xref_model.enable_refresh(True)
        self.groups_model.enable_refresh(True)

        #=====================================================================
        # Views
        #=====================================================================
        self.uf_view = UFTableView(self)
        self.uf_view.setModel(self.uf_model)
        self.font_setting(self.uf_view, 11)
        self.uf_view.setItemDelegateForColumn(self.uf_model._col_state   , ComboBoxDelegate(self, TOOGLE))        
        self.uf_view.setItemDelegateForColumn(self.uf_model._col_lockflag, ComboBoxDelegate(self, LOCKFLAG))      

        self.xref_view = XREFTableView(self)
        self.xref_view.setModel(self.xref_model)
        self.font_setting(self.xref_view, 11)
        self.xref_view.setItemDelegateForColumn(self.xref_model._col_lslockflag, ComboBoxDelegate(self, LOCKFLAG))        
        self.xref_view.setItemDelegateForColumn(self.xref_model._col_f_state   , ComboBoxDelegate(self, STATE))        

        self.groups_view = GroupsTableView(self)
        self.groups_view.setModel(self.groups_model)
        self.font_setting(self.groups_view, 11)

        self.config_view = ConfigurationTableView(self)
        self.config_view.setModel(self.config_model)
        self.font_setting(self.config_view, 11)
        self.config_view.setItemDelegateForColumn(self.config_model._col_value, SpinBoxDelegate(self))       
        self.config_view.model().dataChanged.connect(self.config_model.re_init) 

        #=====================================================================
        # xref options box
        #=====================================================================
        xref_option_box = QtWidgets.QHBoxLayout()
        state_light_box = QtWidgets.QHBoxLayout()
        self.groups_combobox = GroupsWidget(self)
        self.feeder_lineedit = FeederWidget(self)
        self.subst_lineedit  = SubstationWidget(self)
        
        self.light_restore   = LightWidget(name="Restore")
        self.light_demand    = LightWidget(name="ByDemand")
        self.light_rotate    = LightWidget(name="Rotating")
        self.light_uf        = LightWidget(name="UF")

        # Event 
        self.groups_combobox.group_changed.connect(self.re_init_xref_model)
        self.feeder_lineedit.feeder_changed.connect(self.re_init_xref_model)
        self.subst_lineedit.substation_changed.connect(self.re_init_xref_model)

        groups_label = QtWidgets.QLabel("Groups")
        groups_label.setBuddy(self.groups_combobox)
        self.font_setting(groups_label, 12)

        xref_option_box.addWidget(groups_label)
        xref_option_box.addWidget(self.groups_combobox)
        xref_option_box.addWidget(self.feeder_lineedit)
        xref_option_box.addWidget(self.subst_lineedit)
        xref_option_box.addStretch()
        
        state_light_box.addWidget(self.light_restore)
        state_light_box.addWidget(self.light_demand)
        state_light_box.addWidget(self.light_rotate)
        state_light_box.addWidget(self.light_uf)
        xref_option_box.addLayout(state_light_box)

        # =====================================================================
        #Log
        # =====================================================================
        self.Log_table_widget = QtWidgets.QWidget()
        self.Log_table_layout = QtWidgets.QVBoxLayout()
        self.Log_table_view = QtWidgets.QTableView(self)

        self.Log_table_widget.setLayout(self.Log_table_layout)
        self.Log_table_layout.addWidget(self.Log_table_view)

        # =====================================================================
        #Tab(Tab_widget)
        # =====================================================================
        self.Tab_widget = QtWidgets.QTabWidget()
        self.Tab_widget.addTab(self.xref_view,'Group')
        self.Tab_widget.addTab(self.Log_table_widget,'Log')

        # ====================================================================
        # Footer
        # =====================================================================
        footer_box  = QtWidgets.QHBoxLayout()
        self.stop_button = StopButtonWidget("Stop")
        self.stop_button.action0.triggered.connect(self._stop_mode0)
        self.stop_button.action1.triggered.connect(self._stop_mode1)
        self.stop_button.action2.triggered.connect(self._stop_mode2)
        self.stop_button.action3.triggered.connect(self._stop_mode3)

        self.exec_button = ExecButtonWidget("Execute")
        self.exec_button.action0.triggered.connect(self._start_mode0)
        self.exec_button.action1.triggered.connect(self._start_mode1)
        self.exec_button.action2.triggered.connect(self._start_mode2)
        self.exec_button.action3.triggered.connect(self._start_mode3)

        acs_logo    = QtWidgets.QLabel(self)
        acs_logo.setMinimumSize(QtCore.QSize(320, 25))
        # labels.set_label_attributes(acs_logo, text=None, icon="./acs_logo_horizontal_bule_2020.png", tip="Minsait ACS")
        footer_box.addWidget(acs_logo)
        footer_box.addStretch()
        footer_box.addWidget(self.stop_button)
        footer_box.addWidget(self.exec_button)
        
        #=====================================================================
        # Settings Widget
        #=====================================================================
        settings_section = QtWidgets.QVBoxLayout()
        settings_section.addLayout(xref_option_box)
        # settings_section.addWidget(self.xref_view)
        settings_section.addWidget(self.Tab_widget)
        settings_section.addLayout(footer_box)

        settings_widget = QtWidgets.QWidget()
        settings_widget.setLayout(settings_section)

        self.setCentralWidget(settings_widget)

        #=====================================================================
        # Docks
        #=====================================================================
        self.dw_group = DockWidget("Groups")
        self.dw_group.setWidget(self.groups_view)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dw_group)

        self.dw_config = DockWidget("Configuration")
        self.dw_config.setWidget(self.config_view)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dw_config)

        self.dw_uf = DockWidget("UF")
        self.dw_uf.setWidget(self.uf_view)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dw_uf)

        #=====================================================================
        # Preprocessing functions
        #=====================================================================
        self._menu_setup()
        self.re_init_xref_model()

    #=====================================================================
    # Execute Button Functions
    #=====================================================================
    def _start_mode0(self):
        dialog = mode0_ExecDialog(self)
        result = dialog.exec()
        if dialog.args != None:
            task = Worker(args=dialog.args, parent=self)
            self.threadpool.add("restore", dialog.args['group'], task)
            task.start()

            if self.threadpool.get_task_count("restore") > 0:
                tips = self.threadpool.get_task_tips("restore")
                self.light_restore.setToolTip(tips)
                self.light_restore.set_task_color("Green")
                self.stop_button.action0.setEnabled(True)
            logger.info(f"Start a new task --> Mode: restore | options: {dialog.args['group']}")

    def _start_mode1(self):
        dialog = mode1_ExecDialog(self)
        result = dialog.exec()
        if dialog.args != None:
            task = Worker(args=dialog.args, parent=self)
            self.threadpool.add("bydemand", f"('{dialog.args['group']}', {dialog.args['demand']})", task)
            task.start()

            if self.threadpool.get_task_count("bydemand") > 0:
                tips = self.threadpool.get_task_tips("bydemand")
                self.light_demand.setToolTip(tips)
                self.light_demand.set_task_color("Green")
                self.stop_button.action1.setEnabled(True)
            logger.info(f"Start a new task --> Mode: bydemand | Demand: {dialog.args['demand']} | Groups: {dialog.args['group']}")

    def _start_mode2(self):
        dialog = mode2_ExecDialog(self)
        dialog.exec()
        if dialog.args != None:
            task = Worker(args=dialog.args, parent=self)
            self.threadpool.add("rotating", f"('{dialog.args['group']}', {dialog.args['demand']})", task)
            task.start()

            if self.threadpool.get_task_count("rotating") > 0:
                tips = self.threadpool.get_task_tips("rotating")
                self.light_rotate.setToolTip(tips)
                self.light_rotate.set_task_color("Green")
                self.stop_button.action2.setEnabled(True)
            logger.info(f"Start a new task --> Mode: rotating | Demand: {dialog.args['demand']} | Groups: {dialog.args['group']}")

    def _start_mode3(self):
        task = Worker(args={"mode":"3"}, parent=self)
        self.threadpool.add("uf", "uf", task)
        task.start()

        if self.threadpool.get_task_count("uf") > 0:
            tips = self.threadpool.get_task_tips("uf")
            self.light_uf.setToolTip(tips)
            self.light_uf.set_task_color("Green")
            self.stop_button.action3.setEnabled(True)
        logger.info(f"Start the UF task")

    #=====================================================================
    # Stop Button Functions
    #=====================================================================
    def _stop_mode0(self):
        if self.threadpool.get_task_count("restore") > 0:
            pool   = self.threadpool.pool["restore"]
            dialog = mode0_StopDialog(self, pool)
            dialog.exec()
            if dialog.args != None:
                task = self.threadpool.get("restore", dialog.args["options"])
                self.threadpool.delete("restore", dialog.args["options"])
                logger.info(f"Stop the task --> Mode: restore | options: {dialog.args['options']}")
                task.stop()

                tips = self.threadpool.get_task_tips("restore")
                self.light_restore.setToolTip(tips)
                if self.threadpool.get_task_count("restore") == 0: 
                    self.light_restore.set_task_color("White")
                    self.stop_button.action0.setEnabled(False)

    def _stop_mode1(self):
        if self.threadpool.get_task_count("bydemand") > 0:
            pool   = self.threadpool.pool["bydemand"]
            dialog = mode1_StopDialog(self, pool)
            dialog.exec()
            if dialog.args != None:
                task = self.threadpool.get("bydemand", dialog.args["options"])
                self.threadpool.delete("bydemand", dialog.args["options"])
                logger.info(f"Stop the task --> Mode: bydemand | options: {dialog.args['options']}")
                task.stop()

                tips = self.threadpool.get_task_tips("bydemand")
                self.light_demand.setToolTip(tips)
                if self.threadpool.get_task_count("bydemand") == 0:
                    self.light_demand.set_task_color("White")
                    self.stop_button.action1.setEnabled(False)
    
    def _stop_mode2(self):
        if self.threadpool.get_task_count("rotating") > 0:
            pool   = self.threadpool.pool["rotating"]
            dialog = mode2_StopDialog(self, pool)
            dialog.exec()
            if dialog.args != None:
                task = self.threadpool.get("rotating", dialog.args["options"])
                self.threadpool.delete("rotating", dialog.args["options"])
                logger.info(f"Stop the task --> Mode: rotating | options: {dialog.args['options']}")
                task.stop()
                
                tips = self.threadpool.get_task_tips("rotating")
                self.light_rotate.setToolTip(tips)
                if self.threadpool.get_task_count("rotating") == 0:
                    self.light_rotate.set_task_color("White")
                    self.stop_button.action2.setEnabled(False)

    def _stop_mode3(self):
        if self.threadpool.get_task_count("uf") > 0:
            task = self.threadpool.get("uf", "uf")
            self.threadpool.delete("uf", "uf")
            task.stop()

            tips = self.threadpool.get_task_tips("uf")
            self.light_uf.setToolTip(tips)
            self.light_uf.set_task_color("White")
            self.stop_button.action3.setEnabled(False)
            logger.info(f"Stop the UF task")

    def font_setting(self, widget, size=None):
        size = 12 if size == None else size
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(size)
        widget.setFont(font)

    def ask_refresh_rate(self):
        dialog = QtWidgets.QInputDialog(self)
        dialog.setInputMode(QtWidgets.QInputDialog.IntInput)
        dialog.setWindowTitle("Set Refresh Rate")
        dialog.setLabelText("Refresh Rate (seconds)")
        dialog.setIntRange(1, 5*60)
        dialog.setIntValue(self.xref_model.refresh_interval_ms / 1000)
        ok = dialog.exec_()
        if ok:
            refresh_ms = dialog.intValue() * 1000
            self.xref_model.refresh_interval_ms   = refresh_ms
            self.groups_model.refresh_interval_ms = refresh_ms
            self.update_window_title()

    def update_window_title(self):

        refresh_s = int(self.xref_model.refresh_interval_ms) / 1000
        if self.xref_model.is_refresh_enabled():
            refresh = "Refresh [%d secs]" % refresh_s
        else:
            refresh = "Refresh [OFF]"

        info = {
            'app' : TITLE,
            'user': USER,
            'pswd': PSWD,
            'tns' : TNS,
            'refresh': refresh,
        }

        title = "%(app)s   %(user)s@%(pswd)s on %(tns)s        %(refresh)s" % info
        self.setWindowTitle(title)

    def create_action(
            self, text, slot=None, shortcut=None, icon=None,
            tip=None, checkable=False, signal='triggered'):

        action = QAction(text, self)

        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))

        if shortcut is not None:
            action.setShortcut(shortcut)

        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)

        if slot is not None:
            signal = getattr(action, signal)
            signal.connect(slot)

        if checkable:
            action.setCheckable(True)

        return action

    def _menu_setup(self):
        # =====================================================================
        # File Menu
        # =====================================================================
        file_expt_action = self.create_action( "&Export", slot=self.expt_table, tip="Export table")
        file_quit_action = self.create_action( "&Quit"  , slot=self.close, shortcut=QtGui.QKeySequence.Quit, tip="Close the application")
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(file_expt_action)
        file_menu.addAction(file_quit_action)

        # # =====================================================================
        # # Edit Menu
        # # =====================================================================
        # edit_menu = self.menuBar().addMenu(_("&Edit"))
        # copy_action = self.create_action(
        #     _("&Copy table data"), slot=None,
        #     shortcut=QtGui.QKeySequence.Copy,
        #     tip=_("Copy data from the table in tab-separated format for pasting into LibreOffice or Excel"),
        # )
        # edit_menu.addAction(copy_action)

        # =====================================================================
        # View Menu
        # =====================================================================
        view_menu = self.menuBar().addMenu("&View")
        # view_menu.addAction(self.dock1.toggleViewAction())
        view_menu.addAction(self.dw_group.toggleViewAction())
        view_menu.addAction(self.dw_config.toggleViewAction())
        view_menu.addAction(self.dw_uf.toggleViewAction())

        # =====================================================================
        # Settings Menu
        # =====================================================================
        settings_menu = self.menuBar().addMenu("&Settings")
        self.refresh_enable_action = self.create_action("Enable Refresh", checkable=True)
        self.refresh_enable_action.toggled.connect(self.enable_refresh)
        ask_refresh_rate_action = self.create_action("&Refresh Rate", self.ask_refresh_rate)

        settings_menu.addAction(self.refresh_enable_action)
        settings_menu.addAction(ask_refresh_rate_action)

        # =====================================================================
        # Help Menu
        # =====================================================================
        help_menu = self.menuBar().addMenu("&Help")
        help_about_action = self.create_action("&About", self.help_about)
        help_menu.addAction(help_about_action)
    
    def expt_table(self):
        times  = datetime.date.today().strftime("%Y%m%d")
        folder = '/home/acs/tmp'
        path   = os.path.join(folder, f"LoadShedding_{times}.csv")
        fname, ftype = QtWidgets.QFileDialog().getSaveFileName(self, "Save", path, "Excel (*.csv)")
        if fname:
            try:
                worker = ExportTable(self)
                worker.path    = fname
                worker.headers = self.xref_model.header_keys[:-7]
                worker.datas   = [ d[:-7] for d in self.xref_model._datas ]
                worker.start()
                worker.wait()
                QtWidgets.QMessageBox.information(self,"MESSAGE","The CSV file has been created successfully")
                logger.info("The CSV file has been created successfully")
            except:
                QtWidgets.QMessageBox.information(self,"MESSAGE","The CSV file has been created failed")
                logger.info("The CSV file has been created failed")

    def re_init_xref_model(self):

        groups  = self.groups_combobox.group
        feeder  = self.feeder_lineedit.feeder
        subst   = self.subst_lineedit.substation
      
        options = {
            "groups" : groups,
            "feeder" : feeder,
            "subst"  : subst
        }
        # logger.debug(
        #     "Reinitializing point model (%s, %s, %s)"
        #     % (station, category, self.point_type))
        self.xref_model.re_init(options)
    
    def enable_refresh(self, enable):
        self.xref_model.enable_refresh(enable)
        self.refresh_enable_action.setChecked(enable)
        self.update_window_title()

    def help_about(self):
        info = {
            'title': TITLE,
            'year': COPYRIGHT_YEAR,
            'version': __version__,
            'py_version': platform.python_version(),
            'qt_version': QT_VERSION_STR,
            'pyqt_version': PYQT_VERSION_STR,
        }

        QtWidgets.QMessageBox.about(
            self, "About %(title)s" % info,
            """<b>%(title)s</b> v%(version)s
            <p>Copyright &copy; %(year)s Advanced Control Systems, Inc.
            All rights reserved.</p>
            <p>
            Python %(py_version)s -
            Qt %(qt_version)s -
            PyQt %(pyqt_version)s</p>
            <p>Author: Darren Liang, Wilson Kuo</P>
            """ % info)

    def restore_settings(self):
        """
        Load QSettings file if it exists. If it doesn't exist, then load
        some default settings.
        """
        self.settings.beginGroup("Misc")
        restored_geometry = self.restoreGeometry(self.settings.value('Geometry', QtCore.QByteArray()))
        self.restoreState(self.settings.value('WindowState', QtCore.QByteArray()))

        if not restored_geometry:
            # State/geometry was not restored, so set defaults
            self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        
        try:
            self.xref_model.refresh_interval_ms   = int(self.settings.value("RefreshRate"))
            self.groups_model.refresh_interval_ms = int(self.settings.value("RefreshRate"))
        except TypeError:
            self.xref_model.refresh_interval_ms   = DEFAULT_REFRESH_INTERVAL_MILLIS
            self.groups_model.refresh_interval_ms = DEFAULT_REFRESH_INTERVAL_MILLIS
        self.settings.endGroup()

        # Xref View - Column Widths
        self.settings.beginGroup("xref_view")
        self.xref_view.restore_settings(self.settings)
        self.settings.endGroup()       

        # uf View - Column Widths
        self.settings.beginGroup("uf_view")
        self.uf_view.restore_settings(self.settings)
        self.settings.endGroup()   

        # groups View - Column Widths
        self.settings.beginGroup("groups_view")
        try:
            st_view_col_cnt = int(self.settings.value("NumOfColumns"))
        except TypeError:
            # Invalid or missing value
            pass
        else:
            # Don't restore the width of the last column; it should automatically
            # expand as needed. If we restore the width, sometimes we get a
            # spurious scroll bar.
            for col in range(st_view_col_cnt - 1):
                Name = "Col_%02d" % col
                w = int(self.settings.value(Name))
                self.groups_view.setColumnWidth(col, w)
        finally:
            self.settings.endGroup()

        # config View - Column Widths
        self.settings.beginGroup("config_view")
        try:
            st_view_col_cnt = int(self.settings.value("NumOfColumns"))
        except TypeError:
            # Invalid or missing value
            pass
        else:
            # Don't restore the width of the last column; it should automatically
            # expand as needed. If we restore the width, sometimes we get a
            # spurious scroll bar.
            for col in range(st_view_col_cnt - 1):
                Name = "Col_%02d" % col
                w = int(self.settings.value(Name))
                self.config_view.setColumnWidth(col, w)
        finally:
            self.settings.endGroup()
    
    def save_settings(self):
        self.settings.beginGroup("Misc")
        # State of toolbars and dock widgets
        self.settings.setValue('Geometry',    self.saveGeometry())
        self.settings.setValue('WindowState', self.saveState())
        self.settings.setValue("RefreshRate", self.xref_model.refresh_interval_ms)
        self.settings.endGroup()

        # Xref View - Column Widths
        self.settings.beginGroup("xref_view")
        self.xref_view.save_settings(self.settings)
        self.settings.endGroup()

        # uf View - Column Widths
        self.settings.beginGroup("uf_view")
        self.uf_view.save_settings(self.settings)
        self.settings.endGroup()

        # groups_view - Column Widths
        self.settings.beginGroup("groups_view")
        st_view_col_cnt = self.groups_view.horizontalHeader().count()
        self.settings.setValue("NumOfColumns", st_view_col_cnt)
        for col in range(st_view_col_cnt):
            name = "Col_%02d" % col
            self.settings.setValue(name, self.groups_view.columnWidth(col))
        self.settings.endGroup()

        # config_view - Column Widths
        self.settings.beginGroup("config_view")
        st_view_col_cnt = self.config_view.horizontalHeader().count()
        self.settings.setValue("NumOfColumns", st_view_col_cnt)
        for col in range(st_view_col_cnt):
            name = "Col_%02d" % col
            self.settings.setValue(name, self.config_view.columnWidth(col))
        self.settings.endGroup()

    def load_settings(self):
        """
        Load QSettings configuration settings.
        We don't need to check whether the file exists, because it should
        gracefully handle any missing settings.
        """
        self.restore_settings()
        self.enable_refresh(True)

    def closeEvent(self, event):
        """
        If adms_gui is not start compeletely, it will not save app settings.
        """
        if self.isVisible():
            self.save_settings()

def setup_logger():
    #=====================================================================
    # Logging setup
    #=====================================================================
    # Set the logging level of the root logger
    # logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)

    # This sets timestamp for logging to UTC, otherwise it is local
    # logging.Formatter.converter = time.gmtime

    # Set up the console logger
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(LOG_FORMAT)
    stream_handler.setFormatter(stream_formatter)

    logging.getLogger().addHandler(stream_handler)

    # Set up the file logger
    log_dir = '/home/acs/tmp'
    if not os.path.isdir(log_dir):
        # On Windows, tempPath is user-specific
        log_dir = QtCore.QDir.tempPath()
    log_filename = os.path.abspath(os.path.join(log_dir, LOG_FILENAME))
    max_bytes = 1 * 1024 * 1024  # 1 MB
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename, maxBytes=max_bytes, backupCount=1)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(file_handler)
    # logger.info("Logging to file '%s'", log_filename)


def main():
    setup_logger()

    app = create_q_application(TITLE)
    gui = LSApp()
    gui.load_settings()
    gui.update_window_title()
    gui.setVisible(True)
    app.exec_()



if __name__ == '__main__':
    import sys
    sys.exit(main())
