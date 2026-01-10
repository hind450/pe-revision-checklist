#!/bin/bash

echo "=========================================="
echo "PE Assessment System - Web Interface"
echo "=========================================="
echo ""
echo "Starting web server..."
echo ""

cd "$(dirname "$0")/web"
python app.py
