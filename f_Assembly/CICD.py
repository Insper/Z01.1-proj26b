import os
import subprocess

# Arquivos relevantes para os exercícios
ARQUIVOS_MONITORADOS = (
    "src/",
)

# Máximo 
MAX_COMMIT = 5


def git(*args):
    resultado = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return resultado.stdout


def test_limite_de_arquivos_por_commit():
    base = os.environ.get("AUDIT_BASE")
    alvo = os.environ.get("AUDIT_TARGET", "HEAD")

    assert base, "Defina AUDIT_BASE com uma base confiável."

    commits = git(
        "rev-list",
        "--reverse",
        f"{base}..{alvo}",
    ).splitlines()

    problemas = []

    for commit in commits:
        arquivos = git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "-m",
            "--first-parent",
            commit,
        ).splitlines()

        # Conta apenas arquivos dos exercícios.
        monitorados = {
            arquivo
            for arquivo in arquivos
            if any(
                arquivo.startswith(prefixo)
                for prefixo in ARQUIVOS_MONITORADOS
            )
        }

        if len(monitorados) > MAX_COMMIT:
            problemas.append(
                f"{commit[:10]}: {len(monitorados)} arquivos "
                f"alterados: {', '.join(sorted(monitorados))}"
            )

    assert not problemas, (
        "Problema   de CI/CD:\n"
        + "\n".join(problemas)
    )

