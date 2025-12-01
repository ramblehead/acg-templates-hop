#!/usr/bin/env python
# Hey Emacs, this is -*- coding: utf-8; mode: python -*-

# /// script
# requires-python = "==3.14.*"
#
# dependencies = ["autocodegen"]
#
# [tool.uv.sources]
# autocodegen = { path = "../hop/autocodegen", editable = true }
#
# [dependency-groups]
# dev = [
#   "black~=25.11.0",
#   "basedpyright~=1.34.0",
#   "ruff~=0.14.7",
#   "ruff-lsp~=0.0.62",
# ]
# ///

from pathlib import Path

from autocodegen import Config, generate

if __name__ == "__main__":
    spath = Path(__file__)
    project_name = spath.stem
    project_parent = spath.parent.resolve(strict=True)
    project_root = project_parent / f"{project_name}-test"

    project_root.mkdir(exist_ok=True)
    acg_root = (project_parent.parent / "hop" / "templates").resolve(
        strict=True,
    )

    config = Config(
        project_name=project_name,
        project_root=project_root,
        acg_root=acg_root,
    )

    generate(project_name, config)
