#!/bin/bash
set -e
echo "Starting Web3 Decentralized Identity Verification Tool..."
uvicorn app:app --host 0.0.0.0 --port 9104 --workers 1
