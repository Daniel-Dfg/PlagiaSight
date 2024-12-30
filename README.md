![Alt text](/Resources/ExcessFiles/TitleImage.png?raw=true)

![Static Badge](https://img.shields.io/badge/FOSS-white)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

# 🤔 Why PlagiaSight?

Many "plagiarism detection" tools simply provide a basic "plagiarism percentage" without offering meaningful insight into the content. 

PlagiaSight addresses this limitation by offering a comprehensive analysis of text through multiple lenses, aiming to keep results clear and *interpretable*. Our tool doesn’t draw absolute conclusions but instead offers valuable statistics and guidance, allowing users to apply their own judgment.

---

# 📽️ Application Demo

![Alt text](/Resources/ExcessFiles/Demo.gif?raw=true)

---

# 💡 Getting Started with PlagiaSight

Welcome! To start using PlagiaSight, please follow these installation instructions.

## Requirements

- `pip` (version 21 or later)
- `Python` (version 3.7 - 3.12)

1. First, download and unzip [**our latest release**](https://github.com/Daniel-Dfg/PlagiaSight/tags).
2. Then, follow the installation instructions for your operating system below:

### Installation on MacOS / Linux

1. Open the folder you just unzipped.
2. Run `PlagiaSight_Mac_Linux.sh` in your terminal or CLI. 

   - Open your terminal/CLI and enter the full path:
     ```bash
     # Example path
     path/to/plagiasight_folder/PlagiaSight_Mac_Linux.sh
     ```
   - Alternatively, right-click the file and choose the option to run it in the terminal.

   **Note**: The first launch may take 2-3 minutes, depending on your internet connection.

3. If you encounter any issues, try running the command with `sudo`:
   ```bash
   sudo path/to/plagiasight_folder/PlagiaSight_Mac_Linux.sh
   ```

After the first run, you can simply double-click `PlagiaSight_Mac_Linux.sh` to launch PlagiaSight—it should open in seconds.

#### Manual Installation (If Automatic Setup Fails)

If the above steps don’t work:

1. Delete the `venv` folder if it exists in the unzipped folder.
2. Open the terminal at PlagiaSight’s folder and run these commands:
   ```bash
   python3 -m venv .venv                # Create a new virtual environment
   source .venv/bin/activate            # Activate the virtual environment
   pip install -r requirements.txt      # Install dependencies
   python3 src/main.py                  # Run the app
   ```

Making the installation process smoother is a priority for us. Contributions and feedback are welcome!

### Installation on Windows

1. Open the folder you unzipped.
2. Run `PlagiaSight_Windows.bat` in the terminal (CMD or PowerShell).

   - Open CMD/PowerShell and enter the full path:
     ```bash
     # Example path
     path\to\plagiasight_folder\PlagiaSight_Windows.bat
     ```
   - Alternatively, right-click `PlagiaSight_Windows.bat` and choose "Run in terminal."

   **Note**: The first launch may take 2-3 minutes, depending on your internet connection.

3. If installation fails, try running the command as an administrator.

After the first run, you can simply double-click `PlagiaSight_Windows.bat` to launch the app quickly.

**Important**: If you move the PlagiaSight folder after installation, delete the `venv` folder before launching it again.

If you need assistance, feel free to [**contact us**](https://github.com/Daniel-Dfg/PlagiaSight/blob/main/README.md#contact-the-people-behind-the-10-version).

---

# 🤝 Contributing to PlagiaSight

We’re excited to welcome new contributors! Here’s a quick roadmap to get you started:

1. **Read the Manifesto**: Start by reading our [**manifesto**](https://github.com/Daniel-Dfg/PlagiaSight/blob/main/Resources/Manifesto/A%20Manifesto%20for%20PlagiaSight.md). This document outlines the core principles guiding PlagiaSight’s development, codebase structure, and much more. It will give you a comprehensive understanding of the project’s vision.

2. **Submit a Pull Request**: After familiarizing yourself with the manifesto, browse the codebase. If you identify any areas for improvement, [create a Pull Request](https://github.com/Daniel-Dfg/PlagiaSight/pulls) or [open an Issue](https://github.com/Daniel-Dfg/PlagiaSight/issues). Even if your PR isn’t merged, we value every contribution and encourage you to share your ideas.

3. **Explore Additional Documentation**: Proposing new features can be challenging, as predicting their usefulness isn’t always straightforward. Before making a proposal, take a look at our [learning resources](https://github.com/Daniel-Dfg/PlagiaSight/tree/main/Resources/Learning%20Material). This will help ensure your ideas align with the project’s goals.

If you have any questions or concerns about contributing, please [**contact us**](https://github.com/Daniel-Dfg/PlagiaSight/blob/main/README.md#contact-the-people-behind-the-10-version).

---

# 💬 Contact the Team

If you need help or want to reach out to the developers behind PlagiaSight:

**Daniel-Dfg**
- [GitHub](https://github.com/Daniel-Dfg)
- [Email](mailto:danieldefoing@gmail.com)
- Discord: [D:D](https://discord.com/users/720963652286414909)

**LUCKYINS**
- [GitHub](https://github.com/LUCKYINS)
- [Email](mailto:elhusseinabdalrahmanwork@gmail.com)
- Discord: [LUCKYINS](https://discord.com/users/721008804300455978)

**onuriscoding**
- [GitHub](https://github.com/onuriscoding)
- [Email](mailto:onurdogancs@gmail.com)
- Discord: [ginorwhat](https://discord.com/users/332553376707510272)