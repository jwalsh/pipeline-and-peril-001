# Makefile for Experiment 001: Service Cost Optimization
# Automated pipeline for running experiments and generating reports

.PHONY: all clean baseline variations analyze report help

# Configuration
PYTHON := python3
GAMES_PER_CONFIG := 100
SEED := 42
TIMESTAMP := $(shell date +%Y%m%d_%H%M%S)

# Directories
INPUT_DIR := inputs
OUTPUT_DIR := outputs
EXAMPLE_DIR := examples
VIZ_DIR := $(OUTPUT_DIR)/visualizations

# Files
BASELINE_CONFIG := $(INPUT_DIR)/baseline.yaml
VARIATIONS_DIR := $(INPUT_DIR)/variations
RESULTS_FILE := $(OUTPUT_DIR)/results.json
ANALYSIS_FILE := $(OUTPUT_DIR)/analysis.html
OPTIMAL_CONFIG := $(OUTPUT_DIR)/optimal_config.yaml
LOG_FILE := $(OUTPUT_DIR)/experiment_$(TIMESTAMP).log

# Default target
all: setup baseline variations analyze report
	@echo "✅ Experiment 001 complete!"
	@echo "📊 Results available in $(OUTPUT_DIR)/"

# Help target
help:
	@echo "Experiment 001: Service Cost Optimization"
	@echo ""
	@echo "Available targets:"
	@echo "  make all        - Run complete experiment pipeline"
	@echo "  make baseline   - Run baseline configuration (1000 games)"
	@echo "  make variations - Test all cost variations"
	@echo "  make analyze    - Perform statistical analysis"
	@echo "  make report     - Generate HTML report"
	@echo "  make clean      - Remove all outputs"
	@echo "  make help       - Show this help message"
	@echo ""
	@echo "Configuration:"
	@echo "  Games per config: $(GAMES_PER_CONFIG)"
	@echo "  Random seed: $(SEED)"

# Setup directories
setup:
	@echo "🔧 Setting up experiment directories..."
	@mkdir -p $(OUTPUT_DIR)
	@mkdir -p $(VIZ_DIR)
	@mkdir -p $(VARIATIONS_DIR)
	@echo "✅ Directories created"

# Generate input configurations
generate-inputs: setup
	@echo "📝 Generating input configurations..."
	@$(PYTHON) generate_configs.py \
		--output-dir $(VARIATIONS_DIR) \
		--baseline $(BASELINE_CONFIG)
	@echo "✅ Generated $(shell ls $(VARIATIONS_DIR) | wc -l) configurations"

# Run baseline experiment
baseline: setup
	@echo "🎮 Running baseline experiment (1000 games)..."
	@$(PYTHON) run_experiment.py \
		--config $(BASELINE_CONFIG) \
		--games 1000 \
		--seed $(SEED) \
		--output $(OUTPUT_DIR)/baseline_results.json \
		--log $(LOG_FILE)
	@echo "✅ Baseline complete"

# Run all variations
variations: generate-inputs
	@echo "🔬 Running cost variations..."
	@for config in $(VARIATIONS_DIR)/*.yaml; do \
		echo "  Running $$(basename $$config)..."; \
		$(PYTHON) run_experiment.py \
			--config $$config \
			--games $(GAMES_PER_CONFIG) \
			--seed $(SEED) \
			--output $(OUTPUT_DIR)/$$(basename $$config .yaml)_results.json \
			--log $(LOG_FILE); \
	done
	@echo "✅ All variations complete"

# Combine results
combine-results:
	@echo "📊 Combining results..."
	@$(PYTHON) combine_results.py \
		--input-dir $(OUTPUT_DIR) \
		--output $(RESULTS_FILE)
	@echo "✅ Results combined into $(RESULTS_FILE)"

# Statistical analysis
analyze: combine-results
	@echo "📈 Performing statistical analysis..."
	@$(PYTHON) analyze_results.py \
		--input $(RESULTS_FILE) \
		--output-dir $(OUTPUT_DIR) \
		--viz-dir $(VIZ_DIR)
	@echo "✅ Analysis complete"

# Generate HTML report
report: analyze
	@echo "📄 Generating HTML report..."
	@jupyter nbconvert --execute analysis.ipynb \
		--to html \
		--output $(ANALYSIS_FILE) \
		--ExecutePreprocessor.timeout=600
	@echo "✅ Report generated: $(ANALYSIS_FILE)"

# Validate optimal configuration
validate: analyze
	@echo "✓ Validating optimal configuration..."
	@$(PYTHON) run_experiment.py \
		--config $(OPTIMAL_CONFIG) \
		--games 5000 \
		--seed $(SEED) \
		--output $(OUTPUT_DIR)/validation_results.json \
		--log $(LOG_FILE)
	@echo "✅ Validation complete"

# Clean outputs
clean:
	@echo "🧹 Cleaning outputs..."
	@rm -rf $(OUTPUT_DIR)
	@rm -rf $(VARIATIONS_DIR)
	@echo "✅ Outputs cleaned"

# Archive results
archive:
	@echo "📦 Archiving results..."
	@tar -czf experiment_001_$(TIMESTAMP).tar.gz \
		$(OUTPUT_DIR) \
		$(INPUT_DIR) \
		README.md \
		Makefile
	@echo "✅ Archive created: experiment_001_$(TIMESTAMP).tar.gz"

# Quick test (10 games)
test:
	@echo "🧪 Running quick test..."
	@$(PYTHON) run_experiment.py \
		--config $(BASELINE_CONFIG) \
		--games 10 \
		--seed $(SEED) \
		--output $(OUTPUT_DIR)/test_results.json \
		--verbose
	@echo "✅ Test complete"

# Watch experiment progress
watch:
	@tail -f $(LOG_FILE)

# Generate example configuration
example:
	@echo "📝 Generating example configuration..."
	@cat > $(EXAMPLE_DIR)/example_config.yaml <<EOF
	# Example configuration for service costs experiment
	service_costs:
	  compute:
	    cpu: 2
	    memory: 2
	    storage: 1
	    capacity: 5
	  database:
	    cpu: 1
	    memory: 2
	    storage: 3
	    capacity: 3
	  cache:
	    cpu: 1
	    memory: 3
	    storage: 1
	    capacity: 8
	  queue:
	    cpu: 1
	    memory: 1
	    storage: 2
	    capacity: 6
	  load_balancer:
	    cpu: 2
	    memory: 1
	    storage: 1
	    capacity: 10
	  api_gateway:
	    cpu: 1
	    memory: 1
	    storage: 1
	    capacity: 7
	
	simulation:
	  games: 100
	  players: 4
	  strategy: balanced
	  grid_width: 8
	  grid_height: 6
	  max_rounds: 20
	  victory_threshold: 0.8
	EOF
	@echo "✅ Example configuration created"

# Dependencies
$(RESULTS_FILE): $(VARIATIONS_DIR)/*.yaml
$(ANALYSIS_FILE): $(RESULTS_FILE)
$(OPTIMAL_CONFIG): $(RESULTS_FILE)