# findImage

Small CLI to index images and find visually similar images using an average hash (aHash).

Usage

- Build an index for a folder (stores `.findImage_index.json` in your current folder by default):

```powershell
node findImage.js build "D:\Rule34\Images\Klexyai" --recursive
# or using npm script
npm run find -- build "D:\Rule34\Images\Klexyai" --recursive
```

- Find matches using the index (run from the folder where `.findImage_index.json` lives or pass `--index-file`):

```powershell
node findImage.js find "C:\Users\nhien\Downloads\sample.png" --use-index --threshold=8
# or with npm script
npm run find -- find "C:\Users\nhien\Downloads\sample.png" --use-index --threshold=8
```

- Legacy direct search without index:

```powershell
node findImage.js "C:\Users\nhien\Downloads\sample.png" "D:\Rule34\Images\Klexyai" --threshold=8 --recursive
```

Notes

- Lower Hamming distance = more similar. Threshold defaults to 10.
- To change where the index file is written/read, use `--index-file="C:\path\.findImage_index.json"`.
- Wrap Windows paths in quotes if they contain spaces.

Want pHash (better perceptual matching) instead of aHash? I can add it next.
