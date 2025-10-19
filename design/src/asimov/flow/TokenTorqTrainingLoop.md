# Basic TorqTraining Flow Loop and 

The SecureBRLA Flow Loop seeded an Enterprise with RoboTorq and created a ProductionStartFlag from a BRLA to an Oracle, and that's why this document exists.

It's time to use that Oracle to make a Robot start working. But how is does that production happen? What governs how well Robots generate Torq as a result of producing goods, so that Isaac knows how much RoboTorq to mint?

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
  - **Payload**: none yet
  - **Failure Retry Node**: BRLA.UUID
	- **Track**:
    - DataFrame tta_request_data
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













