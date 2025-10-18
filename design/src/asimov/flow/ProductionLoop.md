# Basic Production Flow Loop

Oracles hold all the information relevant to a production task, like:
  - Which robot or robots are assigned to work on that task.
  - How long the production will take in both ticks and steps. 

Robots complete the work associated with an Oracle. 
  - Robots both send and receive AI tokens from the Oracle
  - The interaction between these flow rates helps calculate overall Oracle.torq

In future versions, Oracles will serve as the interface between Robots and Giskard.

BRLA oversees Oracle processing. 
  - RetainerXfer spawns ProductionStartFlag from BRLA to Oracle with payload BRLA-generated tta_request_data (TokenTorqAuth data to start production)
    - ProductionStartFlag request does a schema update on Oracle.is_active.
    - RequestFailed goes back to BRLA from Oracle with payload tta_request_data.
- ProductionStartFlag spawns TokenTorqAuth from Oracle to Robot with payload tta_request_data.
  - RequestFailed goes back to Oracle with payload tta_request_data.
  - tta_request_data += Robot.sit_rep (representative of dict merge)
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
  - Set Robots.production_remaining = 1.0
  - Every tick, this stream sends new TokenTorq to the Robot:
- Every tick (until the next step), TokenTorqDrain does:
  - Robot.token_torq += Giskard.tick_rate (Giskard.tick_rate is dependent on Giskard.token_torq_capacity recalculated every step)
  - Robot cannot start production Robot.token_torq >= Robot.min_token_torq, but only Robots can initiate a TorqFountain during a step.
- Every Robot.step():
  - if not is_trained:
    - if token_torq >= min_token_torq:
      - self.train()  # Set is_trained = True, update efficiency
    - else:
      - log("Waiting for training: {token_torq}/{min_token_torq}")
      - return  # Skip rest
  - elif is_producing and production_remaining > 0.1:
    - mine_torq()  # Convert to Torq, decrement remaining
    - return  # Skip spawn
  - else:
    - if Oracle.is_active and not is_producing:  # Safety check
      - makeTorqFountain = True
      - spawn_TorqFountain(to=Oracle, payload=tta_data + sit_rep)
      - set is_producing = True
    - else:
      - spawn_RequestFailed(to=Oracle, reason="Not ready")
- Robot spawns TorqFountain to Oracle.
- Every TorqFountain.tick():
  - The Robot mines its TokenTorq into Torq with varying efficiency (representing production taking place).
    - The more efficiently it mines TokenTorq, the faster Robot.torq increases.
  - Several factors influence TokenTorq --> Torq conversion.
    - The more a robot has done the same task, the more efficiently it mines TokenTorq.
    - The type of task also influences how Torq is mined.
      - Complex tasks draw TokenTorq from Giskard at a higher rate, but mine slowly when production starts, and then produce lots of torq by the end.
      - Simple tasks draw less TokenTorq, but have flatter Torq curves.
    - The lower Giskard.tick_rate, the harder the robot has to work to mine Torq, the more Torq it produces per unit TokenTorq, but less Torq overall.

## Implications of Torq Mining
Economic growth requires buying more robots (because fleet utilization is high).

But buying more robots won't help if fleet utilization is high because of a shortage of TokenTorq during complex tasks. So, upgrading Giskard's token_torq_capacity must come before new bot purchases

So, who gets to decide to when to upgrade Giskard? Not Giskard, he can only ask. Daneel and Isaac make the decision of when to upgrade Giskard, and both must agree to proceed.

Likewise, when it's time to buy new bots, Daneel does not make that decision. Giskard and Isaac make that call.














