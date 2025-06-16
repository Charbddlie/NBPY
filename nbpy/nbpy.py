import json
import re
from .macro import Rules

def main(in_file, out_file, args):
    line_rules = Rules(args)
    with open(in_file, 'r') as f:
        content = json.load(f)
    with open(out_file, 'w') as f:
        pass

    arg_dict = {
        'indent_num': 0,
        'hide_cnt': 0,
        'show_cnt': 0,
        'other_file': None,
    }
    
    for cell in content['cells']:
        if cell['cell_type'] != 'code': continue
        if cell['source'] == []: continue
        # {in}
        if not re.match(r'^# *?\{in\}$', cell['source'][0].strip()): continue
        del cell['source'][0]
        if not cell['source'][-1].endswith('\n'): cell['source'][-1] += '\n'
        
        # 删除line的内容是一个python变量的line
        for line in cell['source']:
            line = line.rstrip() + '\n'
            # 判断一行只有一个变量（即只包含一个变量名，且没有等号等赋值操作）
            if re.match(r'^\s*\w+\s*$', line): continue

            skip = line_rules(arg_dict, line)
            if skip: continue

            if arg_dict['other_file']:
                with open(arg_dict['other_file'], 'a') as f:
                    f.write(line)
                continue

            if line.startswith('#') and arg_dict['show_cnt']:
                line = line[1:].strip() + '\n'
                arg_dict['show_cnt'] -= 1
            elif not line.startswith('#') and arg_dict['hide_cnt']:
                line = '# ' + line
                arg_dict['hide_cnt'] -= 1

            # 判断一行是否是import，如果是就写入out_file第一行
            if re.match(r'^\s*(from\s+[\w\.]+\s+import\s+[\w\*]+|import\s+[\w\.\*]+)', line):
                # 读取当前out_file内容
                try:
                    with open(out_file, 'r') as f:
                        existing = f.readlines()
                except FileNotFoundError:
                    existing = []
                # 检查是否已存在该import语句
                if line not in existing:
                    # 在第一行插入import语句
                    existing = [line] + existing
                    with open(out_file, 'w') as f:
                        f.writelines(existing)
                continue


            line = '    ' * arg_dict['indent_num'] + line
            with open(out_file, 'a') as f:
                f.write(line)
                
        with open(out_file, 'a') as f:
            f.write('\n')

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
    args.in_file_dir = os.path.dirname(os.path.abspath(args.in_file))
    in_file_name = os.path.splitext(os.path.basename(args.in_file))[0]
    out_file = os.path.join(args.in_file_dir, f"{in_file_name}.py")
    main(in_file=args.in_file, out_file=out_file, args=args)
