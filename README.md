# ipyNB file to PY file

## Instructions:
Add this line to the first line of all code cells you want to output.
```
# {in}
```

Global Indent: Add indent to all subsequent output lines by cnt levels (each level is 4 spaces).
```
# {indent_{cnt}}
```

Uncomment the next cnt commented lines
```
# {show_{cnt}}
```

Comment the next cnt uncommented lines
```
# {hide_{cnt}}
```

Replace the next show_cnt lines with hide_cnt lines
```
# {replace_{show_cnt}_{hide_cnt}}
```

## How to use:
```
nbpy {path2ipynb} {path2py}
```

## Setup:
```
pip install -e .
```