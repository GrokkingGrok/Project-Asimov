# TorqMining Flow Loop Design and Logic

The Torq Mining Flow Loop is where production happens and value is created.

Let's start out with our definitions of TokenTorq, torq_mining_rate, and Torq:
	- TokenTorq: A standardized constraint of how much compute a given robot can wield at any given time, relative to the total compute consumption of the Bond Network, as measured in kWh/token.
	- torq_mining_rate: The rate at which a robot can effectively use TokenTorq to create economic value, as measured in tokens/kWh.
	- Torq: A unitless scalar achieved by multiplying TokenTorq * torq_mining_rate (kWh/token * tokens/kWh = no units)

And picking up [where we left off in TokenTorqTrainingLoop.md](https://github.com/GrokkingGrok/Project-Asimov/blob/MVP/design/src/asimov/flow/TokenTorqTrainingLoop.md):
- Every TorqFountain.tick():
  - The Robot mines its TokenTorq into Torq with varying efficiency (representing production taking place).
    - The more efficiently it mines TokenTorq, the faster Robot.torq increases.
  - Several factors influence TokenTorq --> Torq conversion.
    - The more a robot has done the same task, the more efficiently it mines TokenTorq.
    - The type of task also influences how Torq is mined.
      - Complex tasks draw TokenTorq from Giskard at a higher rate, but mine slowly when production starts, and then produce lots of torq by the end.
      - Simple tasks draw less TokenTorq, but have flatter Torq curves.
    - The lower Giskard.tick_rate, the harder the robot has to work to mine Torq, the more Torq it produces per unit TokenTorq, but less Torq overall.

And then we hammered out the implications of TokenTorq --> Torq conversion: How it affects [Robonomic Expansion, Calvin, and the rest of the system](https://github.com/GrokkingGrok/Project-Asimov/blob/MVP/design/src/RobonomicExpansion.md).

Let's break down the Torq itself.

# Torq as a Measure of Economic Leverage

Torq is a unitless scaling factor. Remember, Enterprises pay for Oracle processed by the Robots contracted to them through a BRLA. So, let's say Conglomocorp pays 10 RT for an Oracle.

Let's also say the Robot assigned to that Oracle just spawned its TorqFountain because it's fully trained by the end of Robot.step(), and Robonomics.tick() has been called.

- 
