#!/usr/bin/env python
# Hey Emacs, this is -*- coding: utf-8; mode: python -*-

# /// script
# requires-python = "==3.14.*"
#
# dependencies = ["autocodegen"]
#
# [tool.uv.sources]
# autocodegen = { path = "../../../acg-templates-hop/hop/autocodegen", editable = true }
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

    acg_templates = spath.parent.resolve(strict=True)
    project_root = acg_templates.parent.resolve(strict=True)
    project_name = project_root.stem

    print(project_name)
    print(project_root)
    print(acg_templates)

    config = Config(
        project_name=project_name,
        project_root=project_root,
        acg_templates=acg_templates,
    )

    generate("nix-hop--poetry-pyside", config)

    config["project_root"] = project_root / "hop"

    generate("poetry-pyside-starter", config)
