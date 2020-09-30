import asyncio
import os
import random
import string
import sys
import re
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget, QDialog

from asyncqt import QEventLoop
from pkg_resources import parse_version
# from qasync import QEventLoop


class Item:
    @property
    def name(self):
        return random.choice([
            'bandizip',
            'chromium',
            'dopamine',
            'figma',
            'firefox',
            'git',
            'illustrator',
            'imposition-wizard',
            'intellij-idea-ultimate',
            'kodi',
            'mpv',
            'nodejs',
            'photoshop',
            'phpstorm',
            'picotorrent',
            'pycharm-professional',
            'rider',
            'sumatrapdf',
            'visual-studio-code',
            'vmware-workstation',
            'webstorm',
            'xd',
        ])

    @property
    def category(self):
        return random.choice(['Design', 'Development', 'Gaming', 'Internet', 'Miscellaneous', 'Multimedia', 'Office'])

    @property
    def description(self):
        return "".join(random.choice(string.ascii_letters) for _ in range(30))

    @property
    def is_checked(self):
        return False

    def get_x(self):
        return self.__x

    def set_x(self, x):
        self.__x = x

    async def is_installed(self):
        await asyncio.sleep(random.randint(1, 15))
        return True

    async def is_updated(self):
        await asyncio.sleep(random.randint(1, 15))
        return await self.is_installed() and parse_version(str(await self.available_version())) <= parse_version(str(await self.installed_version()))

    async def available_version(self):
        await asyncio.sleep(random.randint(1, 5))
        return f"{random.randint(0, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}"

    async def installed_version(self):
        await asyncio.sleep(random.randint(1, 5))
        # content = subprocess.run(["yarn.cmd", "--version"], stdout=subprocess.PIPE)
        process = await asyncio.create_subprocess_exec('yarn.cmd','--version', stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        version = re.search("([\\d.]+)", stdout.decode("utf-8")).group(1)
        return version
        # return f"{random.randint(0, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}"


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=None):
        super(TableModel, self).__init__()
        if data is None:
            data = []
        self._data = data

    def flags(self, index):
        if not index.isValid():
            return
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable

    def headerData(self, section, orientation, role):
        header = ["Name", "Category", "I", "U", "Description", "?"]
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return header[section]

        if role == QtCore.Qt.TextAlignmentRole and orientation == QtCore.Qt.Horizontal and section in [0, 1, 4]:
            return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignLeft

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if (
            role == QtCore.Qt.DisplayRole
            and 0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
            and index.column() in [2, 3]
        ):
            value = self._data[index.row()][index.column()]
            if value == True:
                # return QtGui.QIcon("assets/icons/true.png")
                return "✅"
            if value == False:
                return "🛑"
                # return "🟥"
            else:
                # return "⚙️"
                return "⚠️"

        if (
            role == QtCore.Qt.DisplayRole
            and 0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
        ):
            # if index.column() in [0, 3, 4]:
            #     return QVariant(self._data[index.row()][index.column()])
            return self._data[index.row()][index.column()]

        if (
            role == QtCore.Qt.CheckStateRole
            and 0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
        ):
            if index.column() == 0:
                return self._data[index.row()][index.column()]
            if index.column() == 5:
                return self._data[index.row()][index.column()]

        if (
            role == QtCore.Qt.TextAlignmentRole
            and 0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
            and index.column() in [2, 3]
        ):
            return QtCore.Qt.AlignVCenter + QtCore.Qt.AlignHCenter

        if (
            role == QtCore.Qt.DecorationRole
            and 0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
            and index.column() in [0, 1]
        ):
            icon = f"assets/icons/{self._data[index.row()][index.column()].lower()}.png"
            return QtGui.QIcon(icon if os.path.isfile(icon) else "assets/icons/default.png")

        # if (
        #     role == QtCore.Qt.DecorationRole
        #     and 0 <= index.row() < self.rowCount()
        #     and 0 <= index.column() < self.columnCount()
        #     and index.column() in [3, 4]
        # ):
        #     value = self._data[index.row()][index.column()]
        #     if value == True:
        #         return QtGui.QIcon("assets/icons/true.png")
        #     if value == False:
        #         return QtGui.QIcon("assets/icons/false.png")
        #     else:
        #         return QtGui.QIcon("assets/icons/loading.png")

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if (
            role == QtCore.Qt.DisplayRole
            and 0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
        ):
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, (role,))

    def rowCount(self, index=QtCore.QModelIndex()):
        try:
            return len(self._data)
        except:
            return 0

    def columnCount(self, index=QtCore.QModelIndex()):
        try:
            return len(self._data[0])
        except:
            return 0

    def set_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 800, 400)
        self.setWindowTitle("Winstaller")
        self.setWindowIcon(QIcon("assets/app.ico"))

        self.model = TableModel()
        self.sortermodel = QtCore.QSortFilterProxyModel()
        self.sortermodel.setSourceModel(self.model)

        self.table = QtWidgets.QTableView()
        self.table.setModel(self.sortermodel)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.table.verticalHeader().setVisible(False)

        self.setCentralWidget(self.table)

        asyncio.ensure_future(self.fill_model())

    async def fill_model(self):
        items = [Item() for _ in range(100)]
        data = [[item.name, item.category, "...", "...",
                 item.description, item.is_checked] for item in items]
        self.model.set_data(data)

        await asyncio.gather(
            *(self.update_row(row, item) for row, item in enumerate(items)),
            *(self.update_row_2(row, item) for row, item in enumerate(items))
        )

    async def update_row(self, row, item):
        value = await item.is_installed()
        index = self.model.index(row, 2)
        self.model.setData(index, value)

    async def update_row_2(self, row, item):
        value2 = await item.is_updated()
        index2 = self.model.index(row, 3)
        self.model.setData(index2, value2)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()
