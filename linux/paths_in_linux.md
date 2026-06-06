# Paths in Linux

Have you ever encountered `FileNotFoundError` or similar errors and wondered how to address them? Have you been stuck in situations where the code doesn't work after being moved to another device? This post will cover everything you need to know about **paths in Linux**.

{% card %}📌 **Note**
After reading this post, readers will be able to:

- Differentiate between relative and absolute paths; comprehend the relationship among the current working directory, relative paths, and absolute paths.
- Perform path resolution and path normalization; recognize the roles of `.` and `..` in a path.
- Execute basic Linux commands for navigating the filesystem.
- Understand path-related environment variables; configure environment paths.
- Understand how the shell expands `~` to the user's home directory.
- Understand how the shell locates an executable through the `PATH` variable; inspect executable locations with `which` and `which -a`.
- Troubleshoot "File Not Found" errors in IDEs by inspecting the current working directory.
  {% endcard %}

## Absolute Path, Relative Path, and Working Directory

Imagine you are at the reptile house in a zoo, and you want to navigate to the aviary. You open Google Maps and find a path, following which you arrive at the aviary.

But all of a sudden, your phone is dead, and you cannot navigate to the aquarium from the aviary. But you happen to know the path from every place to the entrance gate and vice versa. So what you do is first go back to the entrance gate, and then head to the aquarium.

In Linux, the reptile house in the first example is the **current working directory (cwd)**, and the path from the reptile house to the aviary is a **relative path**. In the second example, the entrance gate corresponds to the **system root directory**, and the paths from the entrance gate to all places are **absolute paths**.

In Linux, the system root directory is represented as a slash `/`. If you are a Windows user, keep in mind that there are no drives (e.g., C drive) in Linux. Every absolute path starts with a slash:

- `/`: system root directory
- `/home/james`: James's home directory
- `/etc/nginx/nginx.conf`: NGINX configuration file

Every file or directory is associated with a unique absolute path for the operating system to locate. For instance, to locate the `/home/james` directory, Linux starts from the system root directory, then goes to the `home` directory, and finally arrives at the `james` directory. This procedure is deterministic.

However, in projects, we often see paths that do not start with a slash. Those are **relative paths**, for instance:

- `package.json`
- `src/main.py`
- `internal/service/user.go`

If you understand how the system locates a file with an absolute path, you may now wonder: "To locate a file with a relative path, where should the system start from?"

The answer is the current working directory (also referred to as "present working directory"). In the example at the beginning, if you want to check the path to the aviary, you must first tell Google Maps where you are currently.

In the following sections, we will discuss how to determine the current working directory. But now, let's figure out how Linux locates a file with the current working directory and a relative path.

We already know that the procedure of locating a file with an absolute path is deterministic. Therefore, we just need to combine the current working directory and the relative path into an absolute path. This is referred to as **path resolution**. For example, if we try to access `src/main.py` from `/home/james/memo`, the operating system first concatenates them into `/home/james/memo/src/main.py`, and accesses the file with this absolute path.

Every directory in Linux comes with these two special items:

- `.` refers to the **current directory**.
- `..` refers to the **parent directory**. It allows navigation one level up in the directory hierarchy.

For example, `internal/service/./user.go` is equivalent to `internal/service/user.go` because `.` can be removed without altering the path. `/home/james/memo/../coursework` is equivalent to `/home/james/coursework` because `..` moves up one directory from `/home/james/memo` to `/home/james`, and then the path continues to `coursework`. This process of removing `.` and resolving `..` in a path is called **path normalization**.

## Basic Linux Commands

To effectively navigate and manage files in Linux, it is important to familiarize yourself with some basic commands. Practicing these commands is the best way to learn, so I encourage you to open your terminal, type each command, and execute it by pressing Enter. Note that lines starting with `#` are comments, and `$` is the shell/command prompt, which is not part of the command itself.

