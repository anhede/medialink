<p align="center">
    <img width="200" align="center" src="https://raw.githubusercontent.com/anhede/medialink/refs/heads/main/medialink.png" alt="Medialink logo">
</p>
<h1 align="center">Medialink</h1>
Medialink is a Python CLI-tool for bringing order to your digital film and tv-show library. From a messy collection of badly structured folders and files, Medialink can generate a new folder structure with properly named files and folders for use with services such as Plex, Emby, and Jellyfin. Medialink uses links to the original files, so no files are copied or moved. Since the original files are not modified or moved, it allows torrents and other downloads to continue seeding without interruption.

## Installation
### pipx (Recommended)
Medialink can be installed using pipx, which is a tool to install Python CLI tools in isolated environments. This is the recommended way to install Medialink as it will not interfere with other Python packages on your system.
```bash
pipx install medialink
```

### pip
Medialink can also be installed using pip, which is the Python package installer. This is not recommended as it will install Medialink globally on your system and may interfere with other Python packages.
```bash
pip install medialink
```

## Usage

```bash
python cli.py [OPTIONS] SOURCE [TARGET]
```

### Arguments

- `SOURCE` (required): The path to the source directory to scan for films and/or shows. Must exist and be readable.
- `TARGET` (optional): The path to the target directory to populate. Must not exist prior unless specified elsewhere.

### Options

- `-tf, --target-films <path>`: Specify the target directory for films. Must not already exist.

- `-ts, --target-shows <path>`: Specify the target directory for TV shows. Must not already exist.

- `-d, --dry-run`: Perform a dry run of the operation without making any changes.

- `-v, --verbose`: Enable verbose output for detailed information during the execution.

- `--version`: Show the version of the CLI tool.

- `--help`: Show help message and usage information.

### Examples

1. **Basic Usage**:
   ```bash
   python cli.py /path/to/source /path/to/target
   ```

2. **Scan with Target Films Directory**:
   ```bash
   python cli.py /path/to/source --target-films /path/to/films
   ```

3. **Dry Run with Verbose Output**:
   ```bash
   python cli.py /path/to/source --dry-run
   ```

## Developers
If you want to contribute to Medialink, you can clone the repository and install the development dependencies using poetry. Remember to use the `--with=dev` flag to install the development dependencies.
```bash
git clone
cd medialink
poetry install --with=dev   # Installs dev dependencies.
poetry run medialink --help # Run the tool!
```

## License
Medialink is licensed under the GPL-3.0-or-later License. See [LICENSE](LICENSE) for more information.
