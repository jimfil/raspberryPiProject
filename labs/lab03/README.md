**RQ1: Which lecture pipeline phases do you believe you had already implemented in Lab 02?**

Ans: Based on the lab description, the pipeline phases already implemented in Lab 02 were reading the raw sensor input (acquisition), interpreting the signal behavior to create event records (processing/packaging), and writing the output. While these core phases were present, they were executed in a synchronous, tightly coupled loop (read → interpret → write), rather than the decoupled Producer-Queue-Consumer architecture introduced in the current lab.


**RQ2: Which part of your Lab 02 code did you reuse directly?**

Ans: We used directy the files: sampler.py and interpreter.py.

**RQ3: Which part did you have to adapt for the pipeline architecture?**

Ans: To adapt the system for the pipeline architecture, the core execution loop had to be modified from a sequential process into an explicit, concurrent one. The main adaptation was introducing a queue to decouple the data generation phase (Producer) from the data writing phase (Consumer). Additionally, because the producer might generate events faster than the consumer can write them, a backpressure mechanism had to be integrated—specifically using a drop-newest policy to handle cases where the queue reaches its maximum capacity.



