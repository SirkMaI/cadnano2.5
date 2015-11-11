
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox, QLineEdit, QCheckBox

KEY_COL = 0
VAL_COL = 1

class CNPropertyItem(QTreeWidgetItem):
    def __init__(self, cn_model, parent, key=None):
        super(CNPropertyItem, self).__init__(parent, QTreeWidgetItem.UserType)
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self._cn_model = cn_model
        if key is None:
            self._parent_tree = parent
            root = parent.invisibleRootItem() # add propertyitems as siblings

            # Properties
            self._prop_items = {}
            model_props = cn_model.getPropertyDict()

            # add properties alphabetically, but with 'name' on top
            name = cn_model.getName()
            if name is None:
                name = "generic"
            self._key = key = "name"
            self._prop_items[key] = name
            self.setData(KEY_COL, Qt.EditRole, key)
            self.setData(VAL_COL, Qt.EditRole, name) #Qt.DisplayRole

            constructor = type(self)
            for key in sorted(model_props):
                if key == 'name':
                    continue
                p_i = constructor(cn_model, root, key=key)
                self._prop_items[key] = p_i
                p_i.setData(KEY_COL, Qt.EditRole, key)
                model_value = cn_model.getProperty(key)
                p_i.setData(VAL_COL, Qt.EditRole, model_value)
        else:
            self._key = key
    # end def

    def key(self):
        return self._key

    ### PUBLIC SUPPORT METHODS ###
    def cnModel(self):
        return self._cn_model
    # end def

    def itemType(self):
        return None
    # end def

    def configureEditor(self, parent_QWidget, option, model_index):
        m_vh = self._cn_model
        key = self.key()
        if key == 'name':
            return QLineEdit(parent_QWidget)
        data_type = type(model_index.model().data(model_index, Qt.DisplayRole))
        if data_type is str:
            editor = QLineEdit(parent_QWidget)
        elif data_type is int:
            editor = QSpinBox(parent_QWidget)
            editor.setRange(-359,359)
        elif data_type is float:
            editor = QDoubleSpinBox(parent_QWidget)
            editor.setDecimals(0)
            editor.setRange(-359,359)
        elif data_type is bool:
            editor = QCheckBox(parent_QWidget)
        elif data_type is type(None):
            return None
        else:
            raise NotImplementedError
        return editor
    # end def

    def updateModel(self):
        value = self.data(1, Qt.DisplayRole)
        self._cn_model.setProperty(self._key, value)
    # end def

    def setValue(self, property_key, new_value):
        p_i = self._prop_items[property_key]
        current_value = p_i.data(VAL_COL, Qt.DisplayRole)
        if current_value != new_value:
            p_i.setData(VAL_COL, Qt.EditRole, new_value)
    # end def

    def getItemValue(self, property_key):
        return self._prop_items[property_key].data(VAL_COL, Qt.DisplayRole)
    # end def

    def updateViewProperty(self, property_key):
        model_value = self._cn_model.getProperty(property_key)
        item_value = self._prop_items[property_key].data(VAL_COL, Qt.DisplayRole)
        if model_value != item_value:
            self._prop_items[property_key].setData(VAL_COL, Qt.EditRole, model_value)
    # end def
# end class