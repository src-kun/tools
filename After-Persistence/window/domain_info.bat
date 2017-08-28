@echo off
set out_file=%1%
if %out_file%==""(
set out_file=msg.txt
)else(
echo ==============================================
set ipconfig=ipconfig /all
echo %ipconfig%
echo ==============================================
ipconfig /all >> %out_file%
echo.
echo.
)

echo type c:\windows\system32\drivers\etc\hosts >> msg.txt
type c:\windows\system32\drivers\etc\hosts >> msg.txt

echo net user >> msg.txt
net user >> msg.txt

echo whoami /all >> msg.txt
whoami /all >> msg.txt

echo tasklist >> msg.txt
tasklist /V >> msg.txt

echo qprocess * >> msg.txt
qprocess * >> msg.txt 

echo qprocess /SERVER:IP >>  msg.txt
qprocess /SERVER:IP  >> msg.txt

echo set >> msg.txt
set >> msg.txt 

echo systeminfo >> msg.txt 
systeminfo >> msg.txt

echo "net config workstation"
net config workstation >> msg.txt

echo net user /domain >> msg.txt
net user /domain >> msg.txt

echo net group /domain >> msg.txt
net group /domain >> msg.txt

echo net group "domain admins" /domain >> msg.txt
net group "domain admins" /domain >> msg.txt

echo net localgroup administrators /domain >> msg.txt
net localgroup administrators /domain >> msg.txt

echo net group "domain controllers" /domain >> msg.txt
net group "domain controllers" /domain >> msg.txt

echo net view >> msg.txt
net view >> msg.txt

echo net view /domain >> msg.txt
net view /domain >> msg.txt

echo route print >> msg.txt
route print >> msg.txt

echo netstat -an/ano/anb >> msg.txt
netstat -an/ano/anb >> msg.txt