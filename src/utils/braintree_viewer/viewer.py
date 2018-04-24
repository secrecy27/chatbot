try:
    from Tkinter import Tk
    from ttk import Treeview, Scrollbar, Frame
    from Tkconstants import HORIZONTAL, VERTICAL, N, S, E, W, END, BOTH, YES
except ImportError:
    from tkinter import Tk
    from tkinter.ttk import Treeview, Scrollbar, Frame
    from tkinter.constants import HORIZONTAL, VERTICAL, N, S, E, W, END, BOTH, YES

import xml.etree.ElementTree as ET
import sys
from operator import attrgetter

def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


class XML_Viewer(Frame):
    def __init__(self, master, xml=None, heading_text=None, heading_anchor=None, padding=None, cursor=None,
                 takefocus=None, style=None):
        Frame.__init__(self, master, class_="XML_Viewer")

        self._vsb = Scrollbar(self, orient=VERTICAL)
        self._hsb = Scrollbar(self, orient=HORIZONTAL)

        kwargs = {}
        kwargs["yscrollcommand"] = lambda f, l: autoscroll(self._vsb, f, l)
        kwargs["xscrollcommand"] = lambda f, l: autoscroll(self._hsb, f, l)

        if style is not None:
            kwargs["style"] = style

        if padding is not None:
            kwargs["padding"] = padding

        if cursor is not None:
            kwargs["cursor"] = cursor

        if takefocus is not None:
            kwargs["takefocus"] = takefocus

        self._treeview = Treeview(self, **kwargs)

        if heading_text is not None:
            if heading_anchor is not None:
                self._treeview.heading("#0", text=heading_text, anchor=heading_anchor)
            else:
                self._treeview.heading("#0", text=heading_text)

        self._treeview.bind("<<TreeviewOpen>>", self._on_open)
        self._treeview.bind("<<TreeviewClose>>", self._on_close)

        # Without this line, horizontal scrolling doesn't work properly.
        self._treeview.column("#0", stretch=False)
        self._treeview.column("#0", width=500)

        self._vsb['command'] = self._treeview.yview
        self._hsb['command'] = self._treeview.xview

        self._treeview.grid(column=0, row=0, sticky=N + S + W + E)
        self._vsb.grid(column=1, row=0, sticky=N + S)
        self._hsb.grid(column=0, row=1, sticky=E + W)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._element_tree = None
        self._item_ID_to_element = {}

        if xml is not None:
            self.parse_xml(xml)

    def _on_open(self, event):
        item_ID = self._treeview.focus()
        if item_ID not in self._item_ID_to_element: return

        node = self._item_ID_to_element[item_ID]

        self._treeview.item(item_ID, text=self._repr_of_openning_tag(node))

    def _on_close(self, event):
        item_ID = self._treeview.focus()
        if item_ID not in self._item_ID_to_element: return

        node = self._item_ID_to_element[item_ID]

        text = self._repr_of_openning_tag(node) + self._repr_of_closing_tag(node)
        self._treeview.item(item_ID, text=text)

    def parse_xml(self, xml):
        self._element_tree = ET.ElementTree(ET.fromstring(xml))

        self.clear()
        self._walk_xml(self._element_tree.getroot())

    @property
    def element_tree(self):
        return self._element_tree

    @element_tree.setter
    def element_tree(self, element_tree):
        self._element_tree = element_tree

        self.clear()
        self._walk_xml(element_tree.getroot())

    def clear(self):
        self._item_ID_to_element = {}
        self._treeview.delete(*self._treeview.get_children())

    def _repr_of_openning_tag(self, node):
        text = "<" + node.tag

        attrs = node.attrib

        # list function is here necessary to provide support to Python 3
        a_names = list(attrs.keys())
        a_names.sort()

        for a_name in a_names:
            text += ' %s="' % a_name
            text += attrs[a_name]
            text += '"'

        text += ">"
        return text

    def _repr_of_closing_tag(self, node):
        return "</%s>" % node.tag

    def _walk_xml(self, node, depth=0, parent=""):
        text = self._repr_of_openning_tag(node) + self._repr_of_closing_tag(node)

        item = self._treeview.insert(parent, END, text=text)
        self._item_ID_to_element[item] = node

        if node.text:
            text = node.text.strip()
            if text != "":
                for line in text.splitlines():
                    self._treeview.insert(item, END, text=line)

        sorted_nodes = sorted(list(node), key=attrgetter('tag'))
        for child_node in sorted_nodes:
            self._walk_xml(child_node, depth + 1, parent=item)

        if node.tail:
            tail = node.tail.strip()
            if tail != "":
                for line in tail.splitlines():
                    self._treeview.insert(parent, END, text=line)


if __name__ == "__main__":

    if len(sys.argv) != 2 or sys.argv[1] is None or sys.argv[1] == "":
        print("No xml file name specified!")
        exit(0)

    filename = sys.argv[1]

    root = Tk()
    with open(filename, "r") as xml_file:
        xml = xml_file.read()
    XML_Viewer(root, xml, heading_text="Braintree").pack(fill=BOTH, expand=YES)
    root.mainloop()
