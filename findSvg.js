import fs from "fs";
import path from "path";
import crypto from "crypto";

// 📥 Get directory from command line
const DIRECTORY = process.argv[2];

if (!DIRECTORY) {
    console.error("❌ Please provide a directory path.");
    console.log("Usage: node findSvg.js <directory>");
    process.exit(1);
}

function getAllSvgFiles(dir) {
    let results = [];

    const list = fs.readdirSync(dir);
    for (const file of list) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory()) {
            results = results.concat(getAllSvgFiles(filePath));
        } else if (file.toLowerCase().endsWith(".svg")) {
            results.push(filePath);
        }
    }

    return results;
}

function hashFile(filePath) {
    const content = fs.readFileSync(filePath);
    return crypto.createHash("sha256").update(content).digest("hex");
}

function findDuplicateSvgs(directory) {
    const files = getAllSvgFiles(directory);
    const hashMap = {};

    for (const file of files) {
        const hash = hashFile(file);

        if (!hashMap[hash]) {
            hashMap[hash] = [];
        }

        hashMap[hash].push(file);
    }

    return Object.values(hashMap).filter(group => group.length > 1);
}

// 🚀 Run
try {
    const duplicates = findDuplicateSvgs(DIRECTORY);

    if (duplicates.length === 0) {
        console.log("✅  No duplicate SVGs found.");
    } else {
        console.log("⚠️  Duplicate SVG groups:\n");
        duplicates.forEach((group, index) => {
            console.log(`Group ${index + 1}:`);
            group.forEach(file => console.log("  " + file));
            console.log();
        });
    }
} catch (err) {
    console.error("❌ Error:", err.message);
}