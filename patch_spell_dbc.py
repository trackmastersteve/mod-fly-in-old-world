import struct

def patch_spell_dbc(input_filename="Spell.dbc", output_filename="Spell.dbc", target_id=48399, new_id=200001, new_name="Old World Flying", new_description="Allows the player to ride flying mounts in Azeroth."):
    with open(input_filename, "rb") as f:
        data = f.read()

    header_format = "<4sIIII"
    header_size = struct.calcsize(header_format)
    
    magic, record_count, field_count, record_size, string_block_size = struct.unpack_from(header_format, data, 0)
    
    if magic != b'WDBC':
        raise ValueError("File is not a valid WDBC file.")

    records_start = header_size
    records_end = records_start + (record_count * record_size)
    string_block_start = records_end
    
    records_data = bytearray(data[records_start:records_end])
    string_block = bytearray(data[string_block_start:])

    found_record = None

    for i in range(0, len(records_data), record_size):
        rec_id = struct.unpack_from("<I", records_data, i)[0]
        if rec_id == target_id:
            found_record = bytearray(records_data[i:i + record_size])
            break

    if not found_record:
        print(f"Error: Could not find spell ID {target_id} in Spell.dbc!")
        return

    # Update ID to custom spell ID 200001
    struct.pack_into("<I", found_record, 0, new_id)

    # Append new name and description strings
    name_offset = len(string_block)
    string_block.extend(new_name.encode('utf-8') + b'\x00')
    
    desc_offset = len(string_block)
    string_block.extend(new_description.encode('utf-8') + b'\x00')

    new_string_block_size = len(string_block)

    # Map description pointer fields in 3.3.5a layout
    for desc_field_offset in range(136, 200, 4):
        struct.pack_into("<I", found_record, desc_field_offset, desc_offset)

    records_data.extend(found_record)
    new_record_count = record_count + 1

    new_header = struct.pack(header_format, magic, new_record_count, field_count, record_size, new_string_block_size)
    
    with open(output_filename, "wb") as f:
        f.write(new_header)
        f.write(records_data)
        f.write(string_block)

    print(f"Successfully generated Spell.dbc with custom spell ID {new_id}!")

if __name__ == "__main__":
    patch_spell_dbc()
