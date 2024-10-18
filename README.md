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

1. **Clone this repository**:
    ```bash
    git clone https://github.com/omusymcomp/rcsssetup.git
    cd rcsssetup
    ```
2. **Install Python 3 and pip**
    ```bash
    sudo apt-get install -y python3 python3-pip
    ```
3. **Install git-lfs**
    ```bash
    sudo apt-get install git-lfs
    ```
4. **Set up the environment**:
    Use the script to install everything necessary to run RoboCup Soccer 2D League:
    ```bash
    python3 setup.py 
    ```
### Command-Line Options

This tool provides several command-line options to control the setup and installation process.

- `-d` or `--base_dir`  
  - Description: Specify the base directory for setting up the environment.  
  - Default: `$HOME/rcss`  
  - Example:  
    ```bash
    ./setup.sh -d /path/to/your/directory
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

  - Example:  
    ```bash
    ./setup.sh -t all
    ./setup.sh -t librcsc
    ```

- `--upgrade_packages`  
  - Description: Upgrade packages before compilation.  
  - Example:  
    ```bash
    ./setup.sh --upgrade_packages
    ```

- `--is_installation_of_essential_packages`  
  - Description: Specify if you want to install essential packages before compilation.  
  - Example:  
    ```bash
    ./setup.sh --is_installation_of_essential_packages
    ```

- `--add_environment_variable`  
  - Description: Add environment variables. This is required during the initial setup.  
  - Example:  
    ```bash
    ./setup.sh --add_environment_variable
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

## Start a match

To start a match between the installed rc2023 teams, uset the following command:
```bash
python3 auto_match.py -l left_team -r right team
```
- example
```bash
python3 auto_match.py -l HELIOS2023 -r CYRUS
```

### Command-Line Options

This script provides several command-line options to control match settings:

- `-d` or `--base_dir`
  - Description: Specify the base directory for the environment.
  - Default: `$HOME/rcss`
  - Example:
    ```bash
    python3 -d /path/to/your/base/directory
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

## Envirionment Variables

you can configure the following environment variables foe advance setups:
- `TEAM_DIR`: Directory where teams are stored.
- `MATCH_LOG_DIR`: Directory where auto match logs are saved.
```bash
export TEAM_DIR=~/robocup/teams
export MATCH_LOG_DIR=~/robocup/logs
```

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


