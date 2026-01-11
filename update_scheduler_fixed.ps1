# Remove old task
Unregister-ScheduledTask -TaskName 'DailyNumberIncrementer' -Confirm:$false

# Create new task with full Python path
$action = New-ScheduledTaskAction -Execute 'C:\Users\DELL\anaconda3\python.exe' -Argument 'C:\Users\DELL\fancy_job_incrementer\update_number.py' -WorkingDirectory 'C:\Users\DELL\fancy_job_incrementer'
$trigger = New-ScheduledTaskTrigger -Daily -At 3pm
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName 'DailyNumberIncrementer' -Description 'Automatically increments number and commits to GitHub daily'

Write-Host "Task scheduler updated with full Python path!"
Write-Host "It will now run daily at 3:00 PM or when you turn on your laptop after a missed run."
