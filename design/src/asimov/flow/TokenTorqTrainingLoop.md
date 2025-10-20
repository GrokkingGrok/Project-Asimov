# Basic TokenTorqTraining Flow Loop and 

The SecureBRLA Flow Loop seeded an Enterprise with RoboTorq and created a ProductionStartFlag from a BRLA to an Oracle, and that's why this document exists.

It's time to use that Oracle to make a Robot start working. But how is does that production happen? What governs how well Robots generate Torq as a result of producing goods, so that Isaac knows how much RoboTorq to mint?

What is Torq? And what the heck is TokenTorq?
	- TokenTorq: A standardized constraint of how much compute a given robot can wield at any given time, as allocated by Giskard, relative to the total compute consumption of the Bond Network, as measured in kWh/token.
	- torq_mining_rate: The rate at which a robot can effectively use TokenTorq to create economic value, as measured in tokens/kWh.
	- Torq: A unitless scalar achieved by multiplying TokenTorq * torq_mining_rate (kWh/token * tokens/kWh = no units)

# Park that, and check out how it fits into the big picture:

Back to Oracles. They direct a robot or set of robots on what tasks to do. One BRLA may have several Oracles happening concurrently, it may process them one at a time, or one after another, or some combination of the two.

Oracles hold all the information relevant to a production task, like:
  - Which robot or robots are assigned to work on that task.

Robots complete the work associated with an Oracle. 
  - Robots both send and receive AI tokens from the Oracle
  - The interaction between these flow rates helps calculate the overall Oracle.torq

BRLA oversees Oracle processing. 
  - RetainerXfer spawns ProductionStartFlag from BRLA to Oracle with payload: BRLA-generated tta_request_data (TokenTorqAuth data to start production)
    - ProductionStartFlag request does a schema update on Oracle.is_active.
    - RequestFailed goes back to BRLA from Oracle with payload tta_request_data.
- ProductionStartFlag spawns TokenTorqAuth from Oracle to Robot with payload tta_request_data.
  - RequestFailed goes back to Oracle with payload tta_request_data.
  - tta_request_data += Robot.sit_rep (representative of data frame merge)
  - set Robot.ready_to_train = True
- TokenTorqAuth spawns DrainRequest from Robot to Giskard with payload tta_request_data.
  - StreamFailed goes back to Robot from Giskard with payload tta_request_data.
  - TokenTorqAuth calls Giskard.requestNewDrain(tta_request_data)
  - Giskard processes this request quietly.
- Giskard only creates flows on steps.
- Giskard spawns TokenTorqDrain from Giskard to the Robot with payload tta_approval.
  - StreamFailed goes back to Giskard from Robot with payload tta_approval.
  - Set Robot.min_token_torq = tta_approval.min
  - Set Robot.is_trained = False
  - Set Robot.training_remaining = 1.0
  - Every tick, this stream sends new TokenTorq to the Robot:
- Every tick (until the next step), TokenTorqDrain does:
  - Robot.token_torq += Giskard.tick_rate (Giskard.tick_rate is dependent on Giskard.token_torq_capacity recalculated every step)
  - Robot cannot start production Robot.token_torq >= Robot.min_token_torq, but only Robots can initiate a TorqFountain during a step.
- Every Robot.step().training_update():
  - if not is_trained:
    - if token_torq < min_token_torq:
      - log("Waiting for training: {token_torq}/{min_token_torq}")
      - return False
    - else:
      - spawn_TorqFountain(to=Oracle, payload=tta_data + sit_rep)
      - catch exceptions and log spawn_RequestFailed(to=Oracle, reason="Not ready")
      - return true
- Robot spawns TorqFountain to Oracle
  
