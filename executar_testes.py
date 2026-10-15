"""Executa as seis suítes isoladamente; --gui inclui os testes de janela."""
import argparse
from pathlib import Path
import subprocess
import sys


def executar(incluir_gui=False):
    raiz = Path(__file__).resolve().parent
    pastas = [raiz / f"entregavel_{i:02d}" for i in range(1, 6)] + [raiz / "projeto_final"]
    falhas = 0
    for pasta in pastas:
        print(f"\n{'=' * 60}\n{pasta.name}", flush=True)
        resultado = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(pasta), "-p", "testes*.py", "-v"], cwd=pasta)
        falhas += resultado.returncode != 0
    print(f"\nResultado: {len(pastas) - falhas}/{len(pastas)} suítes aprovadas", flush=True)
    if incluir_gui:
        resultado = subprocess.run([sys.executable, "-m", "unittest", "test_interface_grafica", "-v"],
                                   cwd=raiz / "projeto_final")
        falhas += resultado.returncode != 0
    return 1 if falhas else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gui", action="store_true", help="incluir testes gráficos; requer display/Tkinter")
    sys.exit(executar(parser.parse_args().gui))
