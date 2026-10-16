import pygame, random
pygame.init()

W,H=800,600
s=pygame.display.set_mode((W,H))
pygame.display.set_caption("Brick Breaker")
clock=pygame.time.Clock()
font=pygame.font.SysFont("Arial",28,True)

p=pygame.Rect(340,540,120,15)
b=pygame.Rect(390,500,15,15)
dx,dy=5,-5
score,lives=0,3
over=False

def make_bricks():
    return [pygame.Rect(55+x*90,70+y*35,80,25)
            for y in range(5) for x in range(8)]

bricks=make_bricks()

while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT: pygame.quit(); quit()
        if e.type==pygame.KEYDOWN and e.key==pygame.K_r and over:
            p.x,b.x,b.y=340,390,500
            dx,dy=5,-5
            score,lives,over=0,3,False
            bricks=make_bricks()

    if not over:
        k=pygame.key.get_pressed()
        p.x += (k[pygame.K_RIGHT]-k[pygame.K_LEFT])*8
        p.x=max(0,min(W-p.width,p.x))

        b.x+=dx; b.y+=dy

        if b.left<=0 or b.right>=W: dx=-dx
        if b.top<=0: dy=-dy

        if b.colliderect(p) and dy>0: dy=-dy

        for r in bricks[:]:
            if b.colliderect(r):
                bricks.remove(r)
                dy=-dy
                score+=10
                break

        if b.top>H:
            lives-=1
            b.x,b.y=390,500
            dx,dy=random.choice([-5,5]),-5
            if lives==0: over=True

        if not bricks: over=True

    s.fill((18,22,32))

    for r in bricks:
        pygame.draw.rect(s,(220,60,60),r,border_radius=5)

    pygame.draw.rect(s,(50,170,240),p,border_radius=7)
    pygame.draw.circle(s,(255,220,60),b.center,8)

    s.blit(font.render(f"Score: {score}",1,"white"),(20,20))
    s.blit(font.render(f"Lives: {lives}",1,"white"),(680,20))

    if over:
        msg="YOU WIN!" if not bricks else "GAME OVER"
        t=font.render(msg+"  Press R",1,"white")
        s.blit(t,(W//2-t.get_width()//2,300))

    pygame.display.flip()
    clock.tick(60)