#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk

############################################################
#################  THEME / TYPESET  ########################
############################################################


# Constants for the theme and layout
WINDOW_TITLE = "My cross-platform CV"
WRAPLENGTH = 750
PADDING_X = 20
PADDING_Y = 5
TIMELINE_WIDTH = 5
TIMELINE_PADX = 50
WINDOW_GEOMETRY = "1600x1000"
SCROLLBAR_WIDTH = 25

# Theme colors (dark by default)
BG_COLOR = "#2E2E2E"            # Dark grey
TEXT_COLOR = "#00FF00"          # Green
BUTTON_BG_COLOR = "#3E3E3E"     # Slightly lighter dark grey
BUTTON_FG_COLOR = TEXT_COLOR
TIMELINE_COLOR = "#FFFFFF"      # White for timeline elements

TITLE_SIZE = 16
REG_SIZE = 12
FONT_TYPE = 'Helvetica'
FONT_STYLIZING = 'bold'
FONT_TITLE = (FONT_TYPE, TITLE_SIZE, FONT_STYLIZING)
FONT_PARAGRAPH = (FONT_TYPE, REG_SIZE, FONT_STYLIZING)


############################################################
#################  GUI ELEMENTS  ###########################
############################################################

class CollapsibleTimelineEvent(tk.Frame):
    def __init__(self, master, time, description, timeline):
        super().__init__(master, bg=BG_COLOR)
        self.is_collapsed = True
        self.timeline = timeline
        self.create_widgets(time, description)

    def create_widgets(self, time, description):
        self.time_button = self.create_button(self, time, self.toggle_content)
        self.content_frame = self.create_frame(self, description)

    def create_button(self, master, text, command):
        button = tk.Button(master, text=text, command=command, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, anchor="w")
        button.pack(pady=PADDING_Y, anchor='w')
        return button

    def create_frame(self, master, text):
        frame = tk.Frame(master, bg=BG_COLOR)
        label = tk.Label(frame, text=text, justify=tk.LEFT, wraplength=self.winfo_width(), bg=BG_COLOR, fg=TEXT_COLOR)
        label.pack(anchor='w', padx=PADDING_X)
        frame.pack(fill=tk.X)
        frame.pack_forget()
        return frame

    def toggle_content(self):
        if self.is_collapsed:
            self.content_frame.pack(fill=tk.X)
        else:
            self.content_frame.pack_forget()
        self.is_collapsed = not self.is_collapsed
        self.timeline.update_canvas_height()

    def update_wraplength(self, width):
        for label in self.content_frame.winfo_children():
            label.config(wraplength=width - 2 * PADDING_X)

