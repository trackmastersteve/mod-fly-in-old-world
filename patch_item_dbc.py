import struct

def patch_item_dbc(input_filename="Item.dbc", output_filename="Item.dbc", target_id=49177, new_id=900002, book_display_id=61330):
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
    string_block = data[string_block_start:]

    found_record_offset = None

    for i in range(0, len(records_data), record_size):
        rec_id = struct.unpack_from("<I", records_data, i)[0]
        if rec_id == target_id:
            found_record_offset = i
            break

    if found_record_offset is None:
        print(f"Error: Could not find item ID {target_id} in Item.dbc!")
        return

    # Overwrite target ID to custom item ID 900002
    struct.pack_into("<I", records_data, found_record_offset, new_id)

    # Set display ID to the proper book graphic (61330)
    struct.pack_into("<I", records_data, found_record_offset + 4, book_display_id)

    new_header = struct.pack(header_format, magic, record_count, field_count, record_size, string_block_size)
    
    with open(output_filename, "wb") as f:
        f.write(new_header)
        f.write(records_data)
        f.write(string_block)

    print(f"Successfully modified item {target_id} to {new_id} with book display ID {book_display_id}!")

if __name__ == "__main__":
    patch_item_dbc()
