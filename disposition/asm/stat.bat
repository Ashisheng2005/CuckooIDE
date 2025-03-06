@echo off

%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

cd /d "%~dp0"


nasm E:/IDE/disposition/asm/boot.asm -o E:/IDE/disposition/asm/boot.bin
nasm E:/IDE/disposition/asm/loader.asm -o E:/IDE/disposition/asm/loader.bin
edimg imgin:E:/IDE/disposition/asm/c.img copy from:E:/IDE/disposition/asm/loader.bin to:@: imgout:E:/IDE/disposition/asm/c.img
ddrelease64 if=E:/IDE/disposition/asm/boot.bin of=E:/IDE/disposition/asm/c.img bs=512 count=1
qemu-system-i386 -fda E:/IDE/disposition/asm/c.img
pause