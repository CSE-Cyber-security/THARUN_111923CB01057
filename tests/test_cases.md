# Test Cases Cybersecurity Asset Inventory

| ID | Scenario | Input / Action | Expected Result |
|---|---|---|---|
| TC01 | Add valid asset | Unique ID, valid IPv4, allowed type/risk/status, all required fields | Asset is saved to `data/assets.json` and success is shown. |
| TC02 | Add valid IPv6 asset | Unique ID and valid IPv6 address | Asset is accepted and saved. |
| TC03 | Duplicate ID | Add an ID already in the inventory (case-insensitive) | Add is rejected; existing record remains unchanged. |
| TC04 | Blank required field | Submit a blank name, OS, department, or other required field | Prompt repeats; blank data is not saved. |
| TC05 | Invalid asset type | Enter a value outside Workstation, Server, Router, Switch, Application | Prompt repeats until a valid type is entered. |
| TC06 | Invalid risk level | Enter a value outside Low, Medium, High, Critical | Prompt repeats until a valid risk is entered. |
| TC07 | Invalid security status | Enter a value outside Secure, Warning, Vulnerable | Prompt repeats until a valid status is entered. |
| TC08 | Invalid IP address | Enter malformed IP text | Prompt repeats; asset is not saved with an invalid address. |
| TC09 | Search existing asset | Search by stored ID with different letter case | Matching asset details are displayed. |
| TC10 | Search missing asset | Search for an ID that is not stored | “No asset found.” is displayed. |
| TC11 | Update existing asset | Search by ID, then enter a complete valid replacement record | Stored record is updated and persisted. |
| TC12 | Update with duplicate ID | Change an asset ID to an ID used by another record | Update is rejected; original record stays unchanged. |
| TC13 | Delete existing asset | Delete a stored ID | Asset is removed from memory and JSON file. |
| TC14 | Delete missing asset | Delete an unknown ID | “No asset found.” is displayed; data remains unchanged. |
| TC15 | Display inventory | Select display all with multiple records | All records and total/risk/vulnerable counts are shown. |
| TC16 | Empty inventory | Display or summarize when JSON list is empty | Zero counts are shown and no crash occurs. |
| TC17 | Invalid menu choice | Enter text or a number outside 1–7 | Helpful validation message appears and menu is shown again. |
| TC18 | Persistence | Add an asset, exit, and restart | Previously saved asset remains available. |
