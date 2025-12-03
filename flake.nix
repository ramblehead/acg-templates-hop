{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    pre-commit-hooks,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        overlays = [
          (final: prev: {
            python = prev.python314;
            nodejs = prev.nodejs_24;
          })
        ];

        pkgs = import nixpkgs {inherit overlays system;};

        runtimePackages = with pkgs; [
          python
          poetry
          uv

          nodejs
          yarn

          git
          typos
          alejandra
        ];

        runtimeLibs = with pkgs; [
          stdenv.cc.cc

          # Qt libs needed by PySide6 / PyQt6
          qt6.qtbase
          qt6.qtwayland
          qt6.qtdeclarative
          qt6.qtsvg
          qt6.qttools

          # X11/XCB
          xorg.libX11
          xorg.libXext
          xorg.libXrender
          xorg.libXfixes
          xorg.libXrandr
          xorg.libXi
          xorg.libXcursor
          xorg.libXinerama

          xorg.libxcb
          xorg.xcbutil
          xorg.xcbutilimage
          xorg.xcbutilkeysyms
          xorg.xcbutilwm
          xorg.xcbutilcursor
          xorg.xcbutilrenderutil

          # MESA GL — REQUIRED for libGL.so.1
          mesa
          libglvnd

          pkg-config
          fontconfig
          glib
          freetype
          zstd
          libxkbcommon
          wayland

          # dbus

          # glibc # libc, ld-linux, ...
          # stdenv.cc.cc.lib # libstdc++, libgcc_s
          # zlib
          # openssl
          # libuuid
          # curl
          # icu
          # libffi
          # expat
          # bzip2
          # xz
          # # lzma
          # attr
          # acl
          # libxcrypt
          # Add more if you hit a missing .so (see `ldd` later)
        ];
      in {
        checks = {
          pre-commit-check = pre-commit-hooks.lib.${system}.run {
            src = ./.;
            hooks = {
              typos = {
                enable = true; # Source code spell checker
                settings = {
                  write = true; # Automatically fix typos
                  ignored-words = [];
                };
              };
              prettier = {
                enable = true; # Markdown & TS formatter & etc.
                settings = {
                  write = true; # Automatically format files
                  binPath = "yarn prettier";
                  configPath = "./prettier.config.js";
                };
              };
              alejandra.enable = true; # Nix linter & formatter
            };
          };
        };

        devShells.default = pkgs.mkShell {
          packages = runtimePackages;

          # NIX_LD =
          #   pkgs.lib.strings.trim
          #   (builtins.readFile "${pkgs.stdenv.cc}/nix-support/dynamic-linker");
          NIX_LD = pkgs.stdenv.cc.bintools.dynamicLinker;
          NIX_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath runtimeLibs;

          # Qt plugin paths
          QT_PLUGIN_PATH = pkgs.lib.concatStringsSep ":" [
            "${pkgs.qt6.qtbase}/lib/qt6/plugins"
            "${pkgs.qt6.qtwayland}/lib/qt6/plugins"
          ];

          QT_QPA_PLATFORM_PLUGIN_PATH = "${pkgs.qt6.qtbase}/lib/qt6/plugins/platforms";
          QML2_IMPORT_PATH = "${pkgs.qt6.qtdeclarative}/lib/qt6/qml";

          shellHook = ''
            export LD_LIBRARY_PATH="$NIX_LD_LIBRARY_PATH"

            echo "''$(${pkgs.python}/bin/python --version)"
            echo "Using NIX_LD=$NIX_LD"
            echo "Using NIX_LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH"
            echo "Using LD_LIBRARY_PATH=$LD_LIBRARY_PATH"
            echo

            ${self.checks.${system}.pre-commit-check.shellHook}
          '';
        };
      }
    );
}
