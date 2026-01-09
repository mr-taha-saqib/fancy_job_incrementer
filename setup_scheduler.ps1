$action = New-ScheduledTaskAction -Execute 'python' -Argument 'C:\Users\DELL\fancy_job_incrementer\update_number.py' -WorkingDirectory 'C:\Users\DELL\fancy_job_incrementer'
$trigger = New-ScheduledTaskTrigger -Daily -At 12pm
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName 'DailyNumberIncrementer' -Description 'Automatically increments number and commits to GitHub daily' -Force
Write-Host "Task scheduler created successfully! The script will run daily at 12:00 PM (noon)."
