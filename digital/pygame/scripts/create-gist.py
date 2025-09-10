#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Create a GitHub Gist from tangled markdown files
Note: Requires a GitHub token with gist permissions
"""

import json
import subprocess
import os

def create_gist_json():
    """Create JSON payload for gist creation"""
    
    files = [
        "PYGAME-REQUIREMENTS-INDEX.md",
        "PYGAME-REQUIREMENTS.md",
        "DATA-FORMATS.md",
        "IMPLEMENTATION-HANDOFF.md",
        "INTEGRATION-PLAN.md"
    ]
    
    gist_data = {
        "description": "Pipeline & Peril - PyGame Implementation Requirements",
        "public": True,
        "files": {}
    }
    
    for filename in files:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                gist_data["files"][filename] = {
                    "content": f.read()
                }
    
    return json.dumps(gist_data, indent=2)

def main():
    # First, tangle all files from org-mode
    print("Note: Run org-babel-tangle first to extract markdown files!")
    
    # Create gist JSON
    gist_json = create_gist_json()
    
    print("\nGist JSON created. To upload:")
    print("1. Save your GitHub token in GITHUB_TOKEN env variable")
    print("2. Run: curl -X POST -H 'Authorization: token $GITHUB_TOKEN' \\")
    print("        -H 'Accept: application/vnd.github.v3+json' \\")
    print("        https://api.github.com/gists \\")
    print("        -d @gist.json")
    
    with open("gist.json", "w") as f:
        f.write(gist_json)
    
    print("\nGist payload saved to gist.json")

if __name__ == "__main__":
    main()
