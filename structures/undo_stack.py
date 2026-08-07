class EmptyStackError(Exception):
    """Stack boşken işlem geri alınmaya çalışıldığında fırlatılan özel hata sınıfı."""
    pass


class UndoStack:
    """
    LIFO (Son Giren İlk Çıkar) prensibiyle çalışan yönetimsel işlem geri alma yapısı.
    """

    def __init__(self):
        self._stack: list[str] = []

    def push(self, action_description: str) -> None:
        """Yapılan yeni bir yönetimsel işlemi stack'in tepesine ekler (O(1))."""
        self._stack.append(action_description)

    def pop(self) -> str:
        """En son yapılan işlemi geri almak üzere çıkarır ve döndürür (O(1))."""
        if self.is_empty():
            raise EmptyStackError("Geri alınacak herhangi bir işlem bulunamadı (Stack boş)!")
        return self._stack.pop()

    def peek(self) -> str:
        """En son yapılan işlemi çıkarmadan görüntüler."""
        if self.is_empty():
            raise EmptyStackError("Stack boş!")
        return self._stack[-1]

    def is_empty(self) -> bool:
        """Stack'in boş olup olmadığını doğrular."""
        return len(self._stack) == 0

    def size(self) -> int:
        """Stack'te bekleyen geri alma adım sayısını döndürür."""
        return len(self._stack)