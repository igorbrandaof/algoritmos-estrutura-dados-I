"""Executa todos os arquivos testes.py de forma isolada por subprocesso."""
from pathlib import Path
import subprocess,sys
raiz=Path(__file__).resolve().parent
pastas=[raiz/f'entregavel_{i:02d}' for i in range(1,6)]+[raiz/'projeto_final']
falhas=0
for pasta in pastas:
 print('\n'+'='*60+'\n'+pasta.name,flush=True)
 resultado=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(pasta),'-p','testes.py','-v'],cwd=pasta)
 if resultado.returncode:falhas+=1
print(f'\nResultado: {len(pastas)-falhas}/{len(pastas)} suites aprovadas')
sys.exit(1 if falhas else 0)
