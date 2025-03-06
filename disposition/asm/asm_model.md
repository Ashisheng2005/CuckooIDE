stat.bat

```apl
nasm boot.asm -o boot.bin
nasm loader.asm -o loader.bin
edimg imgin:c.img copy from:loader.bin to:@: imgout:c.img
ddrelease64 if=boot.bin of=c.img bs=512 count=1
qemu-system-i386 -fda c.img

```

环境启动文件，在运行asm项目时，会提前调用该文件创建环境，内容可自定义。

其中 boot.asm 是项目执行文件的绝对目录（相对目录）。同理，对于不同的活动执行的项目文件，我们会构建不同的执行命令，模板如下：

```apl
nasm file_path -o file.bin
```



但需要确保本地（云上）正确安装且能够使用如下工具， 以windows环境为例，版本不做强制要求：

```typescript
Bochs-win64-2.8
ddrelease64
edimg
make-3.81
nasm-2.16.03-installer-x64
qemu-w64-setup-20240903
i686-elf-tools-windows
```

