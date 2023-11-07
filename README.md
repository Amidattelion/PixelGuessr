# PixelGuessr
Guess the image has its resolution progressively increase from 2 pixels to full resolution ! Works with a list of user provided urls pointing toward google images.

![image](https://github.com/Amidattelion/PixelGuessr/assets/87083034/4348b473-57f1-4e6e-bdaa-b363b18c50c6) ![image](https://github.com/Amidattelion/PixelGuessr/assets/87083034/8ff2d70e-c58e-48d1-930f-a9a3f8fc1671)

# Setup:
The code have only been tested on Windows, but should works on Linux.

**1 - Clone the repository with git (https://github.com/Amidattelion/PixelGuessr.git) or download and extract it**

**2 - Install the requirements with pip:**

It is advised to first create and activate a dedicated virtual environment before proceeding.
Open a terminal and cd in the "SYMP" folder that you have just extracted, then run the following command to install the python dependencies:

```
$ pip install -r requirements.txt
```

**3 - Create a guess list:**

Create a .txt file and fill it with images to guess. Each line is in format!

```
Category : Answer : URL
```

- Category: the category of the image. The game will loop through each categories
- Answer: the correct answer to guess (will be displayed at the image revealing)
- URL: url pointing toward the image (must end with an image file extension: '.jpg', 'png' are supported, other should be tested). You can also replace the URL with a local path to a picture on your computer

Example of a working "list.txt":

```
Monument : Emerald Buddha : https://upload.wikimedia.org/wikipedia/commons/8/8d/Emerald_Buddha.jpg
VideoGame : Minecraft  : https://image.api.playstation.com/vulcan/img/cfn/11307x4B5WLoVoIUtdewG4uJ_YuDRTwBxQy0qP8ylgazLLc01PBxbsFG1pGOWmqhZsxnNkrU3GXbdXIowBAstzlrhtQ4LCI4.png
Family : Dad : D:\Photo\2019\Christmas\IMG_20191228_175432.jpg
```

**4 - Edit the "LaunchGame.py" file: change the "game_file" variable to the path to your list of urls**

**5 - Launch the Game: "LaunchGame.bat" or python LaunchGame.py**
