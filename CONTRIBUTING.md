# System Architecture Guide for Contributors
If you're thinking of contributing or if you already are contributing and need a refresher, this is where you can get the nitty-gritty details on the Asimov system architecture.

Let's start with the basics. Project-Asimov runs on Python 3.13. 
  * Not the fastest, but dependable and readable. And about the speed...
  * Python 3.13 file reads can be sped up about 10x using `Polars DataFrames`, which we do. Not familiar with Polars?
    * The awesome YouTuber Mariya Sha of `Python Simplified` has a great `Polars` intro video (https://www.youtube.com/watch?v=8GoBlwgbirE)

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
  * Example: Every ``Bondholder`` is connected to ``Isaac`` via a persistent ``flow`` of *DistoStream*.

Let's unpack what that means in more technical terms, so you can see how the abstraction focuses on WHAT the data represents, rather than HOW the underlying data structure gets the job done.
  * A ``Bondholder`` owns at least one ``Bond`` signifying shared ownership of a humanoid ``Robot``.
  * ``Isaac`` is the ``node`` that mints and distributes ``RoboTorq`` to ``Bondholder`` ``nodes``, which happens via a ``edge`` that connects each ``node``.
  * A *DistoStream* is the graph ``edge`` connecting the two ``nodes``, we call any ``edge`` a ``flow``.

## Other Key Terms & Data Structures

From here, we can start defining key terms more readily.

  * ``Graph`` is a collection of 
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
  * This constant trickle is called a *DistroStream* `flow` (specific instances of flows, like *DistroStream*, will be italicized when needed)
  
  **How RoboTorq moves through the Economy: Spending & Investing (Saving Covered Later)**
  * ``Enterprises`` sell goods and services to ``Bondholders``.
  * ``Bondholders`` invest in ``Enterprises`` at ``RoboFund`` in lieu of a stock market.
  * ``RoboFund`` is how ``Bondholders`` invest in individual ``Projects`` that ``Enterprises`` need funding for.
  * `Bondholders` choose which `BuyerFunnels` and `MakerFunnels` to invest in, which are tied to `Projects`.

  **Investing & Commercial Financing**
  * When a `Project` is funded, it is converted to a `Bid`, to be vetted by `BidNet`.
  * If the `Bid` passes initial vetting, `BidNet` asks `Giskard` and `Daneel` for input.
  * `Giskard` (pronounced discard with a 'g') provides various inputs to help `BidNet` decide whether to accept or reject `Bids`, as well as tracking TokenTorq and Torq in the economy.
  * `Daneel` also provides input to `BidNet`.
  * If `Giskard` and `Daneel` are in agreement, `BidNet` always follows their advice.
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
    * A standard step_differential is 24: meaning 24 ticks to every step, simulating a daily cycle where 

Let's stop and think about what this means for a moment, and see how things fit together now that we've defined how time flows in our Robonomics video game.

Scale this up to even a modest 10 `Bondholders`, 1 `Enterprise`, and 1 `Robot`, and you can see how quickly it gets unmanageably complex for a human track without careful attention to detail.

The ultimate goal of Project-Asimov is 
  * A *bare minimum of hundreds of millions* of `Bondholders`.
  * *Tens of millions* of Enterprises, *hundreds of millions* of robots.
  * With the potential for *at least a billion concurrent `flows`*.

# Let's Start Small: A Minimally Viable Product (MVP)

So far, you've seen a lot of big ideas, but they have to start smaller in practice. Two rounds of prototyping helped clarify the MVP, which is also known as v0.2.0. Breaking down the above simulation loop discussion, we can arrive at the following set of MVP Core Requirements.

## v0.2.0 Core Requirements
  - 10 `Bondholders`, 1 `Enterprise`, and 1 `Robot`
  - `Conglomocorp` signs a single BRLA, funded by 100,000 RoboTorq from Isaac via `SecureBRLA` flow.
  - Activate all bondholders on the first BRLA, receiving disto streams (70% spent to Conglomocorp).
  - Use Polars DataFrames for registries and GRAPE for graph management.
  - Ensure all flows self-dissolve after their work is done (e.g., `SecureBRLA`, `SeedXfer`)

## v1.0 Core Requirements
  - Support multiple enterprises (beyond Conglomocorp) with unique BRLAs.
  - Implement Giskard as an AI token manager for auditing robot production and optimizing RoboTorq minting rates.
  - Enable Monte Carlo experiments for economic variability.
  - Scale to tens of thousands of nodes (bondholders, enterprises, robots) with persistent and one-tick flows.

## Development Strategy & Philosophy
Project-Asimov emphasizes the test-driven development (TDD) style, writing tests before coding features to ensure reliability for flows and registries, and making code review easier.

**TDD Example**
For the `SecureBRLA` flow, we’d first write a test like `test_secure_brla_payment` (new file located at `tests/asimov/flow/credit/test_secure_brla.py`) to check that Conglomocorp’s `robotorq_holdings` updates from 0 to 100,000 RoboTorq after a `SeedXfer` flow, using `pytest` (e.g., `assert registry.df["robotorq_holdings"].sum() == 100000.0`). 

Only then do we code the feature intended to pass this test, ensuring robust BRLA signing.

**Why Test Driven Development**
TDD helps keep feature bloat to a minimum: if you want to write a feature, you have to write a test first to get it into main, so just how bad do you want to add that extra little bling that could maybe break 20 other things, maybe not?

It may sound like a pain at first, but once you get the hang of it, you'll see the value when working on a distributed project like this. When someone else is reviewing your pull request, your tests provide context for understanding your code. And that goes the same for when you review their pull request.

## Other Design Philosophy Notes
You'll find that `flows`, as a category, contain the bulk of the system's logic. However, there are **many** different types of `flow`. 

Each `flow` is designed to move a single type of thing, for one particular reason, between two unique `actors`, in only one direction, at a fixed rate, according to each `actor's` permission schema, for an exact duration of ticks or steps, at which point it is *always responsible for flagging itself for removal from the `economy`*. 

This set of simple, yet exact constraints.
  - Prioritizes simplicity and modularity, with flows handling interactions and self-dissolving to keep the graph clean.
  - Encourages scalability
  - Encourages Community input, designing for future AI-driven features (e.g., Giskard) and Monte Carlo runs.

Once the core simulation logic is defined, adding new features becomes a matter of designing new flow loop logic. See this example flow loop logic.

**v0.2.0 *SecureBRLA* Handling**
  - Created during the ``Robonomics.run_model()``, adding a one-tick *SecureBRLA* request from the `BRLA` to `Conglomocorp`.
  - When `Conglomocorp` does not have enough RoboTorq, this *SecureBRLA* creates a *SeedNeeded* request to `Isaac` from `Conglomocorp`.
  - The *SeedNeeded* request spawns a *SeedXfer* credit flow in the amount of 5*brla_retainer_fee (default=5*100,000) from `Isaac` to `Conglomocorp`.
  - The *SeedXfer* credit spawns a *RetainerXfer* credit from `Conglomocorp` to the `BRLA`.
  - The *RetainerXfer* credit pays the brla_retainer_fee to the `BRLA`.
  - This *SecureBRLA* request is marked as completed when the *RetainerXfer* is disbursed successfully.

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
    - **Cons**: Adds complexity for small datasets like the MVP.
    - **Justification**: Prepares for future Monte Carlo runs with large-scale simulations.
    - **Example Usage**: Parallelizing DataFrame joins with `dask.dataframe.from_polars(df)`.
  - **RAY (Future)**:
    - **Description**: A framework for distributed computing and reinforcement learning.
    - **Pros**: Enables parallel flow processing and AI-driven behaviors (e.g., Giskard).
    - **Cons**: Overhead for MVP’s single-node setup.
    - **Justification**: Planned for v1.0 to scale AI and Monte Carlo experiments.
    - **Example Usage**: Distributing flow ticks with `ray.remote(flow.tick)`.
## UI/UX Design
  - **Requirements**:
    - Display real-time flow interactions (e.g., `SecureBRLA` to `SeedXfer`) and registry data (e.g., `robotorq_holdings`) for the MVP.
    - Support TDD with testable UI components (e.g., test flow visualizations with `pytest`).
    - Scale to thousands of nodes (bondholders, enterprises) without lag.
    - **Bonus**: Add a cyberpunk flair—
