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
    print("🔊 Bot:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except:
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

def check_cves_online(service_name, version):
    try:
        query = f"{service_name} {version}"
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={query}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            vulns = []
            for item in data.get("vulnerabilities", []):
                cve_id = item["cve"]["id"]
                description = item["cve"]["descriptions"][0]["value"]
                vulns.append(f"{cve_id}: {description}")
            return vulns if vulns else ["No CVEs found."]
        else:
            return [f"Error fetching CVEs: {response.status_code}"]
    except Exception as e:
        return [f"Error querying CVE API: {e}"]

def check_cves_offline(service_name, version, local_file="[name of the latest json file]"):
    if not os.path.exists(local_file):
        return ["Local CVE file not found."]
    try:
        with open(local_file, "r") as f:
            data = json.load(f)
        vulns = []
        for item in data.get("CVE_Items", []):
            cve_id = item["cve"]["CVE_data_meta"]["ID"]
            desc = item["cve"]["description"]["description_data"][0]["value"]
            if service_name.lower() in desc.lower() and version.lower() in desc.lower():
                vulns.append(f"{cve_id}: {desc}")
        return vulns if vulns else ["No CVEs found in local file."]
    except Exception as e:
        return [f"Error reading local CVE file: {e}"]

def main_loop():
    speak("Voice assistant ready. Say 'Hey Chatbot' to wake me up.")
    while True:
        command = listen()
        if "hey Chatbot" in command:
            speak("I’m listening. Say Nmap or Wireshark.")
            choice = listen()
            if "nmap" in choice:
                speak("Say the target IP or hostname.")
                target = listen()
                speak("Say the scan type number, for example one for TCP connect, four for service detection.")
                for key, (desc, _) in SCAN_TYPES.items():
                    print(f"{key}. {desc}")
                scan_choice = listen()
                if scan_choice in SCAN_TYPES:
                    scan_name, options = SCAN_TYPES[scan_choice]
                    speak(f"Running {scan_name} on {target}")
                    results = run_nmap(target, options)
                    print(results)

                    # CVE lookup
                    all_vulns = []
                    for line in results.splitlines():
                        if "open" in line and "/" in line:
                            parts = line.split()
                            if len(parts) >= 4:
                                port = parts[0]
                                service = parts[2]
                                version = " ".join(parts[3:])
                                speak(f"Checking CVEs for {service} {version} on port {port}")
                                vulns = check_cves_online(service, version)
                                if "Error" in vulns[0] or "No CVEs" in vulns[0]:
                                    vulns = check_cves_offline(service, version)
                                for v in vulns[:3]:
                                    speak(v)
                                all_vulns.extend(vulns)

                    # AI summary
                    analysis = ask_ollama(f"Summarize risks from Nmap + CVE results:\n{results}\n{all_vulns}")
                    speak(analysis)
                else:
                    speak("Invalid scan choice.")
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
                speak("Invalid choice.")

if __name__ == "__main__":
    main_loop()
