# RoboCupSoccerSetup

This tool automates the process of setting up the RoboCup Soccer 2D League environment, installing teams, and configuring dependencies. With a single command, you can get your RoboCup simulation up and running quickly.

## Features

- Automated environment setup for RoboCup Soccer 2D League
- Team installation and configuration in one step
- Easy-to-use command-line interface
- Supports multiple teams and configurations
- Works on Linux-based systems

## Requirements

- **Git**: Ensure Git is installed on your system.
- **Docker**: (Optional) If you plan to use Docker to run simulations.
- **Python 3.x**: The tool uses Python scripts for automation.

## Installation

1. **Clone this repository**:
    ```bash
    git clone https://github.com/your-username/rcsssetup.git
    cd rcsssetup
    ```
2. **Install Python 3 and pip**
    ```bash
    sudo apt-get install -y python3 python3-pip
    ```
3. **Set up the environment**:
    Use the script to install everything necessary to run RoboCup Soccer 2D League:
    ```bash
    python3 setup.py 
    ```
## Command-Line Options

This tool provides several command-line options to control the setup and installation process.

### Basic Options

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

## Usage

### Start the server

After installation, you can start the RoboCup 2D server with the following command:

```bash
rcssserver
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
           ├ rc2023 
           │      ├ HELIOS2023
           │      ├ ...
           │      └ ...
           ├ rc2024
           │      ├ HELIOS2024
           │      ├ ...
           │      └ ...
           └ base_team
                  ├ librcsc (for helios-base)
                  └ helios-base
</pre>

## Start a match

To start a match between the installed teams, uset the following command:
```bash
./auto_match.py teamA teamB
```
- example
```bash
./run_match.py HELIOS helios-base
```

## Envirionment Variables

you can configure the following environment variables foe advance setups:
- `TEAM_DIR`: Directory where teams are stored.
- `MATCH_LOG_DIR`: Directory where match logs are saved.
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


