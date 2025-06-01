class node:
    def __init__(self, value):
        self.value = value
        self.next = None

class queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def __str__(self):
        if self.head is None: return "Kosong"
        
        ret = ""
        i = 0
        cur = self.head

        while cur:
            ret += f"- {i}: {cur.value}\n"
            cur = cur.next
            i += 1

        ret += f"\nAda {self.size} antrian."
        
        return ret

    def enqueue(self, value):
        new_node = node(value)

        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        if self.head is None: return None

        ret = self.head.value
        self.head = self.head.next

        if self.head is None: self.tail = None

        self.size -= 1
        
        return ret

    def peek(self):
        if self.head is None: return None
        return self.head.value
    
    def peek_next(self):
        if self.head is None or self.head.next is None: return None
        return self.head.next.value

    def is_empty(self):
        return self.head is None