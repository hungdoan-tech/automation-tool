E='~'
B=print
import os as A,requests as I,zipfile as J
H='OneDrive '
F=A.path.expanduser(E)
D='Documents'
for C in A.listdir(F):
	if A.path.isdir(A.path.join(F,C))and C.startswith(H):D=C;break
G='automation_tool'
K=A.path.join(A.path.expanduser(E),D,G)
def L():
	if A.path.exists(K):B('Already containing the source code');return
	L=f"https://github.com/hungdoan-tech/automation-tool/archive/main.zip";B('Start download source');H=I.get(L)
	if H.status_code==200:
		C=A.path.join(A.path.expanduser(E),D);F=A.path.join(C,'automated_task.zip')
		with open(F,'wb')as M:M.write(H.content)
		B('Download source successfully')
		with J.ZipFile(F,'r')as N:N.extractall(C)
		A.rename(A.path.join(C,'automation-tool-main'),A.path.join(C,G));A.remove(F);B(f"Extracted source code and placed it in {C}")
	else:B('Failed to download the source')
if __name__=='__main__':L()