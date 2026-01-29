#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime
import random

def already_committed_today():
    """Check if we already committed the daily number update today."""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--grep=^Update number:', '--format=%ci'],
            capture_output=True, text=True, check=True
        )
        if result.stdout.strip():
            last_commit_date = result.stdout.strip()[:10]  # Get YYYY-MM-DD
            today = datetime.now().strftime('%Y-%m-%d')
            return last_commit_date == today
        return False
    except subprocess.CalledProcessError:
        return False

def increment_number():
    """Read the current number, increment it, and write it back."""
    try:
        with open('number.txt', 'r') as f:
            current_number = int(f.read().strip())
    except FileNotFoundError:
        current_number = 0

    new_number = current_number + 1

    with open('number.txt', 'w') as f:
        f.write(str(new_number))

    return new_number

def generate_commit_message(number):
    """Generate a commit message."""
    use_llm = os.environ.get('FANCY_JOB_USE_LLM', 'false').lower() == 'true'

    if use_llm:
        try:
            from transformers import pipeline
            generator = pipeline('text-generation', model='openai-community/gpt2')
            prompt = f"Update number: {datetime.now().strftime('%Y-%m-%d')}"
            result = generator(prompt, max_length=50, num_return_sequences=1)
            return result[0]['generated_text']
        except Exception as e:
            print(f"LLM generation failed: {e}, using default message")
            return f"Update number: {datetime.now().strftime('%Y-%m-%d')}"
    else:
        return f"Update number: {datetime.now().strftime('%Y-%m-%d')}"

def push_pending_commits():
    """Push any pending commits that failed to push previously."""
    try:
        result = subprocess.run(
            ['git', 'rev-list', '--count', 'origin/main..HEAD'],
            capture_output=True, text=True, check=True
        )
        pending_count = int(result.stdout.strip())
        if pending_count > 0:
            print(f"Found {pending_count} unpushed commit(s), pushing now...")
            subprocess.run(['git', 'push'], check=True)
            print("Successfully pushed pending commits!")
            return True
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to push pending commits: {e}")
        return False

def git_commit_and_push(message):
    """Commit and push changes to git."""
    try:
        push_pending_commits()
        subprocess.run(['git', 'add', 'number.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        for attempt in range(3):
            try:
                subprocess.run(['git', 'push'], check=True)
                print(f"Successfully committed and pushed: {message}")
                return
            except subprocess.CalledProcessError:
                if attempt < 2:
                    print(f"Push failed, retrying ({attempt + 2}/3)...")
                    import time
                    time.sleep(5)
        print("Push failed after 3 attempts. Will retry next run.")
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")

def update_cron_job():
    """Update cron job to run at a new random time tomorrow."""
    # Generate random hour (0-23) and minute (0-59)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)

    # Get the absolute path to this script
    script_path = os.path.abspath(__file__)
    repo_path = os.path.dirname(script_path)

    # Create the cron job command
    use_llm = os.environ.get('FANCY_JOB_USE_LLM', 'false').lower() == 'true'
    if use_llm:
        cron_command = f"{random_minute} {random_hour} * * * cd {repo_path} && FANCY_JOB_USE_LLM=true uv run python {script_path}"
    else:
        cron_command = f"{random_minute} {random_hour} * * * cd {repo_path} && python {script_path}"

    print(f"Next run scheduled for {random_hour:02d}:{random_minute:02d}")
    print(f"Cron command: {cron_command}")

    # Note: Actual cron update would require subprocess calls to crontab
    # This is left as a manual step or can be automated with proper permissions

def main():
    print("Starting daily number incrementer...")

    # Check if we already committed today
    if already_committed_today():
        print("Already committed today. Skipping.")
        return

    # Increment the number
    new_number = increment_number()
    print(f"Incremented number to: {new_number}")

    # Generate commit message
    commit_message = generate_commit_message(new_number)

    # Commit and push
    git_commit_and_push(commit_message)

    # Update cron job for next random time
    update_cron_job()

    print("Done!")

if __name__ == "__main__":
    main()
