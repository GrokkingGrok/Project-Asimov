# Robonomic Expansion, Human Interaction, and Calvin Design Doc

RoboTorq economies grow and shrink in direct proportion to the value of the robotic labor occurring at any given time, because that determines how much RoboTorq is minted. Simple enough.

But facilitating that growth may not be so straightforward. Obviously, it requires more Robots, but only if the ones you have are working at capacity because demand (current and/or future) is not met. It leads to this growth failure mode:

**Demand Shortage --> Torq Shortage --> RoboTorq Shortage**

It usually means that BidNet somehow priced robotic labor too low, and now there are too many goods available. There's going to be some kind of pain until balance has been restored.

Strategies to make that pain quicker include: 
- Ensure Daneel is making good recommendations to BidNet when estimating robotic labor for new Bids
- Ensure Giskard is making good decisions on TokenTorq estimation when advising on Bids
- Ensure Daneel is doing a good job at rebalancing fleet utilization
- Ensure Giskard is allocating TokenTorq properly
- amp up the wage share at BidNet.
- Be more selective about what kinds of Projects BidNet accepts
- [lower StashVault returns by loosening hoarding restrictions](https://github.com/GrokkingGrok/Project-Asimov/blob/MVP/CONTRIBUTING.md#:~:text=How%20RoboTorq%20moves,miss%20a%20pledge.), allowing excess supply to get bought up--but be mindful of the inflation that will ensue if this is done too quickly.
- Consider using the Nuclear Isaac Factor to slow down disto streams at the same time, encouraging withdrawals from StashVaults or Staking within them, hedging inflation by slowing DistoStream velocity.

This portion of the simulator will be a research gold mine. Fiat systems typically have to rely on people wanting debt to clear out bad investments, one way or another. It's too soon to tell how exactly a RoboTorq Economy might match up. Maybe someone should build a simulator to try to answer things like that?

So, have fun with all that, econ nerds. But if demand is healthy, and this is your growth failure mode:

**Fleet Capacity Shortage --> Torq Shortage --> RoboTorq Shortage**

Add bots, and you're good to go. Right?

## Not so fast

You can't just add more robots and expect the economy to jumpstart perfectly. Indeed, doing so without careful thought could be like throwing fuel on a fire when what you really need is charcoal. The rough RoboTorq equivalent of quantitative easing would be buying more bots without stopping to wonder why capacity is short.

Daneel's fleet needs to maintain a reserve of robots to smooth out spikes in current utilization via production and future demand through BidNet. This means large purchase agreements need to be planned to include batched shipments over extended periods of time. This allows the reserve pool to grow organically under each successive agreement, ensuring the price of robotic labor at BidNet doesn't plummet because 500k bots got dumped into the reserve pool overnight. These agreements are worth millions each, farmed from a variety of suppliers to drive innovation. Daneel isn't buying bots without a bulk discount. And these purchase agreements are made *long before* the current reserve is empty. 

What is the optimal reserve_fleet_ratio? Sounds like a good question for economists when they are running Asimov.

So, assuming raw material availability, it's unlikely to see a scenario where Daneel doesn't have any robots in reserve. Even still, you might run across what appears to be the following growth failure mode, regardless of how many robots he pulls from reserves:

**Fleet Capacity Shortage --> Torq Shortage --> RoboTorq Shortage**

And that's because what's *really* happening is this growth failure mode:

**TokenTorq Shortage --> Torq Shortage --> RoboTorq Shortage**

In fact, what you'd see is that the more robots you put on the production line, the worse each robot would perform! That's because there's not enough TokenTorq to go around.

If Giskard is short on TokenTorq Capacity, data centers need to be upgraded, which means upgrading a Deep Underground Military Bunker, or even building a new one!

But that's not all. Isaac needs minting backup capacity upgrades: no point in upgrading Giskard or Daneel if you can't store the damn RoboTorq. Yet another growth failure mode. That means sending Starship Data Centers to orbit.

And it takes time to get Robots, data center bunkers, and Starships funded, built, and deployed.

And everybody needs Starlink upgrades.

The bond network is engineered so that no single person or AI should have the power to expand unilaterally, except as a measure of absolute last resort to bypass a gridlock failure. 

Likewise, no single actor can hold back expansion on a whim. And some would argue that butting up against gridlocks is often where truly innovative progress is made. Taking that argument into consideration, eliminating the possibility of at least temporary gridlock isn't even desirable: it also prunes paths of innovation. 

But how is this achieved, much less funded? 

Well, first off, we're mainly dealing with machines running programs, so that makes coordination easier.

# Skins in the Game

It's not just humans with skin in the game.

Isaac will, by default, front up to half the cost of any approved UpgradeProject, or up to a default of 3% of his reserves in any given fiscal year, whichever is lower. Isaac has large currency reserves from Seed Exchanges. But he can not devote too much, as he requires a large reserve of non-RoboTorq currencies to conduct international trade and interact with governments without sending RT overseas or into a bottomless bureaucratic abyss, respectively. But this isn't the International Trade Loop or the Government Oversight and Interactions Design Doc, and Isaac's not the only AI to ante up.

Additionally, Daneel gets a cut of every BRLA for Robotic Fleet Deployment. Daneel also portions a default of 3% of his budget for UpgradeProjects.

Giskard can choose to prioritize UpgradeTokenTorqDrains during production, speeding up delivery.

And Calvin has a parked reserve, built up over time due to overminting from past upgrades, that can be used to fund simulations and debug studies.

Oh, that's right, we haven't talked about Calvin yet. 

Calvin is named after Susan Calvin, the human psychologist for robots from Asimov's work. Here, Calvin is the human representative mechanism of the bond network, among other roles. And humans vote with their RoboTorq on things like economic expansion efforts.

# What exactly does Calvin do?

Before we go any further, let's be clear that the following is **not** presented as an ideal solution, merely a functional one. Remember, the whole point of building this simulator in the first place is to generate as big a set of as close to empirical data as possible for the explicit purpose of studying and answering such optimization questions!

The following is also not how *this* simulation will work. It's the process this simulation will *model*. So with that out of the way...

Calvin is how humans interact with the system, yes, but she has a lot of work to do to get to that point. She (and her digital army of GhostNodes) is the network's forecaster, debugger, voting system, and, for lack of a better term, propaganda wing.

- Forecasting: She will be key in determining expansion decisions by evaluating massive sets of simulation data.
  - She maintains a master network simulation framework for making economic decisions.
    - The model uses historical averages for most data,
    - but any parameter or parameter set can be overridden.
- Debugging: Her GhostNodes attach to any node and monitor all traffic in and out, collecting data.
  - Activating Calvin's debug mode: If --debug is passed to the simulator, Calvin's Parameter File is read, and individual nodes can be easily targeted for verbose logging output as specified within the file schema.
- Voting: She acts as the system's own version of RoboFund, maintaining Funnels and acting as escrow for system upgrades as funds are collected that will be leveraged for these projects.
- Propaganda: She is responsible for communicating the reasoning provided by the other actors for the upgrade request being voted on, as well as the progress toward funded requests.

## The General Idea in a "real" RoboTorq Economy

Let's say Isaac needs more minting backup capacity. It starts when an internal audit raises a flag alerting him, "Possible backup blockchain capacity shortage in 24 months at current minting schedule, +- 5% error." That's about 730 steps, for anyone counting. He needs 12 months (365 standard steps) to prepare a Starship Data Center launch on the long side, so he starts planning.

The first thing he does is alert Calvin. Calvin will check Daneel's and Giskard's data, plug those values into her forecast model in a variety of separate simulation runs (think Monte Carlo, Bayesian, ABM, Game Theory, etc) for each actor's data, and combinations of the two, and send the results back to Isaac. If most forecasts still indicate a need for expansion, he'll request an upgrade and evaluation proceeds.

If the Option 1 voting fails, Option 2 goes into effect, described later.

In our sim, we'll assume Option 1 passes about 75% of the time by default (normal distribution), with 25% going to Option 2. This value will, of course, be tunable in the appropriate parameter file.

Let's look at Option 1 first.

## Option 1: More Simulations, Voting, and Funding
Let's say he makes the request. Giskard and Daneel will consider his request, but they need more data. 

The next phase involves Calvin simulating what would have to go wrong for the investment to cause problems. How much of a drop in production would cause a shortfall? How likely is it? etc. 

We're **not** spinning up recursive Robonomics sims. We'll have random pass rates with a normal distribution, tunable in parameters. Economists can extend the functionality and complicate those decisions as much as they want and write papers about that, too.

What Asimov should do someday, when an LLM is integrated, is train that LLM to analyze sim data and make decisions. But that's far down the road.

But the AIs don't have the only say: Calvin is the human window into the network. And they're the ones who have to fund the upgrade.

Calvin launches a campaign educating every Bondholder of the situation. 

Imagine it: Popups, which have to be annoyingly cleared every time you open your wallet. Uncanny, AI-generated images and videos, asking for your Upgrade Pledge, are on blast on every screen, and you start to feel the propagandAI fatigue. 

Maybe you don't vote out of resentment for the annoyance. Maybe, Isaac withholds your Disto until you do.

Eventually, the public votes, by deciding to send RoboTorq into Calvin's UpgradeFunnel for the expansion—or not.

Again, the possibilities for study here are nearly endless. Should RoboTorq voting be capped to prevent Elon from funding every UpgradeFunnel that involves a Starship? Should this vote be augmented with some other kind of voting? Should the system mint an AltCoin of some type for these votes, that people can only earn through following the system's incentives? What would those incentives be? Does Elon bribe Bondholders to pledge AltCoin with free Grok access if whaling is outlawed? Is the truth that we'd need the whales to expand, given the anti-fiat nature of RoboTorq? The questions just keep flowing, and they're all impossible to answer as of right now!

So, we'll keep it simple (and extendable for those economists) in Asimov. If an UpgradeFunnel gets filled, Calvin's vote is a yes. And Giskard and Daneel vote as well based on some kind of schema check, or straight probability. 

This prevents any one AI from being able to hold back expansions that the rest of the network wants. But what if both Giskard and Daneel are flagging this as a bad decision?

# Option 2: Debug

Why are Giskard and Daneel insistent that the investment in Isaac's mint is a bad call? Do they know something that Calvin doesn't? Who is wrong?

This is Calvin's debugging role. Either her simulations are wrong or they are, and the survival of the RoboTorq economy may depend on resolving this conflict.

For now, this method will wait a random number of steps before doing another round of Option 1 with a higher chance of passing. That process repeats until the votes pass.

But in later versions of Asimov, we should model Calvin's GhostNodes spinning up, tracking data in and out of various key nodes, and feed that data to the hypothetical connected LLM to make decisions in real simulation-time.

Maybe Calvin is wrong, and other issues need to be addressed before the expansion happens. The debugging studies are used to diagnose those prerequisite fixes. If an upgrade is required, she'll spin up a campaign and UpgradeFunnel for the prereq, explaining why the additional upgrade is necessary. 

Once the debugging is done, and Calvin has new simulations or other data that explains the discrepancy, or the economic outlook has changed and there's new data to consider, another round of evaluation and voting begins.

# Gridlock

What if this process never ends, Isaac runs out of minting capacity, and the economy stalls? Obviously, a bug in some software can't be allowed to crash a whole economy.

The nuclear option in this case is allowing a Calvin-authorized official limited control of the system to authorize the upgrade. This situation will be avoided in default simulations. 

However, extending experimental functionality would be as simple as defining a new actor, defining its Flow Loops, and adding an if statement to whichever flow or node's tick/step function you want to spawn the flow. What should this control look like? Who should get it? How long should it last? Maybe you're the one to design the sim, write the paper, start the conversation. Maybe we'll find out someday.

Society must not treat the Bond Network like a God. It is designed to serve humans, recognizing that we don't always know what's best for us, but neither do AIs.

# Financing Approved Expansions

Let's assume for the simulation's sake that the probabilities have been tuned to work smoothly: After a few rounds of studies, nearly every upgrade gets fueled, with only a few taking more than 60 steps, and if the economy collapses, well, there's your data. This is a reasonable general requirement for the MVP.

The key factor of this upgrade process that needs to be modeled is that people must ultimately decide to fund the expansions themselves and then carry through with that funding. The AIs are there to help guide the process to better outcomes, even if they take a little longer to make that better decision, but not hinder progress toward resolution with red tape.

So Calvin sets up the UpgradeFunnels and launches the well-intended propaganda campaign, and Bondholder UpgradePledges start funneling in—Enterprises Bid on the UpgradeProjects. 

You should know the [general drill by now](https://github.com/GrokkingGrok/Project-Asimov/blob/MVP/CONTRIBUTING.md#systemic-actors-and-their-interactions-in-detail-ideal-simulation-behavior), but this one has some Upgrade bling:
  - The UpgradeProjects become UpgradeBRLAs,
  - Giskard allocates TokenTorq
  - Daneel deploys bots
  - Giskard opens TokenTorqDrains
  - Robots mine Torq from TokenTorq
  - Robots process UpgradeOracles to build and launch a new Starship Data Center.
  - Robots open TorqFountains as Oracles are fulfilled along the way.
  - The UpgradeBRLA fires off UpgradeMintRequest darts to Issac.
  - Isaac mints RoboTorq according to the torq_timeline in the UpgradeMintRequest
  - Bondholders receive their DistoStreams
  - DistoStreams get diverted to Calvin's UpgradeFunnels as UpgradePledges
  - UpgradeFunnels continue to fund the UpgradeBRLA, spawning more RoboTorq, etc.

This will need to be studied carefully to understand how much Torq should be applied to UpgradeOracles in this process. Oracles processed under this scheme may need to have special wage_share rates to avoid inflationary pressure. Again, another opportunity for many papers from Economists. I suspect upgrades will be one of the most studied aspects of this monetary system.

A straightforward possibility for hedging inflation in this sim is to allocate a portion of every UpgradeMintRequest to Calvin, and those funds are fully parked until the next time Calvin is called upon, which is likely how Isaac will handle such an occurrence if undue inflation is observed in early runs. 

## Robonomic Expansion Parameters

This table compiles all parameters explicitly or implicitly referenced in this document, considered likely subjects of future study, if not future Asimov Parameters. 

Definitions are in plain English, pseudocode shows basic implementation (e.g., as variables or functions), sample values are reasonable defaults based on context, and explanations describe what the sample implies for simulation behavior. Parameters are grouped by section for clarity.

| Parameter | Definition (English) | Pseudocode | Sample Value | Explanation of Sample Value |
|-----------|----------------------|------------|--------------|-----------------------------|
| **forecast_horizon_steps** | Number of simulation steps ahead for predicting capacity shortages (e.g., 24 months). | `forecast_horizon_steps = 730  # 24 months * ~30.4 days/month` | 730 | Indicates a 24-month lookahead; shortages flagged here trigger early planning, allowing ~50% buffer for builds (e.g., 365-step prep), preventing last-minute crises in stable economies. |
| **build_time_steps** | Steps required to prepare and deploy infrastructure like Starship Data Centers (e.g., 12 months). | `build_time_steps = 365  # 12 months * ~30.4 days/month` | 365 | Represents a 12-month build cycle; if exceeded by delays, it could cause minting stalls, modeling supply chain risks in high-growth scenarios. |
| **option1_pass_rate** | Probability that Option 1 (initial voting) succeeds, following a normal distribution. | `option1_pass_rate ~ normal(mean=0.75, sd=0.1)  # Tunable in params file` | 0.75 | Suggests a baseline optimistic governance; 75% pass rate means most upgrades proceed quickly, but 25% trigger debugging, simulating moderate AI-human friction without frequent gridlock. |
| **debug_delay_steps** | Random steps to wait before retrying Option 1 in debug mode, increasing pass chance. | `debug_delay_steps = random.randint(3, 10)  # Increment pass_rate by 0.05 per retry` | 5 | Models a short debug cycle (e.g., 5 steps ~ few days); quick resolution indicates efficient diagnostics, but longer values test prolonged conflicts, revealing economy stall thresholds. |
| **inflation_hedge_rate** | Portion of UpgradeMintRequest allocated to Calvin and parked to counter inflation. | `inflation_hedge_rate = 0.10  # Applied if inflation > undue_threshold` | 0.10 | Allocates 10% to reserves; this hedges moderate inflation (e.g., from upgrades), stabilizing early runs but potentially slowing growth if over-parked, ideal for testing monetary policy tradeoffs. |
| **undue_inflation_threshold** | Inflation rate triggering the hedge mechanism in early simulations. | `undue_inflation_threshold = 0.02  # If observed_inflation > threshold, activate hedge` | 0.02 | Flags 2%+ inflation as "undue"; low threshold ensures proactive stability in volatile sims, but higher values allow riskier growth, modeling conservative vs. aggressive economies. |
| **max_gridlock_steps** | Maximum steps before nuclear option or forced resolution in stalled processes. | `max_gridlock_steps = 60  # If exceeded, escalate or fail` | 60 | Caps gridlock at ~2 months; prevents infinite loops in sims, but short caps force human intervention often, testing sovereignty erosion; longer values emphasize AI autonomy. |
| **whale_cap_threshold** | Maximum RoboTorq an individual (e.g., Elon) can pledge to prevent dominance. | `whale_cap_threshold = 0.05 * total_torq  # Cap as % of total supply` | 0.05 | Limits whales to 5% influence; promotes equity in voting, reducing "Elon funds everything" scenarios, but if too low, slows funding for big projects like Starships. |
| **altcoin_earn_rate** | Rate at which users earn AltCoins for votes by following system incentives. | `altcoin_earn_rate = 0.01 * oracle_completion  # 1% per fulfilled task` | 0.01 | Earns 1% AltCoin per task; incentivizes participation without fiat, but low rates test engagement decay; higher values could inflate AltCoins, modeling reward dilution. |
| **bribe_influence_weight** | Weight of non-monetary bribes (e.g., Grok access) in swaying pledges. | `bribe_influence_weight = 0.5  # Multiplier on pledge probability` | 0.5 | Halves bribe effectiveness; moderates "Elon bribes with Grok" scenarios, ensuring monetary votes dominate; 1.0 weight simulates unchecked influence, testing oligarchy risks. |
| **anti_fiat_premium** | Premium factor rewarding non-fiat behaviors in AltCoin earning/voting. | `anti_fiat_premium = 1.2  # Boost for rule-following pledges` | 1.2 | Gives 20% boost for "system incentives"; reinforces anti-fiat nature, encouraging organic growth; lower premiums test if whales are "needed," as per questions. |
| **nuclear_scope** | Scope of governmental override (e.g., local vs. global) in gridlock. | `nuclear_scope = ['local', 'federal', 'global']  # Enum for escalation` | 'federal' | Limits to federal level; balances intervention without overreach, modeling subsidiarity; 'global' indicates high-stakes crises, testing international coordination. |
| **nuclear_authority** | Entity granted nuclear control (e.g., official type). | `nuclear_authority = ['official', 'panel', 'AI-assisted']  # Tunable enum` | 'panel' | Assigns to a panel; distributes power, reducing abuse risk; 'official' tests single-point failure, while 'AI-assisted' explores hybrid human-AI overrides. |
| **nuclear_duration** | Steps nuclear control lasts before reverting to normal. | `nuclear_duration = 30  # Steps post-activation` | 30 | Lasts ~1 month; short duration prevents entrenchment, but if too brief, risks repeat gridlock; longer tests "temporary" power creep. |
| **discrepancy_threshold** | Threshold for flagging forecast vs. actual mismatches in debugging. | `discrepancy_threshold = 0.15  # If abs(forecast - actual) > threshold, escalate` | 0.15 | Flags 15%+ mismatches; sensitive enough for early detection without noise; higher thresholds delay debugs, modeling tolerance for uncertainty in economies. |
| **voting_scheme_id** | ID selecting voting mode (simple, capped, AltCoin, etc.). | `voting_scheme_id = [1, 2, 3]  # 1=simple Torq, 2=capped, 3=AltCoin` | 1 | Defaults to simple Torq-voting; easy baseline for MVP, but switching to 3 tests incentive designs, revealing if "earned" votes reduce whale dominance. |
| **ai_vote_mode** | Mode for AI votes (schema check or probabilistic). | `ai_vote_mode = ['schema', 'probabilistic']  # Enum` | 'probabilistic' | Uses probability; introduces AI "uncertainty," modeling non-deterministic governance; 'schema' ensures rule-based consistency, testing rigidity vs. flexibility. |
| **campaign_decay_rate** | Rate at which campaign notifications reduce participation over time. | `campaign_decay_rate = 0.05 / wallet_open  # 5% drop per ignored prompt` | 0.05 | Decays engagement 5% per wallet open; simulates fatigue, where prolonged campaigns lower turnout; lower rates test persistent propaganda effectiveness. |








