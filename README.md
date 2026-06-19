# AI-assistant-for-Network-Mapping-and-Packet-Sniffing
I have created a interactive ai chatbot, which you can give voice commands to automate nmap scans and packet analysis 
First you have to download nmap and wireshark
This chatbot runs on local ai model
The Chatbot is specifically designed for the Raspberry pi 5
For this you can have any linux distro but it has to be based on debian with nmap and wireshark preinstalled
The best option is Kali Linux
It is a operating system specifically made for ethical hackers
It comes with all the tools preinstalled
First you have to install python3
Second you have to ollama 
For installing it, use this command!

curl -fsSL https://ollama.com/install.sh | sh


Then install a local ai model using this command 

ollama pull llama3


I have been using the llama3 model for the past few years and its good


For offline CVE looks you can download the json file from this link



https://nvd.nist.gov/vuln/data-feeds?utm_source=copilot.com


Replace the name of the file with the json file name you have downloaded

For the chatbot to recognize voice commands you will have to install pyttsx3, speechrecognition and pyaudio

It can be downlaoded with this command 


pip install pyttsx3 SpeechRecognition pyaudio requests


For the voice command to work on Raspberry pi 5 

First Install Portaudio on the Raspberry pi 5 with this coommand 

sudo apt install portaudio19-dev python3-pyaudio -y

The chatbot requires pyttsx3 and SpeechRecognition libraries for offline voice command processing

To download them use this command 

pip install SpeechRecognition pyttsx3 pyaudio

To wake up the chatbot, say "Hey Chatbot" 

####You have to say "Hey chatbot" after running the python file####

And follow the on-screen instructions to intiate the scanning process















