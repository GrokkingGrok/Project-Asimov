# The Equation of AI Exchange and the TorqMining Flow Loop Design Doc

The Torq Mining Flow Loop is where production happens and value is created.

Let's start out with our definitions of TokenTorq, torq_mining_rate, and Torq:
	- TokenTorq: A standardized constraint of how much compute a given robot can wield at any given time, 
		- relative to the total compute consumption of the Bond Network, 
		- as measured in kWh/token.
	- torq_factor: The rate at which a robot can use TokenTorq to create economic value, 
		- as measured in tokens/kWh, 
		- based largely on Enterprise.torq_gamble. 
		- Intriguing, right? Patience.
	- Torq: A unitless scalar achieved by multiplying TokenTorq * torq_factor (kWh/token * tokens/kWh = no units)

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

Torq is a unitless scaling factor. Remember, Enterprises pay per Oracle processed by the Robots contracted to them through a BRLA. So, let's say Conglomocorp pays 10 RT for an Oracle.

Let's also say the Robot assigned to that Oracle just spawned its TorqFountain because it's fully trained by the end of Robot.step(), and Robonomics.tick() has been called.

And furthermore, let's assume that Robot.mine_torq() has been called. What needs to happen? Well, we need to have a basic formula for calculating Torq, for starters.

## Wrench in the Works

In order to calculate Torq, we need to know what torq_factor is because: 

`Torq = TokenTorq * torq_factor`

But we can't know what that is until we know what torq_gamble is, because:

`torq_factor = (1/(1-e^(-r * Robot.current.util)) - 0.5) * torq_gamble`

Well, you probably don't understand where that just came from. But that's ok, all you need to know for now is that it's a standard Sigmoid machine learning function, and that you need to know torq_gamble to calculate torq_factor. 

torq_gamble is a value agreed upon by the Enterprise and BidNet at the time of accepting the Bid for this BRLA.

It represents the value added due to production. It is how the Enterprise makes its wager on how much it will be able to sell the final item for.

`torq_gamble = (brla_retainer_fee / Oracle.robot_pool_size + other production costs + overhead) * markup 

Now that we have torq_factor and torq_gamble, we can calculate torq_mined... Once we have a formula for it, at least.

For the Math Nerds in the... front row of the class, probably, I give you:

# The Equation of AI Exchange in Robot.mine_torq()

For Asimov's MVP (and to entice researchers to fork and extend it), it will include simple yet elegantly effective mathematical definitions. It will be easy for future researchers to modify the logic of Robot.mine_torq() using any statistical model and inputs they please.

The basic Equation of AI Exchange formula is simple: 
	- `torq_mined = token_torq_consumed * torq_factor`, 

where:
	- `torq_factor = (1/(1-e^(-ticks * Robot.current.util)) - 0.5) * torq_gamble`

Simple, right? Ok maybe not, that's a whole lotta torq flying around. 

And, where:
	- `token_torq_consumed = TokenTork_available * efficiencies * Robot.current_util`

And, where:
	- `token_torq_available = Giskard.tick_rate + Robot.token_torq`

And, where:` efficiencies = robot.base_efficiency + energy_efficiency * supply_efficiency * x_efficiency * y_efficiency ...`

Once you've done that each call to Robot.mine_torq(), just be sure to 
	- decrement `Robot.token_torq -= TokenTorq_consumed`
	- increase `Oracle.torq
	- decrease `Oracle.production_remaining *= (1 - Robot.current_util * efficiencies)`

Obviously, this could get insanely complex. Economists, roboticists, data scientists, and more will have a field day modifying logic, crunching Asimov output, and publishing on it for years to come, no doubt.

## Finer Points of the Torq efficiency losses (or gains, depending on your perspective) in the Equation of AI Exchange


- Supply Efficiency: Are raw materials being delivered in the expected state?
	- Simple tasks: assume normal distribution with higher average, lower variance
 	- Complex tasks: normal, lower average, higher variance
- More efficiency models can be added at will to model different situations.

So that's how we calculate Torq. 

Now I know what you might thinking: "But, that means that companies get to ask for how much money they want to be created!" Well, yeah.

What do you think happens when a business takes out a loan now?

## But why wouldn't Enterprises just bid low torq_gambles, and price high?

Of course! I hadn't thought of that... Except, come to think of it, what exactly would they gain from such a thing, and how exactly would they do it?

While we haven't quite got there yet, the cost of a BRLA isn't a function of the torq_factor. Sure, it's considered, but it's more of a negotiating point than a function.

And think about what it *really* means... Like we discussed, the torq_factor is going to largely determine how much actual RoboTorq is printed.

**This is the money that the Enterprise's customers need minted for there to be enough RoboTorq to fund the purchase without disturbing the overall circulating money supply.**

Really, we should be more worried about companies bidding high and pricing low so that there is more RoboTorq to chase their goods, making it easier to sell. If Isaac undermints, there will be too few RoboTorq to chase the Enterprise's goods.

So they're not going to be unduly penalized in terms of the cost of a given BRLA. At least, not during that BRLA. But the system will be keeping track.

If an Enterprise is either bad at estimating torq_factor, or they are insistent on trying to game their torq_factor in some way, they'll face much stiffer negotiating tactics at BidNet, and their RoboFund Funnels will alert bondholders. Repeated infractions could result in being kicked off RoboFund, being required to rely on more expensive financing from TorqVaults.

So it's that Enterprise's ability to scheme against a network of AI financial overlords. Should be interesting.

















