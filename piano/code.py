import pytch

class Room(pytch.Stage):
    Backdrops = ["music-room.jpg"]

class WhiteKey(pytch.Sprite):
    Costumes = ["C.png","C2.png"]
    Sounds = ["C6Sound.mp3"]
    SoundNames = ["C6Sound"]

    @pytch.when_green_flag_clicked
    def start(self):
    	self.switch_costume(0)
    	self.go_to_xy(-100,0)
    	self.set_size(0.3)
    	self.sound = self.SoundNames[0]

    @pytch.when_this_sprite_clicked
    def keyClicked(self):
        self.switch_costume(1)
        self.play_sound_until_done(self.sound)
        self.switch_costume(0)


class Song(pytch.Sprite):
    Costumes = ["Cake.png","JingleBells.png",]

    @pytch.when_green_flag_clicked
    def start(self):
        for i in range(2):
            self.index = i;
            self.switch_costume(i)
            self.go_to_xy(-180 + i*100,140)
            self.set_size(0.1)
            pytch.create_clone_of(self)
        self.hide();


class BlackKey(pytch.Sprite):
    Costumes =["BlackKey.png"]

    @pytch.when_green_flag_clicked
    def start(self):
        self.switch_costume(0)
        self.go_to_xy(-85,27)
        self.set_size(0.3)
