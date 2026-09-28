import time

class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_front(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def insert_back(self, value):
        new_node = Node(value)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def search(self, value):
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None

    def remove(self, value):
        node = self.search(value)
        if not node:
            return False
        
        # Ajusta o ponteiro do nó anterior
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next # Era o primeiro nó
            
        # Ajusta o ponteiro do próximo nó
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev # Era o último nó
            
        return True

    def list_forward(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.value))
            current = current.next
        return " → ".join(elements)

    def list_backward(self):
        elements = []
        current = self.tail
        while current:
            elements.append(str(current.value))
            current = current.prev
        return " → ".join(elements)

def main():
    dll = DoublyLinkedList()
    
    print("--- Sequência Obrigatória ---")
    for val in [10, 20, 30, 40, 50]:
        dll.insert_back(val)
    
    dll.remove(30)
    
    print(dll.list_forward())
    print(dll.list_backward())
    
    print("\n--- Teste de Desempenho (100.000 elementos) ---")
    big_list = DoublyLinkedList()
    for i in range(100000):
        big_list.insert_back(i)
        
    targets = {
        "Início (10)": 10,
        "Meio (50000)": 50000,
        "Final (99990)": 99990
    }
    
    for pos, val in targets.items():
        start = time.perf_counter()
        big_list.search(val)
        end = time.perf_counter()
        print(f"Busca no {pos}: {end - start:.6f} segundos")

if __name__ == '__main__':
    main()
