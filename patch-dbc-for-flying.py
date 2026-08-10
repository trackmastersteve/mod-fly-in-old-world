import struct
import sys

input_file = 'AreaTable.dbc'
output_file = 'AreaTable_patched.dbc'
FLYING_FLAG = 17408  # Hex 0x4400 (Applies both Outland flying flags)

try:
    with open(input_file, 'rb') as f:
        header = f.read(20)
        # Unpack the 20-byte header (Signature, Records, Fields, Record Size, String Block Size)
        signature, record_count, field_count, record_size, string_block_size = struct.unpack('<4sIIII', header)
        
        if signature != b'WDBC':
            print("Error: Not a valid DBC file!")
            sys.exit(1)
            
        records = f.read(record_count * record_size)
        string_block = f.read()
except FileNotFoundError:
    print(f"Error: Could not find {input_file} in this directory.")
    sys.exit(1)

# Convert immutable bytes to a mutable bytearray
patched_records = bytearray(records)

# The Flags column is the 5th field (index 4). Each field is 4 bytes.
FLAG_OFFSET = 4 * 4 

for i in range(record_count):
    record_start = i * record_size
    flag_start = record_start + FLAG_OFFSET
    flag_end = flag_start + 4
    
    # Unpack the current flags (little-endian unsigned integer)
    current_flags = struct.unpack('<I', patched_records[flag_start:flag_end])[0]
    
    # Apply the flying flag using bitwise OR
    new_flags = current_flags | FLYING_FLAG
    
    # Pack the modified flags back into the bytearray
    patched_records[flag_start:flag_end] = struct.pack('<I', new_flags)

with open(output_file, 'wb') as f:
    f.write(header)
    f.write(patched_records)
    f.write(string_block)

print("Success! Generated AreaTable_patched.dbc directly.")
