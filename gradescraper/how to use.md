First, you will need to find some way to get the selenium  headless webdriver. The easiest way to do that is by getting it on wsl. A headless browser is a browser without a user interface.

To install wsl: (if you want)
Follow this tutorial: https://www.windowscentral.com/install-windows-subsystem-linux-windows-10 (way better than anything I could explain)

```Also install Windows Terminal from Microsoft Store``` (It's just a better terminal.)

Once the site gets to the ```Disabling Windows Subsystem for Linux using Settings``` section, just close the window.
Then you will want to install firefox on your box so ```sudo apt install firefox```. (This is because I chose to make the program with the firefox version because chromium hates me).

After installing firefox, you will need to install geckodriver.
Geckodriver is basically a link from selenium to firefox.

To install follow these steps:
1. wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
2. tar -xvzf geckodriver-v0.24.0-linux64.tar.gz
3. chmod +x geckodriver
4. sudo mv geckodriver /usr/local/bin

Now, you will probably want to maybe run the program right away once you open windows terminal or your command prompt.
To do that, you can add the run command to your .bashrc in your home directory so, add ```python gradescraper.py``` to the end of the .bashrc file.
