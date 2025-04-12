# 📘 Coding-Scripting-Tutorial PDF Generator

This is a tool to convert well-structured `.txt` files into color-styled PDF guides — ideal for sharing protocols, coding steps, or structured documentation.

---

## 🚀 Features

- 🎨 Syntax-colored PDF output
- ✍️ Supports instructional and scripting blocks
- 📜 Minimal input format
- 📦 No setup beyond installing `fpdf`

---

## 📥 Usage

1. Format your `.txt` file like this:
    ```
    Title: My Workflow
    [Prepared by You, 12 Apr, 2025]

    Step 1: Setup
    - Install dependencies
    """
    $ pip install fpdf
    $ python script.py
    """
    ```

2. Run the converter script:
    The script auto-checks and installs prerequisite modules. However, if you'd like to do it manuyally,
    ```bash
    python "converter-script.py"
    ```

3. Get a beautiful PDF in the same folder!

---

## 📸 Preview

![Sample](../samples/Sample_output.png)

---

## 🧠 Author

Made with ❤️ by [AdhikariPB](https://github.com/adhikaripb)
