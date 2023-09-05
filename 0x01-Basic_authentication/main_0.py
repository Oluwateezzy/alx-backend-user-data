#!/usr/bin/env python3
""" Main 0
"""
from api.v1.auth.auth import Auth

a = Auth()

excluded_paths = ["/api/v1/stat*"]
print(a.require_auth("/api/v1/stats", excluded_paths))