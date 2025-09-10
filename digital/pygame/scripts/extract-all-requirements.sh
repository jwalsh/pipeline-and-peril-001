#!/bin/bash
#!/bin/bash
# Extract all markdown files to create gist

echo "Extracting Pipeline & Peril PyGame Requirements..."

# Create output directory
mkdir -p pygame-requirements-gist

# Note: In actual use, these would be tangled from the org file
# For now, showing what files would be created:

cat << 'EOF' > pygame-requirements-gist/README.md
# Pipeline & Peril PyGame Requirements

This gist contains all requirements documentation for implementing a PyGame version of Pipeline & Peril for playtesting and rules validation.

## Files Included

1. **PYGAME-REQUIREMENTS-INDEX.md** - Navigation and overview
2. **PYGAME-REQUIREMENTS.md** - Complete requirements specification
3. **DATA-FORMATS.md** - JSON schemas and data structures  
4. **IMPLEMENTATION-HANDOFF.md** - Quick start for developers
5. **INTEGRATION-PLAN.md** - Repository structure guide

## Quick Start

1. Read IMPLEMENTATION-HANDOFF.md for overview
2. Check DATA-FORMATS.md for exact schemas
3. Follow INTEGRATION-PLAN.md for project setup
4. Use PYGAME-REQUIREMENTS.md for detailed specs

## Purpose

Create a digital version for:
- Rapid playtesting
- Rules validation
- Statistical analysis
- AI strategy development
- LLM agent integration (Ollama)

EOF

echo "Files ready for gist creation!"
echo "To create gist manually:"
echo "1. Go to https://gist.github.com"
echo "2. Upload the generated .md files"
echo "3. Set description: 'Pipeline & Peril - PyGame Implementation Requirements'"
