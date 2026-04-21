## Section B: Report



**RQ1: What is the role of the MQTT broker? Why don’t we just let the producer and consumer communicate directly (e.g via sockets)?**

Ans: MQTT follows the publish-subscribe model, where clients communicate with a central server called a broker. The broker has some advantages over direct communication, which are: the producer and the consumer just connect to the broker without having direct connection which requires for both of them to be online and know eachothers IP address, the distribution of information through the broker to multiple consumers is easier than a producer connecting directly to them, the reconnection in MQTT brokers is handled automatically and data is queued during downtime and lastly the MQTT broker has simplified security mechanisms, independent from producer and consumer devices. 



**RQ2: What topic structure did you choose and why? How does it support future extensibility (more sensors, more bins)?**

Ans: 



**RQ3: Explain the difference between QoS 0, 1, and 2 in your own words. Which did you use for your motion events and why?**

Ans: 



**RQ4: What is a retained message? Give one concrete example of when it would be useful for your system.**

Ans: A retained message is a message which has a flag activated which enables the message to remain for future subscribers. A retained message would be useful for transferring basic data for our smart bin like status(online, offline; back in x hours,...).



**RQ5: When you subscribed to smartbin/+/motion, which messages did you receive and which did you not? Explain why, based on how + works.**

Ans: 



**RQ6: What happened when you subscribed to #? Why is this useful for debugging but dangerous in production?**

Ans: The wildcard subscription '#' allows us to observe: the entire data flow of a specified topic, the whole timeline of a bug occuring without having to look at disparate log files, which is critical for time-sensitive production issues. It also helps us in tracking and identifying messages sent to wrong topics, or messages with the wrong data format, so it acts as a 'monitor' of the entire topic. But it can be dangerous in production mainly because of the sheer amount of data being transferred through the broker, which could result in potentially slowing down or crashing the message broker, in the client's inability to process the information, leading to memory saturation and out-of-memory errors, or in receiving sensitive client information.  



**RQ7: You published a message while no subscriber was connected (without the retain flag). Then you started a subscriber. Did it receive the message? Why or why not?**

Ans: The subscriber did not receive the message because the broker had no subcribers, so the message without the retained flag was not retained by the broker.



**RQ8: What are the main differences between your run_pipeline.py (threaded queue) and the new producer.py + consumer.py (MQTT)?**

Ans: 



**RQ9: In the threaded version, what happened when the queue was full? In the MQTT version, what happens if the consumer is slow or offline?**

Ans: In the threaded version, if the queue was full, the messages would be lost. But in the MQTT version, given that the consumer is subscribed, the messages would be retained by the broker.



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


