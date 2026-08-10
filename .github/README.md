# Overview (for AzerothCore-Catalouge)
Name: mod-fly-in-old-world
This module for AzerothCore allows server administrators to control which players can use flying mounts in the Old World (Eastern Kingdoms and Kalimdor). It operates similarly to the "Cold Weather Flying" or "Flight Master's License" mechanics, requiring players to learn a specific spell before they are permitted to take off in vanilla zones.

## Features
Controlled Access: Restricts Old World flying behind a custom learnable spell (Default Spell ID: 200001).

Automated Database Injection: Includes pre-configured SQL data in the data/sql/base/ directory to automatically add the custom spell to flight trainers in Dalaran, Honor Hold, and Thrallmar.

Client-Side Automation: Contains an included Python script (patch-dbc-for-flying.py) to easily modify the required client database files without manual hex editing.

## 1. Server-Side Installation
### Clone the Repository
Navigate to your AzerothCore modules directory and clone this repository.

### Recompile the Server
Because this module includes custom C++ logic, you must recompile your worldserver. Run your standard CMake build process (or your preferred Docker build script/manager) to inject the source code into your core.

The module's database files (trainer data) will be automatically injected into your acore_world database the next time you run the database assembler or start your server.

### Configuration
Navigate to your server's etc/modules/ directory.

Copy the template file: cp mod_fly_in_old_world.conf.dist mod_fly_in_old_world.conf

Open the configuration file and ensure the module is enabled: FlyInOldWorld.Enable = 1

(Note: If you wish to use a different Spell ID, such as standard Cold Weather Flying (54197), you must edit the OLD_WORLD_FLYING_SPELL variable in src/FlyInOldWorld.cpp before compiling).

## 2. Client-Side Installation
For the game client to physically allow vertical Z-axis movement in the Old World, you must patch the client's AreaTable.dbc file. The server will handle the spell requirements, but the client must render the 3D flight space.

### Patching the DBC
Extract AreaTable.dbc from your client's local MPQ archives.

Place it in the same directory as the included patch-dbc-for-flying.py script.

Run the Python script to automatically adjust the flight flags for Eastern Kingdoms and Kalimdor.

Pack the modified AreaTable.dbc file into a new custom patch archive (e.g., patch-5.MPQ) inside a DBFilesClient folder.

### Applying the Patch
Place your newly created patch-5.MPQ into your World of Warcraft Data folder.

Crucial: Delete the Cache folder in your World of Warcraft root directory. If you skip this step, the client will load old DBC data and your mounts will stay grounded.

## Usage In-Game
Once the server is running and the client is patched, players simply need to visit a flight trainer in Outland or Northrend, purchase the custom flight license, and mount up in any vanilla zone.
