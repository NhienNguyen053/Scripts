# Install ffmpeg and add to environment variables before running the script
$ffmpegPath = Get-Command ffmpeg -ErrorAction SilentlyContinue

if (-not $ffmpegPath) {
    Write-Host "ffmpeg is not installed or not found in the system PATH. Exiting script."
    exit
}

$inputDir = "E:\Music"  # Input folder
$outputDir = "E:\Audio"  # Output folder

# Create output directory if it doesn't exist
mkdir $outputDir

# Process each MP3 file
Get-ChildItem $inputDir -Filter *.mp3 | ForEach-Object { # Input file type
    $inputFile = $_.FullName
    $outputFile = Join-Path $outputDir "$($_.BaseName).mp3" # Output file type

    # Run ffmpeg command with loudness normalization
    ffmpeg -i $inputFile -filter:a loudnorm=I=-16:TP=0:LRA=11 $outputFile # I: Integrated Loudness, TP: True Peak, LRA: Loudness Range 

    Write-Host "Processed: $inputFile"
}
