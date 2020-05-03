
#Third draft of SIR Balls Model
#the people who start not moving stay not moving when collided
#the 2nd ball just reverses direction in collision

#adding clause to begin full movement when infection drops below x percent

import matplotlib.pyplot as plt
import turtle
import random


wn=turtle.Screen()                                                       #sets the screen for bouncing balls
wn.bgcolor("black")                                                      #sets background-color of the screen
wn.title("BOUNCING BALL SIMULATOR I mean Corona Time!") #sets title of the screen, doesnt seem to do anythin
wn.tracer(0)

balls=[]
Colors=["white","yellow","grey"] #healthy (suss), infected, recovered  (S, I, R)
#master colors list whose order matters for later
num_balls = 100
#want to scale frequency of collision with size of simulation, 
#that is more balls shouldn't automaticly have higher spread rate
Rad = 1 / ( pow(num_balls/10, 1/2) ) 
inf_time = [0]*num_balls
rec_time = 400
num_init_inf = 1
num_infs = 0
frac_imb = 3/4
num_imb = 0
Imb= [] #list to check on imobile balls


frac_trigger = 4/100



#colors=["white","yellow","grey","grey","grey","grey","grey","grey","grey","grey"]
#Mostly recoverd

colors=["white","white","white","white","white","white","white","white","yellow","grey"]
#80 healthy, 10% recover, 10% infected

#colors=["white","yellow","yellow","yellow","yellow","grey"]
#colors=["white","yellow","grey"]
for i in range(num_balls):
    balls.append(turtle.Turtle())
    ball = balls[i]
    ball.shape("circle")
    ball.shapesize(Rad,Rad)
    ball.shapesize(outline=Rad)

    ball_color = random.choice(colors) 
    ball.color(ball_color)

    #randomized intial infected times
    if ball_color == Colors[1]: #Colors since colors is modified currently
        inf_time[i] = random.randint(0, rec_time )

    ball.penup()   #turtle starts by default-at the center of screen,so not to show its movement to another position by drawing line use penup()
    ball.speed(20)    #sets the animation speed
    x=random.randint(-300,300)
    y=random.randint(-250,250)
    ball.goto(x,y)                      #sets position of ball on screen

    S = 6 #speed paramdeter
    ball.dy=random.randint(-S,S)
    ball.dx=random.randint(-S,S)

    #first n are imobile
    if num_imb < frac_imb*num_balls: 
        ball.dy=0
        ball.dx=0
        num_imb += 1
        Imb.append(True)
    else:
        Imb.append(False)

#fixes order agian to deal with later code
colors = Colors
Num_S = [] #arrays to keep track of infections etc
Num_I = []
Num_R = []
num_S = 0
num_I = num_balls #skip false trigger of freed
num_R = 0
Nums = [num_S, num_I, num_R] 

freed = False
freed_time= 0

while Nums[1] > 0:  #go while there are active infections
    wn.update()

    #Once conditions are meet to move freely people begin moving about again
    if not freed and Nums[1] < frac_trigger * num_balls:
        print("freed")
        for i in range(num_balls):
            if Imb[i]: #if previously not moving, change speeds to moving
                ball = balls[i]
                ball.dy=random.randint(-S,S)
                ball.dx=random.randint(-S,S)
        #Now everyone moves
        Imb = [False]*num_balls
        free_move = False
        freed  = True #now longer initate loop
        freed_time = len(Num_S)

    #reset counters
    Nums= [0]*3
    #for ball in balls:
    for i in range(num_balls):
        ball =  balls[i] 
        ball.dy -= 0
        ball.sety(ball.ycor()+ball.dy)
        ball.setx(ball.xcor()+ball.dx)

        #incriment counters
        Nums[ colors.index( ball.color()[0] )  ] += 1

        if ball.color()[0] == colors[1]: #shift time up if infected currently
            inf_time[i] += 1
            if inf_time[i]  >= rec_time: #if infected long enough recover
                ball.color( colors[2] ) 
        
        #checks for boundary wall collision
        if ball.xcor()>330 or ball.xcor()<-330:
            ball.dx*=-1
        if ball.ycor()<-270 or ball.ycor()>270:
            ball.dy*=-1

        #check for collisions with other balls
        for j in range(i+1, num_balls):
            ball_2 = balls[j]
            dist = pow(ball.xcor() - ball_2.xcor(), 2) + pow(ball.ycor() - ball_2.ycor() , 2) 
            if dist <= 300*Rad:
                #For some reason the colors are stored as tuples in the turtle thing
                #change color when getting infected
                if ball.color()[0] == colors[1] and ball_2.color()[0] == colors[0]:
                    ball_2.color(colors[1]) 
                elif ball.color()[0] == colors[0] and ball_2.color()[0] == colors[1]:
                    ball.color(colors[1]) 

                #check for imobile case:
                if Imb[i]:
                    ball_2.dx *= -1
                    ball_2.dy *= -1
                elif Imb[j]:
                    ball.dx *= -1
                    ball.dy *= -1
                else:
                    #since the masses are equal we just exchange velocities
                    dx1 = ball.dx #save v_1
                    dy1 = ball.dy 
                    ball.dx = ball_2.dx #save v_2 = u_1
                    ball.dy = ball_2.dy 
                    ball_2.dx = dx1 #save u_2 = v_1
                    ball_2.dy = dy1 

    #update tallies across times
    Num_S.append(Nums[0]) 
    Num_I.append(Nums[1]) 
    Num_R.append(Nums[2]) 

plt.plot( Num_S, color = "w") 
plt.plot( Num_I, color = "y") 
plt.plot( Num_R, color = "grey") 
ax = plt.gca()

plt.axvline(freed_time,  label='Freedom Time', color = 'r')

ax.set_facecolor('k')
plt.title('White=Sus., Yellow=Inf., Grey=Rec.')
plt.show()
    
wn.mainloop()
