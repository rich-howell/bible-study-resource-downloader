# BibleProject Download Helper

This repository contains a small Python script that automates the downloading of publicly available poster resources from the BibleProject downloads page.

It is intended to help individuals who want to maintain a personal, offline copy of resources that BibleProject already provides via manual download buttons on their website.

## What this script does

Visits the official BibleProject downloads page

- Expands all accordion sections
- Locates Poster download links only _(videos are ignored)_
- Saves posters into folders named after their section
- Uses meaningful, human-readable filenames based on episode titles
- Skips files that already exist _(safe to re-run)_
- Supports a dry-run mode to preview actions before downloading
- Includes a configurable delay between downloads to behave politely
- No content is bundled or redistributed by this repository.

## What this script does not do

- It does not bypass paywalls or authentication
- It does not access private APIs or hidden endpoints
- It does not download videos or non-poster media
- It does not redistribute BibleProject content
- It does not attempt to mirror the website

All downloaded files remain subject to BibleProject’s terms and copyright.

## Requirements

- Python 3.9+
- Playwright (Chromium)
- Requests

## Install dependencies:

```bash
pip install playwright requests
playwright install
```

## Usage

Open the script and configure:

```python
OUTPUT_DIR = r"C:\My Drive\"
DRY_RUN = True
SLEEP_SECONDS = 5
```

## Dry run (recommended first)

```bash
python download-posters.py
```

This will print what would be downloaded without saving any files.

## Actual download

```bash
DRY_RUN = False
```

Then run again. Existing files will be skipped automatically.

## Incremental updates

The script is safe to re-run at any time.

- Existing files are skipped
- New posters added by BibleProject will be downloaded
- No duplicates are created

This makes it suitable for occasional refreshes as new resources are published.

## Disclaimer

This script is intended for personal, educational use only.

It automates the downloading of resources that are already publicly accessible through BibleProject’s official website.
No content is redistributed by this repository.

All rights to the downloaded materials belong to BibleProject.

Please review and comply with their terms of use before running this script:

[https://bibleproject.com/terms/](https://bibleproject.com/terms/)