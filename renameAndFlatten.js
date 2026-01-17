import { promises } from "fs";
import { join, extname, resolve } from "path";

/**
 * Scans a folder, optionally flattens subfolders, and renames files sequentially (1, 2, 3, ...).
 * @param {string} targetFolder - Path to the folder to process.
 */
async function renameAndFlatten(targetFolder) {
    const entries = await promises.readdir(targetFolder, { withFileTypes: true });

    const subfolders = entries.filter((entry) => entry.isDirectory());
    const files = entries.filter((entry) => entry.isFile());

    let fileList = [];

    if (subfolders.length > 0) {
        // If there are subfolders, gather all files inside each one
        for (const folder of subfolders) {
            const folderPath = join(targetFolder, folder.name);
            const innerFiles = await promises.readdir(folderPath, { withFileTypes: true });

            for (const file of innerFiles) {
                if (file.isFile()) {
                    const filePath = join(folderPath, file.name);
                    fileList.push(filePath);
                }
            }
        }
    } else {
        // If no subfolders, use files directly in the folder
        fileList = files.map((f) => join(targetFolder, f.name));
    }

    // Sort by name using natural/numeric sort (e.g., file2 comes before file10)
    fileList.sort((a, b) => {
        const aName = a.split(/(\d+)/).filter(Boolean);
        const bName = b.split(/(\d+)/).filter(Boolean);

        for (let i = 0; i < Math.min(aName.length, bName.length); i++) {
            const aPart = aName[i];
            const bPart = bName[i];
            const aNum = parseInt(aPart);
            const bNum = parseInt(bPart);

            if (!isNaN(aNum) && !isNaN(bNum)) {
                if (aNum !== bNum) return aNum - bNum;
            } else {
                if (aPart !== bPart) return aPart.localeCompare(bPart);
            }
        }
        return aName.length - bName.length;
    });

    // Rename and move files sequentially
    for (let i = 0; i < fileList.length; i++) {
        const oldPath = fileList[i];
        const ext = extname(oldPath);
        const newName = `${i + 1}${ext}`;
        const newPath = join(targetFolder, newName);

        await promises.rename(oldPath, newPath);
    }

    // Remove empty subfolders if any
    for (const folder of subfolders) {
        const folderPath = join(targetFolder, folder.name);
        await promises.rm(folderPath, { recursive: true, force: true });
    }

    console.log(`✅ Renamed and flattened ${fileList.length} files successfully!`);
}

// Example usage
const target = process.argv[2]; // e.g. node renameAndFlatten.js ./myfolder
if (!target) {
    console.error("Please specify a target folder path.");
    process.exit(1);
}

renameAndFlatten(resolve(target)).catch(console.error);