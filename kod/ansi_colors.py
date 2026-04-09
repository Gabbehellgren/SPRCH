#==============================#
#                              #
#            Färger            #
#                              #
#==============================#
# Oscar Hellgren Te23A Ebersteinska Gy

# Ansi color generator handler
# 2026/04/09
class Colors:
    def __init__(self):
        self.colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        self.styles = ["end", "bold", "dim", "italic", "underline", "blink", "blink_fast", "reverse", "hidden", "striketrough"]

        self._generate_standard()


    def _generate_standard(self, mode: int = 1): # TAIL REKURSION AUGHHH
        match mode:
            case 1:
                names = self.colors
                offset = 30

            case 2:
                names = []
                name: str
                for name in self.colors:
                    Name = name.capitalize()
                    names.append(Name)
                offset = 90

            case 3:
                names = []
                name: str
                for name in self.colors:
                    Name = "bg_" + name
                    names.append(Name)
                offset = 40

            case 4:
                names = []
                name: str
                for name in self.colors:
                    Name = "bg_" + name.capitalize()
                    names.append(Name)
                offset = 100

            case 5:
                names = self.styles
                offset = 0
        
        for name in names:
            index = names.index(name) + offset
            str_index = str(index)
            ansi = "\033[" + str_index + "m"
            setattr(self, name, ansi)

        if mode == 5:
            return

        return self._generate_standard(mode + 1)


    def rgb(self, r: int, g: int , b: int, bg: bool = False, name: str = ""):
        match bg:
            case False:
                step = 38

            case True:
                step = 48

        ansi_code = f"\033[{step};2;{r};{g};{b}m"
        if len(name) > 0:
            setattr(self, name, ansi_code)

        return ansi_code