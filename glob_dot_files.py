#!/usr/bin/env python3
import glob
import os
import re
import shutil


def yes(prompt: str):
    for _ in range(3):
        answer = input(f"{prompt}""y/{N}").lower()
        if not len(answer):
            return False
        if answer not in ["y", "n"]:
            continue
        return answer == "y"
    exit()


def main():
    home = os.path.expanduser("~")
    #
    ignore_patterns = [re.compile(exp)
                       for exp in set([
                           # .bash_history, .node_repl_history,
                           # .python_history, .lesshst
                           ".*history$|.lesshst$",
                           "~$",  # vim temp files .gitconfig~
                           r"\.bak$",
                           "_auth",  # auth file
                           r"^\.yarnrc$",  # skip old versions of yarn config
                           "claude.json",
                           "zcompdum.*",
                           "wget-hsts",
                           "pre-oh-my-zsh",
                           "viminfo"
                       ])]
    sep = os.path.sep

    glob_patterns = [
        fr"{home}{sep}.*",
        f"{home}{sep}.config{sep}*.toml",
        "tsconfig.json",
        f"{os.environ.get("LOCALAPPDATA", "")}{sep}clink"
    ]

    def in_ignore_patterns(basename: str):
        return next((m for exp in ignore_patterns
                     if (m := exp.search(basename)) is not None),
                    None) is not None

    def sync_patterns():
        # path -> entryName
        target_sync_files: dict[str, str] = {
            p: synced
            for pattern in glob_patterns
            for p in glob.glob(pattern)
            if os.path.isfile(p) and not in_ignore_patterns(
                synced := os.path.basename(p))
        }

        print("Found files:")
        print("\n".join([f'{k} : {v}' for (k, v)
              in target_sync_files.items()]))

        if yes("Are you sure to copy these files to cwd, "
               f"aka {os.path.realpath(os.path.curdir)}? "):
            for (p, synced) in target_sync_files.items():
                if os.path.exists(synced):
                    os.remove(synced)
                try:
                    os.link(p, synced)
                except Exception as e:
                    print(e)
                    print("Trying copy instead.")
                    shutil.copy(p, synced)
        else:
            print("File copying -- Skipped")

    def clean_up():
        # clean up
        target_clean_files = {
            path: p.name for p in os.scandir(os.path.curdir)
            if (path := os.path.realpath(p.path)) != __file__}
        remove_files = [path for (path, basename) in target_clean_files.items()
                        if in_ignore_patterns(basename)]
        if not len(remove_files):
            return
        print("Attempt to remove files:")
        print(remove_files)
        if yes("Are you sure to remove these file under cwd, "
               f"aka {os.path.realpath(os.path.curdir)}? "):
            for path in remove_files:
                os.remove(path)

    sync_patterns()
    clean_up()


if __name__ == "__main__":
    main()
