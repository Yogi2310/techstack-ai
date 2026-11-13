$text1 = "What if your biggest engineering bottleneck isn't headcount -- it's the fact that humans sleep?"
$text2 = "Every team assumes more developers means faster shipping. But adding engineers also adds meetings, reviews, and miscommunications."
$text3 = "Here's the secret nobody talks about: the real cost of a software team isn't salaries -- it's coordination. Every handoff is a failure point."
$text4 = "AI agents don't hand off. They write code, run tests, catch regressions, and deploy -- in one uninterrupted loop, never waiting for a Slack reply."
$text5 = "Companies using agentic workflows are shipping ten times faster -- not by hiring more people, but by removing the waiting entirely."
$text6 = "So the real question isn't whether AI will replace developers. It's whether your team is building with agents -- or competing against them. What do you think?"

Add-Type -AssemblyName System.Speech

function Speak-To-File($text, $outfile) {
    $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $s.SelectVoice("Microsoft Zira Desktop")
    $s.Rate = -1
    $s.SetOutputToWaveFile($outfile)
    $s.Speak($text)
    $s.SetOutputToDefaultAudioDevice()
    $s.Dispose()
    Write-Host "Done: $outfile"
}

$dir = "D:\Antigravity\Pro\agentic-code\projects\ai_agents_video\audio"
New-Item -ItemType Directory -Path $dir -Force | Out-Null

Speak-To-File $text1 "$dir\clip1.wav"
Speak-To-File $text2 "$dir\clip2.wav"
Speak-To-File $text3 "$dir\clip3.wav"
Speak-To-File $text4 "$dir\clip4.wav"
Speak-To-File $text5 "$dir\clip5.wav"
Speak-To-File $text6 "$dir\clip6.wav"

Write-Host "All 6 audio files generated."
