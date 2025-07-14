@echo off 
:loop 
echo 🔄 Updating HTML from API... 
python python_ssr_generator.py --api local --output index.html 
echo ⏳ Waiting 30 minutes for next update... 
timeout /t 1800 /nobreak 
goto loop 
