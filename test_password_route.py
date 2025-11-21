#!/usr/bin/env python
"""Test script to verify password reset route is accessible"""
import requests
import json

try:
    # Test if the route exists
    response = requests.post(
        "http://127.0.0.1:8000/password/send-code",
        json={"email": "test@example.com"},
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 404:
        print("\n❌ Route not found! Backend service needs to be restarted.")
    elif response.status_code == 422:
        print("\n✅ Route exists! (422 is expected for invalid email)")
    else:
        print(f"\n✅ Route exists! Status: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend. Is the server running on port 8000?")
except Exception as e:
    print(f"❌ Error: {e}")

