# Feabhas Docker Training Project

**Contents**
- [Feabhas Docker Training Project](#feabhas-docker-training-project)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Obtaining the course exercises](#obtaining-the-course-exercises)
  - [Using the Visual Studio Code IDE](#using-the-visual-studio-code-ide)
- [Developing an embedded application](#developing-an-embedded-application)
  - [Building the application image](#building-the-application-image)
  - [Running an application in QEMU](#running-an-application-in-qemu)
  - [Running Applications Using USART3](#running-applications-using-usart3)
- [Building an exercise solution](#building-an-exercise-solution)
- [Creating the template starter projects](#creating-the-template-starter-projects)
- [VS Code tasks and launch actions](#vs-code-tasks-and-launch-actions)
- [VS Code Debugging](#vs-code-debugging)
- [GDB debugging in the container](#gdb-debugging-in-the-container)
  - [Exiting a session](#exiting-a-session)
- [Static analysis using clang-tidy](#static-analysis-using-clang-tidy)
- [Testing support](#testing-support)
- [C/C++ Versions](#cc-versions)
- [C++20 Modules](#c20-modules)
- [Disclaimer](#disclaimer)

# Prerequisites

You will need the following software to use this project:

   * [Docker desktop](https://www.docker.com/products/docker-desktop/)
   * [Visual Studio Code](https://code.visualstudio.com/) and DevContainers extension (installed through VS Code)
   * [Python](https://www.python.org/) (3.9 or later) and TkInter *see note*

*TkInter*: On Windows TkInter is installed alongside python but on 
other platforms you will need to install it manually. Please make sure
you install TkInter for Python3, for example:
   * Ubuntu (Debian, Mint): `sudo apt-get install python3-tk`
   * Fedora: `sudo dnf install python3-tkinter`
   * Arch: `sudo pacman -S tk`
   * RHEL (CentOs, Oracle): `sudo yum install python3-tkinter`
   * macOS: `brew install python-tk`

# Getting Started

Download this [Docker Target](https://github.com/feabhas/docker-target) git
repo to your local machine using either git or unpacking 
the ZIP archive. 

If possible you should store the repo on your local hard 
drive and avoid using network attached storage as the 
editing and build process is disk I/O intensive.

Your cloned folder will be called `docker-target` by default but you can 
rename this folder if you wish. This is your workspace folder that you
would normally open using [Visual Studio Code](https://code.visualstudio.com/)
(see later).

We have initialised an empty git repo in the workspace so that you can 
save your working files at any time.

## Obtaining the course exercises

Inside your `docker-target` workspace subfolder called `scripts` there is 
a `configure.py` script that can be used to copy the course exercises 
into your workspace. 

You can run this script at any time from your host environment
or, once you've opened the project workspace, from a terminal
window in VS Code using the command:

```
$ python3 configure.py
```

The script will supply a list of suitable courses for you to choose from and
these exercises will be download from the appropriate Feabhas GitHub repo.

You will now have a sub-folder with a name of the form `<COURSE>_exercises`.
where `<COURSE>` is the unique code for your course (such as cpp11-501).

If you know you course code you can supply this as a command line parameter
to the script.

Alternatively your course joining instructions will provide a link
to a [Feabhas GitHub](https://github.com/orgs/feabhas/repositories) 
repo containing the the exercise solutions and optional starter templates
required for the training exercises. 

Clone this GitHub `*_exercises` repo into the `docker-target` workspace 
you have just created. 

## Using the Visual Studio Code IDE

If you do not have Visual Studio Code installed then provided your company
security policy permits you to install applications you can 
download it from [Visual Studio Code] (https://code.visualstudio.com/).

Start VS Code and click on the extension icon in the left hand panel
(it shows four squares with the top right one detached from the rest).

In the search box at the top of the left hand panel enter the text

```
dev containers
```
Make sure you include the space. In the **Dev Containers** extension
(from Microsoft) shown in the list of matched extension click 
on the **Install** button and add the Dev Containers extenions.
You may need to restart VS code after doing this. 

In the bottom left corner of the screen there will now be a coloured
icon with an `><` symbol, click on this and select:

   * **Open Folder in container...** 

and open the `docker-target` workspace folder containing
this project.

When VS Code opens the folder this will download a Docker container from 
`feabhas/ubuntu-projects:latest`. This container is configured with a
toolchain for building Feabhas host training projects including:

   * Arm GNU Toolchain
   * QEMU Washing Machine Simulator (WMS)
   * WMS Python GUI application to execute on the host
   * Ubuntu GNU Toolchain and GDB
   * Build tools GNU Make, Ninja and CMake
   * Test tools `googletest`, `gmock`, `puncover` and `valgrind`
  
The container is about 3GB and will take a noticeable amount 
of time to download.

VS Code will connect to the remote container as user `feabhas` (password
`ubuntu`) and copy files from an embedded target project template to
the working folder. Within the container the working folder is mapped
onto `~/workspace`.

The `docker-target` workspace folder will now contain the files 
for building and running applications on the Ubuntu image.

***Note:** The Docker container does not use the embedded QEMU graphics 
but opens a diagnostic interface on port 8888 which is mapped for access 
by the WMS Pythn GUI that is run on the host (see later).

# Developing an embedded application

## Building the application image

The Feahbas project build process uses [CMake](https://cmake.org/) as 
the underlying build system. CMake is itself a build system generator 
and we have configured it to generate the build files used 
by [GNU Make](https://www.gnu.org/software/make/).

Using CMake is a two step process:

   * generate the build configuration files
   * build the application

To simplify this process and to allow you to easily add additional 
source and header files we have created a front end script `build.sh` 
to automate the build.

You can add additional C/C++ source and header files to the `src` directory. If 
you prefer you can place your header files in the `include` directory.

From within VS Code you can use the keyboard shortcut `Ctrl-Shift-B` 
to run one of the build tasks:
    * **Build** standard build
    * **Clean** to remove object and executable files
    * **Reset** to regenerate the CMake build files

Alternatively from within a command shell terminal enter the command:

```
$ ./build.sh
```

This `build.sh` script will detect any source file changes and generate
a new build configuration if required. If new source files are created 
in the `src` folder these will be automatically detected and 
included in the build.

The image `Application.elf` is created in the folder `build/debug`.

You can add a `-v` option to see the underlying build commands:

```
$ ./build.sh -v
```

To delete all object files and recompile the complete project use
the `clean` option:

```
$ ./build.sh clean
```

To clean the entire build directory and regenerate a new CMake build 
configuration use the `reset` option:

```
$ ./build.sh reset
```

## Running an application in QEMU

The Docker based training project runs a version of QEMU that opens
a diagnostics interface on port 8888 which can be accessed from the 
host operating system. A graphic representation of the emulated WMS 
hardware is provided by a Python script (`qemu-qms.py`) that 
**must be run on the host**.

 Make sure you have installed **Python TkInter** on your host if you
are using Linux or macOS (as described in the 
[Prerequisites](#prerequisites) section). 

To run the application without debugging:

   * from your **host** launch the `qemu-wms.py` Python script
   * switch to VS code press Ctrl-Shift-P and type `test task` 
   * in the popup list select **Tasks: Run Test task**
   * in the list of tasks select **Run QEMU**
   * switch to the WMS Python GUI and click on the **Connect** button 

To run with debugging:

   * set a breakpoint in the code
   * from the **host** launch the `qemu-wms.py` Python script
   * press F5 (or run **Debug** task **QEMU Debug**)
   * within 30 secs click **Connect** on the Python GUI

As the application executes changes to the state of the hardware are
displayed on the graphic window and diagnostic messages written to the 
terminal window:

```
[led:A on]
[seven-segment 1]
[led:C on]
[seven-segment 5]
[led:A off]
[seven-segment 4]
```

When the `main` function exits the QEMU emulator will stop.

Once the GUI is connected to the emulator you can use the buttons:

   * `Disconnect` to detach the GUI but leave the emulation running
   * `Halt` to stop the emulation and detach the GUI
   
Closing the Python GUI using the `Quit` button or the normal windows close icon
will also stop the emulation.

On tye WMS Python GUI window the STM32F407 series Cortex-M board is
shown on the left and has a reset button (middle of the board) which can 
be clicked with the mouse to reset the hardware and restart the application. 
Four LED lights are shown on the bottom right of the  board and will display 
coloured boxes when the appropriate GPIO-D pins are set. 

The WMS emulator is shown on the right and animated updates will shown when
GPIO-D pins are set and cleared:
   * seven segment display updates on changes to pins 8-11
   * the motor animates to shown on/off cw/acw rotation on pins 12-13
   * the latching mode (pin 14) for the PS keys has no direct visual feedback

The WMS boards has mouse click input for GPIO-D input pins:
   * Accept and Cancel keys (pins 5 & 4)
   * keys PS1, PS2 & PS3 (pins 1,2,3) switch on the led lights above the key
   * when latched the PS* LEDs remain illuminated when the key is released
   * door open key (pin 0) toggles open/closed when pressed
   * motor feedback sensor (pin 6) is raised once every 0.1 secs when the motor is on
   * click on the centre of the motor spinner to pulse the motor sensor (pin 6)

## Running Applications Using USART3

There are extra launch scripts configured under VS Code **Test Tasks** 
to use when serial I/O on USART3 is required. The QEMU emulator connects
network port 7777 to the USART3 serial port.

When using the Python GUI click on the `Connect+Serial` button to connect 
to both diagnostic and serial ports. The bottom area of the GUI will display an 
interactive text area you can use to send and receive characters.

A `telnet` command is provided in the Docker image configured for single
character I/O  if you prefer to use the ubuntu command line for USART3 testing.

# Building an exercise solution

You must have downloaded the course solutions and stored them in your
workspace as described at the start of this README. If you haven't done so
already run the command

```
$ python3 configure.py
```

And select your course from the list of courses you're presented with.

To build a solution run the command:

```
$ python3 copy_solution.py
```

Select the required solution from the list you are shown. 

You may supply the solution number (optionally omitting a leading zero)
on the command line to avoid the interactive prompt.

On loading a solution the script will:

   * save and commit your current files using git
   * replace all of your source files with those from the the solution
   * rebuild the solution

**Note:** If the script cannot save your source files using git then they are
copied to a `src.bak` folder. Only that last set of source files are saved in
the backup folder.

Alternatively you can build any of the exercise solutions using the 
`build-one.sh` bash script:

```
$ ./build-one.sh N 
```

Where *N* is the exercise number. The exercises must be stored in the 
workspace folder in one of the following locations:
   * A cloned github repo name ending `_exercises`
   * An `exercises/solutions`sub-folder in the workspace
   * A `solutions`sub-folder in the workspace

**NOTE:** this script will copy all files in the `src`  and
`include` directories to a `src.bak` directory in the workspace; 
any files already present in `src.bak` will be deleted.

# Creating the template starter projects

Some training courses supply one or more template starter projects containing
a working application that will be refactored during the exercises.

These templates are used to generate multiple project workspaces in 
named sub folders. To generate the sub projects run the command:

```
$ ./build-template.sh
```

This will generate fully configured projects for each starter template
in a sub folder in the root workspace. Each project
contains a fully configured CMake based build system including a 
copy of the solutions folder. The original toolchain build files in the
project are moved to a `project` sub-folder as they are no longer required.

For each exercise you can now open the appropriate sub-project
folder and work within that folder to build and run your application.

**Note:** if there is a single starter template this will be copied
directly into the `src` and `include` folders rather than create a new
sub folder.

# VS Code tasks and launch actions

VS Code tasks:

   * **Build**
   * **Clean**
   * **Reset**

VS Code test tasks:

   * **Run QEMU** -- `run-qemu.sh` script to start a diagnostic server on port 8888
   * **Run QEMU serial** -- run with USART3 on serial port 7777
   * **Run QEMU container** -- `run-qemu.sh` to run no graphics in the container
   * **Run QEMU container serial** -- no graphics with USART3 on port 7777

VS Code debug tasks (use F5 or Debug view):

   * **QEMU Debug** -- host Python GUI
   * **QEMU Debug serial** -- host Python GUI and USART3
   * **QEMU Debug container** -- no graphics QEMU in container
   * **QEMU Debug container serial** -- no graphics QEMU in container

# VS Code Debugging

To debug your code with the interactive (visual) debugger press the `<F5>` 
key or use the **Run -> Start Debugging** menu.

The debug sessions may stop at the entry to the `main` function and display 
a red error box saying:

```
Exception has occurred.
```

This is normal: just close the warning popup and use the debug 
icon commands at the top of the code window to
manage the debug system. The icons are (from left to right):

   *  **continue** - **stop over** - **step into** - 
      **step return** - **restart** - **stop**
  
A number of debug launch tasks are shown in a drop down list at the top of
the debug view.

Preselect one of the launch options before pressing `<F5>` to debug with:

    * **QEMU debug** to debug using the Python GUI **Connect**
    * **QEMU debug serial** to debug using the Python GUI **Connect+serial** 
    * **QEMU debug container** run without the Python GUI
    * **QEMU debug container serial** to debug without the Python GUI 

#  GDB debugging in the container

To debug a program just using the GPIO port requires two terminal sessions.

1. In one terminal invoke the following script:
```
$ ./run_qemu.sh gdb
```
A monitor window will appear and there will be some debug output. 
The QEMU simulation will halt at the first instruction waiting for a 
GDB connection.

2. In another terminal, run GDB with
```
$ ./gdb-qemu.sh
```

Diagnostic output will appear in the `gdb` window ending with prompt to 
continue:
```
...
..
-- Type <RET> for more, q to quit, c to continue without paging--
```

Press <Enter> at this point to see the code of the `main` function 
and the `(gdb)` prompt for debug commands.

3. Type 
   * `c` (continue) to run
   * `n` for next (step-over)
   * `s` for step (step-in)

If GPIO-D pins 8..11 are written to, output will appear in the QEMU windows, 
such as:

```
[led:A on]
[seven-segment 1]
[led:C on]
[seven-segment 5]
[led:A off]
[seven-segment 4]
```

## Exiting a session

To exit:
1. Use Ctrl-C in the GDB window to interrupt an executing process to return to
the `gdb` prompt.

2. Enter the kill (`k`) command to stop the remote qemu process.

3. Finally `q` will quit gdb

# Static analysis using clang-tidy

The CMake build scripts create a `clang-tidy` target in the 
generated build files if `clang-tidy` is in the command search 
path (`$PATH` under Linux).

To check all of the build files run the command:
```
$ ./build.sh clang-tidy
```

To run `clang-tidy` as part of the compilation process edit 
the `CMakeLists.txt` file and uncomment the line starting with
 `set(CMAKE_CXX_CLANG_TIDY`.

# Testing support

Create a sub-directory called `tests` with it's own `CMakeList.txt` and define
your test suite (you don't need to include `enable_testing()` as this is done
in the project root config).

Invoke the tests by adding the `test` option to the build command:

```
./build.sh test
```
Tests are only run on a successful build of the application and all tests.

You can also use `cmake` or `ctest` directly.

If a test won't compile the main application will still have been built. 
You can temporarily rename the `tests` directory to stop CMake building 
the tests, but make sure you run a `./build.sh reset` to regenerate 
the build scripts.

# C/C++ Versions

The build system supports compiling against different versions of C and 
C++ with the default set in `MakeLists.txt` as C11 and C++17. 
The `build.sh` and `build-one.sh` scripts accept a version option to 
choose a different language option. 

For example, to compile for:
   * C99 add the option `--c99` (or `--C99`) or for 
   * C++23 add `--cpp23` (or `--c++23` `--C++23` `--CPP23`)

# C++20 Modules

Support for compiling C++ modules is enabled by creating a file `Modules.txt` 
in the `src` folder and defining each module filename on a separate 
line in this file. The build will always use GNU Make to ensure modules
are compiled in the order defined in the `Modules.txt` file. Following MSVC 
and VS Code conventions the modules should be defined in `*.ixx` files.

# Disclaimer

Feabhas is furnishing these items *"as is"*. Feabhas does not provide any
warranty of them whatsoever, whether express, implied, or statutory,
including, but not limited to, any warranty of merchantability or fitness
for a particular purpose or any warranty that the contents their will
be error-free.

In no respect shall Feabhas incur any liability for any damages, including,
but limited to, direct, indirect, special, or consequential damages arising
out of, resulting from, or any way connected to the use of the item, whether
or not based upon warranty, contract, tort, or otherwise; whether or not
injury was sustained by persons or property or otherwise; and whether or not
loss was sustained from, or arose out of, the results of, the item, or any
services that may be provided by Feabhas.

The items are intended for use as an educational aid.Typically code solutions 
will show best practice of language features that have been introduced during 
the associated training, but do not represent production quality code. 
Comments and structured documentation are not included because the code 
itself is intended to be studied as part of the learning process.
