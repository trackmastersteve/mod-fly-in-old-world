# Mod - Fly in Old World
This module enables flying mounts in older expansion zones (Azeroth) for World of Warcraft (3.3.5a / AzerothCore). It provides custom items, spell mappings, and vendor integrations so players can purchase and learn old-world flight.

## Prerequisites & Requirements
AzerothCore server environment (running and operational).

World of Warcraft 3.3.5a Client.

Python 3 (for executing the DBC patching utility).

Database management tool (like MySQL Workbench, phpMyAdmin, or terminal CLI).

## Installation & Setup Guide
### Step 1: Clone the Module into Your Server
* Navigate to your AzerothCore modules directory (typically located at `azerothcore-wotlk/modules/`):

```
cd azerothcore-wotlk/modules/
```

* Clone or place this repository folder (`mod-fly-in-old-world`) directly into your modules directory.

### Step 2: Apply the Server Database SQL Files
* Execute the provided SQL installation script against your world database (`acore_world`) to register the custom item template and add it to vendor inventories (such as Hira Snowdawn and Grunda Bronzewing):

```
docker compose exec -T ac-database mysql -u acore -p acore_world < path/to/mod-fly-in-old-world/sql/your_script.sql
```
(Alternatively, run the SQL statements manually using your preferred database GUI client).

### Step 3: Generate Client-Side DBC Patches
Because client items and spell tooltips require local rendering adjustments, you must patch your client DBC files:

* Ensure your extracted base `Item.dbc` and `Spell.dbc` files are placed in your working directory.

* Run the included patching script to generate your custom item ID (`900002`), bind the proper book display ID (`61330`), apply the heirloom quality coloring, and inject the custom Azeroth flight description:

```
python3 patch-dbc-for-flying.py
```
This will generate the updated `Item.dbc` and `Spell.dbc` files.

### Step 4: Package and Install the Client Patch
* Create or update your custom MPQ patch file (e.g., `patch-W.mpq`) using an MPQ editor.

* Place the newly generated `Item.dbc` and `Spell.dbc` inside the `DBFilesClient/` folder structure within your MPQ archive.

* Drop the `patch-W.mpq` file into your World of Warcraft client’s `Data/` (or `Data/enUS/`) directory.

### Step 5: Clear Cache and Launch
Crucial: Delete your client's local cache folder (`Cache/WDB/`) to force the game client to read the new item names, display icons, and tooltips correctly.

Restart your AzerothCore server container/services.

Launch your game client, visit the vendor, and verify your custom Tome of Old World Flight!
