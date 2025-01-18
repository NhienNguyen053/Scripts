$inputDir = "E:\Music"  # input folder
$outputDir = "E:\Audio" # output folder
mkdir $outputDir

# change mp3 to other file type if needed
Get-ChildItem $inputDir -Filter *.mp3 | ForEach-Object {
    $inputFile = $_.FullName
    $outputFile = Join-Path $outputDir "$($_.BaseName)_normalized.wav"
    ffmpeg -i $inputFile -filter:a loudnorm=I=-14:TP=-2:LRA=11 $outputFile
    Write-Host "Processed: $inputFile"
}
# change -14 to other LUFS (Loudness Units Full Scale) if needed