import fs from "fs/promises";
import path from "path";

function printUsage(): void {
  console.log("Usage: node dist/index.js <directory> <extension>");
  console.log("Example: node dist/index.js ./data txt");
}

async function listMatchingFiles(
  rootDir: string,
  extNormalized: string,
  outputPath: string
): Promise<string[]> {
  const results: string[] = [];
  const skipDirs = new Set(["node_modules", ".git"]);

  async function walk(currentDir: string): Promise<void> {
    const entries = await fs.readdir(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        if (skipDirs.has(entry.name)) {
          continue;
        }
        await walk(fullPath);
        continue;
      }

      if (!entry.isFile()) {
        continue;
      }

      if (path.resolve(fullPath) === outputPath) {
        continue;
      }

      const fileExt = path.extname(entry.name).toLowerCase();
      if (fileExt === `.${extNormalized}`) {
        results.push(fullPath);
      }
    }
  }

  await walk(rootDir);
  return results;
}

async function combineFiles(
  directoryArg: string,
  extensionArg: string
): Promise<void> {
  const rootDir = path.resolve(directoryArg);
  const stat = await fs.stat(rootDir);
  if (!stat.isDirectory()) {
    throw new Error("Provided path is not a directory.");
  }

  const extNormalized = extensionArg.startsWith(".")
    ? extensionArg.slice(1).toLowerCase()
    : extensionArg.toLowerCase();

  if (!extNormalized) {
    throw new Error("Extension cannot be empty.");
  }

  const outputPath = path.resolve(
    path.join(rootDir, `${extNormalized}_combined.${extNormalized}`)
  );

  const files = await listMatchingFiles(rootDir, extNormalized, outputPath);
  files.sort((a, b) => {
    const relA = path.relative(rootDir, a);
    const relB = path.relative(rootDir, b);
    return relA.localeCompare(relB);
  });

  const contents: string[] = [];
  for (const filePath of files) {
    const data = await fs.readFile(filePath, "utf8");
    contents.push(data);
  }

  await fs.writeFile(outputPath, contents.join("\n"), "utf8");

  console.log(`Combined ${files.length} file(s) into: ${outputPath}`);
}

async function main(): Promise<void> {
  const [directoryArg, extensionArg] = process.argv.slice(2);
  if (!directoryArg || !extensionArg) {
    printUsage();
    process.exit(1);
  }

  try {
    await combineFiles(directoryArg, extensionArg);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Error: ${message}`);
    process.exit(1);
  }
}

void main();
