 class Library:
    def __init__(self, list, name):
      self.booksList = list
      self.name = name
      self.lendDict = {}

  def displayBooks(self):
      print(f"We have following books in our library: {self.name}")
      for book in self.booksList:
         print(book)

    def lendBook(self, user, book):
        if book not in self.lendDict.keys():
            self.lendDict.update({book:user})
            print("Lender-Book database has been updated. You can take the book now")
        else:
            print(f"Book is already being used by {self.lendDict[book]}")

            def addBook(self, book):
                self.bookList.appened(book)
                print("Book has been added to the book list")

            def returnBook(self, book):
                self.lendDict.pop(book)

        if__name__ == '__main__':
