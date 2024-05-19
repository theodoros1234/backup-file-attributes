# backup-file-attributes
Recursively scans all files, directories and symlinks inside a specified directory, and exports various attributes about them in JSON format with GZIP compression.

# Usage
## Backup
```
./backup-file-attributes.py scan_dir output_file.gz
```
**Warning:** If the output file already exists, it will be replaced without notice.

## Restore
To be done (this hasn't been implemented yet).

# Export format
Data is exported in JSON format with GZIP compression. For each file, directory or symlink, a JSON object with the following information is saved:
- **`filename` (string):** File's name, without the path.
- **`ctime` (int or float):** Creation time
- **`mtime` (int or float):** Modification time
- **`mode` (int):** Read/write/execute permissions
- **`user` (string):** Name of the user who owns this item
- **`group` (string):** Name of the group who owns this item
- **`type` (string):** 'file', 'dir' or 'symlink' depending on what type of item this is
- **[Only on directories] `contents` (array):** Every item inside this directory, as a JSON object with all its attributes
- **[Only on symlinks] `target` (string):** Path that the symlink points to

# Dependencies
- Python 3

**Notice:** The script has only been tested on Linux.
