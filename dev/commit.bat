cd ..
cd sample
pyinstaller --distpath ../bin --onefile %1
git add .
git commit -m %2
git push -u origin main
pause