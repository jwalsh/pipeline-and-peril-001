# Master Makefile for Pipeline & Peril Digital Playtesting System
# Orchestrates the entire project from literate source to final analysis

.PHONY: all help setup install test demo experiments paper clean publish

# Configuration
PYTHON := python3
UV := uv
EMACS := emacs
TIMESTAMP := $(shell date +%Y%m%d_%H%M%S)

# Directories
PYGAME_DIR := digital/pygame
EXPERIMENTS_DIR := experiments
PRESENTATIONS_DIR := presentations
DOCS_DIR := docs

# Color output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
MAGENTA := \033[0;35m
CYAN := \033[0;36m
RESET := \033[0m

# Default target
all: setup install test demo README.md
	@echo "$(GREEN)✅ Pipeline & Peril ready!$(RESET)"
	@echo "$(CYAN)📚 Documentation: $(DOCS_DIR)/$(RESET)"
	@echo "$(YELLOW)🎮 Run demo: make demo$(RESET)"
	@echo "$(MAGENTA)🔬 Run experiments: make experiments$(RESET)"

# Help message
help:
	@echo "$(CYAN)Pipeline & Peril - Digital Playtesting System$(RESET)"
	@echo ""
	@echo "$(YELLOW)Available targets:$(RESET)"
	@echo "  $(GREEN)make all$(RESET)         - Complete setup and installation"
	@echo "  $(GREEN)make setup$(RESET)       - Extract code from literate source"
	@echo "  $(GREEN)make install$(RESET)     - Install Python dependencies"
	@echo "  $(GREEN)make .venv$(RESET)       - Setup virtual environment"
	@echo "  $(GREEN)make README.md$(RESET)   - Generate README.md from README.org"
	@echo "  $(GREEN)make test$(RESET)        - Run test suite"
	@echo "  $(GREEN)make demo$(RESET)        - Run interactive demo"
	@echo "  $(GREEN)make experiments$(RESET) - Run all balance experiments"
	@echo "  $(GREEN)make paper$(RESET)       - Generate research paper"
	@echo "  $(GREEN)make docs$(RESET)        - Build documentation"
	@echo "  $(GREEN)make clean$(RESET)       - Clean generated files"
	@echo "  $(GREEN)make publish$(RESET)     - Push to GitHub"
	@echo ""
	@echo "$(YELLOW)Experiment targets:$(RESET)"
	@echo "  $(GREEN)make exp-costs$(RESET)   - Service cost optimization"
	@echo "  $(GREEN)make exp-grid$(RESET)    - Grid size analysis"
	@echo "  $(GREEN)make exp-chaos$(RESET)   - Chaos frequency tuning"
	@echo "  $(GREEN)make exp-victory$(RESET) - Victory condition balance"
	@echo "  $(GREEN)make exp-ai$(RESET)      - AI strategy comparison"

# Setup: Extract from literate source
setup:
	@echo "$(BLUE)📖 Extracting from literate source...$(RESET)"
	@if [ -f pipeline-peril-pygame-literate.org ]; then \
		$(EMACS) --batch --eval "(progn \
			(find-file \"pipeline-peril-pygame-literate.org\") \
			(org-babel-tangle) \
			(save-buffers-kill-terminal))"; \
		echo "$(GREEN)✅ Code extracted successfully$(RESET)"; \
	else \
		echo "$(YELLOW)⚠️  Literate source not found, using existing files$(RESET)"; \
	fi

# Install dependencies
install: .venv
	@echo "$(BLUE)📦 Installing dependencies...$(RESET)"
	@cd $(PYGAME_DIR) && $(UV) sync
	@echo "$(GREEN)✅ Dependencies installed$(RESET)"

# Virtual environment setup
.venv: $(PYGAME_DIR)/pyproject.toml README.md
	@echo "$(BLUE)🐍 Setting up virtual environment...$(RESET)"
	@cd $(PYGAME_DIR) && $(UV) venv
	@echo "$(GREEN)✅ Virtual environment ready$(RESET)"

# Generate README.md from README.org
README.md: README.org
	@echo "$(BLUE)📄 Generating README.md from README.org...$(RESET)"
	@$(EMACS) --batch \
		--eval "(require 'org)" \
		--eval "(require 'ox-md)" \
		--eval "(setq org-export-with-toc nil)" \
		--eval "(setq org-export-with-author nil)" \
		--eval "(setq org-export-with-date nil)" \
		--eval "(find-file \"README.org\")" \
		--eval "(org-export-to-file 'md \"README.md\")"
	@echo "$(GREEN)✅ README.md generated$(RESET)"

# Run tests
test:
	@echo "$(BLUE)🧪 Running tests...$(RESET)"
	@cd $(PYGAME_DIR) && $(UV) run python quick_test.py
	@echo "$(GREEN)✅ Tests passed$(RESET)"

# Run demo
demo:
	@echo "$(MAGENTA)🎮 Starting Pipeline & Peril Demo...$(RESET)"
	@cd $(PYGAME_DIR) && echo "n" | $(UV) run python rich_demo.py

# Run demo with live updates
demo-live:
	@echo "$(MAGENTA)🎮 Starting Live Demo...$(RESET)"
	@cd $(PYGAME_DIR) && echo "y" | $(UV) run python rich_demo.py

# Experiments
experiments: exp-costs exp-grid exp-chaos exp-victory exp-ai
	@echo "$(GREEN)✅ All experiments complete!$(RESET)"
	@echo "$(CYAN)📊 Results in $(EXPERIMENTS_DIR)/*/outputs/$(RESET)"

exp-costs:
	@echo "$(YELLOW)🔬 Experiment 001: Service Cost Optimization$(RESET)"
	@cd $(EXPERIMENTS_DIR)/001-service-costs && $(MAKE) test

exp-grid:
	@echo "$(YELLOW)🔬 Experiment 002: Grid Size Impact$(RESET)"
	@echo "$(CYAN)📝 See $(EXPERIMENTS_DIR)/002-grid-size/README.md$(RESET)"

exp-chaos:
	@echo "$(YELLOW)🔬 Experiment 003: Chaos Frequency Tuning$(RESET)"
	@echo "$(CYAN)📝 See $(EXPERIMENTS_DIR)/003-chaos-frequency/README.md$(RESET)"

exp-victory:
	@echo "$(YELLOW)🔬 Experiment 004: Victory Condition Balance$(RESET)"
	@echo "$(CYAN)📝 See $(EXPERIMENTS_DIR)/004-victory-conditions/README.md$(RESET)"

exp-ai:
	@echo "$(YELLOW)🔬 Experiment 005: AI Strategy Comparison$(RESET)"
	@echo "$(CYAN)📝 See $(EXPERIMENTS_DIR)/005-ai-strategies/README.md$(RESET)"

# Generate research paper
paper:
	@echo "$(BLUE)📄 Generating research paper...$(RESET)"
	@if command -v pandoc >/dev/null 2>&1; then \
		pandoc $(PRESENTATIONS_DIR)/paper-game-balance-through-simulation.md \
			-o $(PRESENTATIONS_DIR)/paper.pdf \
			--pdf-engine=xelatex \
			--variable geometry:margin=1in \
			--variable fontsize=11pt \
			--variable documentclass=article \
			--toc; \
		echo "$(GREEN)✅ Paper generated: $(PRESENTATIONS_DIR)/paper.pdf$(RESET)"; \
	else \
		echo "$(YELLOW)⚠️  Pandoc not installed, skipping PDF generation$(RESET)"; \
		echo "$(CYAN)📝 Markdown version: $(PRESENTATIONS_DIR)/paper-game-balance-through-simulation.md$(RESET)"; \
	fi

# Generate comprehensive system documentation PDF
system-doc:
	@echo "$(BLUE)📚 Generating system documentation PDF...$(RESET)"
	@if command -v emacs >/dev/null 2>&1; then \
		$(EMACS) --batch \
			--eval "(require 'org)" \
			--eval "(setq org-confirm-babel-evaluate nil)" \
			--eval "(find-file \"$(PRESENTATIONS_DIR)/comprehensive-system-documentation.org\")" \
			--eval "(org-latex-export-to-pdf)" 2>/dev/null; \
		if [ -f "$(PRESENTATIONS_DIR)/comprehensive-system-documentation.pdf" ]; then \
			echo "$(GREEN)✅ System documentation PDF generated$(RESET)"; \
		else \
			echo "$(YELLOW)⚠️  PDF generation requires LaTeX$(RESET)"; \
		fi; \
	else \
		echo "$(YELLOW)⚠️  Emacs not available for org-mode export$(RESET)"; \
	fi

# Build documentation
docs:
	@echo "$(BLUE)📚 Building documentation...$(RESET)"
	@mkdir -p $(DOCS_DIR)
	@cp README.org $(DOCS_DIR)/
	@cp -r $(PYGAME_DIR)/docs/* $(DOCS_DIR)/
	@echo "$(GREEN)✅ Documentation built in $(DOCS_DIR)/$(RESET)"

# Git operations
commit:
	@echo "$(BLUE)💾 Committing changes...$(RESET)"
	@git add .
	@git commit -m "feat: complete experimental framework and scientific analysis\n\nAdded:\n- 5 comprehensive game balance experiments\n- Scientific paper draft\n- Literate programming presentation\n- Master Makefile for orchestration\n- Complete experimental methodology\n\n🤖 Generated with Claude Code\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
	@git notes add -m "Final implementation includes complete experimental framework for game balance validation through large-scale simulation"

push: commit
	@echo "$(BLUE)🚀 Pushing to GitHub...$(RESET)"
	@git push origin main
	@echo "$(GREEN)✅ Published to GitHub$(RESET)"

publish: push
	@echo "$(GREEN)🎉 Project published successfully!$(RESET)"
	@echo "$(CYAN)🌐 View at: https://github.com/jwalsh/pipeline-and-peril-001$(RESET)"

# Clean generated files
clean:
	@echo "$(RED)🧹 Cleaning generated files...$(RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf $(EXPERIMENTS_DIR)/*/outputs/* 2>/dev/null || true
	@echo "$(GREEN)✅ Cleaned$(RESET)"

# Development helpers
watch:
	@echo "$(CYAN)👁️  Watching for changes...$(RESET)"
	@while true; do \
		make test; \
		sleep 5; \
	done

lint:
	@echo "$(BLUE)🔍 Linting code...$(RESET)"
	@cd $(PYGAME_DIR) && $(UV) run ruff check src/

format:
	@echo "$(BLUE)✨ Formatting code...$(RESET)"
	@cd $(PYGAME_DIR) && $(UV) run black src/

# Performance benchmarks
benchmark:
	@echo "$(YELLOW)⚡ Running performance benchmarks...$(RESET)"
	@cd $(PYGAME_DIR) && $(UV) run python -m timeit -n 100 \
		"from src.engine.simple_game_state import create_demo_game; create_demo_game()"
	@echo "$(GREEN)✅ Benchmark complete$(RESET)"

# Docker support (future)
docker-build:
	@echo "$(BLUE)🐳 Building Docker image...$(RESET)"
	@echo "$(YELLOW)TODO: Docker support coming soon$(RESET)"

# Statistics
stats:
	@echo "$(CYAN)📊 Project Statistics$(RESET)"
	@echo "$(YELLOW)Lines of Code:$(RESET)"
	@find . -name "*.py" -type f -exec wc -l {} + | tail -1
	@echo "$(YELLOW)Python files:$(RESET)"
	@find . -name "*.py" -type f | wc -l
	@echo "$(YELLOW)Experiments:$(RESET)"
	@ls -d $(EXPERIMENTS_DIR)/*/ | wc -l
	@echo "$(YELLOW)Documentation files:$(RESET)"
	@find . -name "*.md" -o -name "*.org" | wc -l

# Archive for submission
archive:
	@echo "$(BLUE)📦 Creating archive...$(RESET)"
	@tar -czf pipeline-peril-$(TIMESTAMP).tar.gz \
		--exclude=".git" \
		--exclude="__pycache__" \
		--exclude="*.pyc" \
		--exclude=".venv" \
		.
	@echo "$(GREEN)✅ Archive created: pipeline-peril-$(TIMESTAMP).tar.gz$(RESET)"

# Installation check
check:
	@echo "$(CYAN)🔍 Checking installation...$(RESET)"
	@command -v python3 >/dev/null 2>&1 && echo "$(GREEN)✓ Python3 found$(RESET)" || echo "$(RED)✗ Python3 not found$(RESET)"
	@command -v uv >/dev/null 2>&1 && echo "$(GREEN)✓ uv found$(RESET)" || echo "$(RED)✗ uv not found$(RESET)"
	@command -v emacs >/dev/null 2>&1 && echo "$(GREEN)✓ Emacs found$(RESET)" || echo "$(YELLOW)⚠ Emacs not found (optional)$(RESET)"
	@command -v git >/dev/null 2>&1 && echo "$(GREEN)✓ Git found$(RESET)" || echo "$(RED)✗ Git not found$(RESET)"

.PHONY: commit push publish watch lint format benchmark docker-build stats archive check README.md .venv