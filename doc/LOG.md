TO DO LIST:

- main window class breakdown

IDEAS:

    MAIN WINDOW
    - undo stack view
    - bill model and page
        - export bill
    - analytics page and status bar
        - number of total pieces
        - number of unique pieces
        - number of hardware pieces
        - number of self designed pieces
        - number of assemblies
        - percentages
        - total price
    - project title section
    - images of the components

    DATA STRUCTURES
    - features class
    - ID class
    - measured hardware node quantity reimplementation

    PREFERENCES POPUP WINDOW
    implemented with json files

    - iconpack selection
    - theme selection (stylesheet)
    - last progect
    - recent projects list
    - archive selection
    - status and manufacture entries

    COMPONENTS PAGE

    - automatic assembly status updating
    - add statuses "testing", "CAD polishing"
    - parent-children highlighting
    - node filtering
    - find/edit
    - optional node
    - checkable update hardware node

    ARCHIVE PAGE
    - export archive

DONE:

- coded and documented UndoStack
- implement UndoStack:
  - implement undoable decorator
  - apply produces changes and undoable decorator
  - implement undo and redo actions
