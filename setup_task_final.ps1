# Remove old task if exists
Unregister-ScheduledTask -TaskName 'DailyNumberIncrementer' -Confirm:$false -ErrorAction SilentlyContinue

# Create action with full Python path
$action = New-ScheduledTaskAction -Execute 'C:\Users\DELL\anaconda3\python.exe' -Argument 'C:\Users\DELL\fancy_job_incrementer\update_number.py' -WorkingDirectory 'C:\Users\DELL\fancy_job_incrementer'

# Create TWO triggers:
# 1. Daily at 12 PM
# 2. At logon (when you log into Windows)
$triggerDaily = New-ScheduledTaskTrigger -Daily -At 12pm
$triggerLogon = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

# Settings to ensure it runs
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

# Register the task with both triggers
Register-ScheduledTask -Action $action -Trigger @($triggerDaily, $triggerLogon) -Settings $settings -TaskName 'DailyNumberIncrementer' -Description 'Automatically increments number and commits to GitHub daily' -RunLevel Limited

Write-Host "Task created with TWO triggers:"
Write-Host "1. Daily at 12:00 PM (noon)"
Write-Host "2. Every time you log into Windows"
Write-Host ""
Write-Host "This ensures the script runs at least once per day when you use your laptop."
