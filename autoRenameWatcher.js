import fs from 'fs';
import path from 'path';

// === Read directory from command-line argument ===
const folderPath = process.argv[2];
if (!folderPath) {
    console.error('❌ Please specify a folder path, e.g.:\n   node autoRenameWatcher.js "D:\\Downloads"');
    process.exit(1);
}

// === Verify that the folder exists ===
if (!fs.existsSync(folderPath) || !fs.statSync(folderPath).isDirectory()) {
    console.error('❌ Invalid folder path:', folderPath);
    process.exit(1);
}

console.log(`👀 Watching folder: ${folderPath}`);

// === Helper: find smallest missing positive integer, optionally excluding a filename ===
function getNextNumber(excludeFilename) {
    const files = fs.readdirSync(folderPath)
        .filter(f => f !== excludeFilename); // ignore the current file if provided

    const nums = new Set(
        files
            .map(f => path.parse(f).name)
            .filter(name => /^\d+$/.test(name)) // only numeric names
            .map(Number)
    );

    let i = 1;
    while (nums.has(i)) i++;
    return i;
}

// === Watch the folder for new files ===
fs.watch(folderPath, (eventType, filename) => {
    if (!filename || eventType !== 'rename') return; // triggered on new files or renames

    const filePath = path.join(folderPath, filename);

    // Check if file actually exists (not a deletion)
    fs.stat(filePath, (err, stats) => {
        if (err || !stats.isFile()) return;

        // Wait a bit to ensure file is fully written (esp. downloads)
        setTimeout(() => {
            // compute next number excluding the arriving file so an arriving numeric name
            // (like "4") won't cause the algorithm to skip earlier gaps.
            const nextNumber = getNextNumber(filename);
            const ext = path.extname(filename);
            const newName = `${nextNumber}${ext}`;
            const newPath = path.join(folderPath, newName);

            // If the file is already correctly named (e.g. "2.jpg" and nextNumber is 2), skip.
            const baseName = path.parse(filename).name;
            if (baseName === String(nextNumber)) return;

            // Avoid overwriting an existing file
            if (fs.existsSync(newPath)) {
                console.warn(`⚠️ Target exists, skipping rename: ${newName}`);
                return;
            }

            fs.rename(filePath, newPath, err => {
                if (err) {
                    console.error('❌ Rename failed:', err.message);
                } else {
                    console.log(`✅ Renamed: ${filename} → ${newName}`);
                }
            });
        }, 2000); // Adjust delay if your downloads take longer
    });
});