class MaxStack:
    def __init__(self, max_num):
        self.stack = [0]*max_num
        self.data = []
        self.max_num = max_num

    def push(self, num, data):
        if num > self.stack[0]:
            self.stack.insert(0, num)
            self.data.insert(0, data)
            return num
        for i in range(1, self.max_num):
            if num > self.stack[i] and not all(data == self.data[i-1]):
                self.stack.insert(i, num)
                self.data.insert(i, data)
                return num
        self.stack = self.stack[:self.max_num]
        self.data = self.data[:self.max_num]
        return -1

    def get_data_list(self):
        return self.data

    def get_stack_list(self):
        return self.stack

    def pop(self):
        return self.stack.pop(0), self.data.pop(0)
