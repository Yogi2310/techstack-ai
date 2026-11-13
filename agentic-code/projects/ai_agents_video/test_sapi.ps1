Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
Write-Host "Object created: $s"
Write-Host "Type: " $s.GetType().FullName
$out = "C:\tmp\sapi_test.wav"
New-Item -Path "C:\tmp" -ItemType Directory -Force | Out-Null
$s.SetOutputToWaveFile($out)
$s.Speak("Hello world this is a test")
$s.Dispose()
Write-Host "Done. File exists:" (Test-Path $out)
Get-Item $out -ErrorAction SilentlyContinue | Select-Object Name, Length