class Timeline(tk.Frame):
    def __init__(self, master, title, events):
        super().__init__(master, bg=BG_COLOR)
        self.events = events
        self.create_widgets(title)

    def create_widgets(self, title):
        self.create_label(self, title, FONT_TITLE, "w").pack(fill=tk.X, pady=PADDING_Y)
        self.canvas = tk.Canvas(self, width=TIMELINE_WIDTH, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=TIMELINE_PADX, pady=PADDING_Y, fill=tk.Y)

        self.event_frames = [self.create_event_frame(event) for event in self.events]
        self.update_canvas_height()

    def create_label(self, master, text, font, anchor):
        return tk.Label(master, text=text, bg=BG_COLOR, fg=TEXT_COLOR, font=font, anchor=anchor)

    def create_event_frame(self, event):
        frame = CollapsibleTimelineEvent(self, event['time'], event['description'], self)
        frame.pack(fill=tk.X, pady=PADDING_Y, anchor="w")
        return frame

    def update_canvas_height(self):
        total_height = sum(frame.time_button.winfo_reqheight() + (0 if frame.is_collapsed else frame.content_frame.winfo_reqheight()) for frame in self.event_frames)
        total_height += PADDING_Y * len(self.event_frames)
        self.canvas.config(height=total_height)
        self.canvas.delete("all")
        self.canvas.create_line(TIMELINE_WIDTH // 2, 0, TIMELINE_WIDTH // 2, total_height, fill=TIMELINE_COLOR, width=TIMELINE_WIDTH)

    def update_wraplength(self, width):
        for frame in self.event_frames:
            frame.update_wraplength(width)

class TitleWithParagraph(tk.Frame):
    def __init__(self, master, title, paragraph, center=False):
        super().__init__(master, bg=BG_COLOR)
        self.center = center
        self.is_collapsed = not center
        self.create_widgets(title, paragraph)

    def create_widgets(self, title, paragraph):
        title_anchor = "center" if self.center else "w"
        title_label = self.create_label(self, title, FONT_TITLE, title_anchor)
        
        if self.center:
            title_label.pack(fill=tk.X, pady=PADDING_Y)
            self.paragraph_label = self.create_label(self, paragraph, FONT_PARAGRAPH, 'center')
            self.paragraph_label.pack(fill=tk.X, pady=PADDING_Y)
        else:
            self.title_button = tk.Button(self, text=title, command=self.toggle_content, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_TITLE, anchor=title_anchor)
            self.title_button.pack(fill=tk.X, pady=PADDING_Y)
            self.content_frame = tk.Frame(self, bg=BG_COLOR)
            self.paragraph_label = self.create_label(self.content_frame, paragraph, FONT_PARAGRAPH, 'w', justify=tk.LEFT)
            self.paragraph_label.pack(fill=tk.X, pady=PADDING_Y)
            self.content_frame.pack(fill=tk.X)
            self.content_frame.pack_forget()

    def create_label(self, master, text, font, anchor, justify=tk.CENTER):
        return tk.Label(master, text=text, bg=BG_COLOR, fg=TEXT_COLOR, font=font, anchor=anchor, justify=justify)

    def toggle_content(self):
        if self.is_collapsed:
            self.content_frame.pack(fill=tk.X)
        else:
            self.content_frame.pack_forget()
        self.is_collapsed = not self.is_collapsed

    def update_wraplength(self, width):
        self.paragraph_label.config(wraplength=width - PADDING_X)

class Footnote(tk.Frame):
    def __init__(self, master, text):
        super().__init__(master, bg=BG_COLOR)
        self.create_widgets(text)

    def create_widgets(self, text):
        self.create_label(self, text, FONT_PARAGRAPH, "w").pack(fill=tk.X, pady=PADDING_Y)

    def create_label(self, master, text, font, anchor):
        return tk.Label(master, text=text, bg=BG_COLOR, fg=TEXT_COLOR, wraplength=self.winfo_width(), anchor=anchor, justify="left")

    def update_wraplength(self, width):
        for child in self.winfo_children():
            child.config(wraplength=width - 2 * PADDING_X)



############################################################
#################  PERSONAL CONTENT  #######################
############################################################


APPLICANT = "Count Dracula"
APPLICANT_CONTACT = """\
Address: Bran Castle, Carpathian Mountains, Transylvania
Phone: +40-666-DRACULA (372-2852)
dracu1431@darkmail.com
"""

OBJECTIVE = """\
To sink my teeth into challenging roles that allow me to utilize my centuries of experience in nocturnal management and stakeholder relations. Have strong preference for night-shifts."""
EDUCATION = """\
• (1698) Doctor of Darkness, at Transylvania University of Eternal Night
• (1453) Bachelor of Eternal Night, at Transylvanian School of Dark Arts
• (1449) Completed Mehmed II's Ottoman educative course for royals
"""
SKILLS = """\
• Bat transformation (Advanced)
• Hypnotic gaze (Expert)
• Coffin optimization (Master)
• Fluent in Gothic and Old Slavonic
"""
HOBBIES_AND_INTERESTS = """\
• Blood Donation Drives: Passionate about ensuring a steady supply for the vampiric community.
• Interior Crypt Decoration: Enthusiast of gothic architecture and interior design.
• Night Flights: Enjoys evening excursions and moonlit adventures.
"""

# Widget structure - needs to be created late to avoid GUI issues.
WIDGET_STRUCTURE = [
    (TitleWithParagraph, APPLICANT, APPLICANT_CONTACT, True),
    (TitleWithParagraph, 'Objective', OBJECTIVE),
    (TitleWithParagraph, 'Education', EDUCATION),
    (Timeline, 'Professional Experience', [
        {"time": "(1987-1992) Literacy consultant", "description": """\
• Commissioned a far-eastern entertainment illustrated-medium based on my autobiography
    • Popularity of my life-story's retelling had brought forth its remake in a worldwide-successful drawn-film series, and interactive animatronic-entertainment adaptations"""},
        {"time": "(1897) Diplomat", "description": """\
• Emissary to London, Britain"""},
        {"time": "(1750 - Present) Nightlife Consultant", "description": """\
• Provided strategic guidance to clubs, bars, and nocturnal establishments on ambiance, customer engagement, and beverage selection.
• Implemented innovative strategies for increasing attendance during full moons and other supernatural events."""},
        {"time": "(1470 - present) Vampire Lord", "description": """\
• Managed a diverse team of undead minions with a focus on efficiency and synergy in terrorizing local populations.
• Successfully maintained an extensive network of spooky castles and crypts."""},
    ]),
    (TitleWithParagraph, 'Skills', SKILLS),
    (TitleWithParagraph, 'Hobbies and Interests', HOBBIES_AND_INTERESTS),
]

FOOTNOTE_TEXT = "This is a parody CV, please don't seek evil lords on Github. If you want to contact me: sirhexal@gmail.com (I seldom check on emails there)"


############################################################
#################  RUNNING  ################################
############################################################

class DocumentEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)
        self.configure(bg=BG_COLOR)
        self.create_widgets()
        self.update_window_size()

    def create_widgets(self):
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Create a frame for the scrollable content
        self.scrollable_content_frame = tk.Frame(self.container, bg=BG_COLOR)
        self.scrollable_content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        self.canvas = tk.Canvas(self.scrollable_content_frame, bg=BG_COLOR)
        
        # Create a custom style for the scrollbar
        style = ttk.Style()
        style.configure("Vertical.TScrollbar",
                        width=SCROLLBAR_WIDTH,
                        background=TEXT_COLOR, 
                        troughcolor=BG_COLOR, 
                        arrowcolor=TEXT_COLOR, 
                        gripcount=0, 
                        relief=tk.FLAT)
        style.map("Vertical.TScrollbar", background=[('active', BG_COLOR), ('disabled', BG_COLOR)])
        
        self.scrollbar = ttk.Scrollbar(self.scrollable_content_frame, orient="vertical", command=self.canvas.yview, style="Vertical.TScrollbar")
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)
    
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
    
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
        self.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows
        self.bind_all("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.bind_all("<Button-5>", self._on_mousewheel)    # Linux scroll down
    
        self.widget_frames = [self.create_widget(widget_info) for widget_info in WIDGET_STRUCTURE]
    
        # Create the footnote frame and place it directly in the main container
        self.footnote_frame = Footnote(self.container, FOOTNOTE_TEXT)
        self.footnote_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=PADDING_Y)
    
        self.bind("<Configure>", self.on_resize)

    def create_widget(self, widget_info):
        widget_class, *widget_args = widget_info
        widget = widget_class(self.scrollable_frame, *widget_args)
        widget.pack(fill=tk.X, pady=PADDING_Y)
        return widget

    def on_resize(self, event):
        width = self.winfo_width()
        for widget in self.widget_frames:
            widget.update_wraplength(width)
        self.footnote_frame.update_wraplength(width)  # footnote update

    def update_window_size(self):
        self.update_idletasks()  # Ensure all geometry updates are processed
        self.geometry(WINDOW_GEOMETRY)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        if event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

if __name__ == "__main__":
    app = DocumentEditor()
    app.mainloop()
