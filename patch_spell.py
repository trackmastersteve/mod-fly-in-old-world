import struct

def modify_spell_dbc(input_filename="Spell.dbc", output_filename="Spell.dbc"):
    with open(input_filename, "rb") as f:
        data = f.read()

    # DBC Header format: Magic (4s), Record Count (I), Field Count (I), Record Size (I), String Block Size (I)
    header_format = "<4sIIII"
    header_size = struct.calcsize(header_format)
    
    magic, record_count, field_count, record_size, string_block_size = struct.unpack_from(header_format, data, 0)
    
    if magic != b'WDBC':
        raise ValueError("File is not a valid WDBC file.")

    records_start = header_size
    records_end = records_start + (record_count * record_size)
    string_block_start = records_end
    
    records_data = bytearray(data[records_start:records_end])
    string_block = data[string_block_start:]

    # Search through records to find ID 54197 (Cold Weather Flying)
    target_id = 54197
    found_record = None

    for i in range(0, len(records_data), record_size):
        # The ID is always the first 4-byte integer (I) in a DBC record
        rec_id = struct.unpack_from("<I", records_data, i)[0]
        if rec_id == target_id:
            # Extract the full byte chunk for this single record
            found_record = bytearray(records_data[i:i + record_size])
            break

    if not found_record:
        print(f"Error: Could not find spell ID {target_id} in {input_filename}!")
        return

    # Modify the ID of our cloned record to 200001 (first 4 bytes)
    struct.pack_into("<I", found_record, 0, 200001)

    # Append the new record to our records block
    records_data.extend(found_record)
    new_record_count = record_count + 1

    # Reconstruct the file headers and data blocks
    new_header = struct.pack(header_format, magic, new_record_count, field_count, record_size, string_block_size)
    
    with open(output_filename, "wb") as f:
        f.write(new_header)
        f.write(records_data)
        f.write(string_block)

    print(f"Successfully cloned spell {target_id} to 200001!")
    print(f"New Spell.dbc saved as '{output_filename}' with {new_record_count} total records.")

if __name__ == "__main__":
    modify_spell_dbc()
