#!/usr/bin/env python3
import subprocess, sys, os

script_path = os.path.join(os.path.dirname(__file__), "create_app.sh")
subprocess.run(["bash", script_path] + sys.argv[1:], check=True)