Once the TorqFountain has been spawned, the TokenTorq Training Loop is complete. Looking ahead at Torq Mining from TokenTorq (Production) briefly
- Every TorqFountain.tick():
  - The Robot mines its TokenTorq into Torq with varying efficiency (representing production taking place).
    - The more efficiently it mines TokenTorq, the faster Robot.torq increases.
  - Several factors influence TokenTorq --> Torq conversion.
    - The more a robot has done the same task, the more efficiently it mines TokenTorq.
    - The type of task also influences how Torq is mined.
      - Complex tasks draw TokenTorq from Giskard at a higher rate, but mine slowly when production starts, and then produce lots of torq by the end.
      - Simple tasks draw less TokenTorq, but have flatter Torq curves.
    - The lower Giskard.tick_rate, the harder the robot has to work to mine Torq, the more Torq it produces per unit TokenTorq, but less Torq overall.

## Massive Implications of Torq Mining
Economic growth requires buying more robots (because fleet utilization is high).

But buying more robots won't help if fleet utilization is high because of a shortage of TokenTorq during complex tasks. So, upgrading Giskard's token_torq_capacity must come before new bot purchases

So, who gets to decide to when to upgrade Giskard? Not Giskard, he can only ask. Daneel and Isaac make the decision of when to upgrade Giskard, and both must agree to proceed, but that's not sufficient either. Where would the money come from?

Likewise, when it's time to buy new bots, Daneel does not make that decision. Giskard and Isaac must agree to proceed, but again, not sufficient. Show me the money!

See the Calvin design doc for more information about how these decisions will ultimately be made and funded.

## TokenTork Training Actors
| Actor | Initial State (if relevant) | Role | Final State (if relevant) |
|--------|-----------------------------|------|---------------------------|
| BRLA | irrelevant | Overseer | irrelevant |
| Enterprise | irrelevant | Beneficiary | irrelevant |
| Oracle | Oracle.is_active = False | Source, Target | Oracle.is_active = True |
| Robot | Robot.ready_to_train = False<br/>Robot.is_trained = True<br/>Robot.training_remaining = 0.0 | Source, Target | Robot.ready_to_train = True<br/>Robot.is_trained = False<br/>Robot.training_remaining = 1.0 |
| Giskard | irrelevant | Source, Target | irrelevant |
| Isaac | irrelevant | Minter | irrelevant |

## TokenTork Training Flows
| Flow | Flow Type | Spawned By | Spawns |
|------|-----------|------------|--------|
| ProductionStartFlag | Request | RetainerXfer | TokenTorqAuth |
| TokenTorqAuth | Request | ProductionStartFlag | DrainRequest |
| DrainRequest | Request | TokenTorqAuth | TokenTorqDrain |
| TokenTorqDrain | Transaction | Giskard | irrelevant |
| TorqFountain | Transaction | Robot | irrelevant |
| RequestFailed | Failure | ProductionStartFlag, TokenTorqAuth, DrainRequest, TokenTorqDrain, TorqFountain | failure_retry_node Handles |
| StreamFailed | Failure | TokenTorqDrain | failure_retry_node Handles |

## Dependencies, Assumptions, and Outputs
[Bulleted list of prerequisites, external factors, or configs.]
- **Assumes**: `Robonomics.tick()` is called to initialize.
- **Default parameters**: tta_request_data fetched from BRLA and passed as payload
- **No blocking/waiting**: All flows in this loop are *Dart Flows* that will flag themselves for removal at the end of the same tick they are created.
- **Logging output**: Appended to `src/asimov/output/flow_logs.txt`.
- **RequestFailed or StreamFailed**: Spawn the flow, but actors handle retries.
- **ProductionStartFlag signals successful Secure BRLA Flow Loop**
- **TokenTorqDrain runs every tick** until Robot spawns TorqFountain during step().
- **TorqFountain signals successful TokenTorq Training Loop**

## Sequence of Steps
[Numbered list describing the exact flow in chronological order. Use sub-bullets for details like triggers, method calls, conditions, logging, and completion flags. Reference ticks/cycles for timing.]

