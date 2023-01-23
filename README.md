# CDMO-2021
This project tries to resolve 40 different exercises concerning Constraint Programming in Minizinc and Python (with z3 libraries) in at most 5 minutes. 

All the Minizinc examples need to be converted in *.dzn format:
```console
cd MinizincConstrainProgramming/src/exercices/
python convert.py
```
To run the the examples, it's needed to open the proper IDE and select files from the MinizincConstrainProgramming/src/sortedExercices directory.
<hr/>
Instead for python it's needed to install all the proper requirements first:

```console
pip install -r requirements.txt
```
How to run the code:
```console
python src/smt.py <1..40>
```

