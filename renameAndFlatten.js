const fs = require("fs");
const path = require("path");

/**
 * Scans a folder, optionally flattens subfolders, and renames files sequentially (1, 2, 3, ...).
 * @param {string} targetFolder - Path to the folder to process.
 */
async function renameAndFlatten(targetFolder) {
    const entries = await fs.promises.readdir(targetFolder, { withFileTypes: true });

    const subfolders = entries.filter((entry) => entry.isDirectory());
    const files = entries.filter((entry) => entry.isFile());

    let fileList = [];

    if (subfolders.length > 0) {
        // If there are subfolders, gather all files inside each one
        for (const folder of subfolders) {
            const folderPath = path.join(targetFolder, folder.name);
            const innerFiles = await fs.promises.readdir(folderPath, { withFileTypes: true });

            for (const file of innerFiles) {
                if (file.isFile()) {
                    const filePath = path.join(folderPath, file.name);
                    fileList.push(filePath);
                }
            }
        }
    } else {
        // If no subfolders, use files directly in the folder
        fileList = files.map((f) => path.join(targetFolder, f.name));
    }

    // Sort by name to keep consistent order (optional)
    fileList.sort();

    // Rename and move files sequentially
    for (let i = 0; i < fileList.length; i++) {
        const oldPath = fileList[i];
        const ext = path.extname(oldPath);
        const newName = `${i + 1}${ext}`;
        const newPath = path.join(targetFolder, newName);

        await fs.promises.rename(oldPath, newPath);
    }

    // Remove empty subfolders if any
    for (const folder of subfolders) {
        const folderPath = path.join(targetFolder, folder.name);
        await fs.promises.rm(folderPath, { recursive: true, force: true });
    }

    console.log(`✅ Renamed and flattened ${fileList.length} files successfully!`);
}

// Example usage
const target = process.argv[2]; // e.g. node renameAndFlatten.js ./myfolder
if (!target) {
    console.error("Please specify a target folder path.");
    process.exit(1);
}

renameAndFlatten(path.resolve(target)).catch(console.error);