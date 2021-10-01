Traffic

Firstly, I began building the code based on the source code provided by the lecture. This code used 1 convolutional layer (learning 32 filters using a 3x3 kernel), 1 max-pooling layer (using a 2x2 pool size), 1 hidden layer with 128 nodes, a 0.5 dropout rate, and an output layer with output units for all traffic sign categories. This model performed poorly, with an accuracy of 0.0544. 

I altered this base layer by adding another convulational layer identical to the first, adding a second maxpooling layer identical to the first (after the second convulational layer), adding a hidden layer. This increased the accuracy of the reformed moel to 0.9870 with 0.1048 loss. For experimentation, I also tested decreasing the dropout rate to 0.3, which decreased the model's accuracy to 0.9845, then I increased the dropout rate to 0.6, which decreased the accuracy to 0.9747. From this, I ascertained to keep the dropout rate at 0.5.
