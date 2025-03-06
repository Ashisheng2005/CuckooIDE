    org 07c00h ; ���߱���������װ����0x7c00��

BaseOfStack             equ 07c00h ; ջ�Ļ�ַ
BaseOfLoader            equ 09000h ; Loader�Ļ�ַ
OffsetOfLoader          equ 0100h  ; Loader��ƫ��
RootDirSectors          equ 14     ; ��Ŀ¼��С
SectorNoOfRootDirectory equ 19     ; ��Ŀ¼��ʼ����
SectorNoOfFAT1          equ 1 ; ��һ��FAT��Ŀ�ʼ����
DeltaSectorNo           equ 17 ; ���ڵ�һ���ز��ã�����RootDirSectorsҪ-2�ټ��ϸ�Ŀ¼����������ƫ�Ʋ��ܵõ������ĵ�ַ���ʰ�RootDirSectors-2��װ��һ��������17��

    jmp short LABEL_START
    nop ; BS_JMPBoot ����Ҫ�����ֽڶ�jmp��LABEL_STARTֻ�������ֽ� ���Լ�һ��nop

    BS_OEMName     db 'tutorial'    ; �̶���8���ֽ�
    BPB_BytsPerSec dw 512           ; ÿ�����̶�512���ֽ�
    BPB_SecPerClus db 1             ; ÿ�ع̶�1������
    BPB_RsvdSecCnt dw 1             ; MBR�̶�ռ��1������
    BPB_NumFATs    db 2             ; FAT12 �ļ�ϵͳ�̶�2�� FAT ��
    BPB_RootEntCnt dw 224           ; FAT12 �ļ�ϵͳ�и�Ŀ¼���224���ļ�
    BPB_TotSec16   dw 2880          ; 1.44MB���̶̹�2880������
    BPB_Media      db 0xF0          ; �������������̶�Ϊ0xF0
    BPB_FATSz16    dw 9             ; һ��FAT����ռ����������FAT12 �ļ�ϵͳ�̶�Ϊ9������
    BPB_SecPerTrk  dw 18            ; ÿ�ŵ����������̶�Ϊ18
    BPB_NumHeads   dw 2             ; ��ͷ����bximage ���������������2��
    BPB_HiddSec    dd 0             ; ������������û��
    BPB_TotSec32   dd 0             ; ��֮ǰ�� BPB_TotSec16 ��û�м�¼�����������ɴ˼�¼�������¼�ˣ�����ֱ����0����
    BS_DrvNum      db 0             ; int 13h ����ʱ����ȡ���������ţ�����ֻ����һ������������0 
    BS_Reserved1   db 0             ; δʹ�ã�Ԥ��
    BS_BootSig     db 29h           ; ��չ�������
    BS_VolID       dd 0             ; �����кţ�����ֻ����һ����������Ϊ0
    BS_VolLab      db 'OS-tutorial' ; ��꣬11���ֽ�
    BS_FileSysType db 'FAT12   '    ; ������ FAT12 �ļ�ϵͳ������д�� FAT12 ����8���ֽ�

LABEL_START:
    mov ax, cs
    mov ds, ax
    mov es, ax ; ��ds es����Ϊcs��ֵ����Ϊ��ʱ�ַ����ͱ����ȴ��ڴ�����ڣ�
    mov ss, ax ; ����ջ��Ҳ��ʼ����cs
    mov sp, BaseOfStack ; ����ջ��

    mov ax, 0600h ; AH=06h�����Ϲ�����AL=00h����մ���
    mov bx, 0700h ; �հ�����ȱʡ����
    mov cx, 0 ; ���ϣ�(0, 0)
    mov dx, 0184fh ; ���£�(80, 25)
    int 10h ; ִ��

    mov dh, 0
    call DispStr ; Booting

    xor ah, ah ; ��λ
    xor dl, dl
    int 13h ; ִ��������λ

    mov word [wSectorNo], SectorNoOfRootDirectory ; ��ʼ���ң�����ǰ��������������Ϊ��Ŀ¼���Ŀ�ʼ������19��
LABEL_SEARCH_IN_ROOT_DIR_BEGIN:
    cmp word [wRootDirSizeForLoop], 0 ; ��ʣ��ĸ�Ŀ¼����������0�Ƚ�
    jz LABEL_NO_LOADERBIN ; ��ȣ�������Loader�������ƺ�
    dec word [wRootDirSizeForLoop] ; ��ȥһ������
    mov ax, BaseOfLoader
    mov es, ax
    mov bx, OffsetOfLoader ; ��es:bx����ΪBaseOfLoader:OffsetOfLoader������ʹ��Loader��ռ���ڴ�ռ��Ÿ�Ŀ¼��
    mov ax, [wSectorNo] ; ��ʼ��������ǰ���������������ϻ���
    mov cl, 1 ; ��ȡһ������
    call ReadSector ; ����

    mov si, LoaderFileName ; Ϊ�ȶ���׼�����˴��ǽ�ds:si��ΪLoader�ļ���
    mov di, OffsetOfLoader ; Ϊ�ȶ���׼�����˴��ǽ�es:di��ΪLoaderƫ����������Ŀ¼���е��׸��ļ��飩
    cld ; FLAGS.DF=0����ִ��lodsb/lodsw/lodsd��si�Զ�����
    mov dx, 10h ; ��16���ļ��飨����һ����������Ϊһ���ļ���32�ֽڣ�16���ļ�������һ��������
