import re
import os
from abc import ABC, abstractmethod

class Instr(ABC):
    def __init__(self, template):
        self.pattern, self.match_num = Instr.temp2regex(template)

    @abstractmethod
    def __call__(self, line):
        match = self.pattern.match(line.strip())
        if not match: return False, [0] * self.match_num
        if self.match_num == 0: return True, [0] * self.match_num
        return True, match.groups()

    @staticmethod
    def temp2regex(template):
        match_num = template.count('{num}') + template.count('{cnt}') + template.count('{path}')
        format_template = template.replace('{num}', r'(\d+?)').replace('{cnt}', r'(\d+?)').replace('{path}', r'(.+?)')
        reg_str = r'^#\s*\{' + format_template + r'\}\s*$'
        return re.compile(reg_str), match_num

class IndentStart(Instr):
    def __init__(self):
        super().__init__("indent_start")

    def __call__(self, arg_dict, line):
        match, _ = super().__call__(line)
        if match: 
            arg_dict['indent_num'] += 1
            return True
        return False

class IndentEnd(Instr):
    def __init__(self):
        super().__init__("indent_end")

    def __call__(self, arg_dict, line):
        match, _ = super().__call__(line)
        if match: 
            arg_dict['indent_num'] -= 1
            return True
        return False

class IndentNum(Instr):
    def __init__(self):
        super().__init__("indent_{num}")
    
    def __call__(self, arg_dict, line):
        match, [num] = super().__call__(line)
        if match: 
            arg_dict['indent_num'] = int(num)
            return True
        return False

class HideCnt(Instr):
    def __init__(self):
        super().__init__("hide_{cnt}")

    def __call__(self, arg_dict, line):
        match, [num] = super().__call__(line)
        if match: 
            arg_dict['hide_cnt'] += int(num)
            return True
        return False

class ShowCnt(Instr):
    def __init__(self):
        super().__init__("show_{cnt}")

    def __call__(self, arg_dict, line):
        match, [num] = super().__call__(line)
        if match: 
            arg_dict['show_cnt'] += int(num)
            return True
        return False

class ReplaceShowHide(Instr):
    def __init__(self):
        super().__init__("replace_{num}_{num}")
    
    def __call__(self, arg_dict, line):
        match, [show, hide] = super().__call__(line)
        if match:
            arg_dict['show_cnt'] += int(show)
            arg_dict['hide_cnt'] += int(hide)
            return True
        return False

class OtherFileStart(Instr):
    def __init__(self, path_prefix):
        super().__init__("other_file_start_{path}")
        self.path_prefix = path_prefix

    def __call__(self, arg_dict, line):
        match, [path] = super().__call__(line)
        if match: 
            p = os.path.join(self.path_prefix, path)
            arg_dict['other_file'] = p
            with open(p, 'w') as f: pass
            return True
        return False
    
class OtherFileEnd(Instr):
    def __init__(self):
        super().__init__("other_file_end")

    def __call__(self, arg_dict, line):
        match, _ = super().__call__(line)
        if match: 
            arg_dict['other_file'] = None
            return True
        return False

class Rules():
    def __init__(self, args):
        self.rules = [
            IndentStart(),
            IndentEnd(),
            IndentNum(),
            HideCnt(),
            ShowCnt(),
            ReplaceShowHide(),
            OtherFileStart(args.in_file_dir),
            OtherFileEnd(),
        ]
    def __call__(self, arg_dict, line):
        modify = False
        for rule in self.rules:
            modify = rule(arg_dict, line)
            if modify: break
        return modify