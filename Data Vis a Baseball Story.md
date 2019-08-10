# Data Visualization in Tableau: A Baseball Story

Initial Version:

Final Version: 

## **Summary**

The story shows the relationship of attributes to performance for a group of major league baseball (MLB) players. Using 1,157 player's attributes of height (in inches) and weight (in pounds), and thier statistics for batting average, and home runs the visualizations show there is no advantage for a taller heavier player to perform better.

 A batting average in baseball is a number that represents hits per official time at bat. At the highest levels of baseball, a .300 batting average is considered very good, .350 is exceptional, the combined average for all players is roughly .250 to .270.

A home run ( HR) is ***scored ***when the ball is hit in such a way that the batter is able to circle the bases and reach home safely in one play.  

## **Design**

Exploring the dataset lead me to the question that would be the star of my story:  Does a players mass affect performance?

To show the answer to the question I created various charts looking at weight and height to HRs and batting averages. I chose to ignore the handedness since it does not contribute to my analysis.

To compare physical attributes to performance averages I chose to use a scatter plots based on the information from https://www.perceptualedge.com/articles/ie/the_right_graph.pdf

I chose a bubble chart to show the home runs per height, weight. I like the look and it shows values nicely. 

I created a couple of sets to filter the top players and I chose dual bar graphs to show metrics for the top 30 hitters by weight/HR chart and seprate one for the top 30 hitters by height/HR chart. I add tooltips and allow for a selected player to be highlighted.

I selected the charts for the initial story and placed them in an order sequence.

###### Redesign

I shared my results with 2 people and I *redesigned * the story based on the feedback. During the redesign I asked for feedback through out the process.

I created a measure named BMI for the height to weight ratio using the formula [Weight] / SQUARE([Height]) * 703

I chose to use BMI instead of height and weight which were previously presented individually on charts. 

Using BMI made for a less cluttered, easier to understand presentation. 

I changed the orange bubble chart to be a blue line chart but the imeddiate feedback was that it looked like scribbles.  I removed the chart altogether since it really didn't provide new or different information.

I made used constant colors for the metrics in each chart, so each metrics can easily be identified. BMI is always purple HR is green and batting average is blue.

Due to more feedback I created  metric for height in feet which is height / 12 

I created a dual bar graph to show the top 30 hitters by BMI/Home Runs. This chart has tooltips and allow for a selected player to be highlighted.

The final story was well received.

## **Feedback**

Story 1 was shared with 2 people who were presented with the following questions:

- Do you understand the main point of the visualization?
- Do you have questions about the data?
- Do you have any suggestions for improvements?

Reviewer 1: 

There are too many charts, the 2nd chart was a little confusing at first. There's too much orange on this chart (Weight to Batting Average) and most of the data cluster is outside of the average line, shouldn't the cluster be on the average line?

Otherwise this is a very interesting presentation

Reviewer 2:

The font is small and I don't like the last chart with the orange, it's confusing. All the other colors are nice. But this is very interesting, it made me think about the players in a way I previously have not. Good job.

###### Intermittent feedback on story 2

Reviewer 2: Could you convert height to feet for easier reading?

Reviewer 1: The 1st story has height in inches while graph has feet.

###### ReReview

Story2 was presented with changes inspired from the earlier feedback

Reviewer 1:  I like it, it has a good feel and supports the finding. Good job.

Reviewer 2: This is very nice, it quickly proves the point. Good job.

## Findings

The average player has a height of aprox. 6" with an average weight of 184.5 pounds

Reggie Jackson and Mike Schmidt are of average height and both weight 195 pounds. Both out perform all other players in the dataset with home runs/batting averages of 563 /.262 and 548 / .267 respectively.

The average player has a batting average of .216 and a home run average of 45.

The visualizations show a players physical attributes do not equate to improved performance. 

## Resouces

https://www.wisegeek.com/in-baseball-what-is-a-batting-average.htm

https://en.wikipedia.org/wiki/Home_run

[https://www.perceptualedge.com/articles/ie/the_right_graph.pdf](https://www.perceptualedge.com/articles/ie/the_right_graph.pdf)

https://www.cancer.gov/publications/dictionaries/cancer-terms/def/bmi
