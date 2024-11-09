![Alt text](/Resources/ExcessFiles/TitleImage.png?raw=true)

![Static Badge](https://img.shields.io/badge/FOSS-white)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

# 🤔 Why PlagiaSight ?
Too many existing "plagiarism detection" tools just output a rather meaningless "plagiarism percentage" when the user provides them text.

We decided to adress this issue by ourselves, by creating an app that would provide comprehensive insights by analyzing given text(s) under different perspectives, hence the existence of PlagiaSight !

Our tool aims to keep results clear and *interpretable* (so : the tool won't draw *definitive conclusions*, but rather *provide useful stats and guidance*), allowing users to use their own critical thinking rather than letting the tool forcefully impose a judgment.




# 📽️ Application Demo
![Alt text](/Resources/ExcessFiles/Demo.gif?raw=true)




# 💡 Do you want...
- ⬇️	<ins>**To GET STARTED using PlagiaSight ?**	</ins>
<ul>

Welcome ! Please follow these **installation instructions** :

## Requirements
    - `pip` (version 21 or later)
    - `python 3.7 - 3.12`

First, install and unzip [**our latest release**](https://github.com/Daniel-Dfg/PlagiaSight/tags). Then:

- **MacOS / Linux**


    In the folder you just unzipped, simply run `PlagiaSight_Mac_Linux` **in your terminal/CLI the first time**.


    In other words, open your terminal/CLI and type the full file path :
    ```py
    #should resemble something like this
    path/to/plagiasight_folder/PlagiaSight_Mac_Linux.sh
    ```
    Or just right click on the file and select the option to run it in your terminal. The first time, it can take up to 2-3 minutes to download everything and launch the app, depending of your internet connection.

    If it fails, retry the process in in `sudo/superuser` mode (e.g type `sudo path/to/plagiasight_folder/PlagiaSight_Mac_Linux.sh`).


    The next time you'll want to run PlagiaSight, just run `PlagiaSight_Mac_Linux.sh` (not necessarily in your terminal), and it should launch in seconds :)


    If this doesn't work, you can also install and run the app manually :
      - If there's a folder named `venv` in the release you unzipped, delete it.
      - Then open the terminal at PlagiaSight's folder and the following, one line after another :
          ```python
              python3 -m venv .venv #recreate a 'clean' venv folder
              source venv/bin/activate #activate the venv folder to install dependencies inside
              pip install -r requirements.txt #reinstall dependencies from scratch
              python3 src/main.py #run the app
          ```
  



- **Windows**

    In the folder you just unzipped, simply run `PlagiaSight_Windows.bat` **in your terminal the first time** (cmd/Powershell on Windows).


    In other words, you open your cmd/Powershell and type the full path towards the path :

    ```py
    #should resemble something like this
    path\to\plagiasight_folder\PlagiaSight_Windows.bat
    ```
    Or just right-click on `PlagiaSight_Windows.bat` and click on "run in terminal". It can take up to 2-3 minutes for everything to be installed and for the app to start running the first time, depending on your internet connection.


    If it fails, please retry while being in administrator mode.


    The next time you'll want to run PlagiaSight, just run `PlagiaSight_Windows.bat` (not necessarily in your terminal), and it should launch in seconds :)


IMPORTANT : after you unzipped and executed the release you donwloaded for the first time, a folder named `venv` will appear. If you wish to move PlagiaSight's application folder afterwards, you MUST delete the `venv` folder before launching the application again !


*If you have trouble executing any of these steps*, don't hesitate to [**contact us**](https://github.com/Daniel-Dfg/PlagiaSight/blob/main/README.md#contact-the-people-behind-the-10-version) !




</ul>



- 🤝 <ins>**To CONTRIBUTE to the developement of PlagiaSight ?**	</ins>
<ul>

We're always glad to see new contributors ! Here's a roadmap to get you started :


**1) MANIFESTO** : The #1 thing you must read before contributing is [our short **manifesto**](https://github.com/Daniel-Dfg/PlagiaSight/blob/main/Resources/Manifesto/A%20Manifesto%20for%20PlagiaSight.md).


It contains the principles guiding PlagiaSight's developement, the structure of our codebase, and much more. In essence, it is the map that will guide you when you'll browse through the project's files.



**2) FIRST PULL REQUEST** : Once you read and understood the manifesto, take a look at the codebase. [Make a Pull Request](https://github.com/Daniel-Dfg/PlagiaSight/pulls) or [Open an Issue](https://github.com/Daniel-Dfg/PlagiaSight/issues) if you spot any areas for improvement.


We encourage you to contribute, even if your Pull Request gets closed without being implemented : in PlagiaSight's case, *it's better to try and fail to improve something rather than be scared to tell that something's wrong*.



**3) OTHER DOCUMENTATION** : Suggesting new features is often challenging, notably because predicting how *useful* a new feature will be is not an exact science. In order to maximize the chances to see your idea being approved, please check out the [resources that inspired us](https://github.com/Daniel-Dfg/PlagiaSight/tree/main/Resources/Learning%20Material) first, and consider contributing there if it seems to align with the project's vision.


But we can't stress enough the idea that, in order to propose new features that have a chance of being useful, *you should take a peek at the documentation directly present in the project to understand all contributors' vision first*. This will help ensure your proposals are cohesive with the project's goals.



*If you have questions or concerns regarding contributions*, feel free to [**contact us**](https://github.com/Daniel-Dfg/PlagiaSight/blob/main/README.md#contact-the-people-behind-the-10-version) !

</ul>


# 💬 Contact the people behind the 1.0 version

* **Daniel-Dfg** :
  * [github.com/Daniel-Dfg](https://github.com/Daniel-Dfg)
  * [danieldefoing@gmail.com](mailto:danieldefoing@gmail.com)
  * [D:D](https://discord.com/users/720963652286414909) on Discord


* **LUCKYINS** :
  * [github.com/LUCKYINS](https://github.com/LUCKYINS)
  * [elhusseinabdalrahmanwork@gmail.com](mailto:elhusseinabdalrahmanwork@gmail.com)
  * [LUCKYINS](https://discord.com/users/721008804300455978) on Discord


* **onuriscoding** :
  * [github.com/onuriscoding](https://github.com/onuriscoding)
  * [onurdogancs@gmail.com](mailto:onurdogancs@gmail.com)
  * [ginorwhat](https://discord.com/users/332553376707510272) on Discord
