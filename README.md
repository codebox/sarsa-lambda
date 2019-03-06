# sarsa-lambda

This is a Python implementation of the SARSA &lambda; reinforcement learning algorithm. The algorithm is used to guide a player through a user-defined 'grid world' environment,
inhabited by Hungry Ghosts. Progress can be monitored via the built-in web interface, which continuously runs games
using the latest strategy learnt by the algorithm.

The algorithm's objective is to obtain the highest possible score for the player. The player's score is increased by discovering the exit from the environment, and is decreased slightly with each move
that is made. A large negative penalty is applied if the player is caught by one of the ghosts before escaping. The game finishes when
the player reaches an exit, or is caught by a ghost. The rewards/penalties associated with each of these
events are [easily configurable](https://github.com/codebox/sarsa-lambda/blob/master/environment.py#L16).

The video below shows the algorithm's progress learning a very basic (ghost-free) environment. During the first few games the
player's moves are essentially random, however after playing about 100 games the player begins to take a reasonably direct route
to the exit. After 1000 games the algorithm has discovered an optimal route.

[![Watch the video](https://codebox.net/assets/video/reinforcement-learning-sarsa-lambda/sarsa_blank_poster.png)](https://codebox.net/assets/video/reinforcement-learning-sarsa-lambda/sarsa_blank.webm)

As would be expected, when tested against more complex environments the algorithm takes much longer to discover the best strategy
(10s or 100s of thousands of games). In some cases quite ingenious tactics are employed to evade the ghosts, for example
waiting in one location to draw the ghosts down a particular path, before taking a different route towards the exit:

[![Watch the video](https://codebox.net/assets/video/reinforcement-learning-sarsa-lambda/sarsa_ghosts_poster.png)](https://codebox.net/assets/video/reinforcement-learning-sarsa-lambda/sarsa_ghosts.webm)

To run the code for yourself just clone the project,
draw your own map [in the main.py file](https://github.com/codebox/sarsa-lambda/blob/master/main.py#L15), and
use the following command to let the algorithm start learning:

```
python main.py
```

Progress is saved/resumed automatically. Use Ctrl-C to stop the application, next time the code is run it will
continue from where it left off. In order to monitor progress you can start the web interface like this:

```
python web_server.py
```

and then [watch the games in your web browser](http://localhost:8080) as they run.

