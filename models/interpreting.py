class Interpreting:
    __slots__ = ("text", "allowed_ia", "quest_inside")
    def __init__(self, text='', allowed_ia=False, quest_inside=False):
        self.text = text
        self.allowed_ia = allowed_ia
        self.quest_inside = quest_inside