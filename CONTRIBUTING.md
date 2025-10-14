# System Architecture Guide for Contributors
If you're thinking of contributing or if you already are contributing and need a refresher, this is where you can get the nitty-gritty details on the Asimov system architecture.

As the official design document, this is the One Source of Truth. If it's not here, it's not yet Project-Asimov canon. If you think something in this document contradicts itself, please raise a docs issue on our [Issues Board](https://github.com/GrokkingGrok/Project-Asimov/issues) before you do anything else and forget. When writing new documentation or code, check here to better understand how your feature fits into the grand scheme of things. When you're done, submit an issue if this doc, README.md, or any other doc in this repo needs to be updated.

Quick point of clarification: "Asimov" refers to the Python Package. "Project-Asimov" is the open source effort to create "Asimov". `Robonomics.py` is the Python class that contains an entire Robonomic/RoboTorq Economy. We'll be doing lots of defining in this document.

Let's start with the basics. Project-Asimov runs on Python 3.13. 
  * Not the fastest, but dependable and readable. And about the speed...
  * Various Python 3.13 ops speed up 10x-100x using `Polars DataFrames`, which we do. Not familiar with Polars?
    * The awesome [YouTuber Mariya Sha of Python Simplified has a great Polars intro video](https://www.youtube.com/watch?v=8GoBlwgbirE)

## Overview
Simulating any economy in a pseudo-realistic fashion requires modeling a massive, nearly infinitely tangled web of interactions... Oof, sounds complicated. Maybe it will get better?

Naturally, we'll need to name *all* the parts of this simulated economy to discuss it in any meaningful way, much more so to code it!

The `economy` is a complex data structure known as a `graph`, `actors` are `nodes` in the `graph`, and `flow` are `edges` that... OK, well, that was even worse. Let's try this another way.

## Robonomics Lingo Really Does Help Simplify Things

...once you understand a few basic terms. Thankfully, you have this guide. It helps if you think of this like a video game world. `actors` are the characters, and `flows` are the things they can do.

**Two Steps Back**
  * `flow` describes the act of moving something from one `actor` to another.
    * Each `flow` only goes one way.
    * If that same something needs to move back where it came from, it needs to travel along a different `flow`.
  * `actors` are, in the most general sense, what store the things `flow` into, through, and out of.
  * `actors` also store a large `schema` of attributes that help decide:
    * What is allowed to `flow` into and out of them,
    * At what rates the `flow` may occur, and
    * Under which market conditions the `flow` and rate may occur, etc.
  * Examples of the types of `flow` you'll find are Credits (RoboTorq transactions), Requests (payment requests), Inventory (sale of goods), TokenTorq (info related to AI capacity), Oracle Data (related to production), etc.
  * You'll find the classes that define different instances of `flow` under `src/asimov/flow/`

The naming conventions are designed to distance conversation from the underlying data structures through abstraction, allowing anyone to discuss the simulation without understanding computer science jargon. Let's use the three terms we've already defined in an example.
  * Example: Every ``Bondholder`` is connected to ``Isaac`` via a persistent *DistoStream* ``flow``.

There is a *lot* of information encoded in that sentence.

Let's unpack what that means in more exact terms, so you can see how the abstraction focuses on WHAT the data represents, rather than HOW the underlying data structure gets the job done.
  * A ``Bondholder`` owns at least one ``Bond`` signifying shared ownership of a humanoid ``Robot``.
  * ``Isaac`` is the ``node`` that mints and distributes ``RoboTorq`` to ``Bondholder`` ``nodes``, which happens via a ``edge`` that connects each ``node``.
  * A *DistoStream* is the specific type of graph ``edge`` connecting the two ``nodes``, we call any ``edge`` a ``flow``.
  * It is "persistent" because this particular `flow` will last longer than one cycle of the simulation.

## Other Key Terms & Data Structures

From here, we can start defining key terms more readily.
  * ``Registries`` like `BondholderRegistry` (a Polar DataFrame for storing attributes of every node) and `EnterpriseRegistry` (for enterprises).
  * ``Models`` map ``Registries`` to the ``Economy``'s graph structure. Every data structure inside the simulation can interact with each other through this class: ``src/asimov/models/robonomics.py``
  * ``Oracles`` track the activity of `Robots` as they produce.
  * ``RoboTorq`` is the currency itself, backed by the realized productive output of the Bond Network's fleet as a whole.
  * ``Torq`` is a metric used to help in internal `Oracle` and `Production` auditing/tracking, as well as the valuation of production.
  * ``TokenTorq`` is almost like an internal exchange rate, used to quantify the AI requirements of robotic production within the `Torq` measurement process, assisting with the valuation of RoboTorq.

## Systemic Actors and Their Interactions in Detail (Ideal Simulation Behavior)
A hypothetical "real" RoboTorq Economy would have several AI actors managing the various subsystems, allowing the ``Bondholders`` and ``Enterprises`` to interact with each other smoothly. In this section, all ``boxes that look like this`` denote ``nodes`` (i.e. ``actors`` only).
  
  **How RoboTorq Gets into the Economy**
  * ``Isaac`` is the RoboTorq Economy's AI mint and distribution hub.
  * ``Bondholders`` receive a constant trickle of RoboTorq from ``Isaac``, 24/7/365.
  * This constant trickle is called a *DistoStream* `flow` (specific instances of flows, like *DistroStream*, will be italicized when needed to separate the two ideas in this section)
  
  **How RoboTorq moves through the Economy: Spending & Investing (Saving Covered Later)**
  * ``Enterprises`` sell goods and services to ``Bondholders``.
  * ``Bondholders`` invest in ``Enterprises`` at ``RoboFund`` in lieu of a stock market.
  * ``RoboFund`` is how ``Bondholders`` invest in individual ``Projects`` that ``Enterprises`` need funding for.
  * `Bondholders` choose which `BuyerFunnels` and `MakerFunnels` to invest in, which are tied to `Projects`.

  **Investing & Commercial Financing**
  * When a `Project` is funded, it is converted to a `Bid`, to be vetted by `BidNet`.
  * If the `Bid` passes initial vetting, `BidNet` asks `Giskard` and `Daneel` for input about accepting the bid.
  * `Giskard` (pronounced discard with a 'g') provides various inputs to help `BidNet` decide whether to accept or reject `Bids`, as well as tracking TokenTorq and Torq in the economy.
  * `Daneel` also provides input to `BidNet`.
  * If `Giskard` and `Daneel` agree, `BidNet` always follows their advice.
  * If they are not in agreement, `BidNet` weighs both inputs and is the tiebreaker.
  * `Enterprises` pay brla_retainer_fee to secure `BRLA`.

  **How Production Happens**
  * `Giskard` receives the accepted `Bid` as a Bonded Robotic Labor Agreement, or `BRLA`.
  * He attaches all `Oracles` to the `BRLA`.
  * `Giskard` uses a portion of the brla_retainer_fee for the AI cost of processing `BRLA`.
  * He sends the `BRLA` to `Daneel`.
  * `Daneel's` primary job is to balance the utilization of the robotic fleet.
  * This helps to maximize the rate at which the system can purchase new robots by making smart decisions about how to allocate fleet resources.
  * `Daneel` deploys `Robots` to the `JobSite`.
  * The `BRLA` assigns `Oracles` to `Robots` for production to begin.
  * `Robots` notify the `BRLA` when an `Oracle` is fulfilled.
  
  **How RoboTorq is Recycled & Minted**
  * `Daneel` uses brla_retainer_fee to maintain the fleet.
  * `Enterprises` pay per `Oracle` fulfilled.
  * `BRLA` sends *FulfilledOracle* data to `Giskard`.
  * `Giskard` calculates `Torq` associated with `Oracle`.
  * `Giskard` sends a *MintRequest* to `Isaac`.

## From here, the whole cycle starts over again, and it gets bigger

The simulation loop repeats, propagating changes through the model via two method calls, *tick()* and *step()*:
  * Both of these methods call similarly named functions within individual `actors` and `flows`.
    * ticks are *mostly* associated with `flow`.
    * steps are *mostly* associated with `actors`.
  * 1 call to *step()* happens every X number of calls to *tick()*
    * A standard step_differential is 24: meaning 24 ticks to every step.
  * This simulates a daily cycle where ticks happen on the hour, and steps happen daily.

Let's stop and explore what this means for a moment, and see how things fit together now that we've defined how time flows in our Robonomics video game.

## Ticks of Time in Asimov

In ticks, every `flow` active at the beginning of the cycle will have its tick method called, without exception. In contrast, the vast majority of individual `actors` (Bondholders, Enterprises) do not even have a tick method to call.

AI `actors` that act as prolific generators of `flow`, like `Isaac`, do have a tick method, keeping them in sync with all of the *DistoStreams* emanating from him.

## Steps of Time in Asimov

In steps, every node in the model is activated. *In the whole model*.

This means that `actors` who currently have no connection to the RoboTorq Economy now have the opportunity to spawn their own `flow` to other `actors` at will. But only once however many step_differential ticks has been set!

`actors` currently connected to the economy have the opportunity to do things like change their spending_habits in reaction to market signals.

Then, during the next series of ticks, each `actor` behaves according to the changes made during the previous step.

At the end of every tick or step, the model prunes any completed `flows` from the economy. `actors` with no active `flows` are no longer connected, and can't proactively attempt to do so until the next step.

`flows` can still find and connect with orphaned `actors` during any tick, but `actors` can't choose to become connected until a step is called on it.

## What does all this mean for Asimov?

This keeps the graph lean and fast. This gives the user fine-grained control over how often `actors` update their behavior patterns.

Certain `actors` generate `flow`. Each `flow` starts a chain reaction of new `flows` that branch out across the RoboTorq Economy spontaneously, yet rhythmically, like pulsating blood vessels that expand and contract to the rhythm of every heartbeat, infecting new nooks and crannies of the pre-RoboTorq economy at every pass.

Scale this up to even a modest 10 `Bondholders`, 1 `Enterprise`, and 1 `Robot`, and you can see how quickly it gets unmanageably complex for a human track without careful attention to detail. We'll be going much larger.

The ultimate goal of Project-Asimov is 
  * A *bare minimum of hundreds of millions* of `Bondholders`.
  * *Tens of millions* of `Enterprises`,
  * *hundreds of millions* of `Robots`.
  * With the potential for *1-2 billion concurrent `flows`*.

This will require a large distributed computing cluster. Realistically, that won't happen until people at universities get involved, perhaps even several universities working together.

And we can't model hundreds of millions until we can model tens of millions, which requires millions, and so on down to just a single `Bondholder`.

# So Let's Start Small: A Minimally Viable Product (MVP) and Roadmap to v1.0.0

So far, you've seen a lot of big ideas, but they have to start smaller in practice. 

Two rounds of prototyping provided me with v0.2.0, using Mesa-Frames. v0.2.1 ditches Mesa-Frames. This helps clarify the MVP's Core Requirements. The MVP will be known as v0.3.0. Breaking down the above simulation loop discussion, we can arrive at the following set of MVP Core Requirements, and expand that into a Roadmap to v1.0.0. 

This list is subject to change at any time for any reason, as it gets processed into the Issues Board and MVP Project tracker.

## v0.3.0 MVP Core Requirements (10 bondholders)
  - Use GRAPE for graph management. No Polars yet.
  - Only `actors` are:
    * `Isaac`
    * `Bondholder`
    * `Enterprise`
    * `Robot`
    * `BRLA`
  - The economy will consist of 10 `Bondholders`, 1 `Enterprise`, and 1 `Robot` (robot created by BRLA when needed)
    * No new `actors` can be created.
  - Decide on logging and data collection techniques.
  - `Conglomocorp` signs a single BRLA, funded by 100,000 RoboTorq from Isaac via `SecureBRLA` flow.
  - Robots make products, with no failures or downtime.
  - Inventory is not a concern (doesn't yet exist).
  - Activate all bondholders on the first BRLA, receiving disto streams (70% spent to Conglomocorp)
  - Conglomocorp always has enough RoboTorq to pay for new Oracles (can go negative)
  - `Isaac` mints completed `Oracle` values at a flat markup and distributes immediately upon receiving *MintRequests*
  - Ensure all flows self-dissolve after their work is done (e.g., `SecureBRLA`, `SeedXfer`)
  - Runs for 10 steps at 24 ticks per step (240 ticks)
  - No UI, headless mode only

## v0.4.* Core Requirements (20 bondholders)
  - 1 `Enterprise`, 1 `Robot`
  - Parquet Parameter File for Robonomics args, but not `actors` definitions.
  - `Isaac` can measure the velocity of money.
  - Faker makes `Bondholders`?
  - Runs for 100 steps at 24 ticks per step (2,400 ticks)
  - No UI, headless mode only

## v0.5.* Core Requirements (100 bondholders)
  - 1 `Enterprise`, 1 `Robot`
  - Faker makes `Enterprise`?
  - `Daneel` creates and deploys `Robot` to `BRLA` instead of `BRLA` creating it.
  - `Robot` can have random downtime.
  - `Daneel` measures `Robot` utilization.
  - Runs for 100 steps at 24 ticks per step (2,400 ticks)
  - Consider basic Gradio UI for testing.

## v0.6.* Core Requirements (500 bondholders)
  - 1 `Enterprise`, 1 `Robot`
  - Faker or some static method makes `Robots`
  - `Conglomocorp has to renew its BRLA every 30 Steps, same terms every time.
  - `BidNet` accepts every `Bid` that comes its way from `Conglomocorp`.
  - `BidNet` converts `Bids` to `BRLAs` and hands them off to `Daneel`.
  - `BidNet` can calculate the average cost of a `BRLA`
  - `Daneel can repair `Robots`.
  - Runs for 1,000 steps at 24 ticks per step (24,000 ticks)

## v0.7.* Core Requirements (750 bondholders)
  - 1 `Enterprise`, 1 `Robot`
  - `SeedRequests` are no longer the only way `Enterprises` can join the RoboTorq Economy.
  - `RoboFund` allows `Projects` and `MakerFunnels`.
  - `RoboFund` sends fully funded projects to `BidNet` as a `Bid`.
  - `RoboFund` can calculate the average Funnel size and utilization.
  - Runs for 10,000 steps at 24 ticks per step (240,000 ticks)

## v0.8.* Core Requirements (1000 bondholders)
  - 1 `Enterprise`, 2 `Robots`
  - Parameter File Definitions complete.
  - `Daneel` can purchase new robots.
  - `BidNet` can reject `Bids`.
  - `Isaac can affect FIF `flow` (Demurrage of idle RoboTorq).
  - Initial UI dashboard - viewing only.

## v0.9.* Core Requirements (5000 bondholders)
  - 2 `Enterprise`, 2 `Robots`
  - Bondholders come from Parameter File initialization.
  - `Conglomocorp` has competition.
  - `BidNet` will only accept one bid per 30 step period of time.
  - `Giskard` receives `BRLA` after `Bidnet` accepts, but affects no change, and passes it on to `Daneel`
  - `Bondholders` buy from both `Enterprises`.
  - `Daneel` can move `Robots` between `BRLAs` to balance fleet load.
  - Interactive but limited UI dashboard with live tuning.

## v1.0.* Initial Package Release Core Requirements (up to 10,000 bondholders)
  - Up to 10k bondholders, dozens of Enterprises or more, and as many robots as `Daneel` can purchase.
  - Full Parameter File initialization.
  - Support multiple enterprises (beyond Conglomocorp) with unique BRLAs.
  - `Giskard` creates oracle chains (gathered from parameter file) and attaches them to `BRLA` before handoff to `Daneel`.
  - Enable Monte Carlo experiments on a single machine.
  - Bondholder and Enterprise behavior profiles become more complex on the road to v2.0.*
  - Saving Accounts are now an option, along with consumer financing.
  - Extensive UI dashboard with live tuning.

## v2.0.* Initial Distributed Package Release (100k-1 million bondholders)
  - Dask Integration enables runs on small networks.
  

## v3.0.* Initial Cluster Package Release (1-100 million bondholders)
  - Ray integration scales up to limits of compute availability and affordability.
  - Each AI Actor is an actual AI
  - LLM integration to talk to the simulation as it runs.

So, how are we going to get there? We'll need some solid strategies as well as a fundamental understanding of good design.

## Development Strategy & Philosophy
Project-Asimov emphasizes the test-driven development (TDD) style, writing tests before coding features to ensure reliability for flows and registries, and making code review easier.

**Test-Driven Development Example**
For the `SecureBRLA` flow, we’d first write a test like `test_secure_brla_payment` (new file located at `tests/asimov/flow/credit/test_secure_brla.py`) to check that Conglomocorp’s `robotorq_holdings` updates from 0 to 100,000 RoboTorq after a `SeedXfer` flow, using `pytest` (e.g., `assert registry.df["robotorq_holdings"].sum() == 100000.0`). 

Only then do we code the feature intended to pass this test, ensuring robust BRLA signing.

**Why Test Driven Development**
TDD helps keep feature bloat to a minimum: if you want to write a feature, you have to write a test first to get it into main, so just how bad do you want to add that extra little bling that could maybe break 20 other things, maybe not?

It may sound like a pain at first, but once you get the hang of it, you'll see the value when working on a distributed project like this. When someone else is reviewing your pull request, your tests provide context for understanding your code. And that goes the same for when you review their pull request.

Test-driven development can be a cornerstone of good design and execution when done right, but it's not the whole bridge from idea to final product. Here are some other important notes about the overall design philosophy of Project-Asimov.

## Other Design Philosophy Notes
You'll find that `flow`, as a category, contains the bulk of the simulation's logic. But that doesn't mean they're bloated classes, overflowing with code.

Each `flow` is designed to move a single type of thing, for one particular reason, between two unique `actors`, in only one direction, at a fixed rate, according to each `actor's` attribute schema, for an exact duration of ticks or steps, at which point, it is *always responsible for flagging itself for removal from the `economy`*.

When creating and calling `flow` methods, this object is set it and forget it. You can think of `flows` as ephemeral, self-contained function calls that flash into and out of existence as quickly as they complete their job. Pretty cool, huh?

However, there are **many** different types of `flow`, since each `flow` does exactly one thing.

This set of simple, yet exact constraints provides 
  - Prioritizes simplicity and modularity, with flows handling interactions, and because they're self-dissolving they keep the graph clean and lean
  - Encourages scalability
  - Encourages Community input, designing for future AI-driven features (e.g., Giskard) and Monte Carlo runs. Here's how.

Once the core simulation logic is defined, adding new features largely becomes a matter of designing new flow loop logic. See this example flow loop logic below. Looking at the handling of *SecureBRLA* `flow` in v0.2.1, you'll see that the creation of the *SecureBRLA* `flow` spawns a flurry of activity that loops between three different `actors`:

**v0.2.1 *SecureBRLA* Handling**
  - Created during the ``Robonomics.run_model()``, adding a one-tick *SecureBRLA* request from the `BRLA` to `Conglomocorp`.
  - When `Conglomocorp` does not have enough RoboTorq, this *SecureBRLA* creates a *SeedNeeded* request to `Isaac` from `Conglomocorp`.
  - The *SeedNeeded* request spawns a *SeedXfer* credit flow in the amount of 5*brla_retainer_fee (default=5*100,000) from `Isaac` to `Conglomocorp`.
  - The *SeedXfer* credit spawns a *RetainerXfer* credit from `Conglomocorp` to the `BRLA`.
  - The *RetainerXfer* credit pays the brla_retainer_fee to the `BRLA`.
  - This *SecureBRLA* request is marked as completed when the *RetainerXfer* is disbursed successfully.

This is why I talk about RoboTorq "infecting" the host economy. We'll be using several tools to guide this infection as efficiently as possible.

## Tools & Dependencies
  - **Polars**:
    - **Description**: A fast DataFrame library for in-memory data processing.
    - **Pros**: Blazing speed for large datasets, perfect for bondholder/enterprise registries.
    - **Cons**: Steeper learning curve than Pandas for some operations.
    - **Justification**: Powers efficient DataFrame updates in `BondholderRegistry` for the MVP.
    - **Example Usage**: Querying `robotorq_holdings` with `df.filter(pl.col("bondholder_id") == "conglomocorp_001")`.
  - **GRAPE**:
    - **Description**: A Rust-based graph library for scalable network operations.
    - **Pros**: Handles thousands of nodes/flows with speed, ideal for GRAPE graph management.
    - **Cons**: Less mature API than NetworkX, may need workarounds.
    - **Justification**: Enables flow dissolution and graph scaling in `Robonomics`.
    - **Example Usage**: Removing a flow with `graph.remove_edge("brla_001", "conglomocorp_001")`.
  - **DASK**:
    - **Description**: A parallel computing library for distributed data processing.
    - **Pros**: Scales DataFrame operations across multiple cores or machines.
    - **Cons**: Adds complexity for small datasets like the MVP, will not add until later most likely.
    - **Justification**: Prepares for future Monte Carlo runs with large-scale simulations.
    - **Example Usage**: Running `Isaac` and `Bondholders` on one cluster, running `Robots` and `Daneel` on a second, `BRLAs` and `Giskard` on a third, etc.
  - **RAY (Future)**:
    - **Description**: A framework for distributed computing and reinforcement learning.
    - **Pros**: Enables parallel flow processing and AI-driven behaviors (e.g., Giskard).
    - **Cons**: Overhead for MVP’s single-node setup.
    - **Justification**: Planned for v1.0 to scale AI and Monte Carlo experiments.
    - **Example Usage**: Distributing ticks with `ray.remote(flow.tick)`.
## UI/UX Design
  - **Requirements**:
    - Display real-time flow interactions (e.g., `SecureBRLA` to `SeedXfer`) and registry data (e.g., `robotorq_holdings`) for the MVP.
    - Support TDD with testable UI components (e.g., test flow visualizations with `pytest`).
    - Scale to thousands of nodes (bondholders, enterprises) without lag.
    - **Bonus**: Add a cyberpunk flair, dark mode with neon visuals to wow users/viewers.
## Closing Words

This is a living document. Expect it to change often for now. When a change occurs, expect a [Discussion Board Topic](https://github.com/GrokkingGrok/Project-Asimov/discussions) to pop up, letting everyone know.

Thank you for your hard work and dedication to Project-Asimov.

Jon
