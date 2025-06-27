import os
import sys
import time
import random
import subprocess
from dataclasses import dataclass
from typing import List, Optional

import requests
from seleniumbase import SB

# --- Utility Functions ---

def is_stream_online(username: str) -> bool:
    """
    Checks if the Twitch stream is online.
    Uses a public frontend Client-ID (no OAuth required).
    """
    url = f"https://www.twitch.tv/{username}"
    headers = {"Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko"}
    resp = requests.get(url, headers=headers)
    return "isLiveBroadcast" in resp.text

def handle_accept_captcha(sb):
    """
    Handles Accept/Captcha popups for a given SeleniumBase instance.
    """
    sb.uc_gui_click_captcha()
    sb.sleep(1)
    sb.uc_gui_handle_captcha()
    sb.sleep(1)
    if sb.is_element_present('button:contains("Accept")'):
        sb.uc_click('button:contains("Accept")', reconnect_time=4)

def handle_stream_page(sb, url: str, main_selector: str):
    """
    Opens a stream page, handles captchas, and waits while the stream is visible.
    """
    sb.uc_open_with_reconnect(url, 5)
    handle_accept_captcha(sb)
    if sb.is_element_visible(main_selector):
        papao = sb.get_new_driver(undetectable=True)
        papao.uc_open_with_reconnect(url, 5)
        handle_accept_captcha(papao)
        sb.sleep(10)
        if papao.is_element_present('button:contains("Accept")'):
            papao.uc_click('button:contains("Accept")', reconnect_time=4)
        while sb.is_element_visible(main_selector):
            sb.sleep(10)
        sb.quit_extra_driver()

# --- Main Execution ---

def main():
    KICK_URL = "https://kick.com/brutalles"
    TWITCH_USER = "brutalles"
    TWITCH_URL = f"https://www.twitch.tv/{TWITCH_USER}"
    KICK_SELECTOR = "#injected-channel-player"
    TWITCH_CHAT_SELECTOR = 'div[aria-label="Chat messages"]'

    with SB(uc=True, test=True) as sb:
        # Handle Kick.com stream
        handle_stream_page(sb, KICK_URL, KICK_SELECTOR)
        sb.sleep(1)

        # Handle Twitch stream if online
        if is_stream_online(TWITCH_USER):
            handle_stream_page(sb, TWITCH_URL, TWITCH_CHAT_SELECTOR)
        sb.sleep(1)

if __name__ == "__main__":
    main()
