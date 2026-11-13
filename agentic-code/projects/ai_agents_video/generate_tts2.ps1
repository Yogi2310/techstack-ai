$texts = @(
    "What if your biggest engineering bottleneck isn't headcount -- it's the fact that humans sleep?",
    "Every team assumes more developers means faster shipping. But adding engineers also adds meetings, reviews, and miscommunications.",
    "Here is the secret nobody talks about. The real cost of a software team isn't salaries -- it's coordination. Every handoff is a failure point.",
    "AI agents don't hand off. They write code, run tests, catch regressions, and deploy -- in one uninterrupted loop, never waiting for a Slack reply.",
    "Companies using agentic workflows are shipping ten times faster -- not by hiring more people, but by removing the waiting entirely.",
    "So the real question isn't whether AI will replace developers. It's whether your team is building with agents -- or competing against them. What do you think?"
)

$dir = "D:\Antigravity\Pro\agentic-code\projects\ai_agents_video\audio"
New-Item -ItemType Directory -Path $dir -Force | Out-Null

for ($i = 0; $i -lt $texts.Length; $i++) {
    $outFile = "$dir\clip$($i+1).wav"
    $text = $texts[$i]
    $script = @"
Add-Type -AssemblyName System.Speech
`$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
`$s.Rate = -1
`$s.Volume = 100
`$s.SetOutputToWaveFile('$outFile')
`$s.Speak('$text')
`$s.Dispose()
"@
    $script | powershell -NonInteractive -Command -
    Write-Host "Generated clip$($i+1).wav"
}

Get-Item "$dir\*.wav" | Select-Object Name, @{N='KB';E={[math]::Round($_.Length/1KB,1)}}
