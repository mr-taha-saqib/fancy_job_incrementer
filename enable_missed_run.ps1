$task = Get-ScheduledTask -TaskName 'DailyNumberIncrementer'
$task.Settings.StartWhenAvailable = $true
Set-ScheduledTask -InputObject $task
Write-Host "Task updated! It will now run after a missed schedule when you turn on your computer."
