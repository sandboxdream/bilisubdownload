# Bilibili Subtitle Downloader

[中文文档](README_zh.md)

A tool to download subtitles from Bilibili videos using their BV IDs.

## Features

- Download subtitles from Bilibili videos using BV IDs
- Support for both single-part and multi-part videos
- Save subtitles in both JSON and SRT formats
- Multiple operation modes:
  - Interactive mode: Enter BV IDs manually
  - Command line mode: Provide BV IDs as command line arguments
  - File mode: Read BV IDs from a text file

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - requests

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/sandboxdream/bilisubdownload.git
   cd bilisubdownload
   ```


2. Install required packages:
   ```
   pip install requests
   ```

## Usage

### Interactive Mode

Run the script without any arguments to enter interactive mode:

```
python main.py
```

You will be prompted to enter a BV ID.

### Command Line Mode

Provide one or more BV IDs as command line arguments:

```
python main.py BV1Jm421p7RV
```

You can provide multiple BV IDs:

```
python main.py BV1Jm421p7RV BV2xxx BV3xxx
```

### File Mode

Create a text file with one BV ID per line, then use the `-f` flag:

```
python main.py -f bv_ids.txt
```

Example content of `bv_ids.txt`:
```
BV1Jm421p7RV
BV2xxx
BV3xxx
```

### Help

Display usage information:

```
python main.py -h
```

## Authentication

Some videos may require authentication to access their subtitles. You can provide cookies in a `cookies.txt` file in the same directory as the script.

To get cookies:
1. Log in to Bilibili in your browser
2. Use browser developer tools to copy your cookies
3. Save them to `cookies.txt` in the project directory

## Output

Subtitles are saved in a directory named `output_BVID` where `BVID` is the BV ID of the video. For each part of the video, two files are created:
- `part_N_CID.json`: The subtitle data in JSON format
- `part_N_CID.srt`: The subtitle data in SRT format (compatible with most video players)

## Project Structure

```
bilisubdownload/
├── main.py              # Main script for downloading subtitles
├── cookies.txt          # Optional file for storing authentication cookies
├── bv_ids.txt           # Example file with BV IDs for batch processing
├── README.md            # English documentation
├── README_zh.md         # Chinese documentation
├── LICENSE              # GNU GPL v3.0 license
└── .gitignore           # Git ignore file
```

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Open a Pull Request

## Reporting Issues

If you encounter any problems or have suggestions for improvements, please open an issue on the GitHub repository.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