```bash
# `pwd` (print working directory) displays your current working directory.
$ pwd

# `ls` displays all files and directories in the current working directory.
$ ls

# The `-a` flag lets the `ls` command print all hidden files and directories. In Linux, files and directories starting with `.` are hidden by default.
$ ls -a

# `mkdir` creates a directory if it does not exist.
$ mkdir demo

# `cd` (change directory) navigates you to the specified directory.
$ cd demo

# Now use the `pwd` command to check if your current working directory has been changed.
$ pwd

# `touch` creates an empty file if it does not exist.
$ touch demo.txt

# Use the `ls` command to check if `demo.txt` has been created.
$ ls

# `rm` (remove) removes a file.
$ rm demo.txt

# Use the `ls` command to check if `demo.txt` has been removed.
$ ls

# Move one level up in the directory hierarchy.
$ cd ..

# The `-r` (recursive) flag allows the `rm` command to remove a directory and everything it contains.
$ rm -r demo
```

Take ten minutes to play around with these Linux commands in the terminal and explore how _path resolution_ and _path normalization_ work in Linux. There are some exercises at the end of this post. If you can get all those right, then your understanding of Linux paths is already solid.

## Command-Line Sessions and Environment Variables

Every time you open a terminal window or a tab, a new session is created. Every session operates independently. You can check the environment variables and their values using the `env` command. Below is an excerpt from the `env` command output on my personal cloud server:

```text
LANG=C.UTF-8
USER=james
HOME=/home/james
PATH=/home/james/.pyenv/shims:/home/james/.local/bin:/home/linuxbrew/.linuxbrew/opt/postgresql@18/bin:/home/linuxbrew/.linuxbrew/opt/openjdk@21/bin:/home/james/.go/bin:/home/linuxbrew/.linuxbrew/opt/rustup/bin:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/games
SHELL=/usr/bin/zsh
PWD=/home/james
```

Each line represents a **key-value pair** (or an **entry**), where both the key and value are strings. For each entry, the key is on the left-hand side of `=`, while the value is on the right-hand side. To display the value associated with a specific key, use the command `echo $<key>`:

```bash
$ echo $USER
james
$ echo $HOME
/home/james
```

You may sometimes see a tilde (`~`) in a path. Before passing the path to a program, the shell expands `~` to the user's home directory using the value of the `HOME` variable. For example, in this case, `~/project` is expanded to `/home/james/project` before being passed along. Because a user's home directory is always an absolute path, a `~`-prefixed path becomes an absolute path after expansion. Note that this expansion is a shell feature, not an OS feature — programs that read a path from a config file or other input do not expand `~` on their own.

The operating system and applications use these environment variables throughout their lifecycles. For example, when you change to another directory, the `PWD` environment variable is changed accordingly. The `pwd` command just displays the value of `PWD`.

The value of the `PATH` variable is long and scary, but upon a closer look, you may notice that it is a set of absolute paths separated by a colon (`:`). We can use the `echo $PATH | tr : '\n'` command to make the output easier to read:

```text
/home/james/.pyenv/shims
/home/james/.local/bin
/home/linuxbrew/.linuxbrew/opt/postgresql@18/bin
/home/linuxbrew/.linuxbrew/opt/openjdk@21/bin
/home/james/.go/bin
/home/linuxbrew/.linuxbrew/opt/rustup/bin
/home/linuxbrew/.linuxbrew/bin
/home/linuxbrew/.linuxbrew/sbin
/usr/local/bin
/usr/bin
/bin
/usr/games
```

Here, `echo $PATH` outputs the value of `PATH`, and `|` pipes the output to `tr : '\n'`, which replaces all colons with newline characters (`\n`).

You can set a new environment variable using the `export` command. If the key already exists, the new value will override the previous one.

```bash
$ export TEST="test"
$ echo $TEST
test
```

To prepend an absolute path to the `PATH` variable, a conventional approach is as follows:

```bash
$ export PATH="/my/path:$PATH"
```

Here, a new string is created by concatenating `/my/path:` and the current value of `PATH`. This new value then replaces the original `PATH`. Many installation guides ask you to "add X to the PATH," where X is an absolute path. They are referring to this process.

Each session has its own set of environment variables. This means if you set a variable in one session, it won't affect any other sessions. Additionally, if you close the terminal and reopen it, any changes to environment variables will be lost. To ensure that certain environment variables are set automatically every time you start a new session, add the `export` commands to your **profile configuration file** (or simply **profile file**). The profile file is another big topic. But for now, you just need to know this: if your shell interpreter is `bash`, then your profile file is `.bashrc`; if your shell interpreter is `zsh`, then your profile file is `.zshrc`.

