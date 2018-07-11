# Robot

You can get in from
[Github](https://github.com/sherevv/robot/).

# Requirements

- Python 3.6.x
- numpy
- matplotlib


# Installation
You should use command line terminal.

First variant. Clone repo and go to the package dir

```commandline
git clone https://github.com/Sherevv/robot.git robot

cd robot
```

and execute command:
```
python setup.py install
```
or
```
pip install .
```

Second variant. Remote using pip:

```
pip install git+https://github.com/Sherevv/robot.git
```

# Basic usage

Create script, example start.py
```python
from robot import Robot

r = Robot()

r.mark()
r.step('w')
r.get_tmpr()
r.is_bord('s')

input()  # to prevent close robot window
```

then execute script
```commandline
python start.py
```


# Usage with python command line
Prepare script with function (myfunc.py):
```python
def walk_to_bord(r, side):
    while not r.is_bord(side):
        r.step(side)
```

then run python command line
```commandline
python
```


```
>>> from robot import Robot
>>> from myfunc import walk_to_bord
>>> r = Robot()
>>> walk_to_bord(r, 'o')
```