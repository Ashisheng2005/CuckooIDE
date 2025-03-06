from json import dumps

GDTI = """MOV 
MOVSX  
MOVZX  
PUSH   
POP    
PUSHA  
POPA   
PUSHAD 
POPAD
BSWAP
XCHG
CMPXCHG
XADD   
XLAT"""

IOPTR = """IN
OUT"""

DATI = """LEA
LDS  
LES  
LFS  
LGS  
LSS"""

FTI = """LAHF 
SAHF 
PUSHF
POPF 
PUSHD 
POPD """

AOI = """ADD     
ADC     
INC     
AAA     
DAA     
SUB     
SBB     
DEC     
NEG     
CMP     
AAS     
DAS     
MUL     
IMUL    
AAM  
DIV  
IDIV 
AAD  
CBW  
CWD  
CWDE 
CDQ  
DS
SI
ES
DI
CX   
AL
AX
BX
CX
DX
SS
SP
CS
D
Z"""

SI = """MOVS 
CMPS 
SCAS 
LODS 
STOS 
REP         
REPE
REPZ   
REPNE
REPNZ  
REPC        
REPNC"""

UPTI = """JMP
CALL
RET
RETF"""

CTI = """JA
JNBE
JAE
JNB
JB
JNAE
JBE
JNA
JG
JNLE
JGE
JNL
JL
JNGE
JLE
JNG
JE
JZ  
JNE
JNZ
JC     
JNC    
JNO    
JNP
JPO
JNS    
JO     
JP
JPE 
JS"""

LCI = """LOOP            
LOOPE
LOOPZ  
LOOPNE
LOOPNZ
JCXZ            
JECXZ"""

II = """INT
INTO
IRET"""

PCI = """HLT 
WAIT
ESC   
LOCK
NOP 
STC  
CLC  
CMC  
STD  
CLD  
STI  
CLI """

PI = """DW   
DB
DD
 
PROC  
ENDP  
SEGMENT
ASSUME
ENDS   
END"""

PFPI = """CLC
CMC
STC
CLD
STD
CLI
STI
NOP
HLT 
WAIT
ESC 
LOCK"""

LO = """AND
OR
XOR
NOT
TEST
SHL
SAL
SHR
SAR
ROL
ROR
RCL
RCR
"""


data = {"GDTI":list(i.strip() for i in GDTI.split("\n")),
        "IOPTR":list(i.strip() for i in IOPTR.split("\n")),
        "DATI":list(i.strip() for i in DATI.split("\n")),
        "FTI":list(i.strip() for i in FTI.split("\n")),
        "AOI":list(i.strip() for i in AOI.split("\n")),
        "SI":list(i.strip() for i in SI.split("\n")),
        "UPTI": list(i.strip() for i in UPTI.split("\n")),
        "CTI": list(i.strip() for i in CTI.split("\n")),
        "LCI": list(i.strip() for i in LCI.split("\n")),
        "II": list(i.strip() for i in II.split("\n")),
        "PCI": list(i.strip() for i in PCI.split("\n")),
        "PI": list(i.strip() for i in PI.split("\n")),
        "PFPI": list(i.strip() for i in PFPI.split("\n")),
        "LO": list(i.strip() for i in LO.split("\n")),
        "lineComment": ";"
        }



# data_ = {
#   "GDTI": "#CC7832",
#   "IOPTR": "#629755",
#   "DATI": "#0DAAEE",
#   "FTI": "#8888C6",
#   "AOI": "#9876AA",
#   "SI": "#FF33e9",
#   "UPTI": "#C70039",
#   "CTI": "#FF3333",
#   "LCI": "#33FFFB",
#   "II": "#33FF41",
#   "PCI": "#FFFC33",
#   "PI": "#FFAE33",
#   "PFPI": "#20853B",
#   "LO":"#00fff7",
#   "lineComment": "gray",
#   "char": "#00ff2a",
#   "Tabs": 4,
#   "root_bg": "#3C3f41",
# }


if __name__ == '__main__':
    with open('./keyword.json', "w") as f:
        f.write(dumps(data, indent=2))

    # with open("./Syntax.json", "w") as f:
    #     f.write(dumps(data_, indent=2))
