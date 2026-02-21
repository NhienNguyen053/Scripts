#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import Jimp from 'jimp';

function usage() {
  console.log('Usage:');
  console.log('  Build index: node findImage.js build <targetFolder> [--recursive] [--index-file=path]');
  console.log('  Find image: node findImage.js find <inputImage> [--threshold=10] [--use-index] [--index-file=path]');
  console.log('  Find similar in folder: node findImage.js similar <folderPath> [--threshold=10] [--recursive]');
  console.log('  Legacy: node findImage.js <inputImage> <targetFolder> [--threshold=10] [--recursive]');
}

function isImageFile(file) {
  return /\.(jpe?g|png|gif|bmp|webp|tiff?)$/i.test(file);
}

async function averageHash(filePath) {
  const img = await Jimp.read(filePath);
  img.resize(8, 8).grayscale();
  const pixels = [];
  for (let y = 0; y < 8; y++) {
    for (let x = 0; x < 8; x++) {
      const idx = (y * 8) + x;
      const { r } = Jimp.intToRGBA(img.getPixelColor(x, y));
      pixels[idx] = r;
    }
  }
  const avg = pixels.reduce((a, b) => a + b, 0) / pixels.length;
  return pixels.map(p => (p > avg ? '1' : '0')).join('');
}

function hammingDistance(hashA, hashB) {
  let diff = 0;
  for (let i = 0; i < Math.min(hashA.length, hashB.length); i++) {
    if (hashA[i] !== hashB[i]) diff++;
  }
  diff += Math.abs(hashA.length - hashB.length);
  return diff;
}

async function* walk(dir, recursive) {
  const entries = await fs.promises.readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const res = path.resolve(dir, entry.name);
    if (entry.isDirectory()) {
      if (recursive) {
        yield* walk(res, recursive);
      }
    } else {
      yield res;
    }
  }
}

async function buildIndex(targetFolder, indexPath, recursive = false) {
  const entries = [];
  for await (const filePath of walk(targetFolder, recursive)) {
    if (!isImageFile(filePath)) continue;
    try {
      const stat = await fs.promises.stat(filePath);
      const hash = await averageHash(filePath);
      entries.push({ path: filePath, mtimeMs: stat.mtimeMs, hash });
    } catch (err) {
      // ignore
    }
  }
  const index = { folder: path.resolve(targetFolder), recursive: !!recursive, created: Date.now(), entries };
  await fs.promises.writeFile(indexPath, JSON.stringify(index, null, 2), 'utf8');
  return index;
}

async function loadIndex(indexPath) {
  try {
    const raw = await fs.promises.readFile(indexPath, 'utf8');
    return JSON.parse(raw);
  } catch (err) {
    return null;
  }
}

async function ensureIndexForFolder(targetFolder, indexPath, recursive = false) {
  const absFolder = path.resolve(targetFolder);
  const idx = await loadIndex(indexPath);
  if (!idx || idx.folder !== absFolder || idx.recursive !== !!recursive) {
    return await buildIndex(targetFolder, indexPath, recursive);
  }

  // verify entries and update changed files
  const updated = [];
  const byPath = new Map(idx.entries.map(e => [e.path, e]));
  for await (const filePath of walk(targetFolder, recursive)) {
    if (!isImageFile(filePath)) continue;
    try {
      const stat = await fs.promises.stat(filePath);
      const prev = byPath.get(filePath);
      if (!prev || prev.mtimeMs !== stat.mtimeMs) {
        const hash = await averageHash(filePath);
        updated.push({ path: filePath, mtimeMs: stat.mtimeMs, hash });
      } else {
        updated.push(prev);
      }
    } catch (err) {
      // ignore
    }
  }
  const newIndex = { folder: absFolder, recursive: !!recursive, created: Date.now(), entries: updated };
  await fs.promises.writeFile(indexPath, JSON.stringify(newIndex, null, 2), 'utf8');
  return newIndex;
}

async function findMatches(inputImage, targetFolder, options = {}) {
  const { threshold = 10, recursive = false, indexFile = null, useIndex = false } = options;
  if (!fs.existsSync(inputImage)) throw new Error('Input image not found');
  if (!useIndex) {
    if (!targetFolder || !fs.existsSync(targetFolder)) throw new Error('Target folder not found');
  }

  const inputHash = await averageHash(inputImage);
  const results = [];

  if (useIndex) {
    const idxPath = indexFile || path.join(process.cwd(), '.findImage_index.json');
    let idx = null;
    if (indexFile) {
      idx = await loadIndex(idxPath);
      if (!idx) throw new Error('Index file not found: ' + idxPath);
    } else {
      if (fs.existsSync(idxPath)) {
        idx = await loadIndex(idxPath);
      } else if (targetFolder) {
        idx = await ensureIndexForFolder(targetFolder, idxPath, recursive);
      } else {
        throw new Error('Index file not found and no targetFolder provided to build it');
      }
    }
    for (const e of idx.entries) {
      const dist = hammingDistance(inputHash, e.hash);
      if (dist <= threshold) results.push({ path: e.path, distance: dist });
    }
  } else {
    for await (const filePath of walk(targetFolder, recursive)) {
      if (!isImageFile(filePath)) continue;
      try {
        const h = await averageHash(filePath);
        const dist = hammingDistance(inputHash, h);
        if (dist <= threshold) {
          results.push({ path: filePath, distance: dist });
        }
      } catch (err) {
        // ignore unreadable files
      }
    }
  }

  results.sort((a, b) => a.distance - b.distance);
  return results;
}

