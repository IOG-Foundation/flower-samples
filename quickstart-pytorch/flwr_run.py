# To invoke this script, run `ptyhon flwr_run.py .` if you originally intended to run `flwr run .`
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

    # Here you can add any custom logic before running the Flower CLI
    print("Running Flower Federated Learning Simulation Distributed on a Ray Cluster")

    # Flower run command + all arguments after the script name
    args = ["run"] + sys.argv[1:]

    try:
        run_with_args(args)
    except SystemExit as e:
        # Handle the system exit that Typer might raise
        if e.code != 0:
            print(f"Command failed with exit code {e.code}")
        sys.exit(e.code)
