"""Command-line cybersecurity asset inventory with JSON persistence."""
from __future__ import annotations

import json
import ipaddress
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "assets.json"
ASSET_TYPES = ("Workstation", "Server", "Router", "Switch", "Application")
RISK_LEVELS = ("Low", "Medium", "High", "Critical")
SECURITY_STATUSES = ("Secure", "Warning", "Vulnerable")
FIELDS = (
    ("name", "Asset Name"),
    ("asset_type", "Asset Type"),
    ("ip_address", "IP Address"),
    ("operating_system", "Operating System"),
    ("department", "Owner/Department"),
    ("risk_level", "Risk Level"),
    ("security_status", "Security Status"),
)


def load_assets(path: Path = DATA_FILE) -> list[dict[str, str]]:
    """Load assets from JSON, returning an empty inventory if no file exists."""
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"Could not read asset data from {path}: {exc}") from exc
    if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
        raise ValueError("Asset data must be a JSON list of asset objects.")
    return data


def save_assets(assets: list[dict[str, str]], path: Path = DATA_FILE) -> None:
    """Persist inventory as readable UTF-8 JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(assets, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def normalize_choice(value: str, options: tuple[str, ...], label: str) -> str:
    """Return a canonical choice or raise a helpful validation error."""
    for option in options:
        if value.strip().casefold() == option.casefold():
            return option
    raise ValueError(f"{label} must be one of: {', '.join(options)}.")


def validate_asset(asset: dict[str, str], existing_ids: set[str] | None = None) -> None:
    """Validate required fields, controlled values, IP address, and unique ID."""
    required = ("asset_id",) + tuple(key for key, _ in FIELDS)
    for key in required:
        if not str(asset.get(key, "")).strip():
            raise ValueError(f"{key.replace('_', ' ').title()} cannot be blank.")
    try:
        ipaddress.ip_address(asset["ip_address"].strip())
    except ValueError as exc:
        raise ValueError("IP Address must be a valid IPv4 or IPv6 address.") from exc
    asset["asset_type"] = normalize_choice(asset["asset_type"], ASSET_TYPES, "Asset Type")
    asset["risk_level"] = normalize_choice(asset["risk_level"], RISK_LEVELS, "Risk Level")
    asset["security_status"] = normalize_choice(
        asset["security_status"], SECURITY_STATUSES, "Security Status"
    )
    if existing_ids is not None and asset["asset_id"].casefold() in existing_ids:
        raise ValueError(f"Asset ID {asset['asset_id']} already exists.")


def find_asset(assets: list[dict[str, str]], asset_id: str) -> dict[str, str] | None:
    """Find an asset by case-insensitive ID."""
    return next((a for a in assets if a["asset_id"].casefold() == asset_id.strip().casefold()), None)


def format_asset(asset: dict[str, str]) -> str:
    """Format one asset using the assignment's expected display labels."""
    labels = (
        ("Asset ID", "asset_id"), ("Asset Name", "name"), ("Asset Type", "asset_type"),
        ("IP Address", "ip_address"), ("OS", "operating_system"),
        ("Department", "department"), ("Risk Level", "risk_level"),
        ("Status", "security_status"),
    )
    return "\n".join(f"{label:<13}: {asset[key]}" for label, key in labels)


def summary(assets: list[dict[str, str]]) -> dict[str, int]:
    """Count assets by risk and vulnerable status."""
    return {
        "Total Assets": len(assets),
        "Critical Assets": sum(a["risk_level"] == "Critical" for a in assets),
        "High Risk Assets": sum(a["risk_level"] == "High" for a in assets),
        "Medium Risk Assets": sum(a["risk_level"] == "Medium" for a in assets),
        "Low Risk Assets": sum(a["risk_level"] == "Low" for a in assets),
        "Vulnerable Assets": sum(a["security_status"] == "Vulnerable" for a in assets),
    }


