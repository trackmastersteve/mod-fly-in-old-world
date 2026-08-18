import struct, os, shutil

DBC_DIR = "DBFilesClient"
SPELL_FILE = f"{DBC_DIR}/Spell.dbc"
AREA_FILE = f"{DBC_DIR}/AreaTable.dbc"

if not os.path.exists(SPELL_FILE) or not os.path.exists(AREA_FILE):
    print(f"❌ ERROR: Please ensure vanilla {SPELL_FILE} and {AREA_FILE} exist.")
    exit(1)

# Create safe backups so we can re-run the script without double-patching
if not os.path.exists(f"{SPELL_FILE}.vanilla"):
    shutil.copy(SPELL_FILE, f"{SPELL_FILE}.vanilla")
if not os.path.exists(f"{AREA_FILE}.vanilla"):
    shutil.copy(AREA_FILE, f"{AREA_FILE}.vanilla")

print("--- PATCHING AREATABLE.DBC ---")
with open(f"{AREA_FILE}.vanilla", "rb") as f:
    header = f.read(20)
    magic, rec_count, field_count, rec_size, str_size = struct.unpack('<4sIIII', header)
    records = [f.read(rec_size) for _ in range(rec_count)]
    str_block = f.read(str_size)

for i in range(rec_count):
    fields = list(struct.unpack(f'<{field_count}I', records[i]))
    # If MapID (index 1) is 0 (Eastern Kingdoms) or 1 (Kalimdor)
    if fields[1] in (0, 1):
        # Add AREA_FLAG_OUTLAND (0x400) which hard-enables flying on the client
        fields[4] |= 0x400
    records[i] = struct.pack(f'<{field_count}I', *fields)

with open(AREA_FILE, "wb") as f:
    f.write(header)
    for rec in records:
        f.write(rec)
    f.write(str_block)
print("✅ AreaTable.dbc: Old World maps flagged for flying.")

print("\n--- PATCHING SPELL.DBC ---")
with open(f"{SPELL_FILE}.vanilla", "rb") as f:
    header = f.read(20)
    magic, rec_count, field_count, rec_size, str_size = struct.unpack('<4sIIII', header)
    records = [f.read(rec_size) for _ in range(rec_count)]
    str_block = f.read(str_size)

base_rec = None
for rec in records:
    # 68907 is the CASTABLE Tome spell, not the passive aura
    if struct.unpack('<I', rec[:4])[0] == 68907:  
        base_rec = rec
        break

if not base_rec:
    print("❌ ERROR: Spell 68907 not found in vanilla Spell.dbc.")
else:
    fields = list(struct.unpack(f'<{field_count}I', base_rec))
    fields[0] = 200001  # Set our custom mod Spell ID
    
    # Strip requirements so it doesn't throw errors
    for i in range(len(fields)):
        if fields[i] == 762: fields[i] = 0        # Remove Riding Skill requirement
        if fields[i] in (225, 300): fields[i] = 0 # Remove Skill Value requirement
        if fields[i] == 68: fields[i] = 1         # Drop Level requirement to 1
        
    records.append(struct.pack(f'<{field_count}I', *fields))
    new_header = struct.pack('<4sIIII', magic, rec_count + 1, field_count, rec_size, str_size)
    
    with open(SPELL_FILE, "wb") as f:
        f.write(new_header)
        for rec in records:
            f.write(rec)
        f.write(str_block)
    print("✅ Spell.dbc: Spell 200001 created as a CASTABLE item spell.")
