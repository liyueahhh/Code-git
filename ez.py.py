# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import argparse
import os

cfg_path = r"D:\Code\python\Demo1" + "\\bin\\cfg.json"
pj_cfg_init = {"bin_path": "", "socb_path": "", "last_tc": "", "last_seed": ""}
global_cfg_init = {"cur_pj": "master", "master": pj_cfg_init}
if not os.path.exists(cfg_path):
    file_name = cfg_path.split("\\")[-1]
    file_dir = cfg_path.strip(file_name)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    # print(file_dir)
    with open(cfg_path, "w") as f:
        json.dump(global_cfg_init, f, indent=4)
    global_cfg = global_cfg_init
    print(f"A empty config was created, please config it manually, current project is {global_cfg['cur_pj']}")
else:
    with open(cfg_path, "r") as f:
        global_cfg = json.load(f)
pj_cfg = global_cfg["cur_pj"]

def project(args):
    if args.add is True:
        print(f"try to add a project, project name is {args.pj_name}")
    else:
        print(f"switch to project {args.pj_name}")


parser = argparse.ArgumentParser(description="test for arg")
subparser = parser.add_subparsers(help="sub-command help")
parser_pj = subparser.add_parser("pj", help="project manage help")
parser_pj.add_argument("pj_name", help="set project name with 'ez.py pj <name>'")
parser_pj.add_argument("--add", help="add new project with 'ez.py pj <name> --add'", action="store_true")
parser_pj.set_defaults(func=project)
parser.add_argument("-c", "--cmpl", help="cmpl_ut.pl -wave", nargs="?", const="wave")
# parser.add_argument("-c", "--cmpl", help= "编译", nargs=l"?", const="wave")
parser.add_argument("-t", "--tc", help="用例", nargs="?", const="test")
parser.add_argument("-s", "--seed", help="seed number", default=cfg_dict["last_seed"])
parser.add_argument("-m", "--mode", help="display mode when running program", choices=['mixed', 'origin', 'pure'])
parser.add_argument("--pj", help="project switch")

parser.add_argument("--set", help="set config json item", nargs=2)
parser.add_argument("--clr", help="clr config json item")
parser.add_argument("--cfg", help="show config json items", nargs="?", const="all")
args = parser.parse_args()
args.func(args)

def save_json():
    global_cfg["cur_pj"] = pj_cfg
    with open(cfg_path, "w") as f:
        json.dump(global_cfg, f, indent=4)


def show_dict(cfg_dict, mode="->", tab=1):
    for (k, v) in cfg_dict.items():
        if v is dict:
            show_dict(v, mode, tab + 1)
        else:
            if mode == "->":
                print("\t" * tab + f"{k} -> {v}")
            elif mode == "[]":
                print("\t" * tab + f"{v}[{k}]")
            else:
                print(f"unrecognized mode:{mode}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f"c : {args.cmpl}, t : {args.tc}, s : {args.seed}, m : {args.mode}, cfg : {args.cfg}")
    if args.set is not None:
        pj_cfg[args.set[0]] = args.set[1]
        save_json()
        show_dict(pj_cfg)

    if args.clr is not None:
        if args.clr in pj_cfg_init:
            print(f"Deleting {args.clr} will cause a program error, denied.")
        elif args.clr in pj_cfg:
            pj_cfg.pop(args.clr)
            save_json()
        else:
            print(f"{args.clr} is not a item of config, please check it")
        show_dict(pj_cfg)

    if args.cfg is not None:
        if args.cfg == "all":
            show_dict(pj_cfg)
        elif args.cfg in pj_cfg:
            if pj_cfg[args.cfg] is dict:
                show_dict(pj_cfg[args.cfg])
            else:
                print(f"{args.cfg} -> {pj_cfg[args.cfg]}")
        else:
            print(f"unrecognized cfg parameter : {args.cfg}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
