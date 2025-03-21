# This script serves as the entrypoint for submitting the Flower Federated Learning Simulation as a Ray job.
# To invoke this script, run `ptyhon flwr_run.py .` if you would originally intended to run `flwr run .`

# If you would run:
# flwr run . local-simulation-gpu --run-config "num-server-rounds=5"
# Run this instead:
# python flwr_run.py . local-simulation-gpu --run-config "num-server-rounds=5"

# Via ray job submit,  no need to have local environment with dependencies
# Have ray installed locally (version needs to match the cluster)
# Set the simulation requirements on the job runtime environment
# ray job submit \
# --runtime-env-json '{"working_dir": ".", "pip": ["flwr", "torch==2.5.1", "torchvision==0.20.1", "flwr-datasets[vision]", "datasets==2.14.6"]}' \
# -- python flwr_run.py . local-simulation-gpu --run-config "num-server-rounds=5"


import sys
from typing import List
from flwr.cli.app import typer_click_object

def run_with_args(args: List[str] = None):
    """Run the Flower CLI with the provided arguments."""
    if args is None:
        args = sys.argv[1:]
    
    # Get the original CLI command object
    cli = typer_click_object
    
    # Call the CLI with provided arguments
    # This routes to the correct command based on the first argument
    cli(args, standalone_mode=False)

if __name__ == "__main__":
    print("Running Flower Federated Learning Simulation")
    
    # Flower run command + all arguments after the script name
    args = ["run"] + sys.argv[1:]

    try:
        run_with_args(args)
    except SystemExit as e:
        # Handle the system exit that Typer might raise
        if e.code != 0:
            print(f"Command failed with exit code {e.code}")
        sys.exit(e.code)
