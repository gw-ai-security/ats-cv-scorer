# Kaggle External Data Staging

## Purpose
Store raw Kaggle dataset ZIPs and extracted files outside version control.

## Layout
- `_incoming_zips/`: place downloaded ZIP files here (ignored by git)
- `_unzipped/`: extracted raw files (ignored by git)

## Usage (Windows PowerShell)
```
New-Item -ItemType Directory -Force data\external\kaggle\_unzipped | Out-Null
Expand-Archive -Force data\external\kaggle\_incoming_zips\*.zip data\external\kaggle\_unzipped
```

## Usage (macOS/Linux)
```
mkdir -p data/external/kaggle/_unzipped
unzip -o "data/external/kaggle/_incoming_zips/*.zip" -d data/external/kaggle/_unzipped
```

## Notes
- Do not commit raw datasets.
- Add each dataset to `data/processed/registry.json` after ingestion.
