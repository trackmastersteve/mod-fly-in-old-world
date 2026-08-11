import struct

def fix_spell_dbc(input_filename="Spell.dbc", output_filename="Spell.dbc"):
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
    
    # Extract records and string block safely
    records_data = bytearray(data[records_start:records_end])
    string_block = data[string_block_start:]

    target_id = 54197
    found_record = None

    # Find the record for Cold Weather Flying
    for i in range(0, len(records_data), record_size):
        rec_id = struct.unpack_from("<I", records_data, i)[0]
        if rec_id == target_id:
            found_record = bytearray(records_data[i:i + record_size])
            break

    if not found_record:
        print(f"Error: Could not find spell ID {target_id}!")
        return

    # Change the ID of the cloned record to 200001
    struct.pack_into("<I", found_record, 0, 200001)

    # Append the clean record block matching exact record_size
    records_data.extend(found_record)
    new_record_count = record_count + 1

    # Rebuild valid header with the exact expected field and record sizes
    new_header = struct.pack(header_format, magic, new_record_count, field_count, record_size, string_block_size)
    
    with open(output_filename, "wb") as f:
        f.write(new_header)
        f.write(records_data)
        f.write(string_block)

    print(f"Successfully generated clean Spell.dbc with ID 200001 added ({new_record_count} records, {record_size} bytes/record).")

if __name__ == "__main__":
    fix_spell_dbc()
