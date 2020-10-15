# PRJ_Manager_2020
Desktop application for project breakdown system (PBS)

The goal of the application is to represent a full project in all it's details, 
and also facilitate the file and parts management of the project.
This application will eventually be able to manage any kind of assembly project.

The project is divided in a tree structure, where every type of component can be represented.
Every component has different features that are described in the component line. Such features
are for example the type of the component, (assembly, part, project, ecc...) or the manufacture
of the component (3D printed, off the shelf, ecc...). Then every component has a blank space for 
inserting eventual comments.

The hardware components such as screws, washers, nuts, motors, PCB boards or everything that is 
bought as a finished product can be inserted in the hardware archive and shared between projects.
This facilitates the user, which can use the same type of nut or screw for every project and avoid 
inserting it every time by hand.

With every step up in the level the assembly becomes more and more simple until the final
components are reached. Those component are the one that are then listed in the bill of material
which can also be exported to a separate file.

The file is then exported in a particular .csv file that can be read by the application, so it is recommended
to not edit such file even when possible.