1. **Called by Robonomics.tick()**
2. **ProductionStartFlag.tick()**
  - **Tick Count**: 1
  - **Spawned by**: Spawned from RetainerXfer in tick 0
  - **Payload**: BRLA-generated tta_request_data
  - **Failure Retry Node**: BRLA.UUID
  - **Track**:
    - **DataFrame**: tta_request_data
    - **Boolean**: success = True
    - **Boolean**: makeRequestFailed = False
  - **Schema Checks Total**: 1
    - **Schema to Check**: Oracle.is_active == False
  - **Schema Updates Total**: 1
    - **Schema to Update**: Oracle.is_active = True
  - **Schema Grabs Total**: 1
    - **Schema to Grab**: BRLA.tta_request_data
  - **try**: Core Flow Logic
    - Grab tta_request_data from BRLA
    - If Oracle.is_active == False:
      - Update Oracle.is_active = True
      - **Flow Path 1**: success = True
    - else:
      - **Flow Path 1.1**: makeRequestFailed = True
  - **catch**: Errors checking/updating schema
    - **Flow Path 1.1**: makeRequestFailed = True
    - **Log**: "ProductionStartFlag unable to update Oracle.is_active on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flow Path 1 (Success)
    - **Create Flow**: TokenTorqAuth(source=Oracle.UUID, target=Robot.UUID, payload=tta_request_data, failure_retry_node=Oracle.UUID)
    - **Log**: "ProductionStartFlag spawned TokenTorqAuth from [Oracle.UUID] to [Robot.UUID] on Step: [current_step], Tick: [current_tick]"
  - **catch**: Errors spawning TokenTorqAuth
    - **Log**: "ProductionStartFlag failed to spawn TokenTorqAuth on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flow Path 1.1 (Schema Conflict)
    - **Create Flow**: RequestFailed(source=Oracle.UUID, target=BRLA.UUID, failure_payload={retry=True, reason="Oracle already active", Flow=self}, failure_retry_node=BRLA.UUID)
    - **Log**: "ProductionStartFlag spawned RequestFailed to [BRLA.UUID] because Oracle already active on Step: [current_step], Tick: [current_tick]"
  - **catch**: Errors spawning RequestFailed
    - **Log**: "ProductionStartFlag failed to spawn RequestFailed on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flag for Dissolution
    - **Dissolve Call**: Flag self for removal
    - **Log**: "ProductionStartFlag flagged for dissolution on Step: [current_step], Tick: [current_tick]"
    - **return**: success
  - **catch**: Errors flagging dissolution
    - **Log**: "ProductionStartFlag failed dissolution flag on Step: [current_step], Tick: [current_tick], [error_message]"
    - **return**: False
3. **TokenTorqAuth.tick()**
  - **Tick Count**: 2
  - **Spawned by**: Spawned from ProductionStartFlag in tick 1
  - **Payload**: tta_request_data
  - **Failure Retry Node**: Oracle.UUID
- **Track**:
    - **DataFrame**: tta_request_data
    - **DataFrame**: robot_sit_rep
    - **Boolean**: success = True
    - **Boolean**: makeRequestFailed = False
    - **Dict**: failure_payload = {retry = True, reason = "", Flow = None}
  - **Schema Checks Total**: 1
    - **Schema to Check**: Robot.ready_to_train == False
  - **Schema Updates Total**: 1
    - **Schema to Update**: Robot.ready_to_train = True
  - **Schema Grabs Total**: 1
    - **Schema to Grab**: Robot.sit_rep
  - **try**: Core Flow Logic
    - Grab Robot.sit_rep
    - Merge: tta_request_data += robot_sit_rep
    - If Robot.ready_to_train == False:
      - Update Robot.ready_to_train = True
      - **Flow Path 1**: success = True
    - else:
      - **Flow Path 1.1**: makeRequestFailed = True
  - **catch**: Errors grabbing/merging/updating
    - **Flow Path 1.1**: makeRequestFailed = True
    - **Log**: "TokenTorqAuth unable to prepare sit_rep merge on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flow Path 1 (Success)
    - **Create Flow**: DrainRequest(source=Robot.UUID, target=Giskard.UUID, payload=tta_request_data, failure_retry_node=Robot.UUID)
    - **Log**: "TokenTorqAuth spawned DrainRequest from [Robot.UUID] to [Giskard.UUID] on Step: [current_step], Tick: [current_tick]"
  - **catch**: Errors spawning DrainRequest
    - **Log**: "TokenTorqAuth failed to spawn DrainRequest on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flow Path 1.1 (Already Ready)
    - **Track**: failure_payload = {retry = True, reason = "Robot already ready to train", Flow = self}
    - **Create Flow**: RequestFailed(source=Robot.UUID, target=Oracle.UUID, failure_payload=failure_payload, failure_retry_node=Oracle.UUID)
    - **Log**: "TokenTorqAuth spawned RequestFailed to [Oracle.UUID] because Robot already ready on Step: [current_step], Tick: [current_tick]"
  - **catch**: Errors spawning RequestFailed
    - **Log**: "TokenTorqAuth failed to spawn RequestFailed on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flag for Dissolution
    - **Dissolve Call**: Flag self for removal
    - **Log**: "TokenTorqAuth flagged for dissolution on Step: [current_step], Tick: [current_tick]"
    - **return**: success
  - **catch**: Errors flagging dissolution
    - **Log**: "TokenTorqAuth failed dissolution flag on Step: [current_step], Tick: [current_tick], [error_message]"
    - **return**: False