async function findSimilarImagesInFolder(folderPath, options = {}) {
  const { threshold = 10, recursive = false } = options;
  if (!fs.existsSync(folderPath)) throw new Error('Folder not found');

  // Collect all image paths
  const imagePaths = [];
  for await (const filePath of walk(folderPath, recursive)) {
    if (isImageFile(filePath)) {
      imagePaths.push(filePath);
    }
  }

  // Compute hashes for all images
  const images = [];
  for (const imgPath of imagePaths) {
    try {
      const hash = await averageHash(imgPath);
      images.push({ path: imgPath, hash });
    } catch (err) {
      // ignore unreadable files
    }
  }

  // Find similar pairs
  const similarPairs = [];
  for (let i = 0; i < images.length; i++) {
    for (let j = i + 1; j < images.length; j++) {
      const dist = hammingDistance(images[i].hash, images[j].hash);
      if (dist <= threshold) {
        similarPairs.push({
          image1: images[i].path,
          image2: images[j].path,
          distance: dist
        });
      }
    }
  }

  // Sort by distance (most similar first)
  similarPairs.sort((a, b) => a.distance - b.distance);
  return similarPairs;
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.length < 1) {
    usage();
    process.exit(1);
  }

  const cmd = argv[0];
  try {
    if (cmd === 'build') {
      const targetFolder = argv[1];
      if (!targetFolder) {
        usage();
        process.exit(1);
      }
      let recursive = false;
      let indexFile = null;
      for (let i = 2; i < argv.length; i++) {
        const a = argv[i];
        if (a === '--recursive' || a === '-r') recursive = true;
        if (a.startsWith('--index-file=')) indexFile = a.split('=')[1];
      }
      const defaultIndex = indexFile || path.join(process.cwd(), '.findImage_index.json');
      console.log('Building index at', defaultIndex);
      const idx = await buildIndex(targetFolder, defaultIndex, recursive);
      console.log('Indexed', idx.entries.length, 'images');
      return;
    }

    if (cmd === 'find') {
      const inputImage = argv[1];
      if (!inputImage) {
        usage();
        process.exit(1);
      }
      let threshold = 10;
      let useIndex = false;
      let indexFile = null;
      for (let i = 2; i < argv.length; i++) {
        const a = argv[i];
        if (a.startsWith('--threshold=')) threshold = Number(a.split('=')[1]);
        if (a === '--use-index') useIndex = true;
        if (a.startsWith('--index-file=')) indexFile = a.split('=')[1];
      }

      // if user only passed image and no explicit use-index, try to use default index
      const defaultIndexPath = path.join(process.cwd(), '.findImage_index.json');
      if (!useIndex && !indexFile && fs.existsSync(defaultIndexPath)) {
        useIndex = true;
      }

      if (useIndex || indexFile) {
        const idxPath = indexFile || defaultIndexPath;
        const matches = await findMatches(inputImage, null, { threshold, recursive: false, indexFile: idxPath, useIndex: true });
        if (matches.length === 0) {
          console.log('No matches found');
          return;
        }
        for (const m of matches) console.log(`${m.distance}\t${m.path}`);
        return;
      }

      // legacy: allow passing folder as second arg to search without index
      const targetFolder = argv[2];
      if (!targetFolder) {
        console.error('No index found and no targetFolder provided. Run `build` first or pass a target folder.');
        process.exit(1);
      }
      let threshold2 = 10;
      let recursive2 = false;
      for (let i = 3; i < argv.length; i++) {
        const a = argv[i];
        if (a.startsWith('--threshold=')) threshold2 = Number(a.split('=')[1]);
        if (a === '--recursive' || a === '-r') recursive2 = true;
      }
      const matches = await findMatches(inputImage, targetFolder, { threshold: threshold2, recursive: recursive2, indexFile: null, useIndex: false });
      if (matches.length === 0) {
        console.log('No matches found');
        return;
      }
      for (const m of matches) console.log(`${m.distance}\t${m.path}`);
      return;
    }

    if (cmd === 'similar') {
      const folderPath = argv[1];
      if (!folderPath) {
        usage();
        process.exit(1);
      }
      let threshold = 10;
      let recursive = false;
      for (let i = 2; i < argv.length; i++) {
        const a = argv[i];
        if (a.startsWith('--threshold=')) threshold = Number(a.split('=')[1]);
        if (a === '--recursive' || a === '-r') recursive = true;
      }
      const similarPairs = await findSimilarImagesInFolder(folderPath, { threshold, recursive });
      if (similarPairs.length === 0) {
        console.log('No similar images found');
        return;
      }
      for (const pair of similarPairs) {
        console.log(`${pair.distance}\t${pair.image1}\t${pair.image2}`);
      }
      return;
    }

    // legacy default behavior when first arg is image and second arg folder
    if (argv.length >= 2) {
      const inputImage = argv[0];
      const targetFolder = argv[1];
      let threshold = 10;
      let recursive = false;
      for (let i = 2; i < argv.length; i++) {
        const a = argv[i];
        if (a.startsWith('--threshold=')) threshold = Number(a.split('=')[1]);
        if (a === '--recursive' || a === '-r') recursive = true;
      }
      const matches = await findMatches(inputImage, targetFolder, { threshold, recursive, indexFile: null, useIndex: false });
      if (matches.length === 0) {
        console.log('No matches found');
        return;
      }
      for (const m of matches) console.log(`${m.distance}\t${m.path}`);
      return;
    }

    usage();
    process.exit(1);
  } catch (err) {
    console.error('Error:', err.message || err);
    process.exit(2);
  }
}

if (import.meta.url === `file://${process.argv[1]}` || process.argv[1].endsWith('findImage.js')) {
  main();
}

export { findMatches, findSimilarImagesInFolder, averageHash, hammingDistance };
