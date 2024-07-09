If (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
  Start-Process powershell.exe "-File",('"{0}"' -f $MyInvocation.MyCommand.Path) -Verb RunAs
  exit
}

$taskName = "JoblessWebscraper"
$scriptPath = "$PSScriptRoot\webscraper.bat"

schtasks /Create /TN $taskName /TR "$scriptPath" /SC MINUTE /MO 10 /F