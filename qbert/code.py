import pytch


blocks_left = 0


class Background(pytch.Stage):
    Backdrops = ["background.png"]


class LevelClearedText(pytch.Sprite):
    Costumes = ["level-cleared-text.png"]
    start_shown = False

    @pytch.when_I_receive("level-cleared")
    def congratulate_player(self):
        self.go_to_xy(-150, 80)
        self.show()


class Block(pytch.Sprite):
    Costumes = ["block0.png", "block1.png"]
    start_shown = False

    @pytch.when_green_flag_clicked
    def create_pyramid(self):
        for r in range(7):
            for b in range(7 - r):
                block_x = -150 + (b * 56) + (r * 28)
                block_y = -145 + (r * 42)
                self.go_to_xy(block_x, block_y)
                self.pyramid_r = r
                self.pyramid_b = b
                pytch.create_clone_of(self)
        self.pyramid_r = -1
        self.pyramid_b = -1
        pytch.broadcast("set-up-qbert")

    @pytch.when_I_start_as_a_clone
    def appear(self):
        self.set_size(0.875)
        self.switch_costume("block0")
        self.is_lit_up = False
        self.show()

    @pytch.when_I_receive("check-block")
    def check_whether_landed_on(self):
        qbert_r, qbert_b = Qbert.the_original().pyramid_coordinates()
        if self.pyramid_r == qbert_r and self.pyramid_b == qbert_b:
            if not self.is_lit_up:
                self.switch_costume("block1")
                self.is_lit_up = True

                global blocks_left
                blocks_left -= 1


class Qbert(pytch.Sprite):
    Costumes = ["qbert0.png", "qbert1.png", "qbert2.png", "qbert3.png"]
    start_shown = False

    # This list must have exactly 14 entries.
    bounce = [6, 4, 2, 1, 0, 0, 0, 0, 0, 0, -1, -2, -4, -6]

    @pytch.when_I_receive("set-up-qbert")
    def go_to_starting_position(self):
        self.go_to_xy(-150 + 3 * 56, -145 + (6 * 42) + 28)
        self.set_size(1.0)
        self.switch_costume("qbert1")
        self.move_to_front_layer()
        self.show()
        self.jumping = False
        self.fallen_off = False
        global blocks_left
        blocks_left = len(Block.all_clones())

    def pyramid_coordinates(self):
        y_on_stage = self.get_y()
        pyramid_r = (y_on_stage + 145 - 28) / 42
        x_on_stage = self.get_x()
        pyramid_b = (x_on_stage + 150 - pyramid_r * 28) / 56
        return (pyramid_r, pyramid_b)

    def jump(self, x_speed, y_speed, costume):
        if self.jumping or self.fallen_off:
            return
        self.jumping = True
        self.switch_costume(costume)
        for frame in range(14):
            self.change_x(x_speed)
            self.change_y(y_speed + self.bounce[frame])

        r, b = self.pyramid_coordinates()
        if r < 0 or r >= 7 or b < 0 or b >= (7 - r):
            self.fallen_off = True
            pytch.broadcast("fall-off")
        else:
            pytch.broadcast_and_wait("check-block")

        self.jumping = False

    @pytch.when_I_receive("fall-off")
    def disappear(self):
        for i in range(100, 10, -5):
            self.set_size(i / 100.0)
        self.hide()

    @pytch.when_key_pressed("ArrowUp")
    def jump_up(self):
        self.jump(2, 3, "qbert0")

    @pytch.when_key_pressed("ArrowDown")
    def jump_down(self):
        self.jump(-2, -3, "qbert2")

    @pytch.when_key_pressed("ArrowLeft")
    def jump_left(self):
        self.jump(-2, 3, "qbert3")

    @pytch.when_key_pressed("ArrowRight")
    def jump_right(self):
        self.jump(2, -3, "qbert1")
