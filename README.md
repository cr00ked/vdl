# Vinted Image Downloader

This script downloads images from [Vinted](https://www.vinted.com/)-styled websites in a batch.

## Features

Currently, looping through whole profiles and categories is supported.

## Unsupported features

Authentication
More unknown...

## Requirements

Python 3
*requests* module

## Usage

### Install dependencies

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade requests
```

### Download vdl
```bash
git clone https://github.com/cr00ked/vdl.git
```

### Make vdl executable

```bash
cd vdl
chmod u+x vdl.py
```

### Basic usage

```bash
./vdl.py link <subdirectory>
```

### Example usage

```bash
/vdl.py https://www.vinted.com/womens-clothing/dresses dresses
We have read 1 pages, 48 links, do you want to continue? (y/n) y
We have read 2 pages, 96 links, do you want to continue? (y/n) n
Will proceed to downloading images from 96 links
```

The output can be found in output/dresses directory.
