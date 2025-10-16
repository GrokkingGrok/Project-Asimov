# SecureBRLA Flow Loop

SecureBRLA.py is the first cascading flow in the simulation, an Enterprise needs to pay a BRLA Retainer Fee.

Starting with a BRLA, resulting in newly minted RoboTorq from Isaac going to an Enterprise, then to the BRLA.

## Actors Involved

| Actor | Initial State (if relevant) | Role | Final State (if relevant) |
|--------|-----------------------------|------|---------------------------|
| BRLA | Has retainer fee parameters | Source, Target | Has retainer fee |
| Enterprise | No RoboTorq initially | Source, Target | Excess RoboTorq |
| Isaac | No RoboTorq | Source, Target | No RoboTorq |

## Flows Involved
| Flow | Flow Type | Spawned By | Spawns |
|------|-----------|------------|--------|
| SecureBRLA | Request Dart | `BRLA` | SeedNeeded or RetainerXfer |
| SeedNeeded | Request Dart | SecureBRLA | SeedXfer | 
| SeedXfer | Credit Dart | SeedNeeded | RetainerXfer |
| RetainerXfer | Credit Dart | SeedXfer | BRLA Production Loop |

## Dependencies, Assumptions, and Outputs
[Bulleted list of prerequisites, external factors, or configs.]
- **Assumes**: `Robonomics.tick()` is called to initialize.
- **Default parameters**: `brla_retainer_fee = 100,000`; multipliers like 5x for seeding.
- **No blocking/waiting**: All flows in this loop are *Dart Flows* that will flag themselves for removal at the end of the same tick they are created.
- **Logging output**: Appended to `src/asimov/output/flow_logs.txt`.

## Sequence of Steps
[Numbered list describing the exact flow in chronological order. Use sub-bullets for details like triggers, method calls, conditions, logging, and completion flags. Reference ticks/cycles for timing.]

1. **Called by Robonomic.tick()**
2. **SecureBRLA.tick()**
   - Triggered by: Created during BRLA initialization, activated by Robonomics.tick()
   - Payload: Default Request Logic
   - Track:
     - Boolean result = True
   - Schema Checks Total: 1
     - Check: Enterprise.robotorq_holdings < BRLA.brla_retainer_fee
   - Core Logic:
     - if Enterprise.robotorq_holdings < BRLA.brla_retainer_fee
       - spawn SeedNeeded, see below
     - else spawn RetainerXfer, see below
   - Try: Spawn Flows
     - SeedNeeded
       - Initializes with source=`Enterprise.UUID`, target=`Isaac.UUID`, model=`robonomics`, payload=None.
       - - Log: "SecureBRLA spawned SeedNeeded from [source.UUID] to [target.UUID] on Step: [current_step], Tick: [current_tick]"
     - OR RetainerXfer
       - Initializes with source=`Enterprise.UUID`, target=`BRLA.UUID`, model=`robonomics`, payload=brla_retainer_fee
       - Log: "SecureBRLA spawned RetainerXfer from [source.UUID] to [target.UUID] on Step: [current_step], Tick: [current_tick]"
   - catch: Errors creating flows
     - result = False
     - Log: "SecureBRLA failed to spawn flow from [source.UUID] to [target.UUID] on Step: [current_step], Tick: [current_tick], [error message]"
   - try: Flag for Dissolution
     - Log: "SecureBRLA flagged for dissolution on Step: [current_step], Tick: [current_tick]"
     - Return: result
   - catch: Errors in flagging for dissolution.
     - Log: "SecureBRLA [flow.UUID] not flagged for dissolution on Step: [current_step], Tick: [current_tick], [error message]"
     - Return: False (Do need to waste op setting result to False, it's used to track the case flow creation fails but dissolution succeeds)

3. **SecureBRLA.tick()**
   - Triggered by: Created during initialization, activated by initial call to Robonomics.run_model(), which starts the first tick.
   - Schema Check Total: 1
     - Checks Enterprise.robotorq_holdings < BRLA.brla_retainer_fee
   - Schema Updated:
     - None if True, spawns SeedNeeded
     - else deduct brla_retainer_fee from robotorq_holdings
   - Spawn Details: SeedNeeded
     - Initializes with source=`Enterprise.UUID`, target=`Isaac.UUID`, model=`robonomics`.

4. **Completion and Dissolution**
   - Triggered by: [e.g., After create_flow() for SeedNeeded].
   - Action: [e.g., Marks SecureBRLA as completed and dissolves it].
   - Details:
     - Sets: `self.is_completed = True`.
     - Calls: `try: self.model.graph.dissolve(self)`.
     - Logging: Success: "Dissolved SecureBRLA: brla_001 → conglomocorp_001"; Failure: Error message.
     - Timing: Dissolved before next tick; removed from memory.

5. **[Next Step, e.g., SeedNeeded Processing]**
   - Triggered by: [e.g., Next tick in SeedNeeded's cycle].
   - Action: [e.g., Spawns SeedXfer credit from Isaac to Conglomocorp].
   - Details:
     - Amount: 5 x brla_retainer_fee (default=500,000).
     - Calls: `self.create_flow("Isaac", "conglomocorp_001", "SeedXfer", {"amount": 500000})`.
     - Logging: Success/failure.

[Continue numbering for all steps...]

## Logging and Error Handling
[Dedicated section for all logs and exceptions across the loop. Use a table if many.]

- All actions wrapped in try-except for non-blocking flow.
- Log file: `src/asimov/output/flow_logs.txt`.
- Examples:
  - Spawn success: "Spawned [FlowType]: [source] → [target]".
  - Dissolve failure: "Failed to dissolve [FlowType]: [error]".

## Completion Criteria and Outcomes
[Describe when the loop ends and final states.]
- Loop completes when: [e.g., RetainerXfer updates holdings and marks payment].
- Expected Outcomes:
  - Conglomocorp seeded with RoboTorq.
  - BRLA receives retainer fee.
  - All temporary flows dissolved.
- Edge Cases: [e.g., If seeding fails, loop proceeds but logs error; no retries].

## Potential Improvements or Variations
[Optional: Notes for future iterations, e.g., "Add configurable retainer fees" or "Integrate with other loops like PaymentProcessing."]
