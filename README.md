# PyDOS

# PROJECT IS STILL WORK-IN-PROGRESS, NOT ALL FEATURES WORK

**PyDOS** is a simple, educational DOS-like shell written in Python. It is designed for learning how operating systems, command-line interfaces, and file systems work.

> ⚠️ This project is **not intended for production use**. It exists purely as a learning project.

---

## Features

- Basic command-line interface (CLI) similar to DOS  
- File and folder operations: `cd, dir, mkdir, rmdir` (Not finished)
- Simple command parsing and execution  
- Error handling to simulate real OS behavior  
- Modular structure for easier understanding and expansion
- Users  

---

## Learning Goals

PyDOS is built to help you:

- Understand how command parsing works in a shell  
- Learn how file systems can be simulated in Python  
- Practice working with loops, conditionals, and functions  
- Improve code organization using modules  
- Think like an operating system developer  

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/pydos.git
cd pydos
```

### 2. Run the program

```bash
python main.py
```

### 3. Start using PyDOS
Log in:

```
admin
root
```
Try commands like:

```
echo hello
ver
createuser new_user new_password normal/admin
shutdown
```

---

## Project Structure

```
pydos/
│
├── main.py          # The whole program
├── LICENSE
└── README.md        # Project documentation
```

---

## Recommended Learning Steps

1. Open `filesystem.py` and understand how folders and files are stored.
2. Read `shell.py` to see how user input gets parsed.
3. Add a new command (for example: `help` or `echo`).
4. Break things intentionally and see how error handling works.
5. Refactor parts of the code to improve clarity.

---

## Why This Project Exists

PyDOS exists to make learning fun.

Instead of just writing small isolated exercises, this project gives you a **real structure** to work with. You can gradually expand it and watch it grow into something more advanced.

---

## License

This project is licensed under the **MIT License**.

You are free to:
- Use it
- Modify it
- Share it
- Build on top of it

Just keep the original license notice included.

---

## Final Note

If you improve PyDOS, add new features, or refactor the architecture — that means it’s working exactly as intended.

This is a playground for learning.
