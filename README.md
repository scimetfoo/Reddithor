Reddithor
==========

Reddithor - a fork of HackerTray - allows you to browse the posts from subreddit of your choice from within the tray of your Linux OS. Reddithor automatically updates every 2 minutes in the background. As mentioned in the readme of HackerTray, this application relies on appindicator, and is not guaranteed to run on every computer. 


##Screenshot

![Reddithor Screenshot on Ubuntu](http://i.imgur.com/7tjkMHU.png)

##Installation
Reddithor is distributed as a python package. Do the following to install:

``` sh
sudo pip install Reddithor
OR
#Download Source and cd into it
sudo python setup.py install
```

You can now run Reddithor from anywhere. You can also add it to your OS dependent session autostart method. In Ubuntu, you can access this via: 

1. System > Preferences > Sessions  
(OR)
2. System > Preferences > Startup Applications 

depending on your Ubuntu Version. Or alternatively, you may put it in `~/.config/openbox/autostart`.

###Upgrade
The latest stable version is [![the one on PyPi](https://badge.fury.io/py/Reddithor.svg)](https://pypi.python.org/pypi/Reddithor/)

You can check which version you have installed with `Reddithor --version`.

To upgrade, run `pip install -U Reddithor`. In some cases (Ubuntu), you might
need to clear the pip cache before upgrading:

`sudo rm -rf /tmp/pip-build-root/Reddithor`

Reddithor will automatically check the latest version on startup, and inform you if there is an update available.

##Options

`-c`: Enables comments support. Clicking on links will also open the comments page on Reddit.



##Features
1. Stay up-to-date on Reddit without the distraction of opening Reddit itself.
2. Opens links in your default browser
3. Remembers which links you opened
4. Shows Points/Comment count
5. Allows you to choose a subreddit that you want to keep a tab on

###Troubleshooting

If the app indicator fails to show in Ubuntu versions, consider installing 
python-appindicator with

`sudo apt-get install python-appindicator`

###TODO:

- Write unit tests
- Make a command line executable
- Migrate from pyGtk to pygobject

###Development

To develop on Reddithor, or to test out experimental versions, do the following:

- Clone the project
- Run `(sudo) python setup.py develop` in the Reddithor root directory
- Run `Reddithor` with the required command line options from anywhere.



##Credits

- Abhay Rana for [hackertray](https://github.com/captn3m0/hackertray).

##Author Information
- Murtaza Akbari (murtazasakbari@gmail.com)

##Licence

	Copyright 2016 Murtaza Akbari

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	   http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

