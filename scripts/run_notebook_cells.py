"""
Runner para executar as primeiras N células de um notebook .ipynb no ambiente atual.
Salva figuras geradas e imprime as saídas de cada célula.

Uso:
    python scripts/run_notebook_cells.py --notebook notebooks/play_with_mast_data.ipynb --cells 6
"""
import argparse
import nbformat
import sys
from pathlib import Path
import io
import contextlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def run_cells(nb_path: str, max_code_cells: int = 6):
    nb_path = Path(nb_path)
    if not nb_path.exists():
        print(f"Erro: notebook não encontrado: {nb_path}")
        return 2

    nb = nbformat.read(str(nb_path), as_version=4)
    code_cells = [c for c in nb.cells if c.cell_type == 'code']
    total = min(len(code_cells), max_code_cells)
    print(f"Executando {total} de {len(code_cells)} células de código do notebook: {nb_path.name}\n")

    # Cria pasta de saída para imagens
    out_dir = nb_path.parent / 'executed_outputs'
    out_dir.mkdir(parents=True, exist_ok=True)

    # Ambiente global para exec
    g = {
        '__name__': '__main__',
        '__file__': str(nb_path),
    }

    # Garante que src/ do projeto (dentro do diretório atual) esteja no sys.path
    import os as _os, sys as _sys
    project_src = Path.cwd() / 'src'
    if project_src.exists():
        if str(project_src) not in _sys.path:
            _sys.path.insert(0, str(project_src))
        print(f"(runner) Inserido no sys.path: {project_src}")
    else:
        print(f"(runner) Aviso: pasta src não encontrada em: {project_src}")

    for idx, cell in enumerate(code_cells[:total], start=1):
        code = cell.source
        print('\n' + '='*80)
        print(f"Célula {idx}:\n")
        print(code)
        print('\n--- Saída:')

        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                with contextlib.redirect_stderr(stdout):
                    # Execute the code
                    exec(compile(code, f'<notebook-cell-{idx}>', 'exec'), g)
        except Exception as e:
            print(stdout.getvalue())
            print(f"❌ Erro ao executar célula {idx}: {e}")
            import traceback
            traceback.print_exc()
            return 3

        # Print captured stdout
        out_text = stdout.getvalue()
        if out_text.strip():
            print(out_text)

        # Save any open matplotlib figures
        figs = [plt.figure(n) for n in plt.get_fignums()]
        if figs:
            for i, fig in enumerate(figs, start=1):
                out_fig = out_dir / f'cell_{idx}_fig{i}.png'
                fig.savefig(str(out_fig), bbox_inches='tight')
                print(f"[Figura salva] {out_fig}")
            plt.close('all')
        else:
            print('[Sem figuras geradas]')

    print('\n' + '='*80)
    print('Execução concluída com sucesso.')
    print(f'Imagens e outputs (se houver) em: {out_dir}')
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--notebook', required=True)
    parser.add_argument('--cells', type=int, default=6)
    args = parser.parse_args()
    sys.exit(run_cells(args.notebook, args.cells))
