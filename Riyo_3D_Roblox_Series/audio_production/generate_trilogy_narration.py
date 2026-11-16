import os
import sys
import asyncio
import subprocess
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AUDIO_OUTPUT_DIR = r"D:\Antigravity\Pro\Riyo_3D_Roblox_Series\audio_production"
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

# Highly engaging, lively young narrator voice for Roblox Shorts
VOICE = "en-US-GuyNeural"

STORIES = [
    {
        "id": "story1_black_onion",
        "title": "Story 1: The Forbidden Black Onion",
        "voice": "en-US-GuyNeural",
        "rate": "+12%",
        "pitch": "+2Hz",
        "text": """In my town, if you throw food off the mountain, mythical pets come running. Last week, I threw the Golden Cheese and got a golden dragon. But that night... the giants started throwing food back at US.

A carrot the size of a skyscraper crashed into the town square! Then a steak as big as a football field crushed the mayor's pool. Everyone panicked. My grandma started bench-pressing a military tank just to get ready. And my frog Kevin? He strapped on a tiny titanium helmet and refused to leave my shoulder.

I sprinted to the forbidden vault beneath the pet shop. Locked inside a cryogenic ice cube was a glowing, purple, pulsing vegetable: The Forbidden Black Onion. The shopkeeper grabbed my collar: "Eli, don't! Nobody has thrown that in 500 years. It doesn't attract animals... it wakes up whatever sleeps at the core of the planet!"

I didn't care. The earth split open. A foot made of solid obsidian stomped over our hills. I took a running start, jumped off the water tower, spun three times, and hurled the Black Onion into the storm! It shot across the sky like a purple hypersonic missile!

BOOM! It hit the Titan dead in the chest! The giant froze. Its glowing red eyes suddenly flickered into bright neon blue. It slowly looked down at me... and rolled over on its back like an obedient puppy wanting belly rubs! 

I just tamed a mountain-sized Colossus! But when I climbed up to check its collar... a silver plaque read: "PROPERTY OF SECTOR 9 - DO NOT RELEASE."
"""
    },
    {
        "id": "story2_sky_fishing",
        "title": "Story 2: Sky Fishing Cloud Fortress",
        "voice": "en-US-GuyNeural",
        "rate": "+12%",
        "pitch": "+2Hz",
        "text": """In my town, nobody fishes in water. You cast your fishing rod straight up into the clouds. And whatever bites... you better reel in fast before it drags you into the atmosphere.

See that kid? He baited a gummy worm and caught a flying goldfinch. It drops 10 gold coins every hour. My neighbor used a whole roasted chicken on a steel winch and hooked a Thunder Hawk! It powers his whole house with lightning. But my math teacher got greedy with a Thanksgiving turkey, and a Sky Whale dragged him halfway to the stratosphere! We haven't had homework in three weeks.

I only had a bent paperclip and dental floss. My first catch was a tiny cloud sprite named Nimbus. He eats raindrops and sneezes mini rainbows. Everyone laughed at me. So I went to the crater where the meteor crashed last winter.

I forged the Meteorite Harpoon. I attached it to an industrial titanium crane cable. At midnight during the Blood Moon eclipse, when the sky turned violet, I cast straight into the eye of the swirling black hurricane above the mountains!

The winch started spinning so fast it caught fire! The rod bent in half. I tied the cable to the town hall bell tower. With one final pull... the clouds parted. Out fell a colossal, rusted titanium anchor as big as a battleship!

Attached to the anchor was a glowing chain leading 50,000 feet into the sky. And a speaker on the anchor crackled to life: "HUMAN LIFE-SIGNS CONFIRMED. COMMENCING EXTRACTION."
"""
    },
    {
        "id": "story3_vehicle_harvest",
        "title": "Story 3: Mechanical Garden Vehicle Harvest",
        "voice": "en-US-GuyNeural",
        "rate": "+12%",
        "pitch": "+2Hz",
        "text": """In my town, nobody buys cars or bikes. You dig a hole in your garden, bury scrap metal, water it with motor oil, and wait 24 hours. Whatever sprouts out of the dirt is yours to drive.

Plant a rusty screw? You get a motorized kick-scooter. Plant a lawnmower blade? A racing go-kart sprouts like a watermelon. My neighbor buried a V8 diesel engine, and next morning an armored monster truck was blooming over his fence! The mayor planted a helicopter rotor, and now he lands his private chopper on his roof every evening.

I had zero car parts. All I found in my drawer was a dead AA battery and a flashlight bulb. I buried them, watered it with soda, and the next day... a tiny neon hoverboard popped out of the ground! It hovered behind me like an eager puppy. But I wanted to build something the town had never seen.

I explored the abandoned Sector 9 military lab outside town. Hidden in a titanium safe was a pulsing black cube: The Quantum Core. I buried it in the middle of our farm, dug a moat around it, and poured a barrel of liquid coolant over the soil.

At 3:00 AM, the ground erupted into bright blue electric vines! The earth cracked open. Rising from the soil was a 60-foot stealth mech with dual plasma thrusters and obsidian wings! 

The cockpit hissed open. A holographic display lit up in front of my face and said: "PILOT IDENTIFIED: ELI. FLEET EMERGENCY PROTOCOL ENGAGED. PREPARE FOR ORBIT."
"""
    }
]

async def generate_all():
    print("=" * 60)
    print("🎙️ Generating Neural Voiceover Narration for TaleBlox Trilogy")
    print("=" * 60)
    
    for s in STORIES:
        mp3_file = os.path.join(AUDIO_OUTPUT_DIR, f"{s['id']}.mp3")
        wav_file = os.path.join(AUDIO_OUTPUT_DIR, f"{s['id']}.wav")
        print(f"\n[+] Synthesizing '{s['title']}'...")
        print(f"    Voice: {s['voice']} | Rate: {s['rate']} | Pitch: {s['pitch']}")
        
        comm = edge_tts.Communicate(s['text'], s['voice'], rate=s['rate'], pitch=s['pitch'])
        await comm.save(mp3_file)
        
        # Convert to standard 44.1kHz stereo WAV with broadcast normalization
        subprocess.run([
            "ffmpeg", "-y", "-i", mp3_file,
            "-ar", "44100", "-ac", "2",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            wav_file
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Measure duration with ffprobe
        proc = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", wav_file
        ], capture_output=True, text=True, check=True)
        duration = float(proc.stdout.strip())
        
        print(f"    [OK] Generated: {os.path.basename(wav_file)}")
        print(f"    Duration: {duration:.2f} seconds ({os.path.getsize(wav_file)/(1024*1024):.2f} MB)")

    print("\n" + "=" * 60)
    print("✨ ALL 3 EPISODE NARRATIONS COMPLETED & NORMALIZED!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(generate_all())
