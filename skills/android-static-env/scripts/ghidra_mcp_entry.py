#!/usr/bin/env python3
"""Start upstream PyGhidra-MCP with the verified local Chroma model cache."""
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--model-cache', required=True, type=Path)
    args, remaining = parser.parse_known_args()
    # Chroma 1.x hardcodes Path.home() here and has no cache-path env option.
    # Redirect only this model cache; retain the real user HOME for other tools.
    from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2
    ONNXMiniLM_L6_V2.DOWNLOAD_PATH = args.model_cache.resolve()
    if not (args.model_cache / 'onnx/model.onnx').is_file():
        raise RuntimeError('Missing verified ONNX model; rerun mcp_setup.py install --servers ghidra')
    from pyghidra_mcp.server import main as server_main
    sys.argv = ['pyghidra-mcp', *remaining]
    server_main()


if __name__ == '__main__':
    main()
