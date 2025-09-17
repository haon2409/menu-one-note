import objc
from AppKit import (NSApplication, NSStatusBar, NSPopover, NSView, NSMakeRect,
                   NSSize, NSColor, NSTextView, NSScrollView, NSFont, NSMenu,
                   NSMenuItem, NSImage, NSMutableParagraphStyle, NSParagraphStyleAttributeName,
                   NSBezierPath)
from Foundation import NSObject, NSString, NSTimer

class LineView(NSView):
    def initWithFrame_(self, frame):
        self = objc.super(LineView, self).initWithFrame_(frame)
        if self is None:
            return None
        return self

    def drawRect_(self, rect):
        line_color = NSColor.colorWithWhite_alpha_(0.8, 1.0)
        line_color.set()
        
        text_view = self.superview()
        font = text_view.font()
        paragraph_style = text_view.defaultParagraphStyle()
        
        line_spacing = paragraph_style.lineSpacing()
        line_height = font.ascender() - font.descender() + line_spacing + font.leading()
        
        line_width = self.bounds().size.width
        
        text_inset = text_view.textContainerInset()
        y = text_inset.height
        
        while y < self.bounds().size.height:
            path = NSBezierPath.bezierPath()
            path.moveToPoint_((text_inset.width, y))
            path.lineToPoint_((line_width - text_inset.width, y))
            path.setLineWidth_(1)
            path.stroke()
            y += line_height

class NoteView(NSView):
    def initWithFrame_(self, frame):
        self = objc.super(NoteView, self).initWithFrame_(frame)
        if self is None:
            return None

        self.save_timer = None

        scroll_view = NSScrollView.alloc().initWithFrame_(frame)
        self.text_view = NSTextView.alloc().initWithFrame_(frame)

        font_size = 16
        line_spacing = 5
        font = NSFont.systemFontOfSize_(font_size)
        self.text_view.setFont_(font)
        self.text_view.setEditable_(True)
        self.text_view.setRichText_(False)  # Chỉ nhận plain text
        self.text_view.setBackgroundColor_(NSColor.colorWithWhite_alpha_(0.9, 1.0))
        self.text_view.setTextColor_(NSColor.blackColor())
        self.text_view.setTextContainerInset_(NSSize(30, 30))

        self.paragraph_style = NSMutableParagraphStyle.alloc().init()
        self.paragraph_style.setLineSpacing_(line_spacing)
        self.text_view.setDefaultParagraphStyle_(self.paragraph_style)

        try:
            with open('/Users/haonguyen/Projects/menu/menu_one_note/note.txt', 'r') as f:
                self.text_view.setString_(f.read())
        except FileNotFoundError:
            pass

        # self.line_view = LineView.alloc().initWithFrame_(self.text_view.bounds())
        # self.line_view.setAutoresizingMask_(0x12)
        # self.text_view.addSubview_positioned_relativeTo_(self.line_view, 1, None)

        scroll_view.setDocumentView_(self.text_view)
        self.addSubview_(scroll_view)
        self.text_view.setDelegate_(self)
        self.text_view.setAllowsUndo_(True)

        return self

    def textDidChange_(self, notification):
        content = self.text_view.string()
        if self.save_timer:
            self.save_timer.invalidate()
        self.save_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.5, self, "saveContent:", content, False
        )
        self.text_view.textStorage().addAttribute_value_range_(
            NSParagraphStyleAttributeName, 
            self.paragraph_style, 
            (0, self.text_view.textStorage().length())
        )
        NSApplication.sharedApplication().delegate().updateStatusIconBasedOnText()

    def saveContent_(self, timer):
        content = timer.userInfo()
        with open('/Users/haonguyen/Projects/menu/menu_one_note/note.txt', 'w') as f:
            f.write(content)
        self.save_timer = None

