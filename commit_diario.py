#!/usr/bin/env python3
"""
commit_diario.py - faz um commit por dia em um repositório seu e dá push.

Uso:
    python commit_diario.py /caminho/do/repositorio

Pré-requisitos:
    - Git instalado e já autenticado (SSH ou token) para dar push sem pedir senha
    - Repositório clonado localmente, SEU (não um fork), na branch padrão
    - git config user.email igual a um e-mail cadastrado na sua conta do GitHub
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ARQUIVO_LOG = "log-diario.md"


def git(repo: Path, *args: str) -> str:
    resultado = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return resultado.stdout.strip()


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python commit_diario.py /caminho/do/repositorio")
        return 1

    repo = Path(sys.argv[1]).expanduser().resolve()
    if not (repo / ".git").exists():
        print(f"Não é um repositório git: {repo}")
        return 1

    agora = datetime.now()
    hoje = agora.strftime("%Y-%m-%d")
    log = repo / ARQUIVO_LOG

    # Evita commit duplicado no mesmo dia
    if log.exists() and hoje in log.read_text(encoding="utf-8"):
        print(f"Já existe commit de hoje ({hoje}). Nada a fazer.")
        return 0

    try:
        git(repo, "pull", "--rebase")
        with log.open("a", encoding="utf-8") as f:
            f.write(f"- {agora.strftime('%Y-%m-%d %H:%M:%S')}\n")
        git(repo, "add", ARQUIVO_LOG)
        git(repo, "commit", "-m", f"chore: atualização diária {hoje}")
        git(repo, "push")
    except subprocess.CalledProcessError as erro:
        print("Erro no git:", erro.stderr or erro)
        return 1

    print(f"Commit de {hoje} enviado com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())