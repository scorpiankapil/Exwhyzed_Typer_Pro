# Auto Typer

A Windows application that simulates keyboard typing to help you paste text into applications that don't allow copy/paste (like when using Chrome Remote Desktop).

## Features

- **Modern, Beautiful UI**: Professional-looking interface with intuitive design
- **Configurable Countdown**: Set your own countdown time (0-60+ seconds) before typing starts
- **Configurable typing speed**: Adjust the delay between characters
- **Pause/Resume**: Pause typing anytime and resume when ready (F9 hotkey or button)
- **Stop anytime**: Press ESC key to stop typing at any time
- **Progress tracking**: Real-time progress bar showing typing progress and character count
- **Character counter**: See how many characters are in your text (with thousands separator)
- **Multi-line support**: Handles code, paragraphs, and formatted text
- **Visual status indicators**: Color-coded status messages for different states
- **Hotkeys**: 
  - **ESC** = Stop typing
  - **F9** = Pause/Resume typing

## Installation

1. Make sure you have Python 3.7 or higher installed
2. Install the required dependency:
   ```
   pip install -r requirements.txt
   ```
   Or directly:
   ```
   pip install pynput
   ```

## Usage

1. Run the application:
   ```
   python typer.py
   ```

2. **Paste your text** into the text area (or type it manually)
   - Character count is displayed automatically with formatting

3. **Configure settings**:
   - **Countdown**: Set how many seconds to wait before typing starts (default: 3 seconds)
     - Use 0 if you're already on the target window
     - Use more seconds if you need more time to switch windows
   - **Typing Speed**: Adjust the delay between characters
     - Lower values = faster typing (0.01 is very fast)
     - Higher values = slower typing (0.5 is slow)
     - Default: 0.05 seconds (comfortable speed)

4. **Click "Start Typing"**

5. **Switch to your target window** during the countdown

6. The program will start typing automatically with a progress bar showing your progress

7. **Control typing**:
   - **Press F9** or click "Pause" button to pause/resume typing
   - **Press ESC** or click "Stop" button to stop typing completely
   - Watch the progress bar to see how much has been typed

## Tips

- **Countdown timing**: 
  - Set countdown to 0 if you're already on the target window and ready
  - Use 5-10 seconds if you need to navigate through multiple windows
  - The countdown shows exactly how many seconds remain
- **Typing speed**:
  - For code with many lines, use a delay of 0.01-0.03 seconds for faster input
  - For forms or sensitive inputs, use 0.1-0.2 seconds to be safer
- **Best practices**:
  - Make sure the target window is active and the cursor is in the text field before typing starts
  - The program types exactly what you paste, including line breaks and special characters
  - Use **Pause (F9)** if you need to do something in the target application, then resume when ready
  - The progress bar shows exactly how much text has been typed, so you know if you need to resume after a pause
- **UI features**:
  - Status messages change color to indicate current state (green=ready, blue=typing, orange=paused/countdown, red=stopped)
  - Character counts use thousands separators for easy reading (e.g., "1,234 characters")

## Requirements

- Python 3.7+
- Windows OS (tested on Windows 10)
- pynput library

## Troubleshooting

- **Nothing happens when I click Start**: Make sure you've switched to the target window during the countdown (increase countdown time if needed)
- **Typing is too fast/slow**: Adjust the delay value in the settings
- **Can't stop typing**: Press the ESC key (it works globally) or click the Stop button
- **Want to pause temporarily**: Press F9 key or click the Pause button - then resume with F9 again
- **Installation errors**: Make sure you have admin privileges or try installing with `pip install --user pynput`
- **Hotkeys not working**: Make sure the application window is running and typing is active (hotkeys work globally, but only when typing)

## License

Free to use for personal and commercial purposes.

"# Exwhyzed_Typer_Pro" 
