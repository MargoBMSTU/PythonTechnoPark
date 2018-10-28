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
            if len(result) > 0:
                last = result.pop()
                if (last.__class__ == action.__class__):
                        # Случай подряд идущих insert'ов
                    if (last.__class__ == InsertAction and last.pos + len(last.text) == action.pos):
                        act = InsertAction(last.pos, last.text + action.text, last.from_version, action.to_version)
                        action = act
                        # Случай пересекающихся replace'ов
                    elif (last.__class__ == ReplaceAction and last.pos + len(last.text) >= action.pos):
                        resulting_text = last.text[:action.pos - last.pos] + action.text + last.text[(action.pos - last.pos+len(action.text)):]
                        act = ReplaceAction(last.pos, resulting_text, last.from_version, action.to_version)
                        action = act
                        #случай последовательных delete'ов
                    elif (last.__class__ == DeleteAction and last.pos == action.pos):
                        act = DeleteAction(last.pos, last.length + action.length, last.from_version, action.to_version)
                        action = act
                else:
                    result.append(last)

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


h = TextHistory()
#Эквивалентно одному insert("xyzc",0)
h.insert("x",0)
h.insert("y",1)
h.insert("z",2)
h.insert("c",3)
result = h.get_actions()
print("get_actions len: %d,\n0 elem.text: %s\n" % (len(result) , result[0].text))

h = TextHistory()
h.insert("AAAAAAAAAAAA")
#Эквивалентно одному replace("BoB",2)
h.replace("BBB",2)
h.replace("o",3)
result = h.get_actions()
print("get_actions len: %d,\n1 elem.text: %s\n" % (len(result) , result[1].text))


h = TextHistory()
h.insert("qwertyuiop")
#Эквивалентно одному delete(1,5)
h.delete(1,2)
h.delete(1,3)
result = h.get_actions()
print("get_actions len: %d,\n1 elem.length: %s\n" % (len(result) , result[1].length))
print(h.text)