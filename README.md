# UnitiveFiles

A dual-language project (Node.js and Python) to combine files of the same type into a single file.

## Features

- Recursively scans directories for files matching a given extension
- Skips `node_modules` and `.git` directories
- Combines matching files in alphabetical order
- Outputs to `<extension>_combined.<extension>` in the input directory
- Available in both Node.js (TypeScript) and Python

## Node.js (TypeScript) Version

### Setup

```bash
npm install
npm run build
```

### Usage

```bash
node dist/nodejs/index.js <directory> <extension>
```

**Example:**
```bash
node dist/nodejs/index.js ./data txt
```

## Python Version

### Setup

No external dependencies required. Uses only Python standard library.

### Usage

```bash
python src/python/unitivefiles.py <directory> <extension>
```

**Example:**
```bash
python src/python/unitivefiles.py ./data txt
```

## Output

Both versions create a file named `<extension>_combined.<extension>` in the specified directory containing all matching files concatenated together, separated by newlines.
