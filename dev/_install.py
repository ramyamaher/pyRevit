"""Manage tasks related to the build environment"""
# pylint: disable=invalid-name,broad-except
import sys
import os.path as op
from collections import namedtuple
from typing import Dict

from scripts import utils

RequiredTool = namedtuple("RequiredTool", ["name", "get", "step"])


REQUIRED_TOOLS = [
    RequiredTool(name="dotnet", get="", step="build"),
    RequiredTool(name="msbuild", get="", step="build"),
    RequiredTool(name="go", get="", step="build"),
    RequiredTool(name="gcc", get="", step="build"),
    RequiredTool(
        name="iscc", get=r"C:\Program Files (x86)\Inno Setup 6", step="release"
    ),
    RequiredTool(name="certutil", get="", step="release"),
    RequiredTool(
        name="signtool",
        get=r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.17763.0\x86",
        step="release",
    ),
    RequiredTool(name="nuget", get="", step="release"),
    RequiredTool(name="choco", get="", step="release"),
]


def install(_: Dict[str, str]):
    """Prepare build environment"""
    print("Preparing build environment")
    raise NotImplementedError()


def check(_: Dict[str, str]):
    """Check build environment"""
    all_pass = True
    # check required tools
    for rtool in REQUIRED_TOOLS:
        has_tool = utils.where(op.join(rtool.get, rtool.name))
        if has_tool:
            print(utils.colorize(f"[ <grn>PASS</grn> ]\t{rtool.name} is ready"))
        else:
            all_pass = False
            print(
                utils.colorize(
                    f"[ <red>FAIL</red> ]\t{rtool.name} is "
                    f"required for {rtool.step} step. "
                    f"see --help"
                )
            )

    if not all_pass:
        sys.exit(1)

    return all_pass


def get_tool(tool_name: str):
    """Get full path of a required build tool"""
    for rtool in REQUIRED_TOOLS:
        if rtool.name == tool_name:
            return op.join(rtool.get, rtool.name)
