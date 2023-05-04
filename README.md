Chemical Solution Recipe Editor
===============================

This is a small application / library used for viewing, editing, and storing
chemical solution recipes for research science. It was designed primarily for
creating ACSF / internal recording solutions used in neurophysiology
experiments.


Features
--------

* View/edit a list of _reagents_ including information about their molecular
  weight, osmotic constant, and ion dissociation constants.
* View/edit a list of _solutions_, which define the set of reagents and
  their concentrations for each solution. 
    * Shows estimates of ion concentrations, osmolarity, and reversal potentials.
    * Add notes per-solution. 
* View/edit a list of _recipes_, which are simply a list of _solutions_ and 
  one or more final volumes for each solution. 
    * Shows a table of the masses required for each reagent.
    * May also show molecular weight and concentration for each reagent.
    * Keep notes for each recipe.
    * Copy the recipe to HTML and paste into your favorite word processor.
* Save/load the entire database (reagents, solutions, and recipes) to JSON.
* API for accessing database without GUI.


Requirements
------------ 

* Python 3
* numpy
* PyQt5
* pyqtgraph
