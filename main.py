import yaml
import subprocess
import os
import sys
import datetime
import uuid

def main():
    # -------------------------------------------------------------------------
    # 0. Run Parameters
    # -------------------------------------------------------------------------
    # If data_files is empty, use all files in the data folder
    data_files = ["HR_DATA.csv"]
    query = "how many workers are male and what is their average age?"

    # -------------------------------------------------------------------------
    # 1. Configuration Settings
    #    Edit these values to update config.yaml before running
    # -------------------------------------------------------------------------
    
    # Generate unique run_id
    run_id = f"run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    
    config_updates = {
        "run_id": run_id,
        "model_name": "gpt-5",
        "interactive": False,
        "max_refinement_rounds": 1,
        "preserve_artifacts": True,
        # Add or update API keys here if needed, or rely on existing config.yaml
        # "OPENAI_API_KEY": "...", 
        
        # Optional: Configure specific models for different agents
        # "agent_models": {
        #     "PLANNER": "gpt-4",
        #     "CODER": "gemini-1.5-pro",
        #     "VERIFIER": "gemini-1.5-flash"
        # }
    }

    config_path = "config.yaml"

    # -------------------------------------------------------------------------
    # 2. Update config.yaml
    # -------------------------------------------------------------------------
    print(f"Updating {config_path}...")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            existing_config = yaml.safe_load(f) or {}
        
        # Update existing config with new values
        existing_config.update(config_updates)
        final_config = existing_config
    else:
        final_config = config_updates

    with open(config_path, 'w') as f:
        yaml.dump(final_config, f, default_flow_style=False)
    
    print(f"Configuration saved to {config_path}")

    # -------------------------------------------------------------------------
    # 3. Run dsstar.py
    # -------------------------------------------------------------------------
    # Command: uv run python dsstar.py --data-files HR_DATA.csv --query "..."

    # If data_files is empty, use all files in the data folder
    if not data_files:
        data_dir = "data"
        if os.path.exists(data_dir):
            data_files = [
                f for f in os.listdir(data_dir) 
                if os.path.isfile(os.path.join(data_dir, f)) and not f.startswith('.')
            ]
            print(f"Using all files from {data_dir}: {data_files}")
    
    command = [
        "uv", "run", "python", "dsstar.py",
        "--data-files", *data_files,
        "--query", query
    ]

    print(f"\nExecuting: {' '.join(command)}\n")
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExecution interrupted.")
        sys.exit(0)

if __name__ == "__main__":
    main()
