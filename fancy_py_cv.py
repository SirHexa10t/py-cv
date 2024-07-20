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
        self.time = time
        self.description = description
        self.is_collapsed = True  # Initially collapsed
        self.timeline = timeline  # Reference to the timeline
        self.create_widgets()

    def create_widgets(self):
        self.time_button = tk.Button(self, text=self.time, command=self.toggle_content, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, anchor="w")
        self.time_button.pack(pady=PADDING_Y, anchor='w')

        self.content_frame = tk.Frame(self, bg=BG_COLOR)
        self.description_label = tk.Label(self.content_frame, justify=tk.LEFT, text=self.description, wraplength=self.winfo_width(), bg=BG_COLOR, fg=TEXT_COLOR)
        self.description_label.pack(anchor='w', padx=PADDING_X)
        self.content_frame.pack(fill=tk.X)
        self.content_frame.pack_forget()  # Initially hide the content frame

    def toggle_content(self):
        if self.is_collapsed:
            self.content_frame.pack(fill=tk.X)
            self.is_collapsed = False
        else:
            self.content_frame.pack_forget()
            self.is_collapsed = True
        self.timeline.update_canvas_height()  # Update the canvas height

    def update_wraplength(self, width):
        self.description_label.config(wraplength=width - 2 * PADDING_X)


class Timeline(tk.Frame):
    def __init__(self, master, title, events):
        super().__init__(master, bg=BG_COLOR)
        self.title = title
        self.events = events
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text=self.title, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_TITLE, anchor="w")
        title_label.pack(fill=tk.X, pady=PADDING_Y)

        self.canvas = tk.Canvas(self, width=TIMELINE_WIDTH, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=TIMELINE_PADX, pady=PADDING_Y, fill=tk.Y)

        self.event_frames = []
        for index, event in enumerate(self.events):
            collapsible_event = CollapsibleTimelineEvent(self, event['time'], event['description'], self)
            collapsible_event.pack(fill=tk.X, pady=PADDING_Y, anchor="w")
            self.event_frames.append(collapsible_event)

        self.update_canvas_height()

    def update_canvas_height(self):
        total_height = 0
        for frame in self.event_frames:
            total_height += frame.time_button.winfo_reqheight()
            if not frame.is_collapsed:
                total_height += frame.content_frame.winfo_reqheight()
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
        self.title = title
        self.paragraph = paragraph
        self.center = center
        self.is_collapsed = not center  # Centered title is not collapsible, left-aligned is initially collapsed
        self.create_widgets()

    def create_widgets(self):
        title_anchor = "center" if self.center else "w"
        paragraph_anchor = "center" if self.center else "w"
        
        title_style_args = { 'text': self.title, 'bg': BG_COLOR, 'fg': TEXT_COLOR, 'font': FONT_TITLE, 'anchor': title_anchor, }
        paragraph_label_args = { 'text': self.paragraph, 'wraplength': self.winfo_width(), 'bg': BG_COLOR, 'fg': TEXT_COLOR, 'anchor': paragraph_anchor, }
        def pack_element(elem):
            elem.pack(fill=tk.X, pady=PADDING_Y)
            
        if self.center:
            pack_element(tk.Label(self, **title_style_args))
            self.paragraph_label = tk.Label(self, **paragraph_label_args)
            pack_element(self.paragraph_label)
        else:
            self.title_button = tk.Button(self, command=self.toggle_content, **title_style_args)
            pack_element(self.title_button)
            self.content_frame = tk.Frame(self, bg=BG_COLOR)
            self.paragraph_label = tk.Label(self.content_frame, justify=tk.LEFT, **paragraph_label_args)
            pack_element(self.paragraph_label)
            self.content_frame.pack(fill=tk.X)
            self.content_frame.pack_forget()  # Initially hide the content frame

    def toggle_content(self):
        if self.is_collapsed:
            self.content_frame.pack(fill=tk.X)
            self.is_collapsed = False
        else:
            self.content_frame.pack_forget()
            self.is_collapsed = True

    def update_wraplength(self, width):
        self.paragraph_label.config(wraplength=width - PADDING_X)
        

class Footnote(tk.Frame):
    def __init__(self, master, text):
        super().__init__(master, bg=BG_COLOR)
        self.text = text
        self.create_widgets()

    def create_widgets(self):
        footnote_label = tk.Label(self, text=self.text, bg=BG_COLOR, fg=TEXT_COLOR, anchor="w", justify="left", wraplength=self.winfo_width())
        footnote_label.pack(fill=tk.X, pady=PADDING_Y)

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
        style.configure("Vertical.TScrollbar", width=SCROLLBAR_WIDTH)
        
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
    
        self.widget_frames = []
        for widget_info in WIDGET_STRUCTURE:
            widget_class = widget_info[0]
            widget_args = widget_info[1:]
            widget = widget_class(self.scrollable_frame, *widget_args)
            widget.pack(fill=tk.X, pady=PADDING_Y)
            self.widget_frames.append(widget)
    
        # Create the footnote frame and place it directly in the main container
        self.footnote_frame = Footnote(self.container, FOOTNOTE_TEXT)
        self.footnote_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=PADDING_Y)
    
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.update_wraplengths()

    def update_wraplengths(self):
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
