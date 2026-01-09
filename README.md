# Daily Number Incrementer

A Python script that automatically increments a number in a text file, commits the change to Git, and updates a cron job to run the script at a new random time daily. Perfect for maintaining a daily commit streak or tracking sequential values with a dynamic schedule.

## Setup

### Clone this repository

```bash
git clone https://github.com/mr-taha-saqib/fancy_job_incrementer
cd fancy_job_incrementer
```

### Run the script

The script can be run without dependencies besides the Python standard library, simply by running:

```bash
python update_number.py
```

You might want to run the script manually for the first time to verify it works before setting up a cronjob.

### Optional: Use LLM-based commit message generation

If you wish to use LLM-based commit message generation, you need to install `uv` to manage dependencies. The first time you run it, it will download packages required for its execution and also a large language model from Hugging Face.

```bash
# Use LLM
FANCY_JOB_USE_LLM=true uv run python update_number.py
```

### Setup a cron job to run the script daily

**On Linux/macOS:**

```bash
crontab -e
```

Add the following line to the crontab file:

```bash
0 12 * * * cd /path/to/your/repo && python update_number.py
# or with LLM
0 12 * * * cd /path/to/your/repo && FANCY_JOB_USE_LLM=true uv run python update_number.py
```

This will initially run the script at 12pm (noon) the next day.

**On Windows:**

Use Windows Task Scheduler:
1. Open Task Scheduler
2. Create a new task that runs daily at 12:00 PM (noon)
3. Set the action to run: `python C:\path\to\fancy_job_incrementer\update_number.py`
4. Set the working directory to: `C:\path\to\fancy_job_incrementer`
5. Enable "Run task as soon as possible after a missed start" to ensure it runs when you turn on your laptop

## Usage

The script will increment the number in `number.txt` and commit the change to git. You can modify the script to increment by any value or use a different file to store the number.

By running this you will be able get a fancy streak on your github profile and get a job.

## Features

- Automatically increments a number daily
- Commits changes to Git with timestamped messages
- Optional LLM-based commit message generation
- Suggests random times for next execution (for cron job variety)
- Zero dependencies for basic usage
- Cross-platform support (Linux, macOS, Windows)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is open source and available for anyone to use and modify.
