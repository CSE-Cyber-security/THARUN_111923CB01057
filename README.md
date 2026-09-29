<<<<<<< HEAD
# Cybersecurity Asset Inventory

A command-line asset inventory for recording an organization's IT assets and reviewing their security risk. It supports adding, searching, updating, deleting, and displaying assets. Asset records are saved locally in JSON so they remain available after restarting the program.

## Requirements

- Python 3.10 or newer
- No third-party packages

## Run

From this project folder, run:

```bash
python src/asset_inventory.py
```

On some Windows installations, use `py` instead of `python`:

```powershell
py src/asset_inventory.py
```

Choose a menu option from 1 to 7. New assets require a unique asset ID, name, asset type, IP address, operating system, owner/department, risk level, and security status. The accepted asset types are Workstation, Server, Router, Switch, and Application; accepted risk levels are Low, Medium, High, and Critical; accepted statuses are Secure, Warning, and Vulnerable. The IP address is validated as IPv4 or IPv6.

## Data storage

The program reads and writes `data/assets.json`. Start with an empty JSON list (`[]`) or add records through the program. Keep the file in the project structure so the program can locate it.

## Features

- Create assets with validation and case-insensitive unique IDs
- Search, update, and delete records by ID
- Display all asset details in the assignment's output style
- Summarize total assets by risk level and count vulnerable assets
- Persist inventory changes in JSON

See `tests/test_cases.md` for the assignment verification scenarios. Screenshots illustrating the required operations are stored in `screenshots/`.
=======
# WEEK_1_THARUN_111923CB01057
>>>>>>> f72e1dcc18783a591289102be9adc0d050cb61e8