## Paths to Executables

In Linux, an **executable** is a file that the operating system can run as a program. It can be a **compiled binary** or a **script**.

When we execute a command, the operating system looks for an executable with the same name and runs it. But where are these executables located? For example, if I can run `python` in the current environment, then where is `python`?

You can check the absolute path of the `python` that the operating system is using with the `which python` command. In my environment, I get this:

```text
/home/james/.pyenv/shims/python
```

You may have already noticed that `/home/james/.pyenv/shims` appears in the `PATH` variable. It turns out that when we run a command, the shell iterates over all the directories listed in the `PATH` variable, concatenates each directory path with the command name, and checks whether the resulting file exists. If the command file exists, the shell executes it immediately. If no such file is found after checking all the directories, it displays a message indicating that the command was not found.

`which` alone returns only the first match. To display all the locations of executable files, pass a `-a` flag to the `which` command. For example:

```text
$ which -a ls
/usr/bin/ls
/bin/ls
```

Although there are two candidates for `ls` in the system, Linux always runs the first one.

## Paths in IDEs

If you use VSCode, PyCharm, Cursor, or other graphical IDEs, you usually can run a Python script by clicking a button. Many people don't know what happens behind the scenes, and when they come across a "File Not Found" error, they're often at a loss.

In fact, when you click the button, the IDE runs a command in the background and then displays the output directly. Depending on the IDE you use and the configuration you set up, the current working directory that the IDE uses to run the script may be the project root directory or the directory where the script resides.

When we encounter a "File Not Found" issue, we can always troubleshoot it by printing the current working directory:

```python
import os

print(os.getcwd())
```

Then we manually resolve the relative paths in the Python script and check whether the absolute paths exist.

## Compiler/Interpreter Paths

In addition to `PATH`, many compilers and interpreters rely on specific environment variables to locate related files. For instance, `g++` uses `CPATH` to find header files (e.g., `.hpp`) and `LIBRARY_PATH` to find compiled library files (e.g., `.a`, `.so`, `.dylib`). If you're using Homebrew to install C++ libraries, you’ll need to set these variables in your profile file:

```bash
export CPATH="$CPATH:/opt/homebrew/include"
export LIBRARY_PATH="$LIBRARY_PATH:/opt/homebrew/lib"
```

Here, `/opt/homebrew` is the default Homebrew root directory on macOS with Apple Silicon, but it may vary depending on your operating system or installation setup. Adding these paths ensures that `g++` can find your Homebrew-installed libraries automatically.

Another example is the Python interpreter. It uses the value of the `PYTHONPATH` environment variable to locate modules and packages when you use `import`.

Let's do an experiment. First, we set a value for `PYTHONPATH`:

```bash
export PYTHONPATH=/my/package
```

Then run the following Python script in the same session:

```python
import sys
print(sys.path)
```

You should see `/my/package` in the output list. We can add custom local packages to the Python environment using this approach, which is quite common in Python projects.

## Exercises

1\. Which of the following is NOT an absolute path?
&nbsp;&nbsp;&nbsp;&nbsp; a. `/etc/passwd`
&nbsp;&nbsp;&nbsp;&nbsp; b. `./home/james`
&nbsp;&nbsp;&nbsp;&nbsp; c. `~/demo`
&nbsp;&nbsp;&nbsp;&nbsp; d. `/root/../home/alice`

2\. Which of the following is NOT a relative path?

&nbsp;&nbsp;&nbsp;&nbsp; a. `..`
&nbsp;&nbsp;&nbsp;&nbsp; b. `../alice/demo`
&nbsp;&nbsp;&nbsp;&nbsp; c. `/.ssh/id_rsa`
&nbsp;&nbsp;&nbsp;&nbsp; d. `bob/notes/linux`

3\. Which of the following path resolutions are NOT correct? Select all that apply.

&nbsp;&nbsp;&nbsp;&nbsp; a. `/home/james` + `notes` → `/home/jamesnotes`
&nbsp;&nbsp;&nbsp;&nbsp; b. `/etc/nginx` + `./conf.d` → `/etc/nginx/./conf.d`
&nbsp;&nbsp;&nbsp;&nbsp; c. `/usr/bin/` + `mkdir` → `/usr/bin/mkdir`
&nbsp;&nbsp;&nbsp;&nbsp; d. `/home/bob/demo` + `../coursework` → `/home/bob/demo/coursework`

