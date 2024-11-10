#!/bin/env python
# -*- coding: UTF-8 -*-

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("TOKEN")
TELEGRAM_URL = os.getenv('TELEGRAM_URL')
YOUTUBE_URL = os.getenv('YOUTUBE_URL')
INSTAGRAM_URL = os.getenv('INSTAGRAM_URL')
ID = os.getenv("ID")

# Validate essential environment variables
if not TOKEN:
    raise ValueError("The TOKEN is missing from the environment variables.")

if not TELEGRAM_URL:
    raise ValueError("The Telegram URL is missing from the environment variables.")

if not YOUTUBE_URL:
    raise ValueError("The Telegram URL is missing from the environment variables.")

if not INSTAGRAM_URL:
    raise ValueError("The Telegram URL is missing from the environment variables.")

if not all([TELEGRAM_URL, YOUTUBE_URL, INSTAGRAM_URL]):
    raise ValueError("Missing social medias environment variables. Please check your .env file.")