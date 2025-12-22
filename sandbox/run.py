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
from autocodegen import ProjectConfig, generate


if __name__ == "__main__":
    spath = Path(__file__)
    acg_dir = spath.parent

    with open(acg_dir / "config.toml", "rb") as f:
        # project_config: ProjectConfig = cast(
        #     ProjectConfig, cast(object, tomllib.load(f))
        # )
        # print(json.dumps(project_config, indent=2))
        project_config = ProjectConfig.load(tomllib.load(f), acg_dir=acg_dir)
        print(
            json.dumps(
                project_config.model_dump(mode="json"),
                indent=2,
                ensure_ascii=False,
            )
        )

    acg_dir = acg_dir.resolve(strict=True)
    target_root = acg_dir.parent.resolve(strict=True)
    project_name = target_root.stem

    print(project_name)
    print(target_root)
    print(acg_dir)

    generate(
        project_name=project_name,
        template_name="nix-hop--poetry-pyside",
        target_root=target_root,
        templates_root=acg_dir,
    )

    generate(
        project_name=project_name,
        template_name="poetry-pyside-starter",
        target_root=target_root / "hop",
        templates_root=acg_dir,
    )
