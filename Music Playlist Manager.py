    # ---- Music Playlist Manager ----
   
    class Playlist:

        # STEP 1 - Parameterized Constructor: runs the moment the playlist is created
        def __init__(self, name, genre):
            self.name = name
            self.genre = genre
            self.songs = []
            print(f"Playlist '{self.name}' ({self.genre}) is ready!")

        # STEP 2 - Add a song to the playlist
        def add_song(self, song):
            self.songs.append(song)
            print(f"'{song}' added to {self.name}.")

        # STEP 3 - Remove a song from the playlist
        def remove_song(self, song):
            if song in self.songs:
                self.songs.remove(song)
                print(f"'{song}' removed.")
             else:
                 print(f"'{song}' not found in playlist.")\

        # STEP 4 - Display all songs
        def display(self):
            print(f"\n--- {self.name} ({self.genre}) ---")
            if self.songs:
                for i, song in enumerate(self.songs, 1):
                    print(f" {i}. {song}")
            else:
                print(" No songs yet. Add some!")

        # STEP 5 - Destructor: runs automaticallly when the playlist is deleted
        def __del__(self):
            print(f"Playlist '{self.name}' has been delated. Goodbye!")

    # Object Creation (constructor fires here)
    my_playlist = Playlist("Road Trip Mix", "Pop")

    # STEP 6 - Menu-driven program using the Playlist class
    while True:
        print("\n1. Add Song 2. Remove Song 3. View Playlist 4. Delete & Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            song = input("Enter song name: ")
            my_playlist.add_song(song)
        elif choice == "2":
            song = input("Enter song to remove: ")
            my_playlist.remove_song(song)
        elif choice == "3":
            my_playlist.display()
        elif choice == "4":
            del my_playlist    # Destructor fires here
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")
