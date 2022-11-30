# Noter
Noter is an application with a very specific goal: to help me with my note taking. I take my notes for each of my classes using a system call LaTeX. It allows me to generate fancy pdfs of my notes in a way that looks good. To do so, I need to use some included files with each of my notes and a template file for my notes. And so, Noter is designed to all me to use one copy of my includes and template and automatically propagate these files into all of my class note directories. 

I keep all of my class notes in a specific file hierarchy. It goes as follows: a college folder, then a folder for each of these years (freshman, sophomore, etc.), then a folder for each class. 

When opening Noter you will see numerous input boxes for setting the settings and two buttons. The first setting is “Template Source” this is a folder path to the folder holding the LaTeX includes and template files. Then we have “Includes Files” this is a comma separated list of each of the files that count as an include (do not include spaces). Then we have “Template File’ this is the name of the template file. Then we have “Year Path’ this is a folder path to the folder containing the year folders. Finally we have “Years” this is a comma separated list of each of the year folder (do not include spaces). At the bottom you will see a check box for whether or not you want Noter to automatically rename the ‘template.tex’ file to the name of the class. 

On the opposite side you will see the two buttons that contain the main functionality for the program. The first is “Add Class” this allows you to add a new class (doing so will create the folder and copy the includes and template into it). This button requires that you have filled out the name of the class and the year that the class was taking during. Then we have the “Update Includes’ button. This button allows you to copy the includes into every class folder automatically. This is useful for when I change the include files or add new ones. 

Noter will automatically save the settings into a file called “settings.pkl”, except for the “Rename Template’ button. (sorry I got lazy). 

To use Noter, simply fill out all of the settings and then choose whether to add a new class or update the includes. 
