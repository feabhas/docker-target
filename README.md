# Feabhas Docker Training Project

# Getting Started

Download this git repo to your local machine. If possible you should clone
the repo to your local hard drive and avoid using network attached storage
as the editing and build process is disk I/O intensive.

Avoid placing the folder in an area that is mirrored using OneDrive, 
Google Drive or similar for the same reasons.

Install and then startup VS Code. Use the extension icon (left hand icon
bar) to install the Dev Containers extension from Microsoft. You may need to 
restart VS code after doing this. 

In the bottom left corner of the screen there will now be a green icon with 
an `><` symbol, click on this and select:

   * **Open Folder in container...** 

and open the folder you have just created.

When VS Code opens the folder this will download a Docker container from 
`feabhas/docker-projects:latest`. This container is configured with a
toolchain for building Feabhas embedded training projects including:

   * Arm Embedded Toolchain (11.2)
   * Customised xPack QEMU Washing Machine Simulator (WMS) emulator
   * Host based GCC 11.2 and GDB
   * Build tools GNU Make and CMake 2.23

The container is about 2GB and will take a noticeable amount 
of time to download.

VS Code will connect to the remote container as user `feabhas` (password
`ubuntu`) and copy files from an embedded target project template to
the working folder. Within the container the working folder is mapped
onto `~/workspace`.

This folder will now contain the files for building applications
and running them on the Feabhas QEMU WMS emulator. 

The Docker container does not use the embedded QEMU graphics but opens 
a diagnostic interface on port 8888 which is mapped for access from the host.

# Building an Application

The Feahbas project build process uses [CMake](https://cmake.org/) as the underlying
build system. CMake is itself a build system generator and we have configured
it to generate the build files used by [GNU Make](https://www.gnu.org/software/make/).

Using CMake is a two step process: generate build files and then build. To simplify 
this and to allow you to add additional source and header files we have 
created a front end script `build.sh` to automate the build.

You can add additional C/C++ source and header files to the `src` directory. If 
you prefer you can place your header files in the `include` directory.

From within VS Code you can use the keyboard shortcut `Ctrl-Shift-B` 
to run one of the build tasks:
    * **Build** standard build
    * **Clean** to remove object and executable files
    * **Reset** to regenerate the CMake build files

Alternatively at the project root do:

```
$ ./build.sh
```

This will generate the file `build/debug/Application.elf`, additional size and 
hex files used by some flash memory software tools are also generated.

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

# Building an exercise solution

To build any of the exercise solutions run the script:
```
$ ./build-one.sh N 
```
where `N` is the exercise number. The exercises must be stored in a folder
called `exercises` in one of the following locations:
   * The $HOME folder
   * The workspace`s parent or grandparent folder
   * A sub-folder in the workspace folder

**NOTE:** this script will copy all files in the `src` directory to 
the `src.bak` directory having
removed any files already present in `src.bak`.

# Runing an Application in QEMU

The Docker based training project runs a version of QEMU that opens
a diagnostics interface on port 8888 which can be accessed from the 
host operating system. A graphic represenion of the emulated WMS 
hardware is provided by a Python script (`qemu-qms.py`) that must
be run on the host. 

To run the application without debugging:

   * from the **host** launch the `qemu-wms.py` Python script
   * in VS code press Ctrl-Shft-P and type `test` 
   * in the popup list select **Tasks: Run Test task**
   * in the list of tasks select **Run QEMU**
   * in the host Python GUI click on the **Connect** button 

To run with debugging:

   * set a breakpoint in the code
   * from the **host** launch the `qemu-wms.py` Python script
   * press F5 (or run **Debug** task **QEMU Debug**)
   * within 30 secs click **Connect** on the Python GUI

As the application runs any changes to the state of the hardware are
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

Once `main` exits the QEMU emulator will stop. On the Python GUI
click on the **Halt** button  (displayed when a connection is established) 
to stop the emulation. Closing the Python GUI 
will not stop the emulation; the Python GUI can connect to an already running
emulator.

Use the Python GUI to monitor and interact with the program. 

The Cortex-M board is to the left and has a reset button (middle left) which 
can be clicked with the mouse to reset the hardware, restarting the program. 
Four LED lights are shown on the bottom right of the board and will display 
coloured boxes when the appropriate GPIO-D pins are set. 

The WMS board is on the right and updates as the GPIO-D pins are set
and cleared:
   * seven segment display updates on changes to pins 8-11
   * the motor animates to shown on/off cw/acw rotation on pins 12-13
   * the latching mode (pin 14) for the PS keys has no direct visual feedback

The WMS boards has mouse click input for GPIO-D input pins:
   * Accept and Cancel keys (pins 5 & 4)
   * keys PS1, PS2 & PS3 (pins 1,2,3) switch on the led lights above the key
   * when latched the PS* leds remain illuminated when the key is released
   * door open key (pin 0) toggles open/closed when pressed
   * motor feedback sensor (pin 6) is raised once every 0.1 secs when the motor is on
   * click on the centre of the motor spinner to pulse the motor sensor (pin 6)

## Running Applications Using USART3

There are extra launch scripts configure under VS Code **Test Tasks** 
to run with USART3 connected to the serial port 7777. 

When using the Python GUI click on the `Connect+Serial` button to connect 
to both diagnostic and ports. The bottom area of the GUI will display an interactive text 
area you can use to send and receive using USART3.

A `telnet` command is provided in the Docker image configured for single
character I/O  if you prefer to use the command line for USART teating.

# VS Code tasks and launch actions

VS Code tasks:

   * build
   * clean
   * reset

VS Code test tasks:

   * Run QEMU -- `run-qemu.sh` script to start a diagnostic server on port 8888
   * Run QEMU serial -- run with USART3 on serial port 7777
   * Run QEMU container -- `run-qemu.sh` to run no graphics in the container
   * Run QEMU container serial -- no graphics with USART3 on port 7777

VS Code debug tasks (use F5 or Debug view):

   * QEMU Debug -- use host Python GUI
   * QEMU Debug serial -- host Python GUI and USART3
   * QEMU Debug container -- no grpahics QEMU in container
   * QEMU Debug container serial -- no grpahics QEMU in container

# VS Code Debugging

To debug your code with the interactive (visual) debugger press the `<F5>` key or use the
**Run -> Start Debugging** menu.

The debug sessions may stop at the entry to the `main` function and display 
a red error box saying:

```
Exception has occurred.
```

This is normal: just close the warning popup and use the debug 
icon commands at the top of the code window to
manage the debug system. The icons are (from left to right):
  **continue**, **stop over**, **step into**, **step return**, 
  **restart** and **quit**
  
A number of debug launch tasks are shown in a drop down list at the top of the debug view.

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
The QEMU simulation will halt at the first instruction waiting for a GDB connection.

2. In another terminal, run GDB with
```
$ ./gdb-qemu.sh
```

Diagnostic output will appear in the `gdb` window ending with prompt to continue:
```
...
..
-- Type <RET> for more, q to quit, c to continue without paging--
```

Press <Enter> at this point to see the code of the `main` function and the `(gdb)` 
prompt for debug commands.

3. Type 
   * `c` (continue) to run
   * `n` for next (step-over)
   * `s` for step (step-in)

If GPIO-D pins 8..11 are written to, output will appear in the QEMU windows, such as:
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
