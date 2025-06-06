import json
import re

def main(in_file, out_file):
    with open(in_file, 'r') as f:
        content = json.load(f)

    indent_num = 0
    hide_cnt = 0
    show_cnt = 0

    output = []
    for cell in content['cells']:
        if cell['cell_type'] != 'code': continue
        if cell['source'] == []: continue
        if not re.match(r'^# *?\{in\}$', cell['source'][0].strip()): continue
        del cell['source'][0]
        if not cell['source'][-1].endswith('\n'): cell['source'][-1] += '\n'
        cell_content = []
        
        
        # 删除line的内容是一个python变量的line
        for line in cell['source']:
            line = line.rstrip() + '\n'
            # 判断一行只有一个变量（即只包含一个变量名，且没有等号等赋值操作）
            if re.match(r'^\s*\w+\s*$', line): continue
            
            # 缩进
            match = re.match(r'^#\s*\{indent_(\d+)\}\s*$', line)
            if match:
                indent_num = int(match.group(1))
                continue
            
            # hide
            match = re.match(r'^#\s*\{hide_(\d+)\}\s*$', line)
            if match:
                hide_cnt = int(match.group(1))
                continue

            # {replace_show_hide}
            replace_match = re.match(r'^#\s*\{replace_(\d+)_(\d+)\}\s*$', line)
            if replace_match:
                show_cnt = int(replace_match.group(1))
                hide_cnt = int(replace_match.group(2))
                # 你可以在这里使用 num1 和 num2
                continue

            if line.startswith('#') and show_cnt:
                line = line[1:].strip() + '\n'
                show_cnt -= 1
            elif not line.startswith('#') and hide_cnt:
                line = '# ' + line
                hide_cnt -= 1

            line = '    ' * indent_num + line
            
            cell_content.append(line)
        cell_content.append('\n')
        output += cell_content

    with open(out_file, 'w') as f:
        f.writelines(output)

import argparse
import os
def cli():
    parser = argparse.ArgumentParser(description="Process notebook cells and output to a file.")
    parser.add_argument('in_file', type=str, help='Input notebook file path')
    parser.add_argument('-o', '--output', type=str, default='default.py', help='Output file path relative to current file')
    args = parser.parse_args()

    # 检查输入文件是否存在且为.ipynb文件
    if not os.path.isfile(args.in_file):
        print(f"输入文件不存在: {args.in_file}")
        exit()
    if not args.in_file.endswith('.ipynb'):
        print(f"输入文件不是.ipynb文件: {args.in_file}")
        exit()
    # 获取in_file的目录
    in_file_dir = os.path.dirname(os.path.abspath(args.in_file))
    in_file_name = os.path.splitext(os.path.basename(args.in_file))[0]
    out_file = os.path.join(in_file_dir, f"{in_file_name}.py")
    main(in_file=args.in_file, out_file=out_file)

if __name__ == '__main__':
    cli()