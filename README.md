# Data Recovery Tool

A powerful and flexible data recovery tool built using Python and Click, designed to recover browser data, network information, system details, and application credentials.

## Features

- Recover browser passwords, history, and bookmarks.
- Retrieve saved WiFi passwords and network information.
- Extract system details.
- Recover account credentials for Discord, Minecraft, Epic Games, Uplay, PostgreSQL, etc...

## Installation

Ensure you have Python installed (Python 3.9+ recommended).

### 1. Clone the Repository

```sh
git clone https://github.com/hirusha-adi/Data-Recovery.git
cd Data-Recovery
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

## Usage

The tool provides multiple commands for data recovery.

### General Options

- `-s, --silent` : Silent mode (no console output).
- `-v, --verbose` : Verbose mode (detailed logs).
- `-l, --log` : Enable logging to a file.

### Commands

#### Recover Everything

```sh
python recover.py all
```

#### Browser Data Recovery

```sh
python recover.py browser [OPTIONS]
```

Options:
- `-p, --passwords` : Recover saved browser passwords.
- `-h, --history` : Recover browser history.
- `-b, --bookmarks` : Recover bookmarks.

Example:
```sh
python recover.py browser -p -h
```

#### Network Data Recovery

```sh
python recover.py network [OPTIONS]
```

Options:
- `-w, --wifi` : Recover saved WiFi passwords.
- `-i, --info` : Retrieve network information.

Example:
```sh
python recover.py network -w
```

#### System Information Recovery

```sh
python recover.py system
```

#### Application Data Recovery

```sh
python recover.py apps [OPTIONS]
```

Options:
- `-d, --discord` : Recover Discord tokens.
- `-mc, --minecraft` : Recover Minecraft accounts.
- `-eg, --epicgames` : Recover Epic Games accounts.
- `-up, --uplay` : Recover Uplay accounts.
- `-psql, --postgresql` : Recover PostgreSQL credentials.

Example:
```sh
python recover.py apps -d -mc
```

## License

This project is built by [@hirusha-adi](https://github.com/hirusha-adi). Usage of this tool must comply with ethical guidelines and legal restrictions.

---

⚠ **Disclaimer:** This tool is intended for personal use only. Unauthorized access to data without consent is illegal.


(Font name: Pawp. https://manytools.org/hacker-tools/ascii-banner/)