LABEL_SEARCH_FOR_LOADERBIN:
    cmp dx, 0 ; ��dx��0�Ƚ�
    jz LABEL_GOTO_NEXT_SECTOR_IN_ROOT_DIR ; ����ǰ��һ������
    dec dx ; ����dx��1
    mov cx, 11 ; �ļ�����11�ֽ�
LABEL_CMP_FILENAME: ; �ȶ��ļ���
    cmp cx, 0 ; ��cx��0�Ƚ�
    jz LABEL_FILENAME_FOUND ; ����ȣ�˵���ļ�����ȫһ�£���ʾ�ҵ��������ҵ���Ĵ���
    dec cx ; cx��1����ʾ��ȡ1���ַ�
    lodsb ; ��ds:si����������al��si��1
    cmp al, byte [es:di] ; ���ַ���LOADER  BIN�еĵ�ǰ�ַ������
    jz LABEL_GO_ON ; ��һ���ļ����ַ�
    jmp LABEL_DIFFERENT ; ��һ���ļ���
LABEL_GO_ON:
    inc di ; di��1������һ���ַ�
    jmp LABEL_CMP_FILENAME ; �����Ƚ�

LABEL_DIFFERENT:
    and di, 0FFE0h ; ָ����ļ��鿪ͷ
    add di, 20h ; ����32�ֽڣ���ָ����һ���ļ��鿪ͷ
    mov si, LoaderFileName ; ����ds:si
    jmp LABEL_SEARCH_FOR_LOADERBIN ; ����Ҫ��������һЩ���������Իص�����Loaderѭ���Ŀ�ͷ

LABEL_GOTO_NEXT_SECTOR_IN_ROOT_DIR:
    add word [wSectorNo], 1 ; ��һ������
    jmp LABEL_SEARCH_IN_ROOT_DIR_BEGIN ; ����ִ����ѭ��

LABEL_NO_LOADERBIN: ; ���Ҳ���loader.bin������
    mov dh, 2
    call DispStr; ��ʾNo LOADER
    jmp $

LABEL_FILENAME_FOUND:
    mov ax, RootDirSectors ; ��ax��Ϊ��Ŀ¼��������19��
    and di, 0FFE0h ; ��di���õ����ļ��鿪ͷ
    add di, 01Ah ; ��ʱ��diָ��Loader��FAT��
    mov cx, word [es:di] ; ��ø�������FAT��
    push cx ; ��FAT���ݴ�
    add cx, ax ; +��Ŀ¼������
    add cx, DeltaSectorNo ; ��������ĵ�ַ
    mov ax, BaseOfLoader
    mov es, ax
    mov bx, OffsetOfLoader ; es:bx����ȡ�����Ļ�������ַ
    mov ax, cx ; ax����ʼ������

LABEL_GOON_LOADING_FILE: ; �����ļ�
    push ax
    push bx
    mov ah, 0Eh ; AH=0Eh����ʾ�����ַ�
    mov al, '.' ; AL���ַ�����
    mov bl, 0Fh ; BL����ʾ����
; ����BH��ҳ�룬�˴�����
    int 10h ; ��ʾ���ַ�
    pop bx
    pop ax ; ���漸�е��������ã�����Ļ�ϴ�ӡһ����

    mov cl, 1
    call ReadSector ; ��ȡLoader��һ������
    pop ax ; ����FAT��
    call GetFATEntry ; ����FAT��
    cmp ax, 0FFFh
    jz LABEL_FILE_LOADED ; ������=0FFF�������ļ�������ֱ������Loader
    push ax ; ���´洢FAT�ţ�����ʱ��FAT���Ѿ�����һ��FAT��
    mov dx, RootDirSectors
    add ax, dx ; +��Ŀ¼������
    add ax, DeltaSectorNo ; ��ȡ��ʵ��ַ
    add bx, [BPB_BytsPerSec] ; ��bxָ����һ��������ͷ
    jmp LABEL_GOON_LOADING_FILE ; ������һ������

LABEL_FILE_LOADED:
    mov dh, 1 ; ��ӡ�� 1 ����Ϣ��Ready.��
    call DispStr
    jmp BaseOfLoader:OffsetOfLoader ; ����Loader��

wRootDirSizeForLoop dw RootDirSectors ; ����loader��ѭ���н����õ�
wSectorNo           dw 0              ; ���ڱ��浱ǰ������
bOdd                db 0              ; �����ʵ����һ�ڵĶ����������ȷ�����Ҳ���ǲ���

LoaderFileName      db "LOADER  BIN", 0 ; loader���ļ���

