{
  inputs = {
    ml-ops.url = "github:Preemo-Inc/nix-ml-ops";
    ml-ops.inputs.systems.url = "github:nix-systems/default";
  };
  outputs = inputs @ { ml-ops, ... }:
    ml-ops.lib.mkFlake { inherit inputs; } {
      imports = [
        ml-ops.flakeModules.devcontainer
        ml-ops.flakeModules.nixIde
        ml-ops.flakeModules.nixLd
        ml-ops.flakeModules.pythonVscode
        ml-ops.flakeModules.devenvPythonWithLibstdcxx
      ];
      perSystem = { pkgs, config, lib, system, ... }: {
        ml-ops.devcontainer = {
          nixago.requests.".vscode/settings.json".data = {
            "python.defaultInterpreterPath" = "./.venv/bin/python";
            "python.analysis.typeCheckingMode" = "basic";
            "jupyter.debugJustMyCode" = false;
          };

          nixago.requests.".vscode/launch.json".data = {
            configurations = [
              {
                name = "Python: gradient_langchain_tool_demo.py";
                type = "python";
                request = "launch";
                module = "chainlit";
                args = [ "run" "gradient_langchain_tool_demo.py" ];
                console = "integratedTerminal";
                justMyCode = false;
              }
            ];
          };

          devenvShellModule = {
            languages = {
              python = {
                enable = true;
                poetry = {
                  enable = true;
                  install.allExtras = true;
                };
              };
            };
          };
        };

      };
    };
}
