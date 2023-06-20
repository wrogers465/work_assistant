Set objShell = WScript.CreateObject("WScript.Shell")

' Put the path to your batch file in the following line
batchFile = ".\start_work_assistant.bat" 

objShell.Run batchFile, 0, True