4. **DrainRequest.tick()**
  - **Tick Count**: 3
  - **Spawned by**: Spawned from TokenTorqAuth in tick 2
  - **Payload**: tta_request_data
  - **Failure Retry Node**: Robot.UUID
- **Track**:
    - **DataFrame**: tta_request_data
    - **Boolean**: success = True
    - **Boolean**: makeStreamFailed = False
    - **Dict**: failure_payload = {retry = True, reason = "", Flow = None}
  - **Schema Checks Total**: 1
    - **Schema to Check**: Giskard.token_torq_capacity > 0
  - **Schema Updates Total**: 0
  - **Schema Grabs Total**: 1
    - **Schema to Grab**: Giskard.token_torq_capacity
  - **try**: Core Flow Logic
    - Grab Giskard.token_torq_capacity
    - If Giskard.token_torq_capacity > 0:
      - Call Giskard.requestNewDrain(tta_request_data)
      - **Flow Path 1**: success = True
    - else:
      - **Flow Path 1.1**: makeStreamFailed = True
  - **catch**: Errors grabbing/calling Giskard
    - **Flow Path 1.1**: makeStreamFailed = True
    - **Log**: "DrainRequest unable to contact Giskard on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flow Path 1 (Success)
    - **Create Flow**: TokenTorqDrain(source=Giskard.UUID, target=Robot.UUID, payload=tta_approval, failure_retry_node=Giskard.UUID)
    - **Log**: "DrainRequest spawned TokenTorqDrain from [Giskard.UUID] to [Robot.UUID] on Step: [current_step], Tick: [current_tick]"
  - **catch**: Errors spawning TokenTorqDrain
    - **Log**: "DrainRequest failed to spawn TokenTorqDrain on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flow Path 1.1 (Capacity Exhausted)
    - **Track**: failure_payload = {retry = True, reason = "Giskard capacity exhausted", Flow = self}
    - **Create Flow**: StreamFailed(source=Robot.UUID, target=Giskard.UUID, failure_payload=failure_payload, failure_retry_node=Robot.UUID)
    - **Log**: "DrainRequest spawned StreamFailed to [Giskard.UUID] because capacity exhausted on Step: [current_step], Tick: [current_tick]"
  - **catch**: Errors spawning StreamFailed
    - **Log**: "DrainRequest failed to spawn StreamFailed on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flag for Dissolution
    - **Dissolve Call**: Flag self for removal
    - **Log**: "DrainRequest flagged for dissolution on Step: [current_step], Tick: [current_tick]"
    - **return**: success
  - **catch**: Errors flagging dissolution
    - **Log**: "DrainRequest failed dissolution flag on Step: [current_step], Tick: [current_tick], [error_message]"
    - **return**: False
