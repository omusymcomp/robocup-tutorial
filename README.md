# rcsssetup

This tool automates the process of setting up the RoboCup Soccer 2D League environment, installing teams, and configuring dependencies. With a single command, you can get your RoboCup simulation up and running quickly.

## Features

- Automated environment setup for RoboCup Soccer 2D League
- Team installation and configuration in one step
- Easy-to-use command-line interface
- Supports multiple teams and configurations
- Works on Linux-based systems

## Requirements

- **Git**: Ensure Git is installed on your system.
- **Python 3.x**: The tool uses Python scripts for automation.

## Installation

1. **Install git, Python3, pip, and git-lfs**
    ```bash
    sudo apt-get install -y git python3 python3-pip git-lfs
    ```
2. **Clone this repository**:
    ```bash
    git clone https://github.com/omusymcomp/rcsssetup.git
    ```
3. **Set up the environment**:
    Use the script to install everything necessary to run RoboCup Soccer 2D League:
    ```bash
    cd rcsssetup
    python3 setup.py 
    ```

### Command-Line Options

This tool provides several command-line options to control the setup and installation process.

- `-d` or `--base_dir`  
  - Description: Specify the base directory for setting up the environment.  
  - Default: `$HOME/rcss`  
  - Example:  
    ```bash
    python3 setup.py -d /path/to/your/directory
    ```

- `-t` or `--install_target`  
  - Description: Specify the target to install. `all` installs everything, `minisetup` installs the minimal setup required to run the simulation. For individual tools or teams, choose from the following:
    - `all`: Installs all tools and teams
    - `minisetup`: Installs only the minimal setup required to run the simulation
    - `tools`: Installs only the tools
    - `teams`: Installs only the teams
    - `librcsc`: Installs `librcsc`
    - `rcssserver`: Installs `rcssserver`
    - `soccerwindow2`: Installs `soccerwindow2`
    - `rcssmonitor`: Installs `rcssmonitor`
    - `fedit2`: Installs `fedit2`
    - `loganalyzer3`: Installs `loganalyzer3`
    - `helios_base`: Installs `helios_base`
    - `helios`: Installs `helios`
  - Default: `all`

  - Example:  
    ```bash
    python3 setup.py -t all
    python3 setup.py -t librcsc
    ```

- `--upgrade_packages`  
  - Description: Upgrade packages before compilation.  
  - Example:  
    ```bash
    python3 setup.py --upgrade_packages
    ```

- `--is_installation_of_essential_packages`  
  - Description: Specify if you want to install essential packages before compilation.  
  - Example:  
    ```bash
    python3 setup.py --is_installation_of_essential_packages
    ```

- `--add_environment_variable`  
  - Description: Add environment variables. This is required during the initial setup.  
  - Example:  
    ```bash
    python3 setup.py --add_environment_variable
    ```

## Directory Tree
<pre>
$HOME
└ rcss
     ├ tools
     │     ├ librcsc
     │     ├ rcssserver 
     │     ├ rcssmonitor
     │     ├ soccerwindow2
     │     ├ loganalyzer3
     │     └ fedit2
     │
     └ teams  
           ├ rc2022 
           │      ├ helios2022
           │      ├ ...
           │      └ ...
           ├ rc2023
           │      ├ HELIOS2023
           │      ├ ...
           │      └ ...
           └ base_team
                  ├ librcsc (for helios-base)
                  └ helios-base
</pre>

## Start a auto match

To start a match between the installed rc2023 teams, uset the following command:
```bash
python3 auto_match.py
```

### Command-Line Options

This script provides several command-line options to control match settings:

- `-d` or `--base_dir`
  - Description: Specify the base directory for the environment.
  - Default: `$HOME/rcss`
  - Example:
    ```bash
    python3 auto_match.py -d /path/to/your/base/directory
    ```

- `-l` or `--left_team_name`
  - Description: Specify the name of the team to play on the left side. 
  - Default: `HELIOS2023`
- `-r` or `--right_team_name`
  - Description: Specify the name of the team to play on the right side. 
  - Default: `CYRUS`
  - Example:  
    ```bash
    python3 auto_match.py -l HELIOS2023 -r CYRUS
    ```

- `-n` or `-match_number`
  - Description: Enable synchronized mode. When this flag is set, the server runs in synchronous mode.
  - Default: `Disabled`
  - Example:
    ```bash
    python3 auto_match.py -n 5
    ```

- `is_synch_mode`
  - Description: Specify the number of matches to be played.
  - Default: `3`
  - Example:
    ```bash
    python3 auto_match.py --is_synch_mode
    ```

### Mathch Logs

Auto match logs are saved in the directory:

```bash
$BASE_DIR/log_analysis/log/YYYYMMDDHHMMSS/
```

### Envirionment Variables

you can configure the following environment variables foe advance setups:
- `TEAM_DIR`: Directory where teams are stored.
- `MATCH_LOG_DIR`: Directory where auto match logs are saved.
```bash
export TEAM_DIR=~/robocup/teams
export MATCH_LOG_DIR=~/robocup/logs
```

## Start a match manually

To start a match manually:
 
1. Start the server

    Launch the rcssserver with the following command:
    ```bash
    rcssserver
    ```

2. Launch the monitor

    Open the monitor to view the match visually. Run:
    ```bash
    soccerwindow2
    ```
    Alternatively, if installed, use sswindow2 to start the monitor with standard settings:
    ```bash
    sswindow2
    ```

3. Start the teams

    In separate terminal windows, navigate to the directory where each team's executable or startup script is located. Launch each team by executing:
    ```bash
    ./team_start_script
    ```
    (Replace`team_start_script`with the actual script name for each team.)

4. Start the match
    With the server and monitor running and both teams connected, go to the monitor window. Click anywhere on the monitor screen to display the "Kick Off" button. Then, either click this button or press Control + K to start the match. The game will commence in real time on the monitor.

By following these steps, you can manually initiate and observe a match in the RoboCup Soccer Simulation 2D League.

## Libraries and helios-base

- **[librcsc](https://github.com/helios-base/librcsc)**
- **[rcssserver](https://github.com/rcsoccersim/rcssserver)**
- **[rcssmonitor](https://github.com/rcsoccersim/rcssmonitor)**
- **[soccerwindow2](https://github.com/helios-base/soccerwindow2)**
- **[loganalyzer3](https://github.com/opusymcomp/loganalyzer3)**
- **[fedit2](https://github.com/helios-base/fedit2)**
- **[helios-base](https://github.com/helios-base/helios-base)**


## References

- Hidehisa Akiyama, Tomoharu Nakashima, HELIOS Base: An Open Source Package for the RoboCup Soccer 2D Simulation, In Sven Behnke, Manuela Veloso, Arnoud Visser, and Rong Xiong editors, RoboCup2013: Robot World XVII, Lecture Notes in Artificial Intelligence, Springer Verlag, Berlin, 2014. http://dx.doi.org/10.1007/978-3-662-44468-9_46


