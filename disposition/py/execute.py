from subprocess import (Popen, PIPE, STDOUT)
from chardet import detect

class Execute:

    def __int__(self, RDT=None):
        self.RDT = RDT      # 返回框的连接

    def _get_bytecode_code(self, bytecode):
        """返回一段字节码的可能编码格式，如果无法识别，则默认cp936"""
        if not bytecode:
            return 'cp396'

        code_type = detect(bytecode)['encoding']
        return code_type if code_type else 'cp936'

    def _execute(self, file_path):
        # 这是python文件的执行函数
        p = Popen(f"python {file_path}", shell=True, stdout=PIPE, stderr=STDOUT)
        inform, err = p.communicate()
        if inform:
            inform = str(inform, self._get_bytecode_code(inform))

        if err:
            err = str(err, self._get_bytecode_code(err))

        print(inform if inform else err)
        # return out, err

    def _print(self, *args, sep=' ', end='\n', file=None):
        if args and not file:
            self.RDT.insert('end', sep.join(args) + end)

    def _execute2(self, file_path):
        with open(file_path, "r") as f:
            exec(f.read().replace("print", "_print"), __globals=globals())

if __name__ == '__main__':
    from sys import argv
    path = argv[1]
    Execute()._execute(path)