from subprocess import (Popen, PIPE, STDOUT)
from os import system

class Execute:

    def __int__(self, file_path=None):
        self.file_path = file_path

    def write_bat_file(self, file_path):
        '''根据不同的文件目录编写不同的bat文件内容'''

        text = f"""@echo off

%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

cd /d "%~dp0"

nasm {file_path}/boot.asm -o {file_path}/boot.bin
nasm {file_path}/loader.asm -o {file_path}/loader.bin
edimg imgin:{file_path}/c.img copy from:{file_path}/loader.bin to:@: imgout:{file_path}/c.img
ddrelease64 if={file_path}/boot.bin of={file_path}/c.img bs=512 count=1
qemu-system-i386 -fda {file_path}/c.img
pause"""

        with open(f"./stat.bat", "w", encoding="utf-8") as f:
            f.write(text)


    def _execute(self, file_path=None):
        # print("runing execute.py stat asm file")
        # file_path = self.file_path if not file_path else file_path
        file_path = file_path if file_path else self.file_path
        if not file_path: return False
        # print(file_path)
        #
        # print('\\'.join(file_path.split("\\")[:-1] )+ "\\stat.bat")
        # 这是asm文件的执行函数
        # "D:\MyFile\OS\asm\stat.bat"
        file_path, file_suffix = file_path.split("/")[:-1], file_path.split("/")[-1]
        file_path = '/'.join(file_path)
        if file_path == "": file_path = "."

        self.write_bat_file(file_path)

        print(f"{file_path + "/stat.bat"}")
        p = Popen(
            f"{file_path + "/stat.bat"}",
                  shell=True,
                  stdout=PIPE,
                  stderr=STDOUT
                  )

        out, err = p.communicate()

        return out, err

if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    print("test: ", path)
    Execute()._execute(path)