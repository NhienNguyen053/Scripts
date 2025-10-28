import fs from 'fs';
import path from 'path';

// For first file don't immediately download second file as it can mess up the flow

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

// === Helper: find next available number ===
function getNextNumber() {
    const files = fs.readdirSync(folderPath);
    const numbers = files
        .map(file => path.parse(file).name)
        .filter(name => /^\d+$/.test(name)) // only numeric names
        .map(Number)
        .sort((a, b) => a - b);

    return numbers.length ? numbers[numbers.length - 1] + 1 : 1;
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
            const nextNumber = getNextNumber();
            const ext = path.extname(filename);
            const newName = `${nextNumber}${ext}`;
            const newPath = path.join(folderPath, newName);

            // Avoid renaming if already numbered or name conflict
            if (/^\d+\./.test(filename) || fs.existsSync(newPath)) return;

            fs.rename(filePath, newPath, err => {
                if (err) {}
                else console.log(`✅ Renamed: ${filename} → ${newName}`);
            });
        }, 2000); // Adjust delay if your downloads take longer
    });
});