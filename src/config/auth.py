#!/bin/env python
# -*- coding: UTF-8 -*-

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("TOKEN")

# Validate essential environment variables
if not TOKEN:
    raise ValueError("The Telegram bot TOKEN is missing from the environment variables.")