import pygame


class SpriteSheet:
    def __init__(self, filename, frame_width, frame_height, scale=1):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale

        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except:
            print(f"Предупреждение: не удалось загрузить {filename}, использую fallback-спрайты")
            self.sheet = pygame.Surface((frame_width * 4, frame_height * 4))
            self.sheet.fill((50, 50, 50))

        self.frames = []
        self._extract_frames()

    def _extract_frames(self):
        sheet_width = self.sheet.get_width()
        sheet_height = self.sheet.get_height()

        cols = max(1, sheet_width // self.frame_width)
        rows = max(1, sheet_height // self.frame_height)

        for row in range(rows):
            for col in range(cols):
                x = col * self.frame_width
                y = row * self.frame_height

                if x + self.frame_width <= sheet_width and y + self.frame_height <= sheet_height:
                    frame = self.sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))

                    if self.scale != 1:
                        new_size = (self.frame_width * self.scale, self.frame_height * self.scale)
                        frame = pygame.transform.scale(frame, new_size)

                    self.frames.append(frame)

    def get_frames(self, start, count, flip=False):
        if start >= len(self.frames):
            return []

        end = min(start + count, len(self.frames))
        frames = self.frames[start:end]

        while len(frames) < count and frames:
            frames.append(frames[-1])

        if flip:
            frames = [pygame.transform.flip(f, True, False) for f in frames]

        return frames

    def get_animation(self, row, cols_per_row, flip=False):
        start = row * cols_per_row
        return self.get_frames(start, cols_per_row, flip)