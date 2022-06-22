import os
import random

import pygame
pygame.font.init()

# Extensions implemented:
# Better Visual, Ending


class Obstacle:
    x, y = 700, random.randint(-350, 0)
    width = 80
    height = 500

    def __init__(self):
        self.pipe1 = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pipeUp1 = pygame.transform.scale(pygame.image.load('pipeFacingDown.png'), (80,500))
        self.pipe2 = pygame.Rect(self.x, self.y + self.height + 150, self.width, self.height)
        self.pipeDown1 = pygame.transform.scale(pygame.image.load('pipeFacingUp.png'), (80,500))
        self.pipes = [(self.pipeUp1, self.pipe1),  (self.pipeDown1, self.pipe2)]
        for i in range(4):
            self.createRandomPipe()

    def createRandomPipe(self):
        x = self.pipes[-1][1].x + 280
        y = random.randint(-350, 0)
        newPipeFacingDown = pygame.Rect(x, y, self.width, self.height)
        newPipeFacingUp = pygame.Rect(x, y + self.height + 150, self.width, self.height)

        newPipeFacingUp1 = pygame.transform.scale(pygame.image.load('pipeFacingUp.png'), (80, 500))
        newPipeFacingDown1 = pygame.transform.scale(pygame.image.load('pipeFacingDown.png'), (80, 500))

        tpl1 = (newPipeFacingUp1, newPipeFacingUp)
        tpl2 = (newPipeFacingDown1, newPipeFacingDown)
        self.pipes.append(tpl1)
        self.pipes.append(tpl2)

    def drawPipe(self, screen):
        for pipe in self.pipes:
            screen.blit(pipe[0], (pipe[1].x, pipe[1].y))

    def movePipe(self):
        for pipe in self.pipes:
            pipe[1].x -= 5

    def outOfBounds(self):
        if self.pipes[0][1].x + self.width < 0:
            self.pipes.remove(self.pipes[0])
            self.pipes.remove(self.pipes[0])
            return True

    def collision(self, bird):
        for pipe in self.pipes:
            if bird.colliderect(pipe[1]):
                return True
        if bird.y < 0 or bird.y + 34 > 700:
            return True

class Bird:
    x, y = 100, 316
    size = 20
    speed = 1
    direction = 'Down'
    def __init__(self):
        self.fBird = pygame.Rect(self.x, self.y, self.size, self.size)
        self.bird = pygame.transform.scale(pygame.image.load('flappyBird.png'), (50, 34))

    def displayBird(self, screen):
        screen.blit(self.bird, (self.fBird.x, self.fBird.y))

    def changeDirection(self):
        keys = pygame.key.get_pressed()
        mousePress = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE] or mousePress[0]:
            self.direction = "Up"

    def move(self):
        self.changeDirection()
        self.fBird.x += self.speed
        if self.direction == "Down":
            self.fBird.y += 8
        else:
            self.fBird.y -= 15
            self.direction = "Down"

    def outOfBoundsRight(self):
        if self.fBird.x > 1200 - self.bird.get_width():
            return True

class App:
    birdMoving = True
    ENDING_FONT = pygame.font.SysFont('comicsans', 100)
    background = pygame.transform.scale(pygame.image.load(
        os.path.join("background.png")), (1200, 700))

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.bird = Bird()
        self.pipe = Obstacle()

    def run(self):
        self.init()
        while self.running:
            self.clock.tick(24)
            self.render()
            self.update()
            pygame.display.update()

        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.events()
        if self.bird.outOfBoundsRight():
            self.birdMoving = False
            self.drawEnding(True)

        if self.pipe.collision(self.bird.fBird):
            self.birdMoving = False
            self.drawEnding(False)

        if self.birdMoving == False:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.birdMoving = True
                app = App()
                app.run()
            elif keys[pygame.K_q]:
                self.running = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.cleanUp()
        self.screen.blit(self.background, (0,0))

        self.bird.displayBird(self.screen)
        self.pipe.drawPipe(self.screen)
        if self.birdMoving:
            self.bird.move()
            self.pipe.movePipe()
        if self.pipe.outOfBounds():
            self.pipe.createRandomPipe()


    def cleanUp(self):
        self.screen.fill(0)

    def drawEnding(self, bool):
        str1 = "You Won!"
        str2 = "You Lost!"
        str3 = "Play Again - R"
        str4 = "Quit - Q"

        ending1 = self.ENDING_FONT.render(str1, False, (255, 255, 255))
        ending2 = self.ENDING_FONT.render(str2, False, (255, 255, 255))
        ending3 = self.ENDING_FONT.render(str3, False, (255, 255, 255))
        ending4 = self.ENDING_FONT.render(str4, False, (255, 255, 255))

        if bool == True: #If the player won
            self.screen.blit(ending1, (600 - ending1.get_width() / 2, 250 - ending1.get_height() / 2))

        else:
            self.screen.blit(ending2, (600 - ending2.get_width() / 2, 250 - ending2.get_height() / 2))

        self.screen.blit(ending3, (600 - ending3.get_width() / 2, 280))
        self.screen.blit(ending4, (600 - ending4.get_width() / 2, 320 + ending4.get_height() / 2))



if __name__ == "__main__":
    app = App()
    app.run()