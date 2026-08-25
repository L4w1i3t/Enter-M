@echo off
setlocal

rem Delete all .rpyc files
for /r %%f in (*.rpyc) do del "%%f"

endlocal