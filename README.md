# NBPY: ipyNB file to PY file
Convert jupyter notebook file to python file as you wish.

将jupyter notebook文件转换成python文件的更优雅的方式

## Instructions:
Add this line to the first line of all code cells you want to output.
```
# {in}
```

Global Indent: Add indent to all subsequent output lines by cnt levels (each level is 4 spaces).
```
# {indent_{cnt}}
```

Start a code block that requires indentation.
```
# {indent_start}
and
# {indent_end}
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

## Magic
You can use the above instructions to accomplish the following tasks.

Extract special values in the notebook, and iterate over a list in the Python file.

```
# {in}
# {replace_1_1}
# for task_id in random_indices:
task_id = random_indices[0]
# {indent_1}
task = all_tasks[task_id]
···your code···

# {indent_0}
···other code···
```
to
```
for task_id in random_indices:
# task_id = random_indices[0]
    task = all_tasks[task_id]
    ···your code···

···other code···
```
Run some lines that are only needed in the notebook or hide some lines that are only needed in the python file.
```
···some code···
# {show_2}
# plt.savefig(pic_path)
# print(f'save to {pic_path}')
# {hide_1}
plt.show()
···some code···
```
to
```
···some code···
plt.savefig(pic_path)
print(f'save to {pic_path}')
# plt.show()
···some code···
```

## How to use:
```
nbpy {path2ipynb} {path2py}
```

## Setup:
```
pip install -e .
```