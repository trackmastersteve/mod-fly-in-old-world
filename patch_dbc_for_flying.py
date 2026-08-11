import struct

def patch_dbc_for_flying(
    item_filename="Item.dbc", 
    spell_filename="Spell.dbc", 
    output_dir=".",
    target_item_id=49177, 
    new_item_id=900002, 
    book_display_id=61330,
    target_spell_id=48399,
    new_spell_id=200001,
    new_spell_name="Old World Flying",
    new_spell_desc="Allows the player to ride flying mounts in Azeroth."
):
    # ---------------------------------------------------------
    # 1. PATCH ITEM.DBC
    # ---------------------------------------------------------
    with open(item_filename, "rb") as f:
        item_data = f.read()

    header_format = "<4sIIII"
    header_size = struct.calcsize(header_format)
    
    magic, record_count, field_count, record_size, string_block_size = struct.unpack_from(header_format, item_data, 0)
    
    if magic != b'WDBC':
        raise ValueError("Item.dbc is not a valid WDBC file.")

    records_start = header_size
    records_end = records_start + (record_count * record_size)
    
    item_records = bytearray(item_data[records_start:records_end])
    item_strings = item_data[records_end:]

    found_item_offset = None
    for i in range(0, len(item_records), record_size):
        rec_id = struct.unpack_from("<I", item_records, i)[0]
        if rec_id == target_item_id:
            found_item_offset = i
            break

    if found_item_offset is None:
        print(f"Error: Could not find item ID {target_item_id} in Item.dbc!")
        return

    # Overwrite ID to 900002 and set display ID to book graphic (61330)
    struct.pack_into("<I", item_records, found_item_offset, new_item_id)
    struct.pack_into("<I", item_records, found_item_offset + 4, book_display_id)

    new_item_header = struct.pack(header_format, magic, record_count, field_count, record_size, string_block_size)
    
    patched_item_path = f"{output_dir}/Item.dbc"
    with open(patched_item_path, "wb") as f:
        f.write(new_item_header)
        f.write(item_records)
        f.write(item_strings)
    
    print(f"Successfully patched Item.dbc: Item {target_item_id} -> {new_item_id} (Display ID: {book_display_id})")

    # ---------------------------------------------------------
    # 2. PATCH SPELL.DBC
    # ---------------------------------------------------------
    with open(spell_filename, "rb") as f:
        spell_data = f.read()

    s_magic, s_record_count, s_field_count, s_record_size, s_string_block_size = struct.unpack_from(header_format, spell_data, 0)
    
    if s_magic != b'WDBC':
        raise ValueError("Spell.dbc is not a valid WDBC file.")

    s_records_start = header_size
    s_records_end = s_records_start + (s_record_count * s_record_size)
    
    spell_records = bytearray(spell_data[s_records_start:s_records_end])
    spell_strings = bytearray(spell_data[s_records_end:])

    found_spell_record = None
    for i in range(0, len(spell_records), s_record_size):
        rec_id = struct.unpack_from("<I", spell_records, i)[0]
        if rec_id == target_spell_id:
            found_spell_record = bytearray(spell_records[i:i + s_record_size])
            break

    if not found_spell_record:
        print(f"Error: Could not find spell ID {target_spell_id} in Spell.dbc!")
        return

# Update spell ID to custom spell ID 200001
    struct.pack_into("<I", found_spell_record, 0, new_spell_id)

    # Append new name and description strings to spell string block
    name_offset = len(spell_strings)
    spell_strings.extend(new_spell_name.encode('utf-8') + b'\x00')
    
    desc_offset = len(spell_strings)
    spell_strings.extend(new_spell_desc.encode('utf-8') + b'\x00')

    new_spell_string_block_size = len(spell_strings)

    # Write the name pointer into the primary name field slot (offset 4 in 3.3.5a Spell.dbc)
    struct.pack_into("<I", found_spell_record, 4, name_offset)

    # Overwrite all localized description pointer fields (spanning 136 to 208)
    for desc_field_offset in range(136, 208, 4):
        struct.pack_into("<I", found_spell_record, desc_field_offset, desc_offset)
    
    spell_records.extend(found_spell_record)
    new_spell_record_count = s_record_count + 1

    new_spell_header = struct.pack(header_format, s_magic, new_spell_record_count, s_field_count, s_record_size, new_spell_string_block_size)
    
    patched_spell_path = f"{output_dir}/Spell.dbc"
    with open(patched_spell_path, "wb") as f:
        f.write(new_spell_header)
        f.write(spell_records)
        f.write(spell_strings)

    print(f"Successfully patched Spell.dbc: Spell {target_spell_id} -> {new_spell_id} with custom description.")

if __name__ == "__main__":
    patch_dbc_for_flying()
