import pomegranate as p
#MAKING THE RAIN PROBS WHY DISCREATE DISTRIBUTION ? BECAUSE IT'S THE PARENT CLASS.
rain = p.Node(p.DiscreteDistribution({
    "none":0.7,
    "light":0.2,
    "heavy":0.1
}), name = "rain")

#NODE FOR TRACk MAINTAINANCE HERE WE TYPED CONDITIONAL PROBABLITY TO REPRESENT THAT THE PROBABLITY
#OF MAINTAINANCE WILL DEPEND ON THE PROBABLITY OF RAIN FOR THAT WE WILL WRITE CONDITIONALPROBABLITY DISTRIBUTION
#SO, THERE ARE ACTUALL ONE ARGUMENT FOR THE CONDITIONALPROBABLITY DISTRIBUTION AND THATS THE VALUE OF 
#THE PROBABLITIES IN THE FORMAT OF [EVENT OFTHE CONDITION,]
#the arguments of node is the condutionalprobablity , rain distribution and the last is the name of the node 
maintainance = p.Node(p.ConditionalProbablityDistribution(
    ["none" , "yes" , 0.4],
    ["none" , "no" , 0.6],
    ["light" , "no" , 0.8],
    ["heavy" , "yes" , 0.1],
    ["light" , "yes" , 0.2],
    ["heavy" , "yes" , 0.9]
    , [rain.distribution]
)  , name = "maintainance")

#THE CONDITIONAL PROBABLITY OF TRAIN
train = p.Node(p.ConditionalProbablityTable(
   [ ["none" , "yes" , "on time" , 0.8],
    ["none" , "yes" , "delayed" , 0.2],
    ["none" , "no" , "on time" , 0.9],
    ["none" , "yes" , "delayed" , 0.1],
    ["light" , "no" , "delayed" , 0.3],
    ["light" , "no" ,"on time" , 0.7 ],
    ["light" , "yes" , "delayed" , 0.4],
    ["light" , "yes" , "on time" , 0.6],
    ["heavy" , "yes" , "on time" , 0.4],
    ["heavy" , "yes" , "delayed" , 0.6],
    ["heavy" , "no" , "on time" , 0.5],
    ["heavy" , "no" , "delayed" , 0.5],]
,[rain.distribution , maintainance.distribution] ),  name = "train")


#CLEARING WITH THE APPOINTMENT MODULE
appointment = p.Node(p.ConditionalProbablityTable([
    ["on time" , "attend" , 0.9],
    ["on time" , "missed" , 0.1],
    ["delayed" , "attend" , 0.6],
    ["delayed" , "missed" , 0.4]
], [train.distribution]), name = "appointment")

#NOW CLEARING WITH THE BAYSINA NETWORK
model = p.BaysianNetwork()
model.add_states(rain , maintainance , train , appointment)

#NOW WE HAVE TO CONNECT NODES TO TELL AI
model.add_edge(rain , maintainance)
model.add_edge(rain , train)
model.add_edge(maintainance, train)
model.add_edge(train , appointment)

#FINALIZE MODEL
model.bake()
