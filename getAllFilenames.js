const fs = require('fs');
const path = require('path');

// Replace this with the path to your folder
const folderPath = 'E:/Music';

fs.readdir(folderPath, (err, files) => {
    if (err) {
        return console.error('Unable to scan directory:', err);
    }

    // files is an array of filenames
    files.forEach(file => {
        console.log(file);
    });
});
