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
import json

import tomllib
from autocodegen import TemplateConfig, generate

if __name__ == "__main__":
    spath = Path(__file__)
    acg_templates = spath.parent

    with open(acg_templates / "config.toml", "rb") as f:
        xxx = tomllib.load(f)
        print(json.dumps(xxx, indent=2))

    # exit()

    acg_templates = acg_templates.resolve(strict=True)
    target_root = acg_templates.parent.resolve(strict=True)
    project_name = target_root.stem

    print(project_name)
    print(target_root)
    print(acg_templates)

    config = TemplateConfig(
        project_name=project_name,
        acg_templates=acg_templates,
        target_root=target_root,
    )

    generate("nix-hop--poetry-pyside", config)

    config["target_root"] = target_root / "hop"

    generate("poetry-pyside-starter", config)
