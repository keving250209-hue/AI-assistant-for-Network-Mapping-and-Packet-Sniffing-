import subprocess
import requests
import json
import os
import pyttsx3
import speech_recognition as sr

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)

def speak(text):
    """Speak text aloud using pyttsx3."""
    print("🔊 Bot:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to microphone and return recognized text."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service unavailable.")
        return ""

# Nmap scan types
SCAN_TYPES = {
    "1": ("TCP Connect Scan", ["-sT"]),
    "2": ("SYN Scan", ["-sS"]),
    "3": ("UDP Scan", ["-sU"]),
    "4": ("Service/Version Detection", ["-sV"]),
    "5": ("OS Detection", ["-O"]),
    "6": ("Aggressive Scan", ["-A"]),
    "7": ("All Ports Scan", ["-p-"]),
    "8": ("Top 100 Ports Scan", ["--top-ports", "100"]),
    "9": ("Ping Scan", ["-sn"]),
    "10": ("Script Scan (Vuln)", ["--script", "vuln"])
}

def run_nmap(target, options):
    try:
        result = subprocess.run(
            ["nmap"] + options + [target],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error running Nmap: {e}"

def run_wireshark(interface="eth0", duration=10):
    try:
        result = subprocess.run(
            ["tshark", "-i", interface, "-a", f"duration:{duration}", "-c", "50"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error running Wireshark/tshark: {e}"

def ask_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error querying Ollama: {e}"

def main():
    speak("Welcome to your voice-enabled ethical hacking assistant.")
    speak("Say 'Nmap' for port scanning or 'Wireshark' for packet capture.")

    choice = listen().lower()

    if "nmap" in choice:
        speak("Please say the target IP or hostname.")
        target = listen()
        speak("Say the scan type number, for example one for TCP connect, four for service detection.")
        for key, (desc, _) in SCAN_TYPES.items():
            print(f"{key}. {desc}")
        scan_choice = listen()
        if scan_choice not in SCAN_TYPES:
            speak("Invalid choice.")
            return
        scan_name, options = SCAN_TYPES[scan_choice]
        speak(f"Running {scan_name} on {target}")
        scan_results = run_nmap(target, options)
        analysis = ask_ollama(f"Analyze these Nmap results:\n{scan_results}")
        speak(analysis)

    elif "wireshark" in choice:
        speak("Please say the network interface, default is eth0.")
        interface = listen() or "eth0"
        speak("Please say the capture duration in seconds.")
        duration = listen() or "10"
        speak(f"Capturing packets on {interface} for {duration} seconds.")
        capture = run_wireshark(interface, duration)
        analysis = ask_ollama(f"Analyze this packet capture:\n{capture}")
        speak(analysis)

    else:
        speak("Invalid choice. Please restart and try again.")

if __name__ == "__main__":
    main()
