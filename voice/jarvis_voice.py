#!/usr/bin/env python3
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import warnings
warnings.filterwarnings("ignore")
import pygame

def speak_intro():
    audio_path = os.path.join(os.path.dirname(__file__), "jarvis_cut.ogg")
    
    if not os.path.exists(audio_path):
        print("[*] Jarvis voice file not found, skipping...")
        return
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    speak_intro()
