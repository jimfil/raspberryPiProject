## Section B: Report



**RQ1: What is the role of the MQTT broker? Why don’t we just let the producer and consumer communicate directly (e.g via sockets)?**

Ans: 



**RQ2: What topic structure did you choose and why? How does it support future extensibility (more sensors, more bins)?**

Ans: 



**RQ3: Explain the difference between QoS 0, 1, and 2 in your own words. Which did you use for your motion events and why?**

Ans: 



**RQ4: What is a retained message? Give one concrete example of when it would be useful for your system.**

Ans: 



**RQ5: When you subscribed to smartbin/+/motion, which messages did you receive and which did you not? Explain why, based on how + works.**

Ans: 



**RQ6: What happened when you subscribed to #? Why is this useful for debugging but dangerous in production?**

Ans: 



**RQ7: You published a message while no subscriber was connected (without the retain flag). Then you started a subscriber. Did it receive the message? Why or why not?**

Ans: 



**RQ8: What are the main differences between your run_pipeline.py (threaded queue) and the new producer.py + consumer.py (MQTT)?**

Ans: 



**RQ9: In the threaded version, what happened when the queue was full? In the MQTT version, what happens if the consumer is slow or offline?**

Ans: 



**RQ10: How does the callback pattern in paho-mqtt (on_message) differ from the polling pattern you used in the threaded consumer (queue.get(timeout=0.5))?**

Ans: 



**RQ11: Show one example JSON record from the MQTT-based consumer. Is the structure the same as in previous labs? What about pipeline_latency_ms, is it higher or lower? Why?**

Ans: 



**RQ12: You stopped the consumer and kept the producer running. What happened to the messages published during that time? Were they delivered when the consumer restarted?**

Ans: 



**RQ13: You ran two consumers on the same topic. Did both receive every message? Why does this matter for building scalable systems?**

Ans: 



**RQ14: Could you run the producer on one Raspberry Pi and the consumer on a different machine (e.g., your laptop)? What would you need to change?**

Ans: 



**RQ15: In your own words, what does “decoupling” mean in the context of pub/sub? What are the practical benefits?**

Ans: 



**RQ16: If the Mosquitto broker itself crashes, what happens to your system? How could you mitigate this?**

Ans: 


