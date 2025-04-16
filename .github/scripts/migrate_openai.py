import subprocess
import sys

def run_migration():
    try:
        # Install the latest openai package
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "openai"], check=True)
        
        # Run the migration tool
        result = subprocess.run([sys.executable, "-m", "openai", "migrate"], 
                             capture_output=True, 
                             text=True)
        
        print("Migration output:")
        print(result.stdout)
        if result.stderr:
            print("Migration errors:")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"Error during migration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration() 