class NoteAppDelegate(NSObject):
    def init(self):
        self = objc.super(NoteAppDelegate, self).init()
        if self:
            self.popover = NSPopover.alloc().init()
            
            note_view = NoteView.alloc().initWithFrame_(NSMakeRect(0, 0, 450, 400))
            if note_view:
                self.popover.setContentSize_(NSSize(450, 400))
                self.popover.setContentViewController_(objc.lookUpClass("NSViewController").alloc().initWithNibName_bundle_(None, None))
                self.popover.contentViewController().setView_(note_view)
            
            self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
            self.icon_with_text = NSImage.alloc().initWithContentsOfFile_('/Users/haonguyen/Projects/menu/menu_one_note/one_note_have_text_icon.png')
            self.icon_empty = NSImage.alloc().initWithContentsOfFile_('/Users/haonguyen/Projects/menu/menu_one_note/one_note_no_text_icon.png')
            
            if self.icon_with_text:
                self.icon_with_text.setSize_((22, 22))
            if self.icon_empty:
                self.icon_empty.setSize_((22, 22))
            
            self.status_item.button().setImage_(self.icon_empty if not self.icon_with_text else self.icon_with_text)
            self.status_item.button().setAction_("togglePopover:")
            self.status_item.button().setTarget_(self)
            
            self.popover.setBehavior_(0)
            self.note_view = note_view
            self.setupMenu()
            self.updateStatusIconBasedOnText()
            
        return self

    def setupMenu(self):
        main_menu = NSMenu.alloc().initWithTitle_("MainMenu")
        edit_menu = NSMenu.alloc().initWithTitle_("Edit")
        
        select_all = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Select All", "selectAll:", "a")
        copy = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Copy", "copy:", "c")
        cut = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Cut", "cut:", "x")
        paste = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Paste", "paste:", "v")
        undo = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Undo", "undo:", "z")
        redo = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Redo", "redo:", "Z")
        
        modifier = 1 << 20  # NSCommandKeyMask
        select_all.setKeyEquivalentModifierMask_(modifier)
        copy.setKeyEquivalentModifierMask_(modifier)
        cut.setKeyEquivalentModifierMask_(modifier)
        paste.setKeyEquivalentModifierMask_(modifier)
        undo.setKeyEquivalentModifierMask_(modifier)
        redo.setKeyEquivalentModifierMask_(modifier | 1 << 18)  # NSShiftKeyMask
        
        edit_menu.addItem_(select_all)
        edit_menu.addItem_(copy)
        edit_menu.addItem_(cut)
        edit_menu.addItem_(paste)
        edit_menu.addItem_(undo)
        edit_menu.addItem_(redo)
        
        edit_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Edit", None, "")
        edit_menu_item.setSubmenu_(edit_menu)
        main_menu.addItem_(edit_menu_item)
        
        NSApplication.sharedApplication().setMainMenu_(main_menu)

    def updateStatusIconBasedOnText(self):
        content = self.note_view.text_view.string()
        if content and len(content) > 0:
            self.status_item.button().setImage_(self.icon_with_text)
        else:
            self.status_item.button().setImage_(self.icon_empty)

    def togglePopover_(self, sender):
        if self.popover.isShown():
            self.popover.close()
        else:
            self.popover.setAnimates_(False)
            self.popover.showRelativeToRect_ofView_preferredEdge_(sender.bounds(), sender, 3)        
            self.popover.contentViewController().view().window().makeKeyAndOrderFront_(None)
            self.note_view.text_view.window().makeFirstResponder_(self.note_view.text_view)

    def applicationDidFinishLaunching_(self, notification):
        NSApplication.sharedApplication().setActivationPolicy_(1)

    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        return False

    def undo_(self, sender):
        if self.note_view.text_view.undoManager().canUndo():
            self.note_view.text_view.undoManager().undo()

    def redo_(self, sender):
        if self.note_view.text_view.undoManager().canRedo():
            self.note_view.text_view.undoManager().redo()

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = NoteAppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()