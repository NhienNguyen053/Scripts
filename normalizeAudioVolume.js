const ffmpeg = require('fluent-ffmpeg');
const readline = require('readline');
const path = require('path');

const FILE_TYPE = '.mp3';

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

function adjustVolume(fileName, volumeChange) {
    const fullFileName = fileName.includes(FILE_TYPE) ? fileName : `${fileName}${FILE_TYPE}`;
    const inputPath = path.resolve("E:/Music/", fullFileName);
    const outputPath = path.resolve("E:/Audio/", fullFileName);

    ffmpeg(inputPath)
        .audioFilters(`volume=${volumeChange}dB`)
        .output(outputPath)
        .on('end', () => {
            console.log(`File processed successfully. Saved as: ${outputPath}`);
            promptForNext();
        })
        .on('error', (err) => {
            console.error('Error:', err.message);
            promptForNext();
        })
        .run();
}

function promptForFile() {
    rl.question('Enter the file name: ', (fileName) => {
        rl.question('Enter the volume adjustment (e.g., +3 for increase, -3 for decrease): ', (volumeChange) => {
            if (!isNaN(volumeChange)) {
                adjustVolume(fileName.trim(), parseFloat(volumeChange));
            } else {
                console.error('Invalid volume adjustment. Please enter a valid number.');
                promptForFile();
            }
        });
    });
}

function promptForNext() {
    rl.question('Do you want to adjust another file? (y/n): ', (answer) => {
        if (answer.toLowerCase() === 'y') {
            promptForFile();
        } else {
            console.log('Exiting...');
            rl.close();
        }
    });
}

console.log('Audio Volume Adjuster');
promptForFile();