4\. Which of the following path normalizations are correct? Select all that apply.

&nbsp;&nbsp;&nbsp;&nbsp; a. `/home/alice/notes/../demo` → `/home/alice/notes/demo`
&nbsp;&nbsp;&nbsp;&nbsp; b. `/usr/bin/./touch` → `/usr/bin/touch`
&nbsp;&nbsp;&nbsp;&nbsp; c. `/home/james/./resume` → `home/james/resume`
&nbsp;&nbsp;&nbsp;&nbsp; d. `/home/alice/./../bob/resume` → `/home/bob/resume`

5\. Chris is currently in the `/home/chris/coursework` directory and he runs `cd src/hw1`. Which of the following outcomes are possible? Select all that apply.

&nbsp;&nbsp;&nbsp;&nbsp; a. Chris is navigated to `/src/hw1`
&nbsp;&nbsp;&nbsp;&nbsp; b. An error message is displayed, and Chris stays in the `/home/chris/coursework` directory.
&nbsp;&nbsp;&nbsp;&nbsp; c. Chris is navigated to `/home/chris/coursework/src/hw1`.
&nbsp;&nbsp;&nbsp;&nbsp; d. An error message is displayed, and Chris is navigated to `/src/hw1`.

6\. Bob has trouble navigating to `/home/bob/project/src/main`. His terminal session is as follows:

```bash
$ pwd
/home/bob
$ cd project/src
$ cd main
cd: no such file or directory: main
$ ls
test Main.java build.gradle.kts
```

Which of the following statements are correct? Select all that apply.

&nbsp;&nbsp;&nbsp;&nbsp; a. There is no directory named `main` in `/home/bob/project/src`.
&nbsp;&nbsp;&nbsp;&nbsp; b. When Bob runs the `cd main` command, he stays in the `/home/bob` directory.
&nbsp;&nbsp;&nbsp;&nbsp; c. There are three files or directories in `/home/bob/project/src`.
&nbsp;&nbsp;&nbsp;&nbsp; d. The `cd main` command creates a `main` directory in `/home/bob/project/src`.

7\. Alice adds the following command to her profile file `.bashrc`:

```bash
export PATH="$PATH:/home/alice/bin"
```

She then checks with `echo $PATH` and finds that `/home/alice/bin` has been added to `PATH`. There is a `ls` executable in `/home/alice/bin`. However, when she runs `ls`, the `/home/alice/bin/ls` is not executed. Which of the following statements are correct? Select all that apply.

&nbsp;&nbsp;&nbsp;&nbsp; a. She can check all `ls` executables in the environment using `which -a ls`.
&nbsp;&nbsp;&nbsp;&nbsp; b. If she changes the `export` statement to `export PATH="/home/alice/bin:$PATH"` and moves it to the end of the profile file, `/home/alice/bin/ls` may be executed when she runs `ls`.
&nbsp;&nbsp;&nbsp;&nbsp; c. `/home/alice/bin/ls` was not executed because she is in a wrong working directory.
&nbsp;&nbsp;&nbsp;&nbsp; d. Because she is not using `bash` as a shell interpreter, adding the `export` statement to `.bashrc` doesn't take effect.

8\. James is using a niche IDE, and he runs the following script by clicking the "run" button in the user interface.

```python
if __name__ == "__main__":
    filename = "data/raw_data.txt"

    # Read all content from the file and print it out
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        print(content)
```

The path of this file is `src/test/file.py`, relative to the project root directory. He wants to read the content from `data/raw_data.txt`, relative to the project root directory. However, after running this script, he gets a `FileNotFoundError`. He then checks the current working directory by adding the following at the beginning of the script:

```
import os

print(os.getcwd())
```

The terminal outputs `/home/james/project/src/test`.

What should the value of `filename` be to make the script work?

## Answer Key

{% details Answer Key %}

1. b
2. c
3. ad
4. bd
5. bc
6. ac
7. ab
8. `../../data/raw_data.txt`

{% enddetails %}
