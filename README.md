# RomeRemasteredTools

Plugin for sublime text 4 that adds features for Rome Remasted scripting


## Features


1. Syntax Highlighting for all .txt files

2. Documentation Popups on hover for all terms found in script blocks

3. Autocompletion for all conditions, events, commands, and console commands


## How to Install

Run the following script in the Sublime Text terminal ```(ctrl+` )``` which utilizes git clone for easy installation:
```
import os; path=sublime.packages_path(); (os.makedirs(path) if not os.path.exists(path) else None); window.run_command('exec', {'cmd': ['git', 'clone', 'https://github.com/dementive/RomeRemasteredTools', 'RomeRemasteredTools'], 'working_dir': path})
```
This will only work with git installed on your system.

Alternatively you can download the zip file from github and put the RomeRemasteredTools folder in the packages folder. This is not recommended because you will not receive updates unless you redownload it manually.
The packages folder can easily be found by going to ```preferences``` in the main menu and selecting ```Browse Packages```.
```
C:\Users\YOURUSERNAME\AppData\Roaming\Sublime Text 3\Packages\RomeRemasteredTools
```

## How to Enable Syntax

The syntax can be activated by going to:
```
main menu -> view -> syntax -> Open All with current extention as...
```
With a Rome Remastered .txt file open in sublime 
Select ```Rome Total War``` as the default syntax for .txt.


![Screenshot](/assets/screenshot.png)
![Screenshot2](/assets/screenshot2.png)