MessageLength       equ 9 ; ����������С��Ϣ���˱������ڱ����䳤�ȣ���ʵ�����ڴ������ǵ����������ڶ�ά����
BootMessage:        db "Booting  " ; �˴�����֮��Ϳ���ɾ��ԭ�ȶ����BootMessage�ַ�����
Message1            db "Ready.   " ; ��ʾ��׼����
Message2            db "No LOADER" ; ��ʾû��Loader

DispStr:
    mov ax, MessageLength
    mul dh ; ��ax����dh�󣬽��������ax����ʵ��Զ�ȴ˸��ӣ��˴��Ƚ��͵����
    add ax, BootMessage ; �ҵ���������Ϣ
    mov bp, ax ; �ȸ���ƫ��
    mov ax, ds
    mov es, ax ; �Է���һ����������es
    mov cx, MessageLength ; �ַ�������
    mov ax, 01301h ; ah=13h, ��ʾ�ַ���ͬʱ�����λ
    mov bx, 0007h ; �ڵװ���
    mov dl, 0 ; ��0�У�ǰ��ָ����dh���䣬���Ը����ڼ�����Ϣ�ʹ�ӡ���ڼ���
    int 10h ; ��ʾ�ַ�
    ret

ReadSector:
    push bp
    mov bp, sp
    sub esp, 2 ; �ճ������ֽڴ�Ŵ�������������Ϊcl�ڵ���BIOSʱҪ�ã�

    mov byte [bp-2], cl
    push bx ; ������ʱ��һ��bx
    mov bl, [BPB_SecPerTrk]
    div bl ; ִ�����ax��������bl��ÿ�ŵ����������������������λ��al������λ��ah����ôal����ľ����ܴŵ���������ȡ������ah�������ʣ��û������������
    inc ah ; +1��ʾ��ʼ����������ź�BIOS�е���ʼ����һ����˼���Ƕ��뿪ʼ�ĵ�һ��������
    mov cl, ah ; ����BIOS��׼����cl
    mov dh, al ; ��dh�ݴ�λ���ĸ��ŵ�
    shr al, 1 ; ÿ���ŵ�������ͷ������2�ɵ�������������
    mov ch, al ; ����BIOS��׼����ch
    and dh, 1 ; �Դŵ�ģ2ȡ�࣬�ɵ�λ���ĸ���ͷ������Ѿ�����dh
    pop bx ; ��bx����
    mov dl, [BS_DrvNum] ; ���������Ŵ���dl
.GoOnReading: ; ���¾㱸��ֻǷ��ȡ��
    mov ah, 2 ; ����
    mov al, byte [bp-2] ; ��֮ǰ����Ĵ���������ȡ����
    int 13h ; ִ�ж��̲���
    jc .GoOnReading ; �緢������ͼ�����������������������

    add esp, 2
    pop bp ; �ָ���ջ

    ret

GetFATEntry:
    push es
    push bx
    push ax ; �����õ���pushһ��
    mov ax, BaseOfLoader ; ��ȡLoader�Ļ�ַ
    sub ax, 0100h ; ����4KB�ռ�
    mov es, ax ; �˴����ǻ������Ļ�ַ
    pop ax ; ax���Ǿ��ò�����
    mov byte [bOdd], 0 ; ����bOdd�ĳ�ֵ
    mov bx, 3
    mul bx ; dx:ax=ax * 3��mul�ĵڶ����÷������н�λ����λ������dx��
    mov bx, 2
    div bx ; dx:ax / 2 -> dx������ ax����
; �˴�* 1.5��ԭ���ǣ�ÿ��FAT��ʵ��ռ�õ���1.5����������Ҫ�ѱ��� * 1.5
    cmp dx, 0 ; û������
    jz LABEL_EVEN
    mov byte [bOdd], 1 ; �Ǿ���������
LABEL_EVEN:
    ; ��ʱax��Ӧ���Ѿ��洢�˴�����FAT�����FAT���ƫ�ƣ��������ǽ������������������
    xor dx, dx ; dx��0
    mov bx, [BPB_BytsPerSec]
    div bx ; dx:ax / 512 -> ax���̣������ţ�dx��������������ƫ�ƣ�
    push dx ; �ݴ�dx������Ҫ��
    mov bx, 0 ; es:bx��(BaseOfLoader - 4KB):0
    add ax, SectorNoOfFAT1 ; ʵ��������
    mov cl, 2
    call ReadSector ; ֱ�Ӷ�2��������������ֿ�����FAT�����bug
    pop dx ; ����ReadSectorδ����dx��ֵ�������ﱣ��һ��
    add bx, dx ; ���������������ڴ��У�bx+=dx������������FAT��
    mov ax, [es:bx] ; ��ȡ֮

    cmp byte [bOdd], 1
    jnz LABEL_EVEN_2 ; ��ż���������LABEL_EVEN_2
    shr ax, 4 ; ��4λΪ������FAT��
LABEL_EVEN_2:
    and ax, 0FFFh ; ֻ������4λ

LABEL_GET_FAT_ENRY_OK: ; ʤ��ִ��
    pop bx
    pop es ; �ָ���ջ
    ret

times 510 - ($ - $$) db 0
db 0x55, 0xaa ; ȷ����������ֽ���0x55AA
