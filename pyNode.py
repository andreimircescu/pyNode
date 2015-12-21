from twisted.spread.pb import Root

class pyNode(Root):
    def __init__(self,name):
        self.name = name

    def remote_add(self, one, two):
        answer = one + two
        print("returning result:" , answer)
        return answer

    def remote_hello(self):
        return "hello world"
        
    def remote_substract(self, one, two):
        return one-two



