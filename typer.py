import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from pynput import keyboard

class TyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exwhyzed Typer Pro")
        self.root.geometry("860x820")
        self.root.configure(bg="#0D1117")
        self.root.minsize(780, 750)

        # ── Color palette ──────────────────────────────────────────
        self.C_BG       = "#0D1117"
        self.C_PANEL    = "#161B22"
        self.C_CARD     = "#1C2128"
        self.C_BORDER   = "#30363D"
        self.C_ACCENT   = "#00C853"
        self.C_HOVER    = "#00E676"
        self.C_TEXT     = "#E6EDF3"
        self.C_TEXT2    = "#8B949E"
        self.C_WARN     = "#F9A825"
        self.C_DANGER   = "#E53935"
        self.C_RESET    = "#546E7A"

        # ── Font stack ─────────────────────────────────────────────
        self.FONT       = "JetBrains Mono"
        self.FONT_FB    = "Cascadia Code"
        self.FONT_FB2   = "Consolas"
        self.F_TITLE    = (self.FONT, 18, "bold")
        self.F_SUB      = (self.FONT, 9)
        self.F_SECTION  = (self.FONT, 10, "bold")
        self.F_LABEL    = (self.FONT, 9)
        self.F_LABEL_B  = (self.FONT, 9, "bold")
        self.F_ENTRY    = (self.FONT, 9)
        self.F_EDITOR   = (self.FONT, 10)
        self.F_BTN      = (self.FONT, 10, "bold")
        self.F_STATUS   = (self.FONT, 9, "bold")
        self.F_FOOTER   = (self.FONT, 8)

        # Countdown delay (default 3 seconds)
        self.countdown_seconds = 3

        self.is_typing = False
        self.is_paused = False
        self.stop_typing = False
        self.delay = 0.05  # Default delay in seconds
        self.current_position = 0
        self.full_text = ""
        self.pause_event = threading.Event()
        self.pause_event.set()  # Set initially so typing can proceed
        self.stop_event = threading.Event()  # New stop event for better responsiveness

        # Statistics
        self.total_chars = 0
        self.chars_typed = 0
        self.typing_thread = None  # Keep reference to typing thread

        # Style configuration
        self.setup_styles()

        # ═══════════════════════════════════════════════════════════
        # HEADER
        # ═══════════════════════════════════════════════════════════
        header_frame = tk.Frame(root, bg=self.C_PANEL, height=72)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        header_inner = tk.Frame(header_frame, bg=self.C_PANEL)
        header_inner.pack(fill="both", expand=True)

        # Center: title + subtitle
        header_center = tk.Frame(header_inner, bg=self.C_PANEL)
        header_center.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(
            header_center,
            text="EXWHYZED TYPER PRO",
            font=self.F_TITLE,
            fg=self.C_TEXT,
            bg=self.C_PANEL
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_center,
            text="Professional Automated Input Engine",
            font=self.F_SUB,
            fg=self.C_TEXT2,
            bg=self.C_PANEL
        )
        subtitle_label.pack()

        # Status badge (top-right corner)
        self.status_badge = tk.Label(
            header_inner,
            text="●  READY",
            font=self.F_LABEL_B,
            fg=self.C_ACCENT,
            bg=self.C_PANEL
        )
        self.status_badge.place(relx=1.0, rely=0.5, anchor="e", x=-16)

        # Thin accent line under header
        accent_line = tk.Frame(root, bg=self.C_ACCENT, height=1)
        accent_line.pack(fill="x")

        # ═══════════════════════════════════════════════════════════
        # MAIN CONTAINER
        # ═══════════════════════════════════════════════════════════
        main_container = tk.Frame(root, bg=self.C_BG)
        main_container.pack(fill="both", expand=True, padx=16, pady=12)

        # ── SETTINGS CARD ─────────────────────────────────────────
        settings_outer = tk.Frame(main_container, bg=self.C_BORDER)
        settings_outer.pack(fill="x", pady=(0, 10))

        settings_frame = tk.Frame(settings_outer, bg=self.C_CARD)
        settings_frame.pack(fill="x", padx=1, pady=1)

        # Section header
        settings_header = tk.Frame(settings_frame, bg=self.C_CARD)
        settings_header.pack(fill="x", padx=16, pady=(12, 6))

        tk.Label(
            settings_header,
            text="⚙  CONFIGURATION",
            font=self.F_SECTION,
            fg=self.C_ACCENT,
            bg=self.C_CARD
        ).pack(side=tk.LEFT)

        # Countdown row
        countdown_row = tk.Frame(settings_frame, bg=self.C_CARD)
        countdown_row.pack(fill="x", padx=16, pady=4)

        tk.Label(
            countdown_row,
            text="Countdown (sec):",
            font=self.F_LABEL,
            bg=self.C_CARD,
            fg=self.C_TEXT2
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.countdown_var = tk.StringVar(value="3")
        countdown_entry = tk.Entry(
            countdown_row,
            textvariable=self.countdown_var,
            width=6,
            font=self.F_ENTRY,
            bg=self.C_PANEL,
            fg=self.C_TEXT,
            insertbackground=self.C_ACCENT,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.C_BORDER,
            highlightcolor=self.C_ACCENT
        )
        countdown_entry.pack(side=tk.LEFT, padx=(0, 12), ipady=3)

        tk.Label(
            countdown_row,
            text="Time to switch to target window",
            font=(self.FONT, 8),
            bg=self.C_CARD,
            fg=self.C_TEXT2
        ).pack(side=tk.LEFT)

        # Delay row
        delay_row = tk.Frame(settings_frame, bg=self.C_CARD)
        delay_row.pack(fill="x", padx=16, pady=4)

        tk.Label(
            delay_row,
            text="Typing Speed (sec):",
            font=self.F_LABEL,
            bg=self.C_CARD,
            fg=self.C_TEXT2
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.delay_var = tk.StringVar(value="0.05")
        delay_entry = tk.Entry(
            delay_row,
            textvariable=self.delay_var,
            width=6,
            font=self.F_ENTRY,
            bg=self.C_PANEL,
            fg=self.C_TEXT,
            insertbackground=self.C_ACCENT,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.C_BORDER,
            highlightcolor=self.C_ACCENT
        )
        delay_entry.pack(side=tk.LEFT, padx=(0, 12), ipady=3)

        tk.Label(
            delay_row,
            text="Lower = faster  (0.01 – 0.5 recommended)",
            font=(self.FONT, 8),
            bg=self.C_CARD,
            fg=self.C_TEXT2
        ).pack(side=tk.LEFT)

        # Spacer at bottom of settings card
        tk.Frame(settings_frame, bg=self.C_CARD, height=8).pack()

        # ── TEXT INPUT CARD ────────────────────────────────────────
        text_outer = tk.Frame(main_container, bg=self.C_BORDER)
        text_outer.pack(fill="both", expand=True, pady=(0, 10))

        text_card = tk.Frame(text_outer, bg=self.C_CARD)
        text_card.pack(fill="both", expand=True, padx=1, pady=1)

        # Section header with char counter
        text_header = tk.Frame(text_card, bg=self.C_CARD)
        text_header.pack(fill="x", padx=16, pady=(12, 6))

        tk.Label(
            text_header,
            text="▸  INPUT PAYLOAD",
            font=self.F_SECTION,
            fg=self.C_ACCENT,
            bg=self.C_CARD
        ).pack(side=tk.LEFT)

        self.char_count_label = tk.Label(
            text_header,
            text="CHARS: 0",
            font=self.F_LABEL_B,
            bg=self.C_CARD,
            fg=self.C_ACCENT
        )
        self.char_count_label.pack(side=tk.RIGHT)

        # Text area (terminal-style)
        self.text_area_frame = tk.Frame(text_card, bg=self.C_BORDER)
        self.text_area_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self.text_area = scrolledtext.ScrolledText(
            self.text_area_frame,
            wrap=tk.WORD,
            height=12,
            font=self.F_EDITOR,
            bg=self.C_PANEL,
            fg=self.C_TEXT,
            relief=tk.FLAT,
            borderwidth=0,
            padx=12,
            pady=10,
            insertbackground=self.C_ACCENT,
            selectbackground="#264F78",
            selectforeground=self.C_TEXT
        )
        self.text_area.pack(fill="both", expand=True, padx=1, pady=1)

        # Green border on focus
        self.text_area.bind('<FocusIn>', lambda e: self.text_area_frame.config(bg=self.C_ACCENT))
        self.text_area.bind('<FocusOut>', lambda e: self.text_area_frame.config(bg=self.C_BORDER))

        # Bind text change to update character count
        self.text_area.bind('<KeyRelease>', self.update_char_count)
        self.text_area.bind('<Button-1>', self.update_char_count)
        self.text_area.bind('<Control-v>', lambda e: self.root.after(10, self.update_char_count))

        # ── PROGRESS CARD ──────────────────────────────────────────
        progress_outer = tk.Frame(main_container, bg=self.C_BORDER)
        progress_outer.pack(fill="x", pady=(0, 10))

        progress_card = tk.Frame(progress_outer, bg=self.C_CARD)
        progress_card.pack(fill="x", padx=1, pady=1)

        # Section header
        progress_header = tk.Frame(progress_card, bg=self.C_CARD)
        progress_header.pack(fill="x", padx=16, pady=(12, 8))

        tk.Label(
            progress_header,
            text="◈  EXECUTION MONITOR",
            font=self.F_SECTION,
            fg=self.C_ACCENT,
            bg=self.C_CARD
        ).pack(side=tk.LEFT)

        # Stats row
        stats_row = tk.Frame(progress_card, bg=self.C_CARD)
        stats_row.pack(fill="x", padx=16, pady=(0, 4))

        # Progress %
        self.stat_progress = tk.Label(
            stats_row, text="0%",
            font=(self.FONT, 16, "bold"), fg=self.C_ACCENT, bg=self.C_CARD
        )
        self.stat_progress.pack(side=tk.LEFT, padx=(0, 16))

        # Typed / Remaining / State labels
        stat_details = tk.Frame(stats_row, bg=self.C_CARD)
        stat_details.pack(side=tk.LEFT, fill="x", expand=True)

        self.stat_typed = tk.Label(
            stat_details, text="Typed: 0",
            font=self.F_LABEL, fg=self.C_TEXT2, bg=self.C_CARD, anchor="w"
        )
        self.stat_typed.pack(anchor="w")

        self.stat_remaining = tk.Label(
            stat_details, text="Remaining: 0",
            font=self.F_LABEL, fg=self.C_TEXT2, bg=self.C_CARD, anchor="w"
        )
        self.stat_remaining.pack(anchor="w")

        # State indicator on the right
        self.stat_state = tk.Label(
            stats_row, text="IDLE",
            font=self.F_LABEL_B, fg=self.C_TEXT2, bg=self.C_CARD
        )
        self.stat_state.pack(side=tk.RIGHT)

        # Progress bar
        progress_bar_frame = tk.Frame(progress_card, bg=self.C_CARD)
        progress_bar_frame.pack(fill="x", padx=16, pady=(4, 12))

        # Keep old progress_label for compatibility (hidden or minimal)
        self.progress_label = tk.Label(
            progress_bar_frame,
            text="Progress: 0% (0/0 characters)",
            font=self.F_LABEL,
            bg=self.C_CARD,
            fg=self.C_CARD  # hidden – data shown via stat widgets
        )
        self.progress_label.pack(fill="x")
        self.progress_label.pack_forget()  # hide it entirely

        self.progress_bar = ttk.Progressbar(
            progress_bar_frame,
            style="Cyber.Horizontal.TProgressbar",
            mode='determinate',
            length=700
        )
        self.progress_bar.pack(fill="x")

        # ── CONTROL BUTTONS ────────────────────────────────────────
        button_frame = tk.Frame(main_container, bg=self.C_BG)
        button_frame.pack(pady=6)

        btn_specs = [
            ("start",   "▶  START ATTACK",      self.C_ACCENT,  self.C_BG,   "#33ffaa", self.start_typing),
            ("pause",   "⏸  PAUSE (F9)",        self.C_WARN,    self.C_BG,   "#ffe44d", self.toggle_pause),
            ("stop",    "⏹  TERMINATE (ESC)",   self.C_DANGER,  "#FFFFFF",   "#ff7a7a", self.stop_typing_func),
            ("restart", "🔄  REBOOT",            self.C_RESET,   "#FFFFFF",   "#78909C", self.restart_typing),
        ]

        self._buttons = {}
        for key, text, bg_color, fg_color, active_bg, cmd in btn_specs:
            btn = tk.Button(
                button_frame,
                text=text,
                command=cmd,
                bg=bg_color,
                fg=fg_color,
                font=self.F_BTN,
                width=18,
                height=2,
                relief=tk.FLAT,
                cursor="hand2",
                activebackground=active_bg,
                activeforeground=fg_color,
                borderwidth=0,
            )
            btn.pack(side=tk.LEFT, padx=5)
            self._buttons[key] = btn

        self.start_button   = self._buttons["start"]
        self.pause_button   = self._buttons["pause"]
        self.stop_button    = self._buttons["stop"]
        self.restart_button = self._buttons["restart"]

        # Initial disabled states
        self._disable_button(self.pause_button)
        self._disable_button(self.stop_button)
        self._disable_button(self.restart_button)

        # ── STATUS SECTION ─────────────────────────────────────────
        status_frame = tk.Frame(main_container, bg=self.C_PANEL)
        status_frame.pack(fill="x", pady=(6, 0))

        self.status_label = tk.Label(
            status_frame,
            text="●  Ready — Paste your text and press Start",
            fg=self.C_ACCENT,
            bg=self.C_PANEL,
            font=self.F_STATUS,
            pady=10
        )
        self.status_label.pack()

        hotkeys_label = tk.Label(
            status_frame,
            text="HOTKEYS    ESC → Stop    F9 → Pause / Resume    ↻ Reset available after start",
            fg=self.C_TEXT2,
            bg=self.C_PANEL,
            font=(self.FONT, 8)
        )
        hotkeys_label.pack(pady=(0, 8))

        # ── FOOTER STATUS BAR ──────────────────────────────────────
        footer_line = tk.Frame(root, bg=self.C_BORDER, height=1)
        footer_line.pack(fill="x", side=tk.BOTTOM)

        footer = tk.Frame(root, bg=self.C_PANEL, height=28)
        footer.pack(fill="x", side=tk.BOTTOM)
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="Exwhyzed Typer Pro v1.0  ·  Built with Python  ·  © 2026",
            font=(self.FONT, 8),
            fg=self.C_TEXT2,
            bg=self.C_PANEL
        ).pack(expand=True, pady=4)

        # ── KEYBOARD LISTENER ─────────────────────────────────────
        # ESC key listener
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

        # Initialize character count
        self.update_char_count()

    # ───────────────────────────────────────────────────────────────
    # HELPERS — button enable / disable
    # ───────────────────────────────────────────────────────────────
    def _enable_button(self, btn, bg_color, fg_color, active_bg):
        """Enable a button with its themed colors."""
        btn.config(state=tk.NORMAL, bg=bg_color, fg=fg_color, activebackground=active_bg)

    def _disable_button(self, btn):
        """Disable a button with muted dark colors."""
        btn.config(state=tk.DISABLED, bg=self.C_BORDER, fg=self.C_TEXT2)

    def setup_styles(self):
        """Setup custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Cyber.Horizontal.TProgressbar",
            background=self.C_ACCENT,
            troughcolor=self.C_PANEL,
            borderwidth=0,
            lightcolor=self.C_ACCENT,
            darkcolor=self.C_ACCENT
        )
        # Keep original style name for backward compat (unused but harmless)
        style.configure(
            "Custom.Horizontal.TProgressbar",
            background=self.C_ACCENT,
            troughcolor=self.C_PANEL,
            borderwidth=0,
            lightcolor=self.C_ACCENT,
            darkcolor=self.C_ACCENT
        )

    def _should_stop(self):
        """Quick check if typing should stop"""
        return self.stop_typing or self.stop_event.is_set()

    def _interruptible_sleep(self, seconds):
        """Sleep that can be interrupted by stop event"""
        self.stop_event.wait(timeout=seconds)

    def type_character(self, keyboard_controller, char):
        """Type a single character, handling uppercase and special characters properly"""
        try:
            # Handle newline
            if char == '\n':
                if self._should_stop():
                    return
                keyboard_controller.press(keyboard.Key.enter)
                keyboard_controller.release(keyboard.Key.enter)
                self._interruptible_sleep(0.05)  # Wait for editor to finish auto-indenting
                if self._should_stop():
                    return
                # Clear any auto-indentation added by the target editor
                # Press Home TWICE to handle "smart Home" in editors like VS Code
                # (1st press -> first non-whitespace, 2nd press -> column 0)
                keyboard_controller.press(keyboard.Key.home)
                keyboard_controller.release(keyboard.Key.home)
                self._interruptible_sleep(0.01)
                if self._should_stop():
                    return
                keyboard_controller.press(keyboard.Key.home)
                keyboard_controller.release(keyboard.Key.home)
                self._interruptible_sleep(0.01)
                if self._should_stop():
                    return
                # Select all auto-indented content (Shift+End)
                keyboard_controller.press(keyboard.Key.shift)
                keyboard_controller.press(keyboard.Key.end)
                keyboard_controller.release(keyboard.Key.end)
                keyboard_controller.release(keyboard.Key.shift)
                self._interruptible_sleep(0.01)
                if self._should_stop():
                    return
                # Delete the selected auto-indent
                keyboard_controller.press(keyboard.Key.delete)
                keyboard_controller.release(keyboard.Key.delete)
                return

            # Handle tab
            if char == '\t':
                keyboard_controller.press(keyboard.Key.tab)
                keyboard_controller.release(keyboard.Key.tab)
                return

            if self._should_stop():
                return

            # Handle backtick explicitly for JavaScript template literals
            if char == '`':
                # Backtick is on the same key as tilde, no shift needed
                keyboard_controller.type('`')
                return

            # Mapping for special characters that require Shift (character -> base key)
            shift_chars_map = {
                '!': '1', '@': '2', '#': '3', '$': '4', '%': '5',
                '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
                '_': '-', '+': '=', '{': '[', '}': ']', '|': '\\',
                ':': ';', '"': "'", '<': ',', '>': '.', '?': '/',
                '~': '`'  # Tilde requires Shift+backtick
            }

            # Check if it's an uppercase letter (A-Z)
            if char.isupper() and char.isalpha():
                # Press Shift, type lowercase letter, release Shift
                keyboard_controller.press(keyboard.Key.shift)
                self._interruptible_sleep(0.01)
                keyboard_controller.type(char.lower())
                self._interruptible_sleep(0.01)
                keyboard_controller.release(keyboard.Key.shift)

            # Check if it's a special character that needs Shift
            elif char in shift_chars_map:
                # Press Shift, type the base key, release Shift
                base_char = shift_chars_map[char]
                keyboard_controller.press(keyboard.Key.shift)
                self._interruptible_sleep(0.01)
                keyboard_controller.type(base_char)
                self._interruptible_sleep(0.01)
                keyboard_controller.release(keyboard.Key.shift)

            # For other characters (lowercase letters, numbers, spaces, etc.), type normally
            else:
                keyboard_controller.type(char)

            # After typing auto-closeable brackets, remove editor's auto-inserted closing pair
            # Editors like VS Code auto-insert } after {, ) after (, ] after [
            # Press Delete to remove the auto-inserted character (no-op if editor didn't auto-close)
            if char in ('{', '(', '['):
                self._interruptible_sleep(0.02)
                if not self._should_stop():
                    keyboard_controller.press(keyboard.Key.delete)
                    keyboard_controller.release(keyboard.Key.delete)

        except Exception as e:
            # Fallback: try direct typing if the above fails
            try:
                keyboard_controller.type(char)
            except Exception as fallback_error:
                print(f"Error typing character '{char}' (ord: {ord(char)}): {e}, fallback: {fallback_error}")

    def on_key_press(self, key):
        """Handle hotkeys: ESC to stop, F9 to pause/resume"""
        try:
            if key == keyboard.Key.esc and self.is_typing:
                self.root.after(0, self.stop_typing_func)
            elif key == keyboard.Key.f9 and self.is_typing:
                self.root.after(0, self.toggle_pause)
        except:
            pass

    def update_char_count(self, event=None):
        """Update character count display"""
        text = self.text_area.get("1.0", tk.END)
        char_count = len(text.rstrip('\n'))
        self.char_count_label.config(text=f"CHARS: {char_count:,}")

    def toggle_pause(self):
        """Toggle pause/resume - more reliable with threading"""
        if not self.is_typing:
            return

        # Use threading lock to ensure atomic state change
        if self.is_paused:
            # Resume - will trigger countdown in typing loop
            self.is_paused = False
            self.pause_event.set()  # Release the pause event (triggers countdown in typing loop)
            self.root.after(0, lambda: self._enable_button(
                self.pause_button, self.C_WARN, self.C_BG, "#ffe44d"
            ))
            self.root.after(0, lambda: self.pause_button.config(text="⏸  PAUSE (F9)"))
            # Status will be updated by the countdown in typing loop
        else:
            # Pause
            self.is_paused = True
            self.pause_event.clear()  # Block the pause event
            self.root.after(0, lambda: self._enable_button(
                self.pause_button, self.C_ACCENT, self.C_BG, "#33ffaa"
            ))
            self.root.after(0, lambda: self.pause_button.config(text="▶  RESUME (F9)"))
            self.root.after(0, lambda: self.status_label.config(
                text="⏸  PAUSED — Press F9 to resume, ESC to terminate",
                fg=self.C_WARN,
                bg=self.C_PANEL
            ))
            self.root.after(0, lambda: self.status_label.master.config(bg=self.C_PANEL))
            self.root.after(0, lambda: self.status_badge.config(text="●  PAUSED", fg=self.C_WARN))
            self.root.after(0, lambda: self.stat_state.config(text="PAUSED", fg=self.C_WARN))

    def start_typing(self):
        text = self.text_area.get("1.0", tk.END).replace('\r\n', '\n').replace('\r', '\n').strip('\n').rstrip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to type!")
            return

        try:
            self.delay = float(self.delay_var.get())
            if self.delay < 0:
                raise ValueError("Delay must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid delay value!")
            return

        try:
            self.countdown_seconds = int(self.countdown_var.get())
            if self.countdown_seconds < 0:
                raise ValueError("Countdown must be non-negative")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid countdown value (0 or positive number)!")
            return

        # Stop any existing typing thread first
        if self.typing_thread and self.typing_thread.is_alive():
            self.stop_typing = True
            self.stop_event.set()
            self.pause_event.set()  # Release pause if stuck

        # Reset state
        self.is_typing = True
        self.is_paused = False
        self.stop_typing = False
        self.current_position = 0
        self.full_text = text
        self.total_chars = len(text)
        self.chars_typed = 0
        self.pause_event.set()  # Allow typing to proceed
        self.stop_event.clear()  # Clear stop event

        # Update UI
        self._disable_button(self.start_button)
        self._enable_button(self.pause_button, self.C_WARN, self.C_BG, "#ffe44d")
        self.pause_button.config(text="⏸  PAUSE (F9)")
        self._enable_button(self.stop_button, self.C_DANGER, "#FFFFFF", "#ff7a7a")
        self._enable_button(self.restart_button, self.C_RESET, "#FFFFFF", "#78909C")
        self.status_label.config(
            text=f"⏳  Starting in {self.countdown_seconds}s — Switch to target window!",
            fg=self.C_WARN,
            bg=self.C_PANEL
        )
        status_frame = self.status_label.master
        status_frame.config(bg=self.C_PANEL)
        self.status_badge.config(text="●  COUNTDOWN", fg=self.C_WARN)
        self.stat_state.config(text="COUNTDOWN", fg=self.C_WARN)
        self.progress_bar['maximum'] = self.total_chars
        self.progress_bar['value'] = 0
        self.progress_label.config(text=f"Progress: 0% (0/{self.total_chars:,} characters)")
        self._update_stats(0, 0, self.total_chars)
        self.root.update()

        # Start typing in a separate thread
        self.typing_thread = threading.Thread(target=self.type_text, args=(text,), daemon=True)
        self.typing_thread.start()

    def _update_stats(self, pct, typed, total):
        """Update the progress monitoring widgets."""
        self.stat_progress.config(text=f"{pct:.0f}%")
        self.stat_typed.config(text=f"Typed: {typed:,}")
        remaining = max(0, total - typed)
        self.stat_remaining.config(text=f"Remaining: {remaining:,}")

    def type_text(self, text):
        """Simulate typing the text"""
        # Custom countdown before typing starts - with frequent checks for stop/pause
        countdown = self.countdown_seconds
        for i in range(countdown, 0, -1):
            # Check every 0.1 seconds during countdown for responsiveness
            for _ in range(10):  # 10 checks per second
                if self.stop_typing or self.stop_event.is_set():
                    return
                # Allow pause during countdown
                if self.is_paused:
                    self.pause_event.wait(timeout=0.1)
                else:
                    time.sleep(0.1)

            # Update countdown display
            if not self.stop_typing and not self.stop_event.is_set():
                self.root.after(0, lambda i=i: self.status_label.config(
                    text=f"⏳  Starting in {i} second{'s' if i != 1 else ''}… Switch to target window!",
                    fg=self.C_WARN,
                    bg=self.C_PANEL
                ))
                self.root.after(0, lambda: self.status_label.master.config(bg=self.C_PANEL))

        if self.stop_typing or self.stop_event.is_set():
            return

        self.root.after(0, lambda: self.status_label.config(
            text="▶  Typing… Press ESC to stop, F9 to pause",
            fg=self.C_ACCENT,
            bg=self.C_PANEL
        ))
        status_frame = self.status_label.master
        status_frame.config(bg=self.C_PANEL)
        self.root.after(0, lambda: self.status_badge.config(text="●  TYPING", fg=self.C_ACCENT))
        self.root.after(0, lambda: self.stat_state.config(text="TYPING", fg=self.C_ACCENT))

        # Create keyboard controller
        keyboard_controller = keyboard.Controller()

        # Type each character starting from current position
        was_paused_in_loop = False
        for idx in range(self.current_position, len(text)):
            # Check if we should stop - check multiple times for responsiveness
            if self.stop_typing or self.stop_event.is_set():
                break

            # Check if we're currently paused
            if self.is_paused:
                was_paused_in_loop = True
                # Wait if paused - use event wait for better responsiveness
                while self.is_paused and not (self.stop_typing or self.stop_event.is_set()):
                    # Wait with timeout so we can check stop condition frequently
                    if not self.pause_event.wait(timeout=0.1):
                        # Still paused, check stop condition again
                        if self.stop_typing or self.stop_event.is_set():
                            break
                        continue
                    else:
                        # Pause was released (resumed) - break to do countdown
                        break

            # Final stop check before countdown/typing character
            if self.stop_typing or self.stop_event.is_set():
                break

            # If we just resumed from pause, do a countdown before continuing
            if was_paused_in_loop and not self.is_paused:
                resume_countdown = self.countdown_seconds
                for i in range(resume_countdown, 0, -1):
                    # Check every 0.1 seconds during resume countdown
                    for _ in range(10):  # 10 checks per second
                        if self.stop_typing or self.stop_event.is_set():
                            return
                        # Allow pause during resume countdown
                        if self.is_paused:
                            self.pause_event.wait(timeout=0.1)
                        else:
                            time.sleep(0.1)

                    # Update resume countdown display
                    if not (self.stop_typing or self.stop_event.is_set()):
                        self.root.after(0, lambda i=i: self.status_label.config(
                            text=f"⏳  Resuming in {i} second{'s' if i != 1 else ''}… Switch to target window!",
                            fg=self.C_WARN,
                            bg=self.C_PANEL
                        ))
                        self.root.after(0, lambda: self.status_label.master.config(bg=self.C_PANEL))

                # Final check after resume countdown
                if self.stop_typing or self.stop_event.is_set():
                    break

                # Update status to show typing resumed
                self.root.after(0, lambda: self.status_label.config(
                    text="▶  Typing… Press ESC to stop, F9 to pause",
                    fg=self.C_ACCENT,
                    bg=self.C_PANEL
                ))
                self.root.after(0, lambda: self.status_label.master.config(bg=self.C_PANEL))
                self.root.after(0, lambda: self.status_badge.config(text="●  TYPING", fg=self.C_ACCENT))
                self.root.after(0, lambda: self.stat_state.config(text="TYPING", fg=self.C_ACCENT))

                # Check again if paused during countdown
                if self.is_paused:
                    # Keep flag set so we'll do countdown again when resumed
                    # Use continue to re-check pause state (will go back through pause check)
                    continue

                # Reset the flag after successful resume countdown (ready to type)
                was_paused_in_loop = False

            char = text[idx]
            self.current_position = idx + 1
            self.chars_typed += 1

            # Type the character using our improved method
            self.type_character(keyboard_controller, char)

            # Update progress
            progress = (self.chars_typed / self.total_chars) * 100
            self.root.after(0, lambda p=progress, c=self.chars_typed, t=self.total_chars: self.update_progress(p, c, t))

            # Use interruptible sleep so stop works immediately
            if self._should_stop():
                break
            self._interruptible_sleep(self.delay)

        # Reset UI
        self.root.after(0, self.typing_complete)

    def update_progress(self, percentage, chars_typed, total_chars):
        """Update progress bar and label"""
        self.progress_bar['value'] = chars_typed
        self.progress_label.config(
            text=f"Progress: {percentage:.1f}% ({chars_typed:,}/{total_chars:,} characters)"
        )
        self._update_stats(percentage, chars_typed, total_chars)

    def stop_typing_func(self):
        """Stop typing immediately - more reliable"""
        self.stop_typing = True
        self.stop_event.set()  # Set stop event for immediate response
        self.is_paused = False
        self.pause_event.set()  # Release pause lock so thread can exit immediately
        self.root.after(0, self.typing_complete)

    def restart_typing(self):
        """Restart typing from the beginning"""
        # First stop current typing if active
        if self.is_typing:
            self.stop_typing = True
            self.stop_event.set()
            self.is_paused = False
            self.pause_event.set()
            # Wait a moment for thread to stop
            time.sleep(0.2)

        # Reset all state
        self.is_typing = False
        self.is_paused = False
        self.stop_typing = False
        self.current_position = 0
        self.chars_typed = 0
        self.stop_event.clear()
        self.pause_event.set()

        # Start typing again
        self.start_typing()

    def typing_complete(self):
        self.is_typing = False  # Set this first to prevent button actions
        self._enable_button(self.start_button, self.C_ACCENT, self.C_BG, "#33ffaa")
        self.start_button.config(text="▶  START ATTACK")
        self._disable_button(self.pause_button)
        self.pause_button.config(text="⏸  PAUSE (F9)")
        self._disable_button(self.stop_button)

        # Enable restart button if we have text and have started typing at least once
        if self.full_text and (self.chars_typed > 0 or self.current_position > 0):
            self._enable_button(self.restart_button, self.C_RESET, "#FFFFFF", "#78909C")
        elif self.full_text:
            # Text exists but haven't started - allow restart
            self._enable_button(self.restart_button, self.C_RESET, "#FFFFFF", "#78909C")
        else:
            self._disable_button(self.restart_button)

        status_frame = self.status_label.master

        if self.chars_typed >= self.total_chars:
            self.status_label.config(
                text="✅  OPERATION COMPLETE — All characters deployed successfully",
                fg=self.C_ACCENT,
                bg=self.C_PANEL
            )
            status_frame.config(bg=self.C_PANEL)
            self.status_badge.config(text="●  COMPLETE", fg=self.C_ACCENT)
            self.stat_state.config(text="COMPLETE", fg=self.C_ACCENT)
            self.progress_bar['value'] = self.total_chars
            self.progress_label.config(
                text=f"Progress: 100% ({self.total_chars:,}/{self.total_chars:,} characters)"
            )
            self._update_stats(100, self.total_chars, self.total_chars)
        else:
            self.status_label.config(
                text=f"⏹  TERMINATED — Typed {self.chars_typed:,} / {self.total_chars:,} characters",
                fg=self.C_DANGER,
                bg=self.C_PANEL
            )
            status_frame.config(bg=self.C_PANEL)
            self.status_badge.config(text="●  STOPPED", fg=self.C_DANGER)
            self.stat_state.config(text="STOPPED", fg=self.C_DANGER)
            if self.total_chars > 0:
                pct = (self.chars_typed / self.total_chars) * 100
                self._update_stats(pct, self.chars_typed, self.total_chars)

        # Don't reset chars_typed here - keep it for display and restart functionality
        # Only reset these flags
        self.is_paused = False
        self.stop_typing = False
        self.stop_event.clear()  # Clear stop event for next run

if __name__ == "__main__":
    root = tk.Tk()
    app = TyperApp(root)
    root.mainloop()