def show_assets(assets: list[dict[str, str]]) -> None:
    print("\n=========================================")
    print("  CYBERSECURITY ASSET INVENTORY")
    print("=========================================")
    if not assets:
        print("No assets are currently recorded.")
    for asset in assets:
        print(format_asset(asset))
        print("-----------------------------------------")
    for label, count in summary(assets).items():
        print(f"{label:<20}: {count}")
    print("=========================================")


def prompt_nonempty(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print(f"{label} cannot be blank.")


def prompt_choice(label: str, options: tuple[str, ...]) -> str:
    while True:
        print(f"{label} options: {', '.join(options)}")
        value = input(f"{label}: ").strip()
        try:
            return normalize_choice(value, options, label)
        except ValueError as exc:
            print(exc)


def prompt_asset(asset_id: str | None = None) -> dict[str, str]:
    asset = {"asset_id": asset_id or prompt_nonempty("Asset ID")}
    for key, label in FIELDS:
        if key == "asset_type":
            asset[key] = prompt_choice(label, ASSET_TYPES)
        elif key == "risk_level":
            asset[key] = prompt_choice(label, RISK_LEVELS)
        elif key == "security_status":
            asset[key] = prompt_choice(label, SECURITY_STATUSES)
        elif key == "ip_address":
            while True:
                value = prompt_nonempty(label)
                try:
                    ipaddress.ip_address(value)
                    asset[key] = value
                    break
                except ValueError:
                    print("IP Address must be a valid IPv4 or IPv6 address.")
        else:
            asset[key] = prompt_nonempty(label)
    return asset


def add_asset(assets: list[dict[str, str]]) -> None:
    asset = prompt_asset()
    try:
        validate_asset(asset, {a["asset_id"].casefold() for a in assets})
    except ValueError as exc:
        print(f"Cannot add asset: {exc}")
        return
    assets.append(asset)
    save_assets(assets)
    print("Asset added successfully.")


def search_asset(assets: list[dict[str, str]]) -> None:
    asset_id = prompt_nonempty("Enter asset ID to search")
    asset = find_asset(assets, asset_id)
    print("No asset found." if asset is None else f"\n{format_asset(asset)}")


def update_asset(assets: list[dict[str, str]]) -> None:
    asset_id = prompt_nonempty("Enter asset ID to update")
    current = find_asset(assets, asset_id)
    if current is None:
        print("No asset found.")
        return
    replacement = prompt_asset()
    other_ids = {a["asset_id"].casefold() for a in assets if a is not current}
    try:
        validate_asset(replacement, other_ids)
    except ValueError as exc:
        print(f"Cannot update asset: {exc}")
        return
    current.clear()
    current.update(replacement)
    save_assets(assets)
    print("Asset updated successfully.")


def delete_asset(assets: list[dict[str, str]]) -> None:
    asset_id = prompt_nonempty("Enter asset ID to delete")
    asset = find_asset(assets, asset_id)
    if asset is None:
        print("No asset found.")
        return
    assets.remove(asset)
    save_assets(assets)
    print("Asset deleted successfully.")


def main() -> None:
    try:
        assets = load_assets()
    except ValueError as exc:
        print(exc)
        return
    actions: dict[str, Any] = {
        "1": lambda: add_asset(assets),
        "2": lambda: search_asset(assets),
        "3": lambda: update_asset(assets),
        "4": lambda: delete_asset(assets),
        "5": lambda: show_assets(assets),
        "6": lambda: print("\n".join(f"{k}: {v}" for k, v in summary(assets).items())),
    }
    while True:
        print("\n------------- MAIN MENU -------------")
        print("1. Add asset\n2. Search asset by ID\n3. Update asset\n4. Delete asset")
        print("5. Display all assets\n6. Display security summary\n7. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "7":
            print("Exiting Asset Inventory. Goodbye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Enter a number from 1 to 7.")
        else:
            action()


if __name__ == "__main__":
    main()