5. **TokenTorqDrain.tick()**
  - **Tick Count**: Ongoing (4+ until Robot.step() spawns TorqFountain)
  - **Spawned by**: Spawned from DrainRequest in tick 3
  - **Payload**: tta_approval
  - **Failure Retry Node**: Giskard.UUID
- **Track**:
    - **Float**: tokens_sent
    - **Boolean**: success = True
    - **Boolean**: makeStreamFailed = False
    - **Dict**: failure_payload = {retry = True, reason = "", Flow = None}
  - **Schema Checks Total**: 1
    - **Schema to Check**: Robot.training_remaining > 0
  - **Schema Updates Total**: 3
    - **Schema to Update**:
      - Robot.token_torq += Giskard.tick_rate
      - Robot.min_token_torq = tta_approval.min
      - Robot.training_remaining -= (Giskard.tick_rate / min_token_torq)
  - **Schema Grabs Total**: 2
    - **Schema to Grab**: 
      - Giskard.tick_rate
      - Robot.training_remaining
  - **try**: Core Flow Logic
    - Grab Giskard.tick_rate
    - If Robot.training_remaining > 0:
      - Update Robot.token_torq += Giskard.tick_rate
      - tokens_sent += Giskard.tick_rate
      - Update Robot.training_remaining -= (Giskard.tick_rate / Robot.min_token_torq)
      - **Flow Path 1**: success = True
    - else:
      - **Flow Path 1.1**: makeStreamFailed = True
  - **catch**: Errors grabbing/updating
    - **Flow Path 1.1**: makeStreamFailed = True
    - **Log**: "TokenTorqDrain unable to deliver tokens on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flow Path 1 (Training Continues)
    - **No Flow Spawn** (continues every tick)
    - **Log**: "TokenTorqDrain delivered [Giskard.tick_rate] tokens, training_remaining: [Robot.training_remaining]"
  - **catch**: No spawn, just log above
  - **try**: Flow Path 1.1 (Training Complete)
    - **Track**: failure_payload = {retry = False, reason = "Training complete, spawn TorqFountain", Flow = self}
    - **Create Flow**: StreamFailed(source=Giskard.UUID, target=Robot.UUID, failure_payload=failure_payload, failure_retry_node=Giskard.UUID)
    - **Log**: "TokenTorqDrain ended: Training complete on Step: [current_step], Tick: [current_tick]"
  - **catch**: Errors spawning StreamFailed
    - **Log**: "TokenTorqDrain failed to signal completion on Step: [current_step], Tick: [current_tick], [error_message]"
  - **try**: Flag for Dissolution (if training complete)
    - If Robot.training_remaining <= 0:
      - **Dissolve Call**: Flag self for removal
      - **Log**: "TokenTorqDrain flagged for dissolution - training complete"
      - **return**: success
    - Else:
      - **return**: success (continues next tick)
  - **catch**: Errors flagging dissolution
    - **Log**: "TokenTorqDrain failed dissolution flag on Step: [current_step], Tick: [current_tick], [error_message]"
    - **return**: False
1. **FlowCalled.tick()**
  - **Tick Count**: 
  - **Spawned by**: Spawned from x in tick 1
  - **Payload**: 
  - **Failure Retry Node**: 
	- **Track**:
  - **Schema Checks Total**: 1
    - **Schema to Check**:
  - **Schema Updates Total**: 1
    - **Schema to Update**:
  - **Schema Grabs Total**: 1
    - **Schema to Grab**:
  - **try**: Core Flow Logic
  - **catch**:
  - **try**: Flow Path
    - **Create Flow**:
    - **Log**:
  - **catch**:
  - **try**: Flow Path
    - **Create Flow**:
    - **Log**:
  - **catch**:
  - **try**: Failure Path
    - **Create Flow**:
    - **Log**:
  - **catch**:
  - **try**: Flag for Dissolution
    - **Dissolve Call**:
    - **Log**:
    - **return**:
  - **catch**:
    - **Log**:
    - **return**:













