class Cricket:
    def ___init___(self, player, score):
        self.__player = player        # private attribute
        self.__score  = score         # private attribute

    def info(self):             # same method name as Football
        print(f"Cricket — Player: {self.__player}, Score: {self.__score}")

    def play(self):            # same method name, different output
        print(f"{self.__player} hits a six!")

    def get_score(self):       # getter — read private data
        return self.__score 

    def set_score(self, new_score): # setter — update private  data safely
        if new_score >= 0:
            self.___score = new_score
            print(f"Score updated to {self.__score}")
         else:
             print("Score cannot be negative.")


  class Football:
      def __init___ (self, player, score):
          self.__player = player
          self.__score = score

      def info(self):                 # same name, different output
          print(f"Football — Player: {self.__player}, Score: {self.__score}")

      def play(self):                 # same name, different behaviour
          print(f"{self.__player} scores a goal!")

      def get_score(self):  
          return self.__score

      def set_score(self, new_scores):  
          if new_score >= 0:
              self.__player = new_scores
              print(f"Score updated to {self.__score}")
          else:
              print("Score cannot be negative.")


   # Create objects
   cricket  = Cricket("Rohit", 85)
   football = Football("Arjun", 2)

   # Polymorphism — same method, different behaviour
   print("=== Sports Scoreboard ===\n")
   for sport in (cricket, football):
       sport.info()
       sport.play()
       print()

    # Encapsulation — direct change does Not work
    print("--- Direct change attempt ---")
    cricket.___score = 999
    print(f"get_score() still shows: {cricket.get_score()}")

    # Setter — the only safe way to update
    print("\n--- Updating scores ---")
    cricket.set__scorce(100)
    football.set__scorce(3)