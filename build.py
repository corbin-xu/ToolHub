#!/usr/bin/env python3
"""
JD Supplier Label Generator 构建脚本
1. 使用 PyInstaller 打包 gui_app.py 为 dist/jd-supplier-label-generator.exe
2. 使用 Inno Setup 打包为安装程序 dist/jd-supplier-label-generator-1.1.0.exe（需已安装 Inno Setup）
"""
import subprocess
import sys
import os
from pathlib import Path

# 项目根目录（build.py 所在目录）
ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
EXE_NAME = "jd-supplier-label-generator.exe"
SPEC_FILE = ROOT / "jd-supplier-label-generator.spec"
SETUP_ISS = ROOT / "setup.iss"


def run(cmd, cwd=None, env=None):
    """执行命令，失败时退出"""
    cwd = cwd or ROOT
    print(f"[build] {subprocess.list2cmdline(cmd)}")
    r = subprocess.run(cmd, cwd=cwd, env=env or os.environ)
    if r.returncode != 0:
        print(f"[build] 命令失败，退出码: {r.returncode}")
        sys.exit(r.returncode)


def build_exe():
    """PyInstaller 打包 exe"""
    run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", str(SPEC_FILE)])
    exe = DIST / EXE_NAME
    if not exe.exists():
        print(f"[build] 未找到输出: {exe}")
        sys.exit(1)
    print(f"[build] 已生成: {exe}")
    return exe


def build_installer():
    """Inno Setup 打包安装程序（需安装 Inno Setup 并加入 PATH）"""
    # 常见安装路径
    iscc_names = ["iscc", "ISCC.exe"]
    iscc_paths = [
        Path(os.environ.get("ProgramFiles(x86)", "")) / "Inno Setup 6" / "ISCC.exe",
        Path(os.environ.get("ProgramFiles", "")) / "Inno Setup 6" / "ISCC.exe",
        Path("D:/Inno Setup 6/ISCC.exe"),
    ]
    iscc = None
    for name in iscc_names:
        try:
            r = subprocess.run([name, "/?"], capture_output=True, timeout=5)
            if r.returncode == 0:
                iscc = name
                break
        except FileNotFoundError:
            pass
    if not iscc:
        for p in iscc_paths:
            if p.exists():
                iscc = str(p)
                break
    if not iscc:
        print("[build] 未找到 Inno Setup (iscc)。请安装 Inno Setup 6 或将 ISCC.exe 加入 PATH。")
        print(f"[build] 跳过安装包步骤，仅保留 dist/{EXE_NAME}")
        return False
    run([iscc, str(SETUP_ISS)])
    print(f"[build] 安装包已生成到: {DIST}")
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="构建 JD Supplier Label Generator 可执行程序与安装包")
    parser.add_argument("--exe-only", action="store_true", help="仅打包 exe，不生成安装程序")
    parser.add_argument("--installer-only", action="store_true", help=f"仅生成安装程序（假定 dist/{EXE_NAME} 已存在）")
    args = parser.parse_args()

    if not args.installer_only:
        build_exe()
    if not args.exe_only:
        build_installer()


if __name__ == "__main__":
    main()
