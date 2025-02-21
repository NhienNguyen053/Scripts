const fs = require('fs');
const path = require('path');

const folderPath = path.resolve('E:/Music');

function renameFilesInFolder(folder) {
    fs.readdir(folder, (err, files) => {
        if (err) {
            console.error('Error reading folder:', err.message);
            return;
        }

        files.forEach((file) => {
            const oldFilePath = path.join(folder, file);
            const newFileName = file.replace(/_/g, "'");
            const newFilePath = path.join(folder, newFileName);

            fs.rename(oldFilePath, newFilePath, (err) => {
                if (err) {
                    console.error(`Error renaming file "${file}":`, err.message);
                } else {
                    console.log(`Renamed: "${file}" → "${newFileName}"`);
                }
            });
        });
    });
}

// Run the function
renameFilesInFolder(folderPath);
