#!/bin/bash
set -e

echo "=========================================================="
echo "  🏥 MEDIKIOSK LOCAL PROTOTYPE SUITE (PS 26047)"
echo "=========================================================="

# 1. Start FastAPI Backend Gateway on Port 8000
echo "▶️  [1/3] Starting FastAPI Clinical Gateway on http://localhost:8000 ..."
PYTHONPATH=. /opt/homebrew/bin/python3.14 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

sleep 2

# 2. Start Doctor Portal on Port 3000
echo "▶️  [2/3] Starting Doctor Consultation Portal on http://localhost:3000 ..."
/opt/homebrew/bin/python3.14 -m http.server 3000 --directory doctor_portal/public &
DOCTOR_PID=$!

# 3. Start Flutter Kiosk Web on Port 8080
echo "▶️  [3/3] Starting Patient Intake Kiosk on http://localhost:8080 ..."
/opt/homebrew/bin/python3.14 -m http.server 8080 --directory kiosk_app/build/web &
KIOSK_PID=$!

echo ""
echo "✨ ALL SERVICES ACTIVE & SYNCED:"
echo "   1. 📱 Patient Kiosk UI:       http://localhost:8080"
echo "   2. 🩺 Doctor Review Portal:    http://localhost:3000"
echo "   3. ⚡ FastAPI Gateway & Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services."

cleanup() {
    echo "Stopping all services..."
    kill $BACKEND_PID $DOCTOR_PID $KIOSK_PID 2>/dev/null || true
    exit 0
}

trap cleanup INT TERM
wait
