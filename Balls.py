


import matplotlib.pyplot as plt

import turtle
import random

def is_collided_with(a, b, rad):
        dist = pow(a.xcor() - b.xcor(), 2) + pow(a.ycor() - b.ycor() , 2) 
        #dist = pow(dist, 1/2) 
        #This scaling of rad seems to fix the distance of collisions just fine
        if dist <= 300*rad: 
            return True
        return False

wn=turtle.Screen()                                                       #sets the screen for bouncing balls
wn.bgcolor("black")                                                      #sets background-color of the screen
wn.title("BOUNCING BALL SIMULATOR I mean Corona Time!")                                      #sets title of the screen
wn.tracer(0)

balls=[]
colors=["white","yellow","grey"]
# healthy (suss), infected, recovered  (S, I, R)
#the order is respected by later code

num_balls = 40
num_balls = 100
Rad = 1
inf_time = [0]*num_balls
rec_time = 400
num_init_inf = 1
num_infs = 0

for x in range(num_balls):
    balls.append(turtle.Turtle())

#modify ratio of colors to biase color choice
#colors=["white","yellow","grey","grey","grey","grey","grey","grey","grey","grey"]
colors=["white","white","white","white","white","white","white","white","yellow","grey"]
for ball in balls:
    ball.shape("circle")
    ball.shapesize(Rad,Rad)
    ball.shapesize(outline=Rad)

    ball.color(random.choice(colors) )
#    ball.color(colors[0])
#    if num_infs < num_init_inf:
#        ball.color(colors[1])
#        num_infs += 1
#
    #no imune version
    #ball.color( random.choice([ "white", "yellow"] ) )


    ball.penup()   #turtle starts by default-at the center of screen,so not to show its movement to another position by drawing line use penup()
    ball.speed(2)    #sets the animation speed
    x=random.randint(-200,200)
    y=random.randint(-200,200)
    ball.goto(x,y)                      #sets position of ball on screen
    #speed paramdeter
    S = 3 
    ball.dy=random.randint(-S,S)
    ball.dx=random.randint(-S,S)
#gravity=0.1 #No gravity becasue random movement
gravity=0


#randomized intial infected times
for i in range(num_balls):
    if balls[i].color()[0] == colors[1]:
        inf_time[i] = random.randint(0, rec_time )


colors=["white","yellow","grey"]

Num_S = []
Num_I = []
Num_R = []

num_S = 100
num_I = 1
num_R = 0

#go while there are active infections
while num_I > 0:
    wn.update()
    num_S = 0
    num_I = 0
    num_R = 0

    #for ball in balls:
    for i in range(num_balls):
        ball =  balls[i] 
        ball.dy -= gravity 
        ball.sety(ball.ycor()+ball.dy)
        ball.setx(ball.xcor()+ball.dx)

        ind = colors.index( ball.color()[0] )
        if ind ==0:
            num_S +=1
        elif ind ==1:
            num_I +=1
        else:
            num_R +=1

        #shift time up if infected currently
        if ball.color()[0] == colors[1]:
            inf_time[i] += 1
            if inf_time[i]  >= rec_time:
                ball.color( colors[2] ) 
        
        #checks for a wall collision
        if ball.xcor()>330:
            ball.dx*=-1
        if ball.xcor()<-330:
            ball.dx*=-1
        #Check for a bounce from lower surface
        if ball.ycor()<-270:
            ball.dy*=-1
        if ball.ycor()>270:
            ball.dy*=-1

        #check for collisions with other balls
        for j in range(i+1,num_balls):
            if is_collided_with( ball, balls[j] , Rad):
                ball_2 = balls[j]

                #For some reason the colors are stored as tuples in the turtle thing
                #change color when getting infected
                if ball.color()[0] == colors[1] and ball_2.color()[0] == colors[0]:
                    ball_2.color(colors[1]) 
                elif ball.color()[0] == colors[0] and ball_2.color()[0] == colors[1]:
                    ball.color(colors[1]) 

                #since the masses are equal we just exchange velocities
                #save v_1
                dx1 = ball.dx 
                dy1 = ball.dy 
                #save v_2 = u_1
                ball.dx = ball_2.dx
                ball.dy = ball_2.dy 
                #save u_2 = v_1
                ball_2.dx = dx1 
                ball_2.dy = dy1 

    #update tallies across times
    Num_S.append(num_S) 
    Num_I.append(num_I) 
    Num_R.append(num_R) 

plt.plot( Num_S, color = "w") 
plt.plot( Num_I, color = "y") 
plt.plot( Num_R, color = "grey") 
ax = plt.gca()
ax.set_facecolor('k')
plt.title('White=Sus., Yellow=Inf., Grey=Rec.')
plt.show()
    
wn.mainloop()
