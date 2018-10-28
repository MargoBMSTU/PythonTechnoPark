class TextHistory:
    def __init__(self):
        self._text = ''
        self._version = 0
        self.actions = []

    @property
    def text(self):
        return self._text

    @property
    def version(self):
        return self._version



    def insert(self, text, pos = None):
        if pos == None:
            pos = len(self._text)
        action = InsertAction(pos, text, self._version, self._version + 1)
        self._version += 1
        self.actions.append(action)
        self._text = action.apply(self._text)
        return self._version

    def replace(self, text, pos = None):
        if pos == None:
            pos = len(self._text)
        action = ReplaceAction(pos, text, self._version, self._version + 1)
        self._version += 1
        self.actions.append(action)
        self._text = action.apply(self._text)
        return self._version

    def delete(self, pos, length):
        action = DeleteAction(pos, length, self._version, self._version + 1)
        self._version += 1
        self.actions.append(action)
        self._text = action.apply(self._text)
        return self._version

    def action(self, action):
        if action.from_version != self._version:
            raise ValueError
        self._version = action.to_version
        self._text = action.apply(self._text)
        self.actions.append(action)
        return self._version

    def get_actions(self, from_version = 0, to_version = None):
        if to_version == None:
            to_version = self._version
        if to_version > self._version or from_version > to_version or from_version > self._version or from_version < 0:
            raise ValueError
        result = []
        for action in self.actions:
            if action.from_version < from_version:
                continue
            elif action.to_version > to_version:
                break
            result.append(action)
        return result


class Action:
    def __init__(self, pos, from_version, to_version):
        self. pos = pos
        self.from_version = from_version
        self.to_version = to_version

    def apply(self, text):
        pass


class InsertAction(Action):
    def __init__(self, pos, text, from_version, to_version):
        super(InsertAction, self).__init__(pos, from_version, to_version)
        self.text = text

    def apply(self, gettext):
        if (self.pos < 0) or (self.pos > len(gettext)):
            raise ValueError
        gettext = gettext[:self.pos] + self.text + gettext[self.pos:]
        return gettext

class ReplaceAction(Action):
    def __init__(self, pos, text, from_version, to_version):
        super(ReplaceAction, self).__init__(pos, from_version, to_version)
        self.text = text

    def apply(self, gettext):
        if (self.pos < 0) or (self.pos > len(gettext)):
            raise ValueError
        gettext = gettext[:self.pos] + self.text + gettext[(self.pos+len(self.text)):]
        return gettext


class DeleteAction(Action):
    def __init__(self, pos,length, from_version, to_version):
        super(DeleteAction, self).__init__(pos, from_version, to_version)
        self.length = length

    def apply(self, gettext):
        # if self.length == 0:
        #     return gettext
        if (self.pos < 0) or (self.pos+self.length > len(gettext)):
            raise ValueError
        gettext = gettext[:self.pos] + gettext[self.pos+self.length:]
        return gettext


# h = TextHistory()
# h.insert("abc")
# print(h.version)
# #h.replace("kkkkk", 2)
# #h.delete(2,10)
# #h.insert("kek",2)

# i = InsertAction(0,"kehgyygygy",1,69)
# h.action(i)
# print(h.text,h.version,h.actions)