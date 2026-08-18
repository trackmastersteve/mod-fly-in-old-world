# Mod - Fly in Old World
This module enables flying mounts in older expansion zones (Azeroth) for World of Warcraft (3.3.5a / AzerothCore). It provides custom items, spell mappings, and vendor integrations so players can purchase and learn old-world flight.

## Prerequisites & Requirements
* AzerothCore server environment (running and operational).

* World of Warcraft 3.3.5a Client.

* Python 3 (for executing the DBC patching utility).

* Database management tool (like MySQL Workbench, phpMyAdmin, or terminal CLI).

* MPQ Editor (e.g., Ladik's MPQ Editor) to package the custom client patch.

## Installation & Setup Guide
### Step 1: Clone the Module into Your Server
* Navigate to your AzerothCore modules directory (typically located at `azerothcore-wotlk/modules/`):

```
cd azerothcore-wotlk/modules/
```

* Clone or place this repository folder (`mod-fly-in-old-world`) directly into your modules directory.

### Step 2: Compile the Server
Because this module utilizes a custom WotLK C++ `ItemScript` to bypass the vanilla spell engine, you must recompile your worldserver binary to include the new logic.

If using Docker:

```
docker compose build ac-worldserver
```

### Step 3: Apply the Server Database SQL Files
* Execute the provided SQL installation script against your world database (`acore_world`) to register the custom item template, define the script hooks, and add the Tome to vendor inventories (Hira Snowdawn, Grunda Bronzewing, and Wind Rider Jahubo):

```
docker compose exec -T ac-database mysql -u root -ppassword acore_world < modules/mod-fly-in-old-world/data/sql/db-world/base/db_world_mod_fly_in_old_world_trainers.sql
```
(Alternatively, run the SQL statements manually using your preferred database GUI client).

### Optional: In-Game GM Commands
If you wish to manually add the `Tome of Old World Flight` to a specific vendor outside of the default list, log in with a GM account, target the desired vendor NPC, and run the following command in chat:

```
.npc add item 900002
```

### Step 4: Generate Client-Side DBC Patches
Because the vanilla 3.3.5a client hardcodes map ceilings and spell requirements, you must patch your base DBC files to allow the cast and lift the flight restrictions:

* Ensure your extracted, vanilla `AreaTable.dbc` and `Spell.dbc` files are placed inside a `DBFilesClient` folder next to the python script.

* Run the included patching script to apply the Outland flight flags to Eastern Kingdoms/Kalimdor, and to clone the custom spell (`200001`) with WotLK level/skill requirements stripped:

```
python3 patch_dbc.py
```
This will generate the updated `AreaTable.dbc` and `Spell.dbc` files.

### Step 5: Package and Install the Client Patch
* Create or update your custom MPQ patch file (e.g., `patch-W.mpq`) using your MPQ Editor. Ensure file signatures and attributes are unchecked/disabled when creating the archive.

* Place the newly generated `AreaTable.dbc` and `Spell.dbc` inside the `DBFilesClient/` folder structure within your MPQ archive.

* Drop the `patch-W.mpq` file into your World of Warcraft client’s `Data/` directory.

### Step 6: Clear Cache and Launch
* Crucial: Delete your client's local cache folder (`Cache/WDB/`) to force the game client to read the new item names, display icons, and tooltips correctly.

* Copy the freshly patched `AreaTable.dbc` and `Spell.dbc` files to your server's mapped `Data/dbc/` folder so the server shares the exact same map coordinates as the client.

* Restart your AzerothCore server container/services.

* Launch your game client, visit a flight vendor, and enjoy the skies over Azeroth!
