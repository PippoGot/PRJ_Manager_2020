# ComponentTree.py

Subclass of the Tree class. Adds some specific functions for the managing of the components tree.

- initializes the data of the current node: init_node_attrs
- read and save .csv files that can be stored and opened: save_file, read_file
- calculates the number of the children to add: calc_number

# ModelTreeETE.py

Model for the components tree to be displayed in views.

- manages all the model functions needed to add and remove components and to display the component tree
- provides saving and reading file operations through the data structure class (ComponentTree)
- provides printing representation through the Tree class

# ProxyTree.py

Proxy model for the tree model. Hides the unwanted columns and sorts the components in a specific order.

# HardwareModel.py

TO CHANGE THE DATA STRUCTURE WITH A "ModelTreeETE.py" CLASS FOR EASIER DATA MANAGING.
TO CHANGE THE FILE NAME WITH "ModelHardware.py"

Class for the management of the hardware archive. Such archive should be available for every assembly project.
This is achieved through the storing of an internal .csv file with all the hardware components used in the previous
and current project. Adding and removing such components can be performed inside the dedicated page of the application.

- manages the model functions needed to add and remove component to the archive and to display them in the views
- read and save .csv files that can be stored and opened: readArchive, saveArchive (change it to work with the ComponentTree class)
- calculates the number of the children to add: calculateNumber (move it in the ComponentTree)
- represent a node as a string for the filtering function: stringAtRow (move it in the proxy model) 

# HardwareProxyModel.py

TO CHANGE THE FILE NAME WITH "ProxyHardware.py"

Proxy model for the hardware model. Hides unwanted columns and sorts the components in a specific order.

# ModelCombobox.py

Subclass of QStringListModel. Adds read and write capabilities to store a combobox list.

# ModelBill.py

TO DESIGN THE BASIC DATA STRUCTURE FOR THE MANAGING OF THE MODEL AND THE MODEL CLASS

This class generates a data structure (similiar to a list) from all of the leaf (level 5) components.
It's purpose is to have a bill of material for the ordering of components without having to count the parts by hand.

# UIMainWindow.py <- ui_main_window.ui

TO INTEGRATE "removeBeforeMorph" IN TO "morphHardware" 

Main application window. It should be responsible for all of the actions performable inside the application.
contains the different application pages and the actions. Should also contains all the globally used models.

Current preformable actions:
- New file
- Open file
- Save file
- Save As file
- Clear file

- Add part
- Add hardware to list
- Add leaf part
- Morph hardware
- Update hardware
- Remove part

- Show deprecated

Actions to add:
- Export bill of materials

- Undo
- Redo
- (separate add hardware to list in different cathegories)

- Expand all
- Collapse all

# UITreeEditor.py <- ui_components_page.ui

TO CHANGE THE NAME INTO "UIComponentsPage.py"

Class responsible of the displaying and editing of the components tree.
Takes a ModelTreeETE class for its view and mapper.

# UIPropEditor.py <- ui_component_editor.ui

TO CHANGE THE NAME INTO "UIComponentEditor.py"

Class responsible for editing a new component that is about to be added to the tree.
It is a popup window that emits a ComponentTree instance.

# UIHardwareEditor.py <- ui_hardware_editor_page.ui

TO CHANGE THE VIEW INTO A TREEVIEW WHEN CHANGING THE HARDWARE MODEL TO A TREE MODEL
TO CLEAN THE FUNCTIONS CODE

Class responsible for the editing and displaying of the hardware archive, as well as adding and removing new
hardware components and consumables.

# UIHardwareSelector.py <- ui_hardware_selector.ui

TO CLEAN THE FUNCTIONS CODE

Class responsible for selecting a specific hardware component form the archive to be added in the list or
to be changed inside the list. It is a popup window that emits a ComponentTree instance.

# util.py

Class with general purpose